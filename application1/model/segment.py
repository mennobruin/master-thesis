

class Segment:

    def __init__(self, channel, x, dt, f_sample, gps_time, unit=None):
        self.channel = channel
        self.x = x
        self.dt = dt
        self.f_sample = f_sample
        self.gps_time = gps_time
        self.unit = unit
        self.decimated = False

    @property
    def x_size(self):
        return int(self.dt * self.f_sample)
