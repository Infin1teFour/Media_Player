import tkinter as tk
import os
import pyglet


root = tk.Tk()
root.title("media player")
root.resizable(0, 0)
root.configure(bg="#717291")
root.iconbitmap("grafiki/icon.ico")


pyglet.options['win32_gdi_font'] = True
pyglet.resource.add_font("NovaSquare-Regular.ttf")
font = "Nova Square"


def open():
    root.destroy()
    os.system("python3 " + "player" + ".py")

def quit():
    root.destroy()

info = tk.Label(root, text="Media player", font=(font, 20, "bold"), width=25, height=2, bg="#717291")
info.grid(row=0, column=0,)

start = tk.Button(root, text="start", width=20, height=2, command=lambda: open(), bg= "#525269", font=("Arial", 8,"bold"))
start.grid(row=1, column=0)

quit_button = tk.Button(root, text="quit", width=20, height=2, command=lambda: quit(), bg= "#525269", font=("Arial", 8,"bold"))
quit_button.grid(row=3, column=0)

root.mainloop()