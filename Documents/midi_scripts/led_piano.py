import os
import mido
import RPi.GPIO as GPIO
import sys
import signal
import threading
import time

# Map every note in any octave to C4-B4 for your piano (MIDI notes 60-71)
note_to_pin = {
    60: 21,  # C4 (Middle C)
    61: 20,  # C#4
    62: 26,  # D4
    63: 16,  # D#4
    64: 19,  # E4
    65: 13,  # F4
    66: 12,  # F#4
    67: 6,   # G4
    68: 5,   # G#4
    69: 24,  # A4
    70: 23,  # A#4
    71: 22   # B4
}

def map_note_to_piano(note):
    """Map any MIDI note to the C4-B4 range on your piano."""
    note_in_c4_range = (note % 12) + 60  # Shifts any octave note to C4-B4 range
    return note_in_c4_range

paused = False
playback_position = 0
pause_event = threading.Event()
max_velocity = 0
velocity_threshold = 0
active_notes = set()  # Track currently active notes

def handle_signal(signum, frame):
    global paused
    if signum == signal.SIGUSR1:
        paused = True
        pause_event.set()
        print(f"Paused at position: {playback_position}")
        sys.stdout.flush()
    elif signum == signal.SIGUSR2:
        paused = False
        pause_event.clear()

def get_tempo(midi_file_path):
    """Retrieve the tempo from the MIDI file."""
    midi_file = mido.MidiFile(midi_file_path)
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
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

def process_midi_message(msg, channel_select):
    """Process MIDI messages and control GPIO accordingly."""
    if msg.type in ['note_on', 'note_off'] and 0 <= msg.channel <= channel_select:
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


def main():
    global playback_position, paused, max_velocity, velocity_threshold, active_notes

    # Check if the MIDI file path, channels_allowed, percentage, and playback_position are provided
    if len(sys.argv) > 4:
        channels_allowed_value = int(sys.argv[1])  # Convert from string to integer
        midi_file_path = sys.argv[2]
        percentage = float(sys.argv[3])
        playback_position = float(sys.argv[4])  # Get playback position from arguments (in seconds)
        print(f"Channels Allowed: {channels_allowed_value}")
        print(f"Playing MIDI file: {midi_file_path} with filtering percentage: {percentage}")
        print(f"Starting from playback position: {playback_position} seconds")
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

        # Calculate the playback position in ticks
        ticks_per_second = midi_file.ticks_per_beat / (60 / get_tempo(midi_file_path))
        start_ticks = int(playback_position * ticks_per_second)

        playback = midi_file.play()

        # Skip directly to the first message at or beyond the start_ticks
        current_ticks = 0
        for msg in playback:
            current_ticks += msg.time  # Update current ticks

            # Check if we've reached or exceeded the start_ticks
            if current_ticks >= start_ticks:
                print(f"Starting playback at tick position: {current_ticks}")
                playback_position += (current_ticks - start_ticks) / ticks_per_second  # Update playback position
                break  # Exit the loop once we reach the desired position

        # Start processing MIDI messages immediately
        while True:
            if paused:
                pause_event.wait()  # Wait while paused
                continue
            
            try:
                # Process the current message
                process_midi_message(msg, channel_select)

                # Update playback position in seconds
                playback_position += msg.time / ticks_per_second  

                # Get the next message for processing
                msg = next(playback)

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

