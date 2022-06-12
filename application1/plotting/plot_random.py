import pickle

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import copy as cp

from application1.handler.triggers import LocalPipeline
from application1.model.histogram import Hist
from application1.plotting.plot import plot_histogram_cdf, plot_histogram
from resources.constants import PLOT_DIR

np.random.seed(3)


def find_nearest_index(array, value):
    return np.abs(array - value).argmin()


# x1 = np.random.normal(loc=0, scale=1, size=10000)
# x2 = np.random.normal(loc=1, scale=1, size=200)
# h1 = Hist(x1, l2_nbin=10)
# h2 = Hist(x2, l2_nbin=10)

test_file = f'test_1264625000_1264635000_f50.pickle'
with open(test_file, 'rb') as pkf:
    data = pickle.load(pkf)
    h_trig_cum = data['trig']
    h_aux_cum = data['aux']
    available_channels = data['channels']

pipeline = LocalPipeline(trigger_file='GSpy_ALLIFO_O3b_0921_final.csv')
labels = list(pipeline.labels)
channel = 'V1:ENV_WEB_SEIS_W'
transformation_name = ''
h1 = h_aux_cum[channel, transformation_name]
h2 = Hist(np.array([]))
for label in labels:
    h2 += h_trig_cum[channel, transformation_name, label]

h1_cp = cp.deepcopy(h1)
h2_cp = cp.deepcopy(h2)
h1_cp += h2_cp

i_min = find_nearest_index(h1_cp.cdf, 0.01)
i_max = find_nearest_index(h1_cp.cdf, 0.99)

h1.align(h2)

# fig = plot_histogram(histogram=h1, channel=channel, transformation=transformation_name, data_type="aux", return_fig=True)
# plot_histogram(histogram=h2, channel=channel, transformation=transformation_name, data_type="trig", fig=fig, save=True)
#
# fig = plot_histogram_cdf(histogram=h1, channel=channel, transformation=transformation_name, data_type="aux", return_fig=True)
# # plt.axvline(x=h1_cp.xgrid[i_min], color='k', linestyle='--')
# # plt.axvline(x=h1_cp.xgrid[i_max], color='k', linestyle='--')
# plot_histogram_cdf(histogram=h2, channel=channel, transformation=transformation_name, data_type="trig", fig=fig, save=True)

fig = plt.figure(figsize=(10, 8), dpi=300)
ax1 = fig.gca()
ax2 = ax1.twinx()

ax1.plot(h1_cp.xgrid[::-1], 100 * h1.cdf, '-', label="trig",)
ax2.plot(h1_cp.xgrid[::-1], 100 * (1-h2.cdf), '-', label="aux",)
plt.plot(h1_cp.xgrid[::-1], 100 * ((1-h2.cdf) - (1-h1.cdf)), '-', label=r"$\Delta$")
plt.xlim(min(h1_cp.xgrid), max(h1_cp.xgrid))
plt.xlabel("x")
ax1.set_ylabel("% vetoed")
ax2.set_ylabel("% DT")
plt.legend()
plt.title(channel)
save_name = f'veto_{channel}_{transformation_name}.png'
fig.savefig(PLOT_DIR + save_name, dpi=fig.dpi)


fig = plt.figure(figsize=(10, 8), dpi=300)
ax1 = fig.gca()
ax2 = ax1.twinx()

x_mean = (h1.xgrid[0] + h1.xgrid[-1]) / 2
x_new = h1.xgrid - x_mean

ax1.plot(x_new[::-1], 100 * h1.cdf, '-', label="trig",)
ax2.plot(x_new[::-1], 100 * (1-h2.cdf), '-', label="aux",)
plt.plot(x_new[::-1], 100 * ((1-h2.cdf) - (1-h1.cdf)), '-', label=r"$\Delta$")
plt.xlim(min(x_new), max(x_new))
plt.xlabel("x")
ax1.set_ylabel("% vetoed")
ax2.set_ylabel("% DT")
plt.legend()
plt.title(channel)
save_name = f'transformed_veto_{channel}_{transformation_name}.png'
fig.savefig(PLOT_DIR + save_name, dpi=fig.dpi)

plt.clf()
plt.plot(x_new, h1.cdf)
plt.xlim(min(x_new), max(x_new))
plt.show()

cdf1 = h1.cdf
middle = len(x_new) // 2
left, right = x_new[:middle], x_new[middle:]
cdf_left = cdf1[:middle]
cdf_right = cdf1[middle:]

x_combined = right + abs(left[::-1])
cdf_combined = cdf_right + cdf_left[::-1]

plt.plot(x_combined, cdf_combined)
plt.xlim(min(x_combined), max(x_combined))
plt.show()
