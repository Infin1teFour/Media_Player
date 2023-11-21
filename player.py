import tkinter as tk
from tkinter import ttk
import pygame.mixer as mixer
from mutagen.mp3 import MP3
import os

root = tk.Tk()
root.resizable(0,0)
mixer.init()
songindex = -1

playing = False
folder = os.listdir("media")

def play():
    global player, playing
    if not playing:
        mixer.music.play()
        playing = True
    else:
        mixer.music.pause()
        playing = False


def back():
    pass

def forward():
    global player, folder, totaltime, progress, songindex, timer, playing, currenttime
    songindex += 1
    audio = "media/"+folder[songindex]
    mixer.music.load(audio)
    info = MP3(audio)
    minutes, seconds = convert(info.info.length)
    minutes = round(minutes)
    seconds = round(seconds)
    totaltime = tk.Label(root, text=str(minutes)+":"+str(seconds)).grid(column=2, row=1)
    progress.config(maximum=info.info.length)
    timer = 0
    currenttime.config(text="00:00")
    progress.config(value=0)
    playing = False


progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate')
progress.grid(column=0, row=0, columnspan=3, pady=10)

currenttime = tk.Label(root, text="00:00")
currenttime.grid(column=0, row=1)
totaltime = tk.Label(root, text="00:00").grid(column=2, row=1)

BackwardsButton = tk.Button(root, text="back", padx=10, pady=5, command=back).grid(column=0, row=2)
PlayButton = tk.Button(root, text="play / pause", padx=10, pady=5, command=play).grid(column=1, row=2)
ForwardsButton = tk.Button(root, text="forward", padx=10, pady=5, command=forward).grid(column=2, row=2)


def convert(seconds):
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    return(mins, seconds)

timer = 0
def update():
    global timer, playing, currenttime, progress
    if playing:
        if currenttime == totaltime:
            playing = False
            timer = 0
            songindex += 1
            return
        timer += 1
        minutes, seconds = convert(timer)
        minutes = round(minutes)
        seconds = round(seconds)
        currenttime.config(text=str(minutes)+":"+str(seconds))
        progress.config(value=timer)
        root.update()
    root.after(1000, update)

root.after(1000, update)
forward()
root.mainloop()