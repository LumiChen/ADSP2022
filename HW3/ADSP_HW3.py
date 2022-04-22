import wave
import numpy as np
import simpleaudio as sa
import pyaudio
import soundfile
import matplotlib.pyplot as plt
from scipy.fftpack import fft


# 定義正弦波
def sine(frequency, duration, rate):
    n = int(duration * rate)
    interval = 2 * np.pi * frequency / rate
    return np.arange(n) / rate, np.sin(np.arange(n) * interval)  # 產生兩個特定頻率的聲音資料


def generator(f1, f2, duration, rate=44100, start=0):
    t1, d1 = sine(f1, duration, rate)
    t2, d2 = sine(f2, duration, rate)
    data = np.stack((t1 + start, d1, d2), axis=1)
    return data


if __name__ == '__main__':

    do_once = False
    # initail
    fs = 44100  # sampling fraquency
    while not do_once:
        # user inputs
        # 題目要求功能
        print("------------請輸入簡譜-------------")
        score = list(input("score:"))
        print("------------請輸入beat------------")
        beat_temp = list(input("beat:"))
        beat = map(int, beat_temp)
        if len(score) == len(beat_temp):
            print("------------請輸入要存的檔名------------")
            name = str(input("name:"))
            # score = ['1', '1', '5', '5', '6', '6', '5']
            # beat = [1, 1, 1, 1, 1, 5, 2]
            # name = "ADSP_HW3"

            # 新增功能
            # 設定Do的初始頻率
            # 設定每個拍子的秒數
            Do = 131   # Hz
            seconds_per_beat = 0.5
            beat = [i * seconds_per_beat for i in beat]  # 調整beat秒數

            freq = {'0': 0,                    # 第三種功能 當輸入0時會靜音
                    '1': Do,                   # Do
                    '2': Do * (2**(2 / 12)),   # Re
                    '3': Do * (2**(4 / 12)),   # Mi
                    '4': Do * (2**(5 / 12)),   # Fa
                    '5': Do * (2**(7 / 12)),   # So
                    '6': Do * (2**(9 / 12)),   # La
                    '7': Do * (2**(11 / 12))}  # Si

            wave_data = []
            for i in range(len(score)):
                tmp = generator(f1=freq[score[i]], f2=freq[score[i]],  # 雙聲道
                                duration=beat[i], start=i * beat[i])
                wave_data = np.append(wave_data, tmp)
            wave_data = wave_data.reshape(int(len(wave_data) / 3), 3)

            # 播放
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paFloat32, channels=2, rate=fs, output=True)
            stream.write(wave_data[:, 1:].astype(np.float32).tobytes())
            stream.stop_stream()
            stream.close()
            p.terminate()

            # 存檔
            soundfile.write(name + '.wav', wave_data[:, 1:], fs, subtype='PCM_24')
            print("{} saved".format(name + '.wav'))

            do_once = True
        else:
            print("*****請注意簡譜與beat長度需為等長*****")


