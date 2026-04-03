import mido

def get_midi_timeline(file_path):
    mid = mido.MidiFile(file_path)
    timeline = []
    absolute_time = 0
    #A midi file contains messages that represents events like note on
    for msg in mid:
        absolute_time += msg.time # mido converts ticks to seconds automatically
        if msg.type == 'note_on' and msg.velocity > 0:
            timeline.append({
                'note': msg.note, 
                'expected_time': absolute_time
            })
    return timeline

score = get_midi_timeline('sonata.mid')