# Music-Playerify
program służy do odtwarzania plików z podanego folderu "media"

## Code explanation

Code uses two pyhton files to work first one is <span style="color:#62adfb">***[downloader.py](https://github.com/Infin1teFour/Media_Player/blob/main/downloader.py)*** </span> and the second file is <span style="color:#62adfb">***[player.py](https://github.com/Infin1teFour/Media_Player/blob/main/player.py)***</span>. In this section some parts of the code in those files will be explained.

### Explaining <span style="color:#62adfb">***[downloader.py](https://github.com/Infin1teFour/Media_Player/blob/main/downloader.py)***</span>

This section of code imports all modules (libraries) needed for the program. That includes ***pytube*** ( library used to download files from YouTube ), ***os*** ( a module providing functions for interacting with the operating system ), and ***moviepy*** ( a tool for video editing: cutting, concatenations, title insertions, video compositing, video processing, and creation of custom effects ).
```python
from pytube import YouTube
import os
from moviepy.editor import *
```
<span style ="color: #5d5d5d" >lines 2-4</span><br>

____________________________________________________________________________________
<br>
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
<span style ="color: #5d5d5d" >lines 7-22</span><br>

