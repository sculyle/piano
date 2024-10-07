#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  GUI_10_5.py
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
from tkinter import HORIZONTAL, Button  # import Button and HORIZONTAL



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

song1like = 0
song2like = 0
song3like = 0
song4like = 0


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
        stop =1
    elif stop ==1:
        stop = 0
    currentsong()
    bar()
   

   

   
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

enable = 0
stop = 0
song = 'Select song choice.'
like = 0


label2 = tk.Label(root, text = song, font = ('Ariel', 13), background = 'white')
label2.grid(columnspan = 3, column = 8, row = 15)


   
   
   
style = ttk.Style()
style.configure('TButton', background = 'white')

button1_image = Image.open('/home/instrumentgroup/Downloads/button_wii-theme(1).png')
button1_image_tk = ImageTk.PhotoImage(button1_image)    
button1 = tk.Button(root, image = button1_image_tk, command = button_func1, background = 'white', borderwidth = 0)
button1.grid(column = 3, row = 6)
button2_image = Image.open('/home/instrumentgroup/Downloads/button_jingle-bells(1).png')
button2_image_tk = ImageTk.PhotoImage(button2_image)
button2 = tk.Button(root, image = button2_image_tk, command = button_func2, background = 'white', borderwidth = 0)
button2.grid(column = 3, row = 8)
button3_image = Image.open('/home/instrumentgroup/Downloads/button_song-a(1).png')
button3_image_tk = ImageTk.PhotoImage(button3_image)
button3 = tk.Button(root, image = button3_image_tk, command = button_func3, background = 'white', borderwidth = 0)
button3.grid(column = 3, row = 10)
button4_image = Image.open('/home/instrumentgroup/Downloads/button_song-b(2).png')
button4_image_tk = ImageTk.PhotoImage(button4_image)
button4 = tk.Button(root, image = button4_image_tk, command = button_func4, background = 'white', borderwidth = 0)
button4.grid(column = 3, row = 12)
pause_button = tk.Button(root, image = pause_pic, command = pause, background = 'white', borderwidth = 0)
pause_button.grid(column = 9, row = 16)
like_button = tk.Button(root, image = like_pic, command = likeit, background = 'white', borderwidth = 0)
like_button.grid(column = 10, row = 16)



def display():
    global song, enable, canvas
    if enable == 0:
            imagepath = '/home/instrumentgroup/Downloads/loading2.0.png'
            song = 'Select song choice.'
    if enable == 1:
        imagepath = '/home/instrumentgroup/Downloads/wii.png'
        song = '♪♫ Playing Wii Theme ♪♬'
    if enable == 2:
        imagepath = '/home/instrumentgroup/Downloads/lesbells.png'
        song = '♪♫ Playing Jingle Bells ♪♬'
    if enable == 3:
        imagepath = '/home/instrumentgroup/Downloads/cutie2.0.png'
        song = '♪♫ Playing Song A ♪♬'
    if enable == 4:
        imagepath = '/home/instrumentgroup/Downloads/eatingcats.png'
        song = '♪♫ Playing Song B ♪♬'
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
        bar()
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
         

def currentsong():
    if enable == 0:
        print('loading')
    if enable == 1 and stop == 0:
        print('Wii Theme')
    elif enable ==2 and stop == 0:
        print('Jingle Bells')
    elif enable ==3 and stop == 0:
        print('Song C')
    elif enable ==4 and stop == 0:
        print('Song D')
    elif stop == 1:
        print('Song is on Pause')
    like_func()
    display()
    pause()
    bar()
   


bar()
display()

 



root.mainloop()
