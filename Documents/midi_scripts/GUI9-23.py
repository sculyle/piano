import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk


root = tk.Tk()
root.configure(background = 'white')

canvas = tk.Canvas(root, width = 400, height = 400, background = 'white')
canvas.grid(columnspan=20, rowspan = 20)
label = tk.Label(root, text = ' Song Choice', font = ('Roboto', 15), background = 'white')
label.grid(columnspan =3, column = 2, row = 4)
#play_button_path = 'Downloads\\leplaybutton.png'
#pause_button_path = 'Downloads\\lepausebutton.png'
#pause_path = play_button_path
#play_path = pause_button_path




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

def pause():
    global stop
    stop =1
    currentsong()
   
def play():
    global stop
    stop = 0
    currentsong()

play_image = Image.open('/home/instrumentgroup/Downloads/playbutton.png')
play_image_tk = ImageTk.PhotoImage(play_image)
play_button = tk.Button(root, image=play_image_tk, command=play, background = 'white', borderwidth = 0)
play_button.grid(column=9, row=16)

pause_image = Image.open('/home/instrumentgroup/Downloads/pausebutton.png')
pause_image_tk = ImageTk.PhotoImage(pause_image)
pause_button = tk.Button(root, image=pause_image_tk, command=pause, background = 'white', borderwidth = 0)
pause_button.grid(column=8, row=16,padx=(0, 10))



enable = 0
stop = 0
song = 'Select song choice.'

label2 = tk.Label(root, text = song, font = ('Ariel', 13), background = 'white')
label2.grid(columnspan = 6, column = 4, row = 14)

   

#display()
   
   
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
#pauseplz = ttk.Button(root, text = 'Pause', command = pause)
#pauseplz.grid(column = 2, row = 8)
#playplz = ttk.Button(root, text = 'Play', command = play)
#playplz.grid(column = 2, row = 9)




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
    display()


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
        imagepath = '/home/instrumentgroup/Downloads/utie2.0.png'
        song = '♪♫ Playing Song C ♪♬'
    if enable == 4:
        imagepath = '/home/instrumentgroup/Downloads/eatingcats.png'
        song = '♪♫ Playing Song D ♪♬'
    image_path = imagepath
    image_og = Image.open(image_path)
    image_tk = ImageTk.PhotoImage(image_og)
    canvas.image_tk = image_tk
    canvas.grid(columnspan = 6, column = 8, row = 6)
    canvas.create_image(8, 4, image = canvas.image_tk, anchor = 'nw')
    label2.config(text=song)
 
display()


root.mainloop()
