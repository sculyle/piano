import os
import mido
import RPi.GPIO as GPIO
import time
import sys

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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        midi_file_path = sys.argv[1]
        print(f"Playing MIDI file: {midi_file_path}")
    else:
        print("No MIDI file path provided")
        sys.exit(1)

    # Set up GPIO pins
    GPIO.setmode(GPIO.BCM)
    for pin in note_to_pin.values():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    paused = False

    try:
        midi_file = mido.MidiFile(midi_file_path)
        print(f"Loaded MIDI file: {midi_file_path}")

        for msg in midi_file.play():
            while paused:
                time.sleep(0.1)  # Wait while paused
            
            if msg.type == 'note_on' and msg.velocity > 0:
                mapped_note = map_note_to_piano(msg.note)
                pin = note_to_pin.get(mapped_note)
                if pin:
                    GPIO.output(pin, GPIO.HIGH)  # Turn on the corresponding GPIO pin
                    print(f"Note ON: {msg.note} (mapped to {mapped_note}), Pin {pin}")
                else:
                    print(f"Note ON: {msg.note} (mapped to {mapped_note}), No GPIO Pin")
            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                mapped_note = map_note_to_piano(msg.note)
                pin = note_to_pin.get(mapped_note)
                if pin:
                    GPIO.output(pin, GPIO.LOW)  # Turn off the corresponding GPIO pin
                    print(f"Note OFF: {msg.note} (mapped to {mapped_note}), Pin {pin}")
                else:
                    print(f"Note OFF: {msg.note} (mapped to {mapped_note}), No GPIO Pin")

    finally:
        for pin in note_to_pin.values():
            GPIO.output(pin, GPIO.LOW)  # Turn off all pins
        GPIO.cleanup()  # Cleanup GPIO settings after the MIDI file is done playing
        print("\nSong Ended")
        sys.stdout.flush()
