import math
import numpy
import matplotlib.pyplot as plt

from settings import Settings

class Waveform:
    def __init__(
        self,
        waveform: numpy.ndarray,
        settigns: Settings
    ):
        self.waveform = waveform
        self.duration = numpy.round((waveform.size - 1) * settigns.ps, 6)
        self.settings = settings
        return

    def plot(self):
        ps = 1 / settings.fs
        time = numpy.arange(0, self.duration + ps, ps)
        plt.plot(time, self.waveform)
        plt.show()
        return

class Trigger(Waveform):
    def __init__(
        self,
        settings: Settings,
        duration: float = 0.001,
        voltage: float = 3,
    ):
        nsamples = int(settings.fs * duration)
        waveform_list = [voltage] * nsamples
        waveform_list += [0]

        self.waveform = numpy.array(waveform_list)
        self.duration = duration
        self.settings = settings
        return

if __name__ == "__main__":
    # test
    settings = Settings()
    duration = 1 # sec
    time = numpy.arange(0, duration + settings.ps, settings.ps)
    _wf = numpy.sin(2 * math.pi * time)

    waveform = Waveform(_wf, settings)
    waveform.plot()
    
    trigger = Trigger(settings)
    trigger.plot()