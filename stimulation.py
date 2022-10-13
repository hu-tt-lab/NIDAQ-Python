import nidaqmx
import numpy

class Stimulation:
    def __init__(
        self,
        stim_ts: numpy.ndarray,
        type = "trigger"
    ):
        self.type = type
        self.stim_ts = stim_ts
        return

class SingleMS(Stimulation):
    def __init__(
        self,
        ntrials: int = 30,
        interval: float = 5, # sec
    ):
        self.type = "trigger"
        begin = 0
        

class iTBS(Stimulation):
    def __init__(
        self,
        ntrials: int = 30,
        # voltage: float = 40
    ):
        begin = 0
        interval = 10 # sec
        end = begin + interval * ntrials
        timestamps = numpy.array([
            [numpy.round(ts + itr, 5) for itr in numpy.arange(0, 2, 0.2)]
            for ts in numpy.arange(begin, end, interval)
        ]).flatten()
        stim_ts = convert_to_tbs(timestamps)

        self.type = "trigger"
        self.stim_ts = stim_ts

class Interval():
    def __init__(self, duration):
        pass

class Timeline():
    def __init__(
        self,
        stimulations: list[Stimulation] = [],
        fs: float = 40000,
        device: str = "Dev2",
        stim_ch: str = "ao0",
        trig_ch: str = "ao1",
    ):
        self.stimulations = stimulations
        self.fs = fs
        self.device = device
        self.stim_ch = stim_ch
        self.trig_ch = trig_ch

        self.stim_timeline = numpy.array([])
        self.trig_timeline = numpy.array([])
        return

    def play(
        self, timeout=1800
    ):
    # TODO: finish this script
        if self.type == "trigger":
            waveform = self._generate_trigger_waveform()

        nsamples = self.waveform.shape[0]
        with nidaqmx.Task() as write_task:
            for o in [f"{self.device}/ao0"]:
                aochan = write_task.ao_channels.add_ao_voltage_chan(o)
                aochan.ao_max = 3.5   # output range of USB-4431
                aochan.ao_min = -3.5

            write_task.timing.cfg_samp_clk_timing(rate=self.fs, source='OnboardClock', samps_per_chan=nsamples)
            write_task.write(outdata, auto_start=True)
            write_task.wait_until_done(timeout=timeout)
            write_task.stop()
        return

    def _generate_trigger_waveform(self, stim_ts: numpy.ndarray):
        trig_voltage = 3 # V
        duration = rec_fin - rec_start # sec
        nsample = int(duration * self.fs)
        
        trig_duration = max(0.005, 2/self.fs)
        t = numpy.linspace(0, duration, nsample, endpoint=False)

        trigger_waveform = numpy.zeros(nsample)
        for trig_timing in self.stimulations:
            trig_rise = int(self.fs * trig_timing)
            trig_fall = int(self.fs * (trig_timing + trig_duration))
            trigger_waveform[trig_rise: trig_fall] = trig_voltage
        
        return trigger_waveform

def convert_to_tbs(stim_ts: numpy.ndarray):
    return  numpy.array([
        [numpy.round(ts + itr, 5) for itr in [0, 0.02, 0.04]]
        for ts in stim_ts
    ]).flatten()

def record():
    pass

if __name__ == "__main__":
    stim_trials = 30
    stim_begin = 10 # sec
    stim_interval = 5 # sec
    stim_end = stim_begin + stim_interval * stim_trials
    stim_ts = numpy.arange(stim_begin, stim_end, stim_interval)
    tbs_ts = convert_to_tbs(stim_ts)
    recording_end = stim_end + 10 # sec

    itbs_trials = 30
    itbs_begin = stim_begin
    itbs_interval = 10 # sec
    itbs_end = itbs_begin + itbs_interval * itbs_trials
    itbs_ts = numpy.array([
        [numpy.round(ts + itr, 5) for itr in numpy.arange(0, 2, 0.2)]
        for ts in numpy.arange(itbs_begin, itbs_end, itbs_interval)
    ]).flatten()
    itbs_ts = convert_to_tbs(itbs_ts)

    single_ms = Stimulation(stim_ts, "trigger")
    single_TBS = Stimulation(tbs_ts, "trigger")
    iTBS = iTBS()


    stimulations = [
        single_ms,
        iTBS,
        single_ms
    ]