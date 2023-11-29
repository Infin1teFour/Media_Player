import tkinter as tk
from tkinter import ttk
from tkinter import *
import pygame.mixer as mixer
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis
import os
import random
import tkinter.filedialog as filedialog
import shutil
from downloader import download
import pyglet

root = tk.Tk()
root.resizable(0,0)
root.title("Media Player")
root.config(bg="#717291")

pyglet.options['win32_gdi_font'] = True
pyglet.resource.add_font("NovaSquare-Regular.ttf")
font = ("Nova Square", 12)

if not os.path.exists("media"):
    os.mkdir("media")

mixer.init()
songindex = -1

played = False
playing = False
folder = os.listdir("media")
looping = False
pastSelected = 0
pastProgress = 0


def play():
    global playing, played
    if not playing:
        if not played:
            mixer.music.play(loops=looping)
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
    progress.config(to=info.info.length)
    timer = 0
    currenttime.config(text="0:00")
    playing = False
    root.title(folder[songindex])
    Songname.config(text=folder[songindex])
    played = False
    play()


def forward():
    global player, folder, totaltime, progress, songindex, timer, playing, currenttime, played, looping, info
    if not looping:
        songindex += 1
    try:
        audio = "media/"+folder[songindex]
    except IndexError:
        songindex = 0
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
    timer = 0
    currenttime.config(text="0:00")
    playing = False
    root.title(folder[songindex])
    Songname.config(text=folder[songindex])
    played = False
    progress.set(0)
    progress.config(to=info.info.length)
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
    files = filedialog.askopenfilenames(filetypes=[("Media files", ".mp3 .wav .ogg")])
    for i in files:
        folder.append(i.split("/")[-1])
        queue.insert(tk.END, i.split("/")[-1])
        shutil.copy(i, "media/"+i.split("/")[-1])
    noSongCheck()

def downloadButton():
    global DownloadEntery, folder, queue
    name = download(DownloadEntery.get())
    folder.append(name)
    queue.insert(tk.END, name)

def noSongCheck():
    global folder, queue
    if Songname.cget("text") == "No songs in folder":
        Songname.config(text=folder[0])
        root.title(folder[0])
        forward()
        play()

Songname = tk.Label(root, text="",bg="#717291", font=font)
Songname.grid(column=0, row=0, columnspan=3, pady=10, padx=10)

progress = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=420, sliderlength=20, showvalue=0, bg="#717291", fg="#15d104", highlightthickness=0, troughcolor="#525269")
progress.grid(column=0, row=1, columnspan=3, pady=10)

currenttime = tk.Label(root, text="00:00",bg="#717291")
currenttime.grid(column=0, row=2)
totaltime = tk.Label(root, text="00:00",bg="#717291")
totaltime.grid(column=2, row=2)

BackwardsButton = tk.Button(root, text="back", padx=10, pady=5, command=back, bg="#525269").grid(column=0, row=3)
PlayButton = tk.Button(root, text="play / pause", padx=10, pady=5, command=play, bg="#525269").grid(column=1, row=3)
ForwardsButton = tk.Button(root, text="forward", padx=10, pady=5, command=forward, bg="#525269").grid(column=2, row=3)

randomButton = tk.Button(root, text="random", padx=10, pady=5, command=lambda: random.shuffle(folder), bg="#525269").grid(column=0, row=4)
loopStatus = tk.Label(root, text="looping: "+str(looping),bg="#717291")
loopStatus.grid(column=1, row=4)
loopButton = tk.Button(root, text="loop", padx=10, pady=5, command=loop, bg="#525269").grid(column=2, row=4)

queue = tk.Listbox(root, width=70, height=10, bg="#000000", fg="#08e600")
queue.grid(column=0, row=5, columnspan=3)

importButton = tk.Button(root, text="import", padx=10, pady=5, command=importer, bg="#525269").grid(column=1, row=6)

DownloadEntery = tk.Entry(root, width=50,bg="#AEB0DF")
DownloadEntery.grid(column=0, row=7, columnspan=2)

DownloadButton = tk.Button(root, text="download", padx=10, pady=5, command=downloadButton, bg="#525269").grid(column=2, row=7)

volumeSlider = tk.Scale(root, from_=100, to=0, orient=tk.VERTICAL, length=420, sliderlength=20, bg="#717291", fg="#15d104", highlightthickness=0, troughcolor="#525269")
volumeSlider.grid(column=3, row=0, rowspan=8, padx=10)
volumeSlider.set(100)

volumeLabel = tk.Label(root, text="Volume")
volumeLabel.grid(column=3, row=8)

for i in folder:
    queue.insert(tk.END, i)

def convert(seconds):
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    return(mins, seconds)

def update():
    global playing, currenttime, progress, queue, songindex, looping, pastSelected, time, pastProgress, info
    selected = queue.curselection()
    if selected != () and selected[0] != pastSelected:
        looping = False
        loopStatus.config(text="looping: "+str(looping))
        songindex = selected[0]-1
        pastSelected = selected[0]
        forward()

    volume = volumeSlider.get()
    mixer.music.set_volume(volume/100)
    if playing:
        seek = progress.get()
        print(info.info.length)
        print(seek)
        if seek == round(info.info.length):
            playing = False
            timer = 0
            songindex += 1
            if looping:
                songindex -= 1
            forward()
            root.after(1000, update)
            seek = 0
            pastProgress = 0
            return
        print(pastProgress)
        if seek - pastProgress != 0:
            mixer.music.stop()
            mixer.music.play(start=seek)
        seek = progress.get()+1
        progress.set(seek)
        minutes, seconds = convert(seek)
        minutes = round(minutes)
        seconds = round(seconds)

        if seconds > 9:
            currenttime.config(text=str(minutes)+":"+str(seconds))
        else:
            currenttime.config(text=str(minutes)+":"+"0"+str(seconds))
        progress.set(seek)
        pastProgress = seek
    root.update()
    root.after(1000, update)

root.after(1000, update)

if len(folder) > 0:
    forward()
    play()
else:
    Songname.config(text="No songs in folder")
root.mainloop()