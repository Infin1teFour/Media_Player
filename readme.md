<!--Hipity hopity-->
# Music-Player
## Contents

- [Introduction](#introduction)
- [Using the program](#using-the-program)
- [Code-Explenation](#code-explanation)    
- [Credits](#credits)

## Introduction

This is a simple media player application built with Python. It uses several libraries including `tkinter` for the GUI, `pygame.mixer` for audio playback, and `pyglet` for font rendering. Program doesn`t reqiere user to download any libraries it will download them by it self.

## Using the program

To run this program, execute the `player.py` file.

To download music from **YouTube**, follow these steps:
1. Copy the link to the audio that you want to download.
2. Paste the link into the entry bar at the bottom of the window.
3. Press the ***download*** button next to the entry bar.

To import files from another folder, press the import button and select the desired file destination.<br> 

To play the imported or downloaded audio, select it from the playlist 
in the middle of the window and press the play button.<br>

Use the ***forward*** and ***backward* buttons to navigate through the playlist.<br>

The ***loop button*** allows you to loop the currently playing audio.<br>

Press the ***play/pause button*** to control the playback.<br>

The ***random*** button shuffles the playlist.<br>

The ***motives*** button allows you to customize the appearance of the music player.
## Code explanation

Code uses two pyhton files to work first one is ***[downloader.py](https://github.com/Infin1teFour/Media_Player/blob/main/downloader.py)***  and the second file is ***[player.py](https://github.com/Infin1teFour/Media_Player/blob/main/player.py)***. In this section some parts of the code in those files will be explained.

- [Explaining-downloader.py](#explaining-downloaderpy)
    
- [Explaining-player.py](#explainig-playerpy)
    


### Explaining ***[downloader.py](https://github.com/Infin1teFour/Media_Player/blob/main/downloader.py)***
- [Importing-libraries](#importing-libraries)
- [Defining-download-function](#defineing-download-function) 
#### ***Importing libraries***
This section of code imports all modules (libraries) needed for the program. That includes `pytube` ( library used to download files from YouTube ), `os` ( a module providing functions for interacting with the operating system ), and `moviepy` ( a tool for video editing: cutting, concatenations, title insertions, video compositing, video processing, and creation of custom effects ).
```python
from pytube import YouTube
import os
from moviepy.editor import *
```


#### ***Defineing download function*** 

The following section of code defines a function `download(url)`. This function is responsible for downloading a YouTube video, converting it to an mp3 file, and saving it in the "media" folder. It uses the **pytube** library to download the video, and the **moviepy** library to convert the video to an mp3 file. The **os** module is used to interact with the file system. 

```python
def download(url):
    global folder, queue
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    video.download("media")
    print("Downloaded "+yt.title+" to media folder")
    filename = os.listdir("media")
    for name in filename:
        if name.endswith(".mp4"):
            audio = AudioFileClip("media/"+name)
            nameNomp4 = name.replace(".mp4", "")
            audio.write_audiofile("media/"+nameNomp4+".mp3")
            os.remove("media/"+name)
            return nameNomp4+".mp3"
    print("Converted to mp3")
```
<br>

### Explainig ***[player.py](https://github.com/Infin1teFour/Media_Player/blob/main/player.py)*** 
- [Importing-libraries-and-handling-import-errors](#importing-libraries-and-handling-import-errors)
- [Creating-tkinter-window-and-setting-up-variables](#creating-tkinter-window-and-setting-up-variables)
- [Defining-button-functions](#defining-button-functions)
- [Function-to-check-if-there-are-any-songs-in-the-folder](#function-to-check-if-there-are-any-songs-in-the-folder)
#### ***Importing libraries and handling import errors***
This Python script is trying to import several modules that are required for a media player application if its unable to do so it dawnoads the missing reqirements.Here's a brief explanation of what each module does:</br>

- `os`: Provides functions for interacting with the operating system.
- `tkinter`: The standard Python interface to the Tk GUI toolkit.
- `random`: Generates pseudo-random numbers.
- `pygame.mixer`: Used to mix sound for Pygame applications.
-  `mutagen.mp3`,  `mutagen.wave`,  `mutagen.oggvorbi`: Mutagen is a Python module to handle audio metadata, these are used to handle different audio formats.
- `tkinter.filedialog`: Provides a dialog box to select files and directories.
- `shutil`: Provides high-level file operations.
- `downloader`: imports functions from  ***[downloader.py](https://github.com/Infin1teFour/Media_Player/blob/main/downloader.py)***.
- `pyglet`: A Python module for creating games and multimedia applications.</br></br> 
If any of these modules are not found (causing an `ImportError`), it attempts to install them using the command `pip install -r requirements.txt`, and then restarts the script. The ***[requirements.txt](https://github.com/Infin1teFour/Media_Player/blob/main/requirements.txt)*** file contains a list of all the necessary modules. The script is then restarted with the command python ***[player.py](https://github.com/Infin1teFour/Media_Player/blob/main/player.py)***.
```python
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
```

#### ***Creating tkinter window and setting up variables*** 
This block of code initializes the main window of the application, sets its title to "Media Player", makes it non-resizable, sets the background color ( `bg` ) to a shade of grey, and sets the window icon.
<br>

```python
root = tk.Tk()
root.resizable(0,0)
root.title("Media Player")
root.config(bg="#717291")
root.iconbitmap("icon.ico")
```
</br>

This block of code sets up the font rendering options for the application. It uses the Nova Square font.</br>

```python
pyglet.options['win32_gdi_font'] = True
pyglet.resource.add_font("NovaSquare-Regular.ttf")
font = "Nova Square"
```
</br>

This block of code checks if a directory named `"media"` exists in the current directory. If it doesn't, it creates one. This is where the media files for the player will be stored.</br>

```python
if not os.path.exists("media"):
    os.mkdir("media")
```
</br>

This block of code initializes the `pygame.mixer` module for audio playback and sets the initial song index to -1.</br>

```python
mixer.init()
songindex = -1
```
</br>

This block of code sets up several variables for the application. `played` and `playing` are flags to track the playback status. folder is a list of files in the "media" directory. looping is a flag to track if the playlist should loop. pastSelected and pastProgress are variables to track the previously selected song and playback progress.<br>

```played = False
playing = False
folder = os.listdir("media")
looping = False
pastSelected = 0
pastProgress = 0
```

#### ***Defining button functions***

The `play` function controls the playback of the media. If the media is not currently playing, it will start or resume playback. If the media is currently playing, it will pause playback.

```python
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
```
</br>

The `back` function loads and plays the previous song in the folder. If the current song is the first one, it will loop back to the last song. It also updates the GUI to reflect the new song's information.

```python
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
```
</br>

The `forward` function loads and plays the next song in the folder. If the current song is the last one, it will loop back to the first song. It also updates the GUI to reflect the new song's information.

```python
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
```
<br>

The `loop` function toggles the looping status of the playlist. If looping is currently off, it will turn it on. If looping is currently on, it will turn it off.

```python
def loop():
    global looping
    if not looping:
        looping = True
    else:
        looping = False
    loopStatus.config(text="looping: "+str(looping))
```
<br>

The `importer` function allows the user to import media files into the application. It opens a file dialog for the user to select files, then copies the selected files into the "media" folder and adds them to the playlist.

```python
def importer():
    global folder, queue
    files = filedialog.askopenfilenames(filetypes=[("Media files", ".mp3 .wav .ogg")])
    for i in files:
        folder.append(i.split("/")[-1])
        queue.insert(tk.END, i.split("/")[-1])
        shutil.copy(i, "media/"+i.split("/")[-1])
    noSongCheck()
```
</br>

The `downloadButton` function downloads a media file from a URL entered by the user, then adds the downloaded file to the "media" folder and the playlist.

```python
def downloadButton():
    global DownloadEntery, folder, queue, playing
    name = download(DownloadEntery.get())
    folder.append(name)
    queue.insert(tk.END, name)
```

#### ***Function to check if there are any songs in the folder***
The `noSongCheck` function checks if there are any songs in the folder. If the `Songname` label text is "No songs in folder", it means there are no songs in the folder. In this case, it sets the `Songname` label text and the window title to the name of the first song in the folder, then calls the `forward` and `play` functions to start playing the first song.
```python
def noSongCheck():
    global folder, queue
    if Songname.cget("text") == "No songs in folder":
        Songname.config(text=folder[0])
        root.title(folder[0])
        forward()
        play()
```
#### change_color1() and change_color2()

This function attempts to change the background color of widgets in applylist1 and applylist2 to the colors specified by root_entry and button_entry respectively. It also tries to change the foreground color of queue and the background color of DownloadEntery to the colors specified by listbox_entry and entry_entry respectively. If any of these operations fail (for example, if the specified color is not valid), a TclError is caught and a message is printed to the console.

```python
def change_color1():
    global applylist1, root_entry, button_entry, applylist2
    try:
        for wid in applylist1:
            wid.config(bg=root_entry.get())
    except TclError:
        print("No data to change root color")
    else:
        print("color changed")
    try:
        for wid1 in applylist2:
                wid1.config(bg=button_entry.get())
    except TclError:
        print("No data to change button color")
    else:
        print("color changed")
    try:
        queue.config(fg=listbox_entry.get())
    except TclError:
        print("No data to change button color")
    else:
        print("color changed")   
    try:
        DownloadEntery.config(bg=entry_entry.get())
    except TclError:
        print("No data to change button color")
    else:
        print("color changed")    
```
<br>

This function changes the background color of widgets in applylist1 and applylist2 to root_bg and button_bg respectively. It also changes the foreground color of queue and the background color of DownloadEntery to listbox_fg and entry_bg respectively. This function does not catch any exceptions, so it assumes that the color values are valid. After all color changes have been made, it prints a message to the console indicating that the default colors have been set.
```python
def change_color2():
    global applylist1, root_entry, button_entry, applylist2
    for wid2 in applylist1:
        wid2.config(bg=root_bg)
    
    for wid3 in applylist2:
        wid3.config(bg=button_bg)
    
    queue.config(fg=listbox_fg)
    DownloadEntery.config(bg=entry_bg)
    print("Default colors have been set")
    
```

**Note**: The variables applylist1, applylist2, root_entry, button_entry, root_bg, button_bg, listbox_entry, entry_entry, listbox_fg, entry_bg, queue, and DownloadEntery are assumed to be globally defined.
#### Motives function
This function creates a new top-level window (root2) with the title "Motiv settings". The window is not resizable and its background color is set to root_bg.

In this window, several labels and entry fields are created for the user to enter their preferred colors for different parts of the application. The labels are used to instruct the user on what each entry field is for, and the entry fields are where the user can enter their color choices.

The labels and entry fields are arranged in a grid layout. Each label is followed by its corresponding entry field in the next row of the grid.

There are entry fields for the following:

- Background color (root_entry)
- Button color (button_entry)
- Listbox color (listbox_entry)
- Entry bar color (entry_entry)
Two buttons are also created in this window:

- The "Apply changes" button (apply_button), which when clicked, calls the change_color1() function to apply the color changes entered by the user.
- The "Default" button, which when clicked, calls the change_color2() function to reset the colors to their default values.
Finally, a "quit" button (quit_button1) is created, which when clicked, calls the quit2() function to close the window.

**Note**: The variables root_entry, button_entry, listbox_entry, root2, root_label, root_entry, button_entry, button_label, listbox_entry, listbox_label, apply_button, entry_entry, root_bg, entry_bg, button_bg, and the functions change_color1(), change_color2(), and quit2() are assumed to be globally defined.

```python
def motyw():
    global root_entry, button_entry, listbox_entry, root2, root_label, root_entry, button_entry, button_label, listbox_entry, listbox_label, apply_button, entry_entry
    root2 = tk.Toplevel(root)
    root2.resizable(0,0)
    root2.title("Motiv settings")
    root2.config(bg= root_bg)
    root_label = Label(root2, text="Enter background color", bg= root_bg)
    root_label.grid()
    root_entry = Entry(root2, width=50,bg=entry_bg)
    root_entry.grid()
    button_label = Label(root2, text="Enter button color", bg= root_bg)
    button_label.grid()
    button_entry = Entry(root2, width=50,bg=entry_bg)
    button_entry.grid()
    listbox_label = Label(root2, text="Enter listbox color", bg= root_bg)
    listbox_label.grid()
    listbox_entry = Entry(root2, width=50,bg=entry_bg)
    listbox_entry.grid()
    entry_label = Label(root2, text="Enter entrybar color", bg= root_bg)
    entry_label.grid()
    entry_entry = Entry(root2, width=50,bg=entry_bg)
    entry_entry.grid()
    apply_button = Button(root2, text = "Aply changes", bg=button_bg, command=change_color1)
    apply_button.grid()
    apply_button = Button(root2, text = "Default", bg=button_bg, command=change_color2)
    apply_button.grid()
    quit_button1 = tk.Button(root2, text="quit", command= quit2, bg=button_bg)
    quit_button1.grid()
```

## Credits 

This project is the result of the efforts of :

**Jan Jakowicki** - Responsible for the core functionality of the program.<br>

**Bastian Wiciński** - Handled the documentation of the code.<br> 

**Jakub Dratwa** - Took charge of the User Interface (UI). <br>











