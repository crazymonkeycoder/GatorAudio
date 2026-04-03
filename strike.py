import sounddevice as sd
import numpy as np
from collections import deque
import time
freq = 48000
buffer_size = int(freq * 0.2) 
audio_buffer = deque(maxlen=buffer_size)
THRESHOLD_RATIO = 2.5 
long_term_vol = 0.001

def callback(indata, frames, time_info, status):
    global long_term_vol
    audio_data = indata.flatten()
    audio_buffer.extend(audio_data)
    current_vol = np.max(np.abs(audio_data))
    
    if current_vol > (long_term_vol * THRESHOLD_RATIO) and current_vol > 0.005:
        timestamp = time.time()
        full_slice = np.array(audio_buffer)
        fft_data = np.abs(np.fft.rfft(full_slice * np.hanning(len(full_slice))))
        hz = np.argmax(fft_data) * (freq / len(full_slice))
        print(f"STRIKE! Time: {timestamp:.3f} | Hz: {hz:.1f} | Vol: {current_vol:.4f}")
    long_term_vol = (long_term_vol * 0.95) + (current_vol * 0.05)
with sd.InputStream(callback=callback, channels=1, samplerate=freq):
    while True:
        time.sleep(1)