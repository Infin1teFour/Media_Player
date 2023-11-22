import tkinter as tk
from tkinter import ttk
import pygame.mixer as mixer
from mutagen.mp3 import MP3
import os

root = tk.Tk()
root.resizable(0,0)
mixer.init()
songindex = -1

played = False
playing = False
folder = os.listdir("media")

def play():
    global playing, played
    if not playing:
        if not played:
            mixer.music.play()
            played = True
        else:
            mixer.music.unpause()
        playing = True
    else:
        mixer.music.pause()
        playing = False


def back():
    global player, folder, totaltime, progress, songindex, timer, playing, currenttime, played 
    songindex -= 1
    audio = "media/"+folder[songindex]
    mixer.music.load(audio)
    info = MP3(audio)
    minutes, seconds = convert(info.info.length)
    minutes = round(minutes)
    seconds = round(seconds)
    totaltime.config(text=str(minutes)+":"+str(seconds))
    progress.config(maximum=info.info.length)
    timer = 0
    currenttime.config(text="00:00")
    progress.config(value=0)
    playing = False
    root.title(folder[songindex])
    Songname.config(text=folder[songindex])
    played = False

def forward():
    global player, folder, totaltime, progress, songindex, timer, playing, currenttime, played 
    songindex += 1
    audio = "media/"+folder[songindex]
    mixer.music.load(audio)
    info = MP3(audio)
    minutes, seconds = convert(info.info.length)
    minutes = round(minutes)
    seconds = round(seconds)
    totaltime.config(text=str(minutes)+":"+str(seconds))
    progress.config(maximum=info.info.length)
    timer = 0
    currenttime.config(text="00:00")
    progress.config(value=0)
    playing = False
    root.title(folder[songindex])
    Songname.config(text=folder[songindex])
    played = False

Songname = tk.Label(root, text="")
Songname.grid(column=0, row=0, columnspan=3, pady=10, padx=10)

progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate')
progress.grid(column=0, row=1, columnspan=3, pady=10)

currenttime = tk.Label(root, text="00:00")
currenttime.grid(column=0, row=2)
totaltime = tk.Label(root, text="00:00")
totaltime.grid(column=2, row=2)

BackwardsButton = tk.Button(root, text="back", padx=10, pady=5, command=back).grid(column=0, row=3)
PlayButton = tk.Button(root, text="play / pause", padx=10, pady=5, command=play).grid(column=1, row=3)
ForwardsButton = tk.Button(root, text="forward", padx=10, pady=5, command=forward).grid(column=2, row=3)


def convert(seconds):
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    return(mins, seconds)

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
        if seconds > 9:
            currenttime.config(text=str(minutes)+":"+str(seconds))
        else:
            currenttime.config(text=str(minutes)+":"+"0"+str(seconds))
        progress.config(value=timer)
        root.update()
    root.after(1000, update)

root.after(1000, update)
forward()
root.mainloop()