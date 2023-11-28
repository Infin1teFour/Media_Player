import tkinter as tk
from tkinter import ttk
import pygame.mixer as mixer
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis
import os
import random
import tkinter.filedialog as filedialog
import shutil
from downloader import download

root = tk.Tk()
root.resizable(0,0)
mixer.init()
songindex = -1

played = False
playing = False
folder = os.listdir("media")
looping = False
pastSelected = 0

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
    if songindex < -len(folder):
        songindex = len(folder)-1
    audio = "media/"+folder[songindex]
    mixer.music.load(audio)
    try:
        info = MP3(audio)
    except:
        try:
            info = WAVE(audio)
        except:
            try:
                info = OggVorbis(audio)
            except:
                print("error reading file")
                
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
    play()


def forward():
    global player, folder, totaltime, progress, songindex, timer, playing, currenttime, played, looping
    if not looping:
        songindex += 1
    try:
        audio = "media/"+folder[songindex]
    except IndexError:
        songindex = 0
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
    play()

def loop():
    global looping
    if not looping:
        looping = True
    else:
        looping = False
    loopStatus.config(text="looping: "+str(looping))

def importer():
    global folder, queue
    files = filedialog.askopenfilenames()
    for i in files:
        folder.append(i.split("/")[-1])
        queue.insert(tk.END, i.split("/")[-1])
        shutil.copy(i, "media/"+i.split("/")[-1])

def downloadButton():
    global DownloadEntery, folder, queue
    name = download(DownloadEntery.get())
    folder.append(name)
    queue.insert(tk.END, name)


Songname = tk.Label(root, text="")
Songname.grid(column=0, row=0, columnspan=3, pady=10, padx=10)

progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=420, mode='determinate')
progress.grid(column=0, row=1, columnspan=3, pady=10)

currenttime = tk.Label(root, text="00:00")
currenttime.grid(column=0, row=2)
totaltime = tk.Label(root, text="00:00")
totaltime.grid(column=2, row=2)

BackwardsButton = tk.Button(root, text="back", padx=10, pady=5, command=back).grid(column=0, row=3)
PlayButton = tk.Button(root, text="play / pause", padx=10, pady=5, command=play).grid(column=1, row=3)
ForwardsButton = tk.Button(root, text="forward", padx=10, pady=5, command=forward).grid(column=2, row=3)

randomButton = tk.Button(root, text="random", padx=10, pady=5, command=lambda: random.shuffle(folder)).grid(column=0, row=4)
loopStatus = tk.Label(root, text="looping: "+str(looping))
loopStatus.grid(column=1, row=4)
loopButton = tk.Button(root, text="loop", padx=10, pady=5, command=loop).grid(column=2, row=4)

queue = tk.Listbox(root, width=70, height=10)
queue.grid(column=0, row=5, columnspan=3)

importButton = tk.Button(root, text="import", padx=10, pady=5, command=importer).grid(column=1, row=6)

DownloadEntery = tk.Entry(root, width=50)
DownloadEntery.grid(column=0, row=7, columnspan=2)

DownloadButton = tk.Button(root, text="download", padx=10, pady=5, command=downloadButton).grid(column=2, row=7)


for i in folder:
    queue.insert(tk.END, i)

def convert(seconds):
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    return(mins, seconds)

def update():
    global timer, playing, currenttime, progress, queue, songindex, looping, pastSelected
    selected = queue.curselection()
    if selected != () and selected[0] != pastSelected:
        looping = False
        loopStatus.config(text="looping: "+str(looping))
        songindex = selected[0]-1
        pastSelected = selected[0]
        forward()
        
    if playing:
        if currenttime == totaltime:
            playing = False
            timer = 0
            songindex += 1
            forward()
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
play()
root.mainloop()