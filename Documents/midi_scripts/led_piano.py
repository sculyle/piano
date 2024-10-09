import os
import mido
import RPi.GPIO as GPIO
import sys
import signal
import threading

# Map every note in any octave to C4-B4 for your piano (MIDI notes 60-71)
note_to_pin = {
    60: 4,   # C4 (Middle C)
    61: 17,  # C#4
    62: 27,  # D4
    63: 22,  # D#4
    64: 23,  # E4
    65: 10,  # F4
    66: 9,   # F#4
    67: 11,  # G4
    68: 5,   # G#4
    69: 6,   # A4
    70: 26,  # A#4
    71: 21   # B4
}

def map_note_to_piano(note):
    """Map any MIDI note to the C4-B4 range on your piano."""
    note_in_c4_range = (note % 12) + 60  # Shifts any octave note to C4-B4 range
    return note_in_c4_range

paused = False
playback_position = 0
pause_event = threading.Event()
resume_event = threading.Event()
max_velocity = 0
velocity_threshold = 0
active_notes = set()  # Track currently active notes

def handle_signal(signum, frame):
    global paused, playback_position
    if signum == signal.SIGUSR1:
        paused = True
        pause_event.set()
        #print("Paused")
        print(f"Paused at position: {playback_position}")
        sys.stdout.flush()
        sys.exit()
    elif signum == signal.SIGUSR2:
        paused = False
        resume_event.set()
        #print("Resumed")

def get_tempo(midi_file_path):
    """Retrieve the tempo from the MIDI file."""
    midi_file = mido.MidiFile(midi_file_path)
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                # Tempo is specified in microseconds per beat
                return mido.tempo2bpm(msg.tempo)  # Convert to BPM
    return 120  # Default to 120 BPM if no tempo is found

def find_max_velocity(midi_file):
    """Scan the MIDI file to find the maximum velocity value."""
    max_velocity = 0
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > max_velocity:
                max_velocity = msg.velocity
    return max_velocity



# Add this function to continuously update playback position
def update_playback_position(playback):
    global playback_position
    while True:
        if paused:
            time.sleep(0.1)  # Sleep if paused to avoid busy-waiting
            continue
        try:
            msg = next(playback)  # Get the next MIDI message
            playback_position += msg.time  # Update playback position
            time.sleep(0.01)  # Add slight delay to reduce CPU usage
        except StopIteration:
            break


def main():
    global playback_position, paused, max_velocity, velocity_threshold, active_notes
    
    # Check if the MIDI file path, channels_allowed, percentage, and playback_position are provided
    if len(sys.argv) > 4:
        channels_allowed_value = int(sys.argv[1])  # Convert from string to integer
        midi_file_path = sys.argv[2]
        percentage = float(sys.argv[3])
        playback_position = int(sys.argv[4])  # Get playback position from arguments
        print(f"Channels Allowed: {channels_allowed_value}")
        print(f"Playing MIDI file: {midi_file_path} with filtering percentage: {percentage}")
        print(f"Starting from playback position: {playback_position}")
    else:
        print("No MIDI file path, channels allowed, filtering percentage, or playback position provided")
        sys.exit(1)

    # Determine channel_select based on channels_allowed_value
    if channels_allowed_value == 1:
        channel_select = 6
    elif channels_allowed_value == 0:
        channel_select = 15
    else:
        print("Invalid channels_allowed_value. It should be either 0 or 15.")
        sys.exit(1)

    # Check if the file exists
    if not os.path.isfile(midi_file_path):
        print(f"File not found: {midi_file_path}")
        sys.exit(1)

    # Set up GPIO pins
    GPIO.setmode(GPIO.BCM)
    for pin in note_to_pin.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    # Set signal handlers
    signal.signal(signal.SIGUSR1, handle_signal)
    signal.signal(signal.SIGUSR2, handle_signal)

    try:
        midi_file = mido.MidiFile(midi_file_path)
        print(f"Loaded MIDI file: {midi_file_path}")

        # Find the maximum velocity in the MIDI file
        max_velocity = find_max_velocity(midi_file)
        velocity_threshold = max_velocity * (percentage / 100)
        print(f"Max Velocity: {max_velocity}, Velocity Threshold: {velocity_threshold}")

        # Initialize playback
        playback = midi_file.play()

        

        # Continue playback from the current position
        while True:
            if paused:
                pause_event.wait()  # Wait while paused
                continue
            
            try:
                msg = next(playback)
                playback_position += msg.time

                # Modify this part to utilize channel_select
                if msg.type in ['note_on', 'note_off']:
                    # Only process note messages if they are on the allowed channels
                    if 0 <= msg.channel <= channel_select:
                        mapped_note = map_note_to_piano(msg.note)
                        pin = note_to_pin.get(mapped_note)

                        if msg.type == 'note_on' and msg.velocity > velocity_threshold:
                            if pin:
                                GPIO.output(pin, GPIO.HIGH)  # Turn on the corresponding GPIO pin
                                active_notes.add(msg.note)  # Add note to active notes
                                print(f"Note ON: {msg.note} (mapped to {mapped_note}), Pin {pin}, Velocity: {msg.velocity}")
                        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                            if pin:
                                GPIO.output(pin, GPIO.LOW)  # Turn off the corresponding GPIO pin
                                active_notes.discard(msg.note)  # Remove note from active notes
                                print(f"Note OFF: {msg.note} (mapped to {mapped_note}), Pin {pin}")

                # Output currently active notes
                print(f"Currently active notes: {list(active_notes)}")

            except StopIteration:
                # MIDI file playback has finished
                print("MIDI playback has finished.")
                break

    finally:
        for pin in note_to_pin.values():
            GPIO.output(pin, GPIO.LOW)  # Turn off all pins
        GPIO.cleanup()  # Cleanup GPIO settings after the MIDI file is done playing
        print("\nSong Ended")
        sys.stdout.flush()

if __name__ == "__main__":
    main()

