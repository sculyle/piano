import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
import subprocess

root = tk.Tk()

canvas = tk.Canvas(root, width = 600, height = 300)
canvas.grid(columnspan=8, rowspan = 9)
label = ttk.Label(root, text = 'Choose Your Song', font = ('Calibri', 15))
label.grid(columnspan =1, column = 1, row = 1)

enable = 0
stop = 0

#image_og = Image.open('unpetitchat.jpeg')

def button_func1():
    global enable
    enable = 1
    currentsong()
def button_func2():
    global enable
    enable =2
    currentsong()
def button_func3():
    global enable
    enable =3
    currentsong()
def button_func4():
    global enable
    enable = 4
    currentsong()

def pause():
    global stop
    stop =1
    currentsong()
def play():
    global stop
    stop = 0
    currentsong()

    
style = ttk.Style()
style.configure('TButton', background = 'white')
    
button1 = ttk.Button(root, text = 'Song A', command = button_func1)
button1.grid(column = 1, row = 2)
button2 = ttk.Button(root, text = 'Song B', command = button_func2)
button2.grid(column = 1, row = 3)
button3 = ttk.Button(root, text = 'Song C', command = button_func3)
button3.grid(column = 1, row = 4)
button4 = ttk.Button(root, text = 'Song D', command = button_func4)
button4.grid(column = 1, row = 5)
pauseplz = ttk.Button(root, text = 'Pause', command = pause)
pauseplz.grid(column = 1, row = 6)
playplz = ttk.Button(root, text = 'Play', command = play)
playplz.grid(column = 1, row = 7)




def currentsong():
    if enable == 1 and stop == 0:
        print('Song A')
    elif enable ==2 and stop == 0:
        print('Song B')
    elif enable ==3 and stop == 0:
        print('Song C')
    elif enable ==4 and stop == 0:
        print('Song D')
    elif stop == 1:
        print('Song is on Pause')





root.mainloop()
