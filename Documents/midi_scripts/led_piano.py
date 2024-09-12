import RPi.GPIO as GPIO
import mido

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Map MIDI note numbers to GPIO pins
note_to_pin = {
    60: 5,  # C4 (Middle C)
    61: 6,  # C#4
    62: 23,  # D4
    63: 11,  # D#4
    64: 9,  # E4
    65: 10,  # F4
    66: 22,  # F#4
    67: 27,  # G4
    68: 17,  # G#4
    69: 4,  # A4
    70: 26,  # A#4
    71: 21  # B4
}

# Setup GPIO pins as outputs
for pin in note_to_pin.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Open the MIDI file
midi_file_path = '/home/instrumentgroup/Downloads/Carol.mid'
midi_file = mido.MidiFile(midi_file_path)

# Process the MIDI file
try:
    for msg in midi_file.play():
        if msg.type == 'note_on' and msg.velocity > 0:
            pin = note_to_pin.get(msg.note)
            if pin:
                GPIO.output(pin, GPIO.HIGH)  # Turn on the corresponding GPIO pin
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            pin = note_to_pin.get(msg.note)
            if pin:
                GPIO.output(pin, GPIO.LOW)  # Turn off the corresponding GPIO pin
finally:
    # Ensure all notes are turned off at the end
    for pin in note_to_pin.values():
        GPIO.output(pin, GPIO.LOW)  # Turn off all pins
    GPIO.cleanup()  # Cleanup GPIO settings after the MIDI file is done playing
