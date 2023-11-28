from pytube import YouTube
import os
from moviepy.editor import *

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

