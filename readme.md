# Music-Player
This is a simple media player application built with Python. It uses several libraries including `tkinter` for the GUI, `pygame.mixer` for audio playback, and `pyglet` for font rendering.

## Code explanation

Code uses two pyhton files to work first one is ***[downloader.py](https://github.com/Infin1teFour/Media_Player/blob/main/downloader.py)***  and the second file is ***[player.py](https://github.com/Infin1teFour/Media_Player/blob/main/player.py)***. In this section some parts of the code in those files will be explained.

### Explaining ***[downloader.py](https://github.com/Infin1teFour/Media_Player/blob/main/downloader.py)***

#### 1. ***Importing  libraries***
This section of code imports all modules (libraries) needed for the program. That includes `pytube` ( library used to download files from YouTube ), `os` ( a module providing functions for interacting with the operating system ), and `moviepy` ( a tool for video editing: cutting, concatenations, title insertions, video compositing, video processing, and creation of custom effects ).
```python
from pytube import YouTube
import os
from moviepy.editor import *
```


__________________________________________________________________________________
#### 2. ***Defineing dawnload function*** 

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

### Explainig ***[player.py](https://github.com/Infin1teFour/Media_Player/blob/main/player.py)*** <br>
#### 1. ***Importing  libraries and handling import errors***
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
__________________________________________________________________________________
#### 2. ***Creating tkinter window and setting up variables*** 
<br>
This block of code initializes the main window of the application, sets its title to "Media Player", makes it non-resizable, sets the background color to a shade of grey, and sets the window icon.
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
This block of code checks if a directory named "media" exists in the current directory. If it doesn't, it creates one. This is where the media files for the player will be stored.</br>

```python
if not os.path.exists("media"):
    os.mkdir("media")
```
</br>
This block of code initializes the pygame.mixer module for audio playback and sets the initial song index to -1.</br>

```python
mixer.init()
songindex = -1
```
</br>
This block of code sets up several variables for the application. played and playing are flags to track the playback status. folder is a list of files in the "media" directory. looping is a flag to track if the playlist should loop. pastSelected and pastProgress are variables to track the previously selected song and playback progress.<br>

```played = False
playing = False
folder = os.listdir("media")
looping = False
pastSelected = 0
pastProgress = 0
```
__________________________________________________________________________________
#### 3. ***Defining button functions***

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
______________________________________________________________________
#### 4. ***Function to check if there are any songs in the folder***
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
______________________________________________________________________