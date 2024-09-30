import tkinter as tk
from tkinter import ttk
import subprocess
import os
import signal
import mido

# Function to find max velocity
def find_max_velocity(midi_file_path):
    """Scan the MIDI file to find the maximum velocity value."""
    max_velocity = 0
    midi_file = mido.MidiFile(midi_file_path)
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > max_velocity:
                max_velocity = msg.velocity
    return max_velocity

root = tk.Tk()

canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=8, rowspan=9)
label = ttk.Label(root, text='Choose Your Song', font=('Calibri', 15))
label.grid(columnspan=1, column=1, row=1)

enable = 0
stop = 0
process = None

# Variables for user input
velocity_percentage = tk.DoubleVar(value=50)  # Default value

def button_func1():
    global enable
    enable = 1
    currentsong()

def button_func2():
    global enable
    enable = 2
    currentsong()

def button_func3():
    global enable
    enable = 3
    currentsong()

def button_func4():
    global enable
    enable = 4
    currentsong()

def pause():
    global process
    if process:
        print("Pausing the song.")
        process.send_signal(signal.SIGUSR1)  # Send signal to pause
    else:
        print("No song is currently playing.")

def play():
    global process
    if process:
        print("Resuming the song.")
        process.send_signal(signal.SIGUSR2)  # Send signal to resume
    else:
        print("No song is currently playing.")

def stop_previous_process():
    """Stop the previous process if it's running."""
    global process
    if process:
        print("Stopping current process.")
        process.send_signal(signal.SIGINT)  # Send interrupt signal
        process.wait()  # Wait for process to terminate
        process = None

def run_led_piano(midi_file_path, percentage):
    global process
    stop_previous_process()

    print(f"Running led_piano.py with file: {midi_file_path} and filtering percentage: {percentage}")

    process = subprocess.Popen(['python3', 'led_piano.py', midi_file_path, str(percentage)], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                               preexec_fn=os.setsid)  # Start the process in a new process group

def currentsong():
    global enable, stop
    if stop == 1:
        print('Playback is paused')
        stop_previous_process()
        return

    percentage = velocity_percentage.get()
    if enable == 1:
        print('Playing Song A')
        run_led_piano('/home/instrumentgroup/Downloads/Carol.mid', percentage)
    elif enable == 2:
        print('Playing Song B')
        run_led_piano('/home/instrumentgroup/Downloads/Pathetique.mid', percentage)
    elif enable == 3:
        print('Playing Song C')
        run_led_piano('/home/instrumentgroup/Downloads/wii.mid', percentage)
    elif enable == 4:
        print('Playing Song D')
        # Add the path for Song D if available

# Velocity percentage input
ttk.Label(root, text='Velocity Filter Percentage (0-100):').grid(column=1, row=0)
velocity_entry = ttk.Entry(root, textvariable=velocity_percentage)
velocity_entry.grid(column=2, row=0)

style = ttk.Style()
style.configure('TButton', background='white')

button1 = ttk.Button(root, text='Song A', command=button_func1)
button1.grid(column=1, row=2)
button2 = ttk.Button(root, text='Song B', command=button_func2)
button2.grid(column=1, row=3)
button3 = ttk.Button(root, text='Song C', command=button_func3)
button3.grid(column=1, row=4)
button4 = ttk.Button(root, text='Song D', command=button_func4)
button4.grid(column=1, row=5)
pauseplz = ttk.Button(root, text='Pause', command=pause)
pauseplz.grid(column=1, row=6)
playplz = ttk.Button(root, text='Play', command=play)
playplz.grid(column=1, row=7)

root.mainloop()
