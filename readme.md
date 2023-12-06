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


____________________________________________________________________________________

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