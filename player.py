import tkinter as tk
from tkinter import ttk
from audioplayer import AudioPlayer

root = tk.Tk()
root.resizable(0,0)

playing = False

def play():
    global player, playing
    if not playing:
        player = AudioPlayer("media\The Amazing Digital Circus - Main Theme.mp3")
        player.play(block=False)
        playing = True
    else:
        player.pause()
        playing = False

progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate').grid(column=0, row=0, columnspan=3, pady=10)

currenttime = tk.Label(root, text="00:00").grid(column=0, row=1)
totaltime = tk.Label(root, text="00:00").grid(column=2, row=1)

BackwardsButton = tk.Button(root, text="back", padx=10, pady=5, command=back).grid(column=0, row=2)
PlayButton = tk.Button(root, text="play / pause", padx=10, pady=5, command=play).grid(column=1, row=2)
ForwardsButton = tk.Button(root, text="forward", padx=10, pady=5, command=forward).grid(column=2, row=2)

root.mainloop()