import os
import mido
import RPi.GPIO as GPIO
import time
import threading
import sys
import termios
import tty


# Map every note in any octave to C4-B4 for your piano (MIDI notes 60-71)
note_to_pin = {
    60: 5,   # C4 (Middle C)
    61: 6,   # C#4
    62: 23,  # D4
    63: 11,  # D#4
    64: 9,   # E4
    65: 10,  # F4
    66: 22,  # F#4
    67: 27,  # G4
    68: 17,  # G#4
    69: 4,   # A4
    70: 26,  # A#4
    71: 21   # B4
}

# Function to map any MIDI note to the C4-B4 range
def map_note_to_piano(note):
    """Map any MIDI note to the C4-B4 range on your piano."""
    note_in_c4_range = (note % 12) + 60  # Shifts any octave note to C4-B4 range
    return note_in_c4_range

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
for pin in note_to_pin.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Prompt user to choose between MIDI files
midi_file_path_1 = '/home/instrumentgroup/Downloads/Carol.mid'
midi_file_path_2 = '/home/instrumentgroup/Downloads/Pathetique.mid'
midi_file_path_3 = '/home/instrumentgroup/Downloads/wii.mid'

# Extract file names without extensions
file_name_1 = os.path.splitext(os.path.basename(midi_file_path_1))[0]
file_name_2 = os.path.splitext(os.path.basename(midi_file_path_2))[0]
file_name_3 = os.path.splitext(os.path.basename(midi_file_path_3))[0]

# Prompt user to choose between MIDI files
print(f"Choose a MIDI file to play:")
print(f"1: {file_name_1}")
print(f"2: {file_name_2}")
print(f"3: {file_name_3}")
choice = input("Enter song choice: ")

if choice == '1':
    midi_file_path = midi_file_path_1
elif choice == '2':
    midi_file_path = midi_file_path_2
elif choice == '3':
    midi_file_path = midi_file_path_3
else:
    print("Invalid choice, defaulting to Carol")
    midi_file_path = midi_file_path_1

# Function to handle pause and resume
paused = False

def toggle_pause():
    global paused
    paused = not paused
    if paused:
        print("Playback paused. Press 'p' again to resume.")
    else:
        print("Playback resumed.")

# Non-blocking input for the 'p' key
def get_input():
    """Monitor keyboard input to detect 'p' for pausing."""
    global paused
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        while True:
            key = sys.stdin.read(1)
            if key == 'p':
                toggle_pause()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# Start the input listener in a separate thread
input_thread = threading.Thread(target=get_input)
input_thread.daemon = True
input_thread.start()

# Process the MIDI file with note remapping and pause function
try:
    midi_file = mido.MidiFile(midi_file_path)
    
    print("Press 'p' to pause/resume during playback.")
    
    for msg in midi_file.play():
        while paused:
            time.sleep(0.1)  # Wait while paused
        
        if msg.type == 'note_on' and msg.velocity > 0:
            mapped_note = map_note_to_piano(msg.note)
            pin = note_to_pin.get(mapped_note)
            if pin:
                GPIO.output(pin, GPIO.HIGH)  # Turn on the corresponding GPIO pin
        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
            mapped_note = map_note_to_piano(msg.note)
            pin = note_to_pin.get(mapped_note)
            if pin:
                GPIO.output(pin, GPIO.LOW)  # Turn off the corresponding GPIO pin
finally:
    for pin in note_to_pin.values():
        GPIO.output(pin, GPIO.LOW)  # Turn off all pins
    GPIO.cleanup()  # Cleanup GPIO settings after the MIDI file is done playing
