# Importing and installing modules
try:
    import os
    import tkinter as tk
    import random
    from tkinter import ttk
    from tkinter import *
    import pygame.mixer as mixer
    from mutagen.mp3 import MP3
    from mutagen.wave import WAVE
    from mutagen.oggvorbis import OggVorbis
    import tkinter.filedialog as filedialog
    import shutil
    from downloader import download
    import pyglet
except ImportError:
    import os
    print("Error importing modules")
    os.system("pip install -r requirements.txt")
    print("Restarting...")
    os.system("python player.py")
    
root_bg = "#717291"
button_bg = "#525269"
listbox_fg = "#08e600"
entry_bg = "#AEB0DF"

# Opening tkinter window   
root = tk.Tk()
root.resizable(0,0)
root.title("Media Player")
root.config(bg="#717291")
root.iconbitmap("grafiki/icon.ico")

# Setting up fonts
pyglet.options['win32_gdi_font'] = True
pyglet.resource.add_font("NovaSquare-Regular.ttf")
font = "Nova Square"

# Creating media folder if it doesn't exist
if not os.path.exists("media"):
    os.mkdir("media")

# Setting up pygame mixer
mixer.init()
songindex = -1

# Setting up variables
played = False
playing = False
folder = os.listdir("media")
looping = False
pastSelected = 0
pastProgress = 0


# Button functions 
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
    global DownloadEntery, folder, queue, playing
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





Songname = tk.Label(root, text="",bg=root_bg, font=(font, 12))
Songname.grid(column=0, row=0, columnspan=3, pady=10, padx=10)

progress = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=420, sliderlength=20, showvalue=0, bg=root_bg, highlightthickness=0, troughcolor=button_bg)
progress.grid(column=0, row=1, columnspan=3, pady=10)
currenttime = tk.Label(root, text="00:00",bg=root_bg)
currenttime.grid(column=0, row=2)
totaltime = tk.Label(root, text="00:00",bg=root_bg)
totaltime.grid(column=2, row=2)

BackwardsButton = tk.Button(root, text="back", padx=10, pady=5, command=back, bg=button_bg).grid(column=0, row=3)
PlayButton = tk.Button(root, text="play / pause", padx=10, pady=5, command=play, bg=button_bg).grid(column=1, row=3)
ForwardsButton = tk.Button(root, text="forward", padx=10, pady=5, command=forward, bg=button_bg).grid(column=2, row=3)

randomButton = tk.Button(root, text="random", padx=10, pady=5, command=lambda: random.shuffle(folder), bg=button_bg).grid(column=0, row=4)
loopStatus = tk.Label(root, text="looping: "+str(looping),bg=root_bg)
loopStatus.grid(column=1, row=4)
loopButton = tk.Button(root, text="loop", padx=10, pady=5, command=loop, bg=button_bg).grid(column=2, row=4)

queue = tk.Listbox(root, width=70, height=10, bg="#000000", fg="#08e600", font=(font, 9))
queue.grid(column=0, row=5, columnspan=3)

importButton = tk.Button(root, text="import", padx=10, pady=5, command=importer, bg=button_bg).grid(column=1, row=6)

DownloadEntery = tk.Entry(root, width=50,bg=entry_bg)
DownloadEntery.grid(column=0, row=7, columnspan=3)

DownloadButton = tk.Button(root, text="download", padx=10, pady=5, command=downloadButton, bg=button_bg).grid(column=2, row=7)

volumeSlider = tk.Scale(root, from_=100, to=0, orient=tk.VERTICAL, length=420, sliderlength=20, bg=root_bg, highlightthickness=0, troughcolor=button_bg)
volumeSlider.grid(column=3, row=0, rowspan=8, padx=10)
volumeSlider.set(100)

volumeLabel = tk.Label(root, text="Volume", bg=root_bg)
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

# Checking if there are any songs in the folder
if len(folder) > 0:
    forward()
    play()
else:
    Songname.config(text="No songs in folder")

def change_colour1():
    global applylist1, root_entry, button_entry, applylist2
    for wid in applylist1:
        wid.config(bg = root_entry.get())
    
    DownloadEntery.config(bg= entry_entry.get())
    queue.config(fg = listbox_entry.get())
def motyw():
    global root_entry, button_entry, listbox_entry, root2, root_label, root_entry, button_entry, button_label, listbox_entry, listbox_label, apply_button, entry_entry
    root2 = tk.Toplevel(root)
    root2.resizable(0,0)
    root2.title("Media Player - motywy")
    root2.config(bg= root_bg)
    root_label = Label(root2, text="podaj kolor tła", bg= root_bg)
    root_label.grid()
    root_entry = Entry(root2, width=50,bg=entry_bg)
    root_entry.grid()
    button_label = Label(root2, text="podaj kolor przycisków", bg= root_bg)
    button_label.grid()
    button_entry = Entry(root2, width=50,bg=entry_bg)
    button_entry.grid()
    listbox_label = Label(root2, text="podaj kolor napisu w polu wyboru piosenki", bg= root_bg)
    listbox_label.grid()
    listbox_entry = Entry(root2, width=50,bg=entry_bg)
    listbox_entry.grid()
    entry_label = Label(root2, text="podaj kolor napisu w polu wyboru piosenki", bg= root_bg)
    entry_label.grid()
    entry_entry = Entry(root2, width=50,bg=entry_bg)
    entry_entry.grid()
    apply_button = Button(root2, text = "potwierdź", bg=button_bg, command=change_colour1)
    apply_button.grid()

ui_button = tk.Button(root, text="motyw", padx=10, pady=5, command=motyw, bg=button_bg)
ui_button.grid()
applylist1 = [root, volumeLabel, volumeSlider, loopStatus, currenttime, totaltime, progress, Songname]
applylist2 = [DownloadButton, importButton, randomButton, ForwardsButton, PlayButton, BackwardsButton]
root.mainloop()