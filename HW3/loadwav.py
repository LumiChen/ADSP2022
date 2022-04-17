import wave
import numpy as np
import simpleaudio as sa
import matplotlib.pyplot as plt


def sounds_(freq, amp, duration, sampling_freq=44100):
    t = np.linspace(0, duration, int(duration * sampling_freq))
    wave_data = amp * np.sin(2 * np.pi * freq * t)
    wave_data = wave_data.astype(np.int16)
    wave_data = (2 ** 15 - 1) * wave_data
    play_obj = sa.play_buffer(wave_data, 2, 2, sampling_freq)
    play_obj.wait_done()


# 88200  44100
freq = {'1': 262, '2': 294, '3': 330, '4': 349, '5': 392, '6': 440, '7': 494}

for i in [1, 1, 5, 5, 6, 6, 5,
          4, 4, 3, 3, 2, 2, 1,
          5, 5, 4, 4, 3, 3, 2,
          5, 5, 4, 4, 3, 3, 2,
          1, 1, 5, 5, 6, 6, 5,
          4, 4, 3, 3, 2, 2, 1]:
    sounds_(freq[str(i)], 4, 1, 44100)


# file = wave.open('wave.wav', 'wb')
# file.setnchannels(1)
# file.setsampwidth(2)
# file.setframerate(sampling_freq)
# file.setcomptype('NONE', 'not compressed')
# file.writeframes(wave_data.tobytes())
# file.close()
