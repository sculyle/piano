#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  withbar.py
#  
#  Copyright 2024  <instrumentgroup@instrument>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
import subprocess
import os
import signal
import mido
from tkinter import HORIZONTAL, Button  # import Button and HORIZONTAL


# Setup Config
root = tk.Tk()
root.configure(background = 'white')

canvas = tk.Canvas(root, width = 400, height = 400, background = 'white')
canvas.grid(columnspan=20, rowspan = 20)
label = tk.Label(root, text = ' Song Choice', font = ('Roboto', 15), background = 'white')
label.grid(columnspan =3, column = 2, row = 4)
play_button_path = '/home/instrumentgroup/Downloads/playbutton.png'
pause_button_path = '/home/instrumentgroup/Downloads/pausebutton.png'
likee = '/home/instrumentgroup/Downloads/likee.jpg'
nolikee = '/home/instrumentgroup/Downloads/nolikee.jpg'
pause_path = play_button_path
play_path = pause_button_path


# Like Button Declarations
song1like = 0
song2like = 0
song3like = 0
song4like = 0


# Variables to track state
enable = 0
stop = 0
process = None
song = 'Select song choice.'
like = 0
velocity_percentage = tk.DoubleVar(value=50)  # Default value
channels_allowed = tk.BooleanVar(value=False)  # Checkbox variable

# Function responsible for the update of the progress bar value
progress = ttk.Progressbar(root, orient=HORIZONTAL,
              length=200, mode='determinate')
# This button will initialize the progress bar#duration = mid.length <-- function which will give duration of file in seconds.
lengthx = 100
count = 0
updatelength = 0
oldenable = 0

# Function responsible for the update of the progress bar value
def bar():
    import time
    global lengthx, stop, enable, updatelength, count, oldenable
    if updatelength < 100 and stop == 0:
        if (oldenable == enable):
            count += 1
            updatelength = (lengthx / 10) * count  # Update based on lengthx
    if oldenable != enable:
        count = 0
        updatelength = 0
    if updatelength > 100:
        updatelength = 100
        if oldenable != enable:
            count = 0
            updatelength = 0
    if (stop ==1):
        count = count
        updatelength = updatelength
    print(enable)
    progress['value'] = updatelength
    root.update_idletasks()
    print(f"Update Length: {updatelength}, Count: {count}")
    oldenable = enable
    print(enable)
    if updatelength < 100:
    #Schedule the next update only if progress is less than 100
        root.after(2000, bar)

   

   
progress.grid(row=  14, column = 9)

# This button will initialize the progress bar
#another_button = Button(root, text='Start', command=bar)
#another_button.grid(row = 13, column  = 9)
 


# Button Functions
def button_func1():
    global enable, stop
    enable = 1
    stop = 0
    currentsong()
def button_func2():
    global enable, stop
    enable =2
    stop = 0
    currentsong()
def button_func3():
    global enable, stop
    enable =3
    stop = 0
    currentsong()
def button_func4():
    global enable, stop
    enable = 4
    stop = 0
    currentsong()

# Like Button Function
def likeit():
    global like, song1like, song2like, song3like, song4like
    if (enable ==1):
        if song1like == 0:
            song1like =1
        else: song1like = 0
    elif (enable ==2):
        if song2like == 0:
            song2like = 1
        else: song2like= 0
    elif (enable ==3):
        if song3like == 0:
            song3like = 1
        else: song3like= 0
    elif (enable ==4):
        if song4like == 0:
            song4like = 1
        else: song4like= 0
    if like == 1:
        like = 0
    else: like = 1
    like_func()

def pause():
    global stop
    if stop ==0:
        print("Pausing the song")
        process.send_signal(signal.SIGUSR1)  # Send signal to pause
        stop =1
    elif stop ==1:
        stop = 0
        print("Playing the song")
        process.send_signal(signal.SIGUSR2)  # Send signal to ... play?
        bar()
    currentsong()



def play():  # Not used anymore???
    global process, stop
    if process:
        print("Resuming the song.")
        stop = 0  # Mark that the song is no longer paused
        process.send_signal(signal.SIGUSR2)  # Send signal to resume
        currentsong()  # Call currentsong to update with the new percentage
    else:
        print("No song is currently playing.")

#Inturrupt when changing playback option  
def stop_previous_process():
    global process
    if process:
        print("Stopping current process.")
        process.send_signal(signal.SIGINT)  # Send interrupt signal
        process.wait()  # Wait for process to terminate
        process = None  
   


#  ----------------- Ask MIDI for info -----------------  
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

   
   
   
# Function to handle the slider update
def slider_update(val):
    global stop
    if enable != 0 and stop == 0:
        print(f"Slider updated, new velocity filter: {val}%")
        currentsong()  # Automatically play with new percentage
    elif stop == 1:
        print(f"Slider updated to {val}%, but the song is paused, so it will not restart.")
#-------------------------------------------------------
   
   
#def play():
 #   global stop
  #  stop = 0
   # currentsong()

like_pic = ImageTk.PhotoImage(Image.open(likee))
nolike_pic = ImageTk.PhotoImage(Image.open(nolikee))
play_pic = ImageTk.PhotoImage(Image.open(play_button_path))
pause_pic = ImageTk.PhotoImage(Image.open(pause_button_path))
 

##pause_image = Image.open('Downloads\\pausebutton.png')
##pause_image_tk = ImageTk.PhotoImage(pause_image)
#pause_button = tk.Button(root, image=pause_image_tk, command=pause, background = 'white', borderwidth = 0)
#pause_button.grid(column=8, row=16,padx=(0, 10))
#play_image = Image.open('Downloads\\playbutton.png')
#play_image_tk = ImageTk.PhotoImage(play_image)
      #  play_button = tk.Button(root, image=play_image_tk, command=play, background = 'white', borderwidth = 0)
    #play_button.grid(column=9, row=16)


#  -------------------- DISPLAY AND IMAGE SETUP --------------------
#enable = 0
stop = 0
song = 'Select song choice.'
like = 0

#Label for Song title
label2 = tk.Label(root, text = song, font = ('Ariel', 13), background = 'white')
label2.grid(columnspan = 3, column = 8, row = 15)

style = ttk.Style()
style.configure('TButton', background = 'white')

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

#Pause Button
pause_button = tk.Button(root, image = pause_pic, command = pause, background = 'white', borderwidth = 0)
pause_button.grid(column = 9, row = 16)

#Like Button
like_button = tk.Button(root, image = like_pic, command = likeit, background = 'white', borderwidth = 0)
like_button.grid(column = 10, row = 16)

# Velocity Percentage Slider
velocity_slider_label = tk.Label(root, text="Set Velocity Filter", font=('Ariel', 13), background='white')
velocity_slider_label.grid(columnspan=6, column=8, row=18)

velocity_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, variable=velocity_percentage, command=slider_update)
velocity_slider.grid(columnspan=6, column=8, row=19)

# Checkbox for channels_allowed
channels_checkbox = tk.Checkbutton(root, text="Play Only Piano Notes", variable=channels_allowed, background='white')
channels_checkbox.grid(columnspan=2, column=13, row=20)



def display():
    global song, enable, canvas
    if enable == 0:
            imagepath = '/home/instrumentgroup/Downloads/loading2.0.png'
            song = 'Select song choice.'
    if enable == 1:
        imagepath = '/home/instrumentgroup/Downloads/wii.png'
        song = 'â™ªâ™« Playing Wii Theme â™ªâ™¬'
    if enable == 2:
        imagepath = '/home/instrumentgroup/Downloads/lesbells.png'
        song = 'â™ªâ™« Playing Jingle Bells â™ªâ™¬'
    if enable == 3:
        imagepath = '/home/instrumentgroup/Downloads/cutie2.0.png'
        song = 'â™ªâ™« Playing Song A â™ªâ™¬'
    if enable == 4:
        imagepath = '/home/instrumentgroup/Downloads/eatingcats.png'
        song = 'â™ªâ™« Playing Song B â™ªâ™¬'
    image_path = imagepath
    image_og = Image.open(image_path)
    image_tk = ImageTk.PhotoImage(image_og)
    canvas.image_tk = image_tk
    canvas.grid(columnspan = 6, column = 9, row = 6)
    canvas.create_image(8, 4, image = canvas.image_tk, anchor = 'nw')
    label2.config(text=song)
    label2.grid(columnspan =3, column = 8, row = 15)

def pause():
    if stop ==1:
        pause_button.config(image=play_pic)
    else:
        pause_button.config(image=pause_pic)



def like_func():
    global like, song1like, song2like, song3like, song4like
    if song1like ==1 and enable ==1 :
        like_button.config(image=like_pic)
    elif song2like ==1 and enable ==2:
        like_button.config(image=like_pic)
    elif song3like ==1 and enable ==3:
        like_button.config(image=like_pic)
    elif song4like ==1 and enable ==4:
        like_button.config(image=like_pic)
    else:
        like_button.config(image=nolike_pic)

         
def run_led_piano(midi_file_path, percentage):
    global process
    stop_previous_process()

    # Get the state of channels_allowed (assumed to be a boolean)
    channels_allowed_value = int(channels_allowed.get())  # Convert to 0 or 1
    print(pathpath.length)
    process = subprocess.Popen(['python3', 'led_piano.py', str(channels_allowed_value), midi_file_path, str(percentage)],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                               preexec_fn=os.setsid)  # Start the process in a new process group


# Run playback script
def run_led_piano(midi_file_path, percentage):
    global process
    stop_previous_process()

    # Get the state of channels_allowed (assumed to be a boolean)
    channels_allowed_value = int(channels_allowed.get())  # Convert to 0 or 1
    print(f"Channels Allowed: {channels_allowed_value}. Running led_piano.py with file: {midi_file_path} and filtering percentage: {percentage}")
   
    process = subprocess.Popen(['python3', 'led_piano.py', str(channels_allowed_value), midi_file_path, str(percentage)],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                               preexec_fn=os.setsid)  # Start the process in a new process group



# Control of call to the playback script
def currentsong():
    percentage = velocity_percentage.get()
    if enable == 0:
        print('loading')
    if enable == 1 and stop == 0:
        print('Wii Theme')
        run_led_piano('/home/instrumentgroup/Downloads/wii.mid', percentage)
    elif enable == 2 and stop == 0:
        print('Jingle Bells')
        run_led_piano('/home/instrumentgroup/Downloads/Carol.mid', percentage)
    elif enable == 3 and stop == 0:
        print('National Anthem')
        run_led_piano('/home/instrumentgroup/Downloads/USA.mid', percentage)
    elif enable == 4 and stop == 0:
        print('All the Small Things')
        run_led_piano('/home/instrumentgroup/Downloads/BLINK.mid', percentage)
    elif stop == 1:
        print('Song is on Pause')
    like_func()
    display()
    pause()
   


bar()
display()

 


root.mainloop()
