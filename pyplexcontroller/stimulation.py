import nidaqmx
import numpy
from typing import List, Union

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
        interval: float = 5
    ):
        self.type = "trigger"
        begin = 0 # sec
        stim_end = begin + interval * ntrials
        stim_ts = numpy.arange(begin, stim_end, interval)
        # tbs_ts = convert_to_tbs(stim_ts)
        return stim_ts

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
        self.type = "interval"
        self.duration = duration

class Timeline():
    def __init__(
        self,
        stimulations: List[Union[Stimulation, Interval]] = [],
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
        trig_duration = max(0.005, 2/self.fs)
        self.record_intervals = (
            1, # before start
            5, # after start
            5, # before end
            1  # after end
        )

        self.stim_timeline = []
        self.trig_timeline = []

        for stimulation in stimulations:
            if stimulation.type == "trigger":
                # Convert the timestamps to a waveform
                waveform = self._generate_trigger_waveform(stimulation.stim_ts)
                # Append the waveform to the stim_timeline
                # self.stim_timeline += [waveform]
            elif stimulation.type == "interval":
                # Generate interval based on the duration
                nsamples = int(stimulation.duration * self.fs)
                waveform = numpy.zeros(nsamples)
                # self.stim_timeline += [waveform]
        self.stim_timeline = numpy.ndarray(self.stim_timeline).flatten()
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
    
    def _append_to_timeline(self, timeline: list, waveform: numpy.ndarray):
        start_trig = self._generate_trigger_waveform(numpy.array([self.record_intervals[0]]))
    
    def _rec_start_trigger(self):
        trig_waveform = self._generate_trigger_waveform()
    
    def _trigger_waveform(self, ts: float = 0):
        trig_rise = int(self.fs * ts)
        trig_fall = int(self.fs * (ts + self.trig_duration))
        trigger_waveform[trig_rise: trig_fall] = trig_voltage

    def _generate_trigger_waveform(self, stim_ts: numpy.ndarray):
        trig_voltage = 3 # V
        
        duration = stim_ts[-1] + trig_duration # sec
        nsample = int(duration * self.fs)
        
        t = numpy.linspace(0, duration, nsample, endpoint=False)

        trigger_waveform = numpy.zeros(nsample)
        for ts in stim_ts:
            trig_rise = int(self.fs * ts)
            trig_fall = int(self.fs * (ts + trig_duration))
            trigger_waveform[trig_rise: trig_fall] = trig_voltage
        trigger_waveform[-1] = 0
        
        return trigger_waveform

def convert_to_tbs(stim_ts: numpy.ndarray):
    return  numpy.array([
        [numpy.round(ts + itr, 5) for itr in [0, 0.02, 0.04]]
        for ts in stim_ts
    ]).flatten()

def record():
    pass

if __name__ == "__main__":

    single_ms = SingleMS(ntrials=30, interval=5)
    iTBS = iTBS(ntrials=30)
    stimulations = [
        single_ms,
        five_min,
        iTBS,
        single_ms
    ]
    
    timeline = Timeline(stimulations)
