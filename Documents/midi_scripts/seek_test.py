import mido
import time

def play_midi_file(file_path, seek_time=0):
    # Load the MIDI file
    mid = mido.MidiFile(file_path)

    # Get the tempo in microseconds per beat
    tempo = 500000  # Default tempo (120 BPM)
    ticks_per_beat = mid.ticks_per_beat

    # Calculate the total time of the MIDI file
    total_time = sum(msg.time for track in mid.tracks for msg in track if not msg.is_meta)

    # Calculate the seek position in ticks
    seek_ticks = int((seek_time / (total_time / ticks_per_beat)) * ticks_per_beat)

    # Start playback
    for track in mid.tracks:
        time_passed = 0
        for msg in track:
            time_passed += msg.time
            if time_passed < seek_ticks:
                continue  # Skip messages until we reach the seek position

            # Send the MIDI message (for example, to a MIDI output)
            if not msg.is_meta:
                print(msg)  # Replace this with actual MIDI output code
                time.sleep(mido.tick2second(msg.time, ticks_per_beat, tempo))  # Wait for the message duration

# Example usage
play_midi_file('/home/instrumentgroup/Downloads/test_cde.mid', seek_time=0)  # Seek to 30 seconds
