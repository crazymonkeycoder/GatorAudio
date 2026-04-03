import mido
import sounddevice as sd
import numpy as np
from collections import deque
import time
def get_midi_timeline(file_path):
    mid = mido.MidiFile(file_path)
    timeline = []
    absolute_time = 0
    for msg in mid:
        absolute_time += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            timeline.append({'note': msg.note, 'time': absolute_time})
    return timeline
def hz_to_midi(hz):
    if hz < 50: return None
    return int(round(12 * np.log2(hz / 440) + 69))
freq = 48000
buffer_size = int(freq * 0.2)
audio_buffer = deque(maxlen=buffer_size)
long_term_vol = 0.001
THRESHOLD_RATIO = 2.5
midi_name = ''
score = get_midi_timeline(midi_name)
score_index = 0
start_time = None
def callback(indata, frames, time_info, status):
    global long_term_vol, score_index, start_time
    
    audio_data = indata.flatten()
    audio_buffer.extend(audio_data)
    current_vol = np.max(np.abs(audio_data))
    if current_vol > (long_term_vol * THRESHOLD_RATIO) and current_vol > 0.005:
        if start_time is None: 
            start_time = time.time()
            print("Performance Started!")
        actual_time = time.time() - start_time
        full_slice = np.array(audio_buffer)
        fft_data = np.abs(np.fft.rfft(full_slice * np.hanning(len(full_slice))))
        hz = np.argmax(fft_data) * (freq / len(full_slice))
        played_midi = hz_to_midi(hz)
        if score_index < len(score):
            expected = score[score_index]
            error = actual_time - expected['time']
            
            print(f"STRIKE! Note: {played_midi} | Expected: {expected['note']} | Offset: {error:+.3f}s")            
            score_index += 1

    long_term_vol = (long_term_vol * 0.95) + (current_vol * 0.05)
with sd.InputStream(callback=callback, channels=1, samplerate=freq):
    print("AI ready. Play the first note of your MIDI file...")
    while score_index < len(score):
        time.sleep(0.1)