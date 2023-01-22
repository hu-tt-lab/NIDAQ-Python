import numpy as np
import nidaqmx as ni
from nidaqmx import constants

fs = 800000          # サンプリングレート 800 kHz
dur = 3600           # 波形の時間長さ 3600 sec
n_samp = fs * dur    # 波形のサンプル数

chunk_dur = 2                       # 波形を何秒で区切るか 2 sec
chunk_size = fs * chunk_dur        # チャンクサイズ
n_chunk = int(n_samp / chunk_size)  # チャンク数

def get_wav_chunk(i: int):
    start = i * chunk_size
    end = start + chunk_size - 1
    t = np.linspace(start, end, chunk_size)  # 1チャンク分の
    wav = np.sin(2 * np.pi * t)      #  1 Hz sin波
    return wav

with ni.Task() as task:
    task.ao_channels.add_ao.voltage_chan("Dev1/ao1")  # タスクにoutputチャンネル追加
    task.timing.cfg_samp_clk_timing(
        rate = fs,              # サンプリングレート
        samps_per_chan = n_samp # サンプル数
    )
    for i_chunk in range(n_chunk):
        task.write(get_wav_chunk(i_chunk), auto_start=True)  # 波形出力
        task.wait_unitl_done()                               # 待機
        task.stop()                                          # 終了