import os
import mido
import RPi.GPIO as GPIO
import time
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
    global paused
    if signum == signal.SIGUSR1:
        paused = True
        pause_event.set()
        print("Paused")
    elif signum == signal.SIGUSR2:
        paused = False
        resume_event.set()
        print("Resumed")

def find_max_velocity(midi_file):
    """Scan the MIDI file to find the maximum velocity value."""
    max_velocity = 0
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > max_velocity:
                max_velocity = msg.velocity
    return max_velocity

def main():
    global playback_position, paused, max_velocity, velocity_threshold, active_notes
    
    # Check if the MIDI file path and percentage are provided
    if len(sys.argv) > 2:
        midi_file_path = sys.argv[1]
        percentage = float(sys.argv[2])
        print(f"Playing MIDI file: {midi_file_path} with filtering percentage: {percentage}")
    else:
        print("No MIDI file path or filtering percentage provided")
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

        while True:
            if paused:
                pause_event.wait()  # Wait while paused
                continue
            
            try:
                msg = next(playback)
                playback_position += msg.time

                # Only process note messages if they are on channels 1-7 (0-6 in mido)
                if msg.type in ['note_on', 'note_off'] and 0 <= msg.channel <= 6:
                    mapped_note = map_note_to_piano(msg.note)
                    pin = note_to_pin.get(mapped_note)

                    if msg.type == 'note_on' and msg.velocity >= velocity_threshold:
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
                break

    finally:
        for pin in note_to_pin.values():
            GPIO.output(pin, GPIO.LOW)  # Turn off all pins
        GPIO.cleanup()  # Cleanup GPIO settings after the MIDI file is done playing
        print("\nSong Ended")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
