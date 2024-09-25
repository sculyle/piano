import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
import subprocess
import os
import signal
import mido

# Function to find max velocity (from the old version)
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
root.configure(background='white')

canvas = tk.Canvas(root, width=400, height=400, background='white')
canvas.grid(columnspan=20, rowspan=20)

# Song label
label = tk.Label(root, text='Song Choice', font=('Roboto', 15), background='white')
label.grid(columnspan=3, column=2, row=4)

# Variables to track state
enable = 0
stop = 0
process = None
song = 'Select song choice.'
velocity_percentage = tk.DoubleVar(value=50)  # Default value

# Functions for button handling
def button_func1():
    global enable, stop
    enable = 1
    stop = 0
    currentsong()

def button_func2():
    global enable, stop
    enable = 2
    stop = 0
    currentsong()

def button_func3():
    global enable, stop
    enable = 3
    stop = 0
    currentsong()

def button_func4():
    global enable, stop
    enable = 4
    stop = 0
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
    percentage = velocity_percentage.get()
    if enable == 1 and stop == 0:
        print('Playing Wii Theme')
        run_led_piano('/home/instrumentgroup/Downloads/wii.mid', percentage)
    elif enable == 2 and stop == 0:
        print('Playing Jingle Bells')
        run_led_piano('/home/instrumentgroup/Downloads/Carol.mid', percentage)
    elif enable == 3 and stop == 0:
        print('Playing Song C')
        run_led_piano('/home/instrumentgroup/Downloads/Pathetique.mid', percentage)
    elif enable == 4 and stop == 0:
        print('Playing Song D')
        # Add path for Song D if available
    elif stop == 1:
        print('Song is on Pause')

    display()

# Function to handle the slider update
def slider_update(val):
    if enable != 0 and stop == 0:
        print(f"Slider updated, new velocity filter: {val}%")
        currentsong()  # Automatically play with new percentage

def display():
    global song, enable, canvas
    imagepath = '/home/instrumentgroup/Downloads/loading2.0.png'  # Default image path
    
    if enable == 1:
        imagepath = '/home/instrumentgroup/Downloads/wii.png'
        song = '? Playing Wii Theme ?'
    elif enable == 2:
        imagepath = '/home/instrumentgroup/Downloads/lesbells.png'
        song = '? Playing Jingle Bells ?'
    elif enable == 3:
        imagepath = '/home/instrumentgroup/Downloads/utie2.0.png'
        song = '? Playing Song C ?'
    elif enable == 4:
        imagepath = '/home/instrumentgroup/Downloads/eatingcats.png'
        song = '? Playing Song D ?'
    
    image_og = Image.open(imagepath)
    image_tk = ImageTk.PhotoImage(image_og)
    canvas.image_tk = image_tk
    canvas.grid(columnspan=6, column=8, row=6)
    canvas.create_image(8, 4, image=canvas.image_tk, anchor='nw')
    label2.config(text=song)

# Play and Pause buttons
play_image = Image.open('/home/instrumentgroup/Downloads/playbutton.png')
play_image_tk = ImageTk.PhotoImage(play_image)
play_button = tk.Button(root, image=play_image_tk, command=play, background='white', borderwidth=0)
play_button.grid(column=9, row=16)

pause_image = Image.open('/home/instrumentgroup/Downloads/pausebutton.png')
pause_image_tk = ImageTk.PhotoImage(pause_image)
pause_button = tk.Button(root, image=pause_image_tk, command=pause, background='white', borderwidth=0)
pause_button.grid(column=8, row=16, padx=(0, 10))

# Song buttons
button1_image = Image.open('/home/instrumentgroup/Downloads/button_wii-theme(1).png')
button1_image_tk = ImageTk.PhotoImage(button1_image)
button1 = tk.Button(root, image=button1_image_tk, command=button_func1, background='white', borderwidth=0)
button1.grid(column=3, row=6)

button2_image = Image.open('/home/instrumentgroup/Downloads/button_jingle-bells(1).png')
button2_image_tk = ImageTk.PhotoImage(button2_image)
button2 = tk.Button(root, image=button2_image_tk, command=button_func2, background='white', borderwidth=0)
button2.grid(column=3, row=8)

button3_image = Image.open('/home/instrumentgroup/Downloads/button_song-a(1).png')
button3_image_tk = ImageTk.PhotoImage(button3_image)
button3 = tk.Button(root, image=button3_image_tk, command=button_func3, background='white', borderwidth=0)
button3.grid(column=3, row=10)

button4_image = Image.open('/home/instrumentgroup/Downloads/button_song-b(2).png')
button4_image_tk = ImageTk.PhotoImage(button4_image)
button4 = tk.Button(root, image=button4_image_tk, command=button_func4, background='white', borderwidth=0)
button4.grid(column=3, row=12)

# Label for song title
label2 = tk.Label(root, text=song, font=('Ariel', 13), background='white')
label2.grid(columnspan=6, column=4, row=14)

# Velocity Percentage Slider
velocity_slider_label = tk.Label(root, text="Set Velocity Filter", font=('Ariel', 13), background='white')
velocity_slider_label.grid(columnspan=6, column=4, row=18)

velocity_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, variable=velocity_percentage, background='white', command=slider_update)
velocity_slider.grid(columnspan=6, column=4, row=19)

# Display initial image
display()

root.mainloop()
