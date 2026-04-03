import sounddevice as sd
import numpy as np
freq = 48000
dur = 0.1

recording = sd.rec(int(dur*freq), samplerate=freq, channels=1)
sd.wait()
print(recording[:10])
print(f'\nPeak Vol: {np.max(np.abs(recording)):.5f}')
