import sounddevice as sd
import numpy as np

def hz_to_note(hz):
    if hz < 50: return None
    # MIDI formula: 12 * log2(f/440) + 69
    midi_num = 12 * np.log2(hz / 440) + 69
    n = int(round(midi_num))
    
    names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    note_name = names[n % 12]
    octave = (n // 12) - 1
    return f"{note_name}{octave}"

freq = 48000
dur = 0.3
#find out with testinputdevice
micId = 1 

# Memory to filter out random flickers
last_note = None

print("Piano Reader Active. Play a scale!")

try:
    while True:
        recording = sd.rec(int(dur*freq), samplerate=freq, channels=1, device=micId)
        sd.wait()
        
        audio_data = recording.flatten()
        peak = np.max(np.abs(audio_data))
        
        # Adjust this threshold based on gain
        if peak > 0.005: # Bumped slightly to ignore background air
            fft_data = np.abs(np.fft.rfft(audio_data))
            if np.max(fft_data) > (np.mean(fft_data) * 10):
                max_index = np.argmax(fft_data)
                detected_hz = max_index * (freq / len(audio_data))
                
                if 50 < detected_hz < 4000:
                    note = hz_to_note(detected_hz)
                    
                    # Only print if we hear the same note twice (Stability)
                    if note == last_note:
                        print(f"Note: {note} | Hz: {detected_hz:.1f} | Vol: {peak:.4f}")
                    
                    last_note = note
        else:
            last_note = None
            print("Listening...", end='\r')

except KeyboardInterrupt:
    print("\nStopped.")