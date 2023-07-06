import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageGrab

def handle_mouse(event):
  canvas.create_oval((event.x-2, event.y-2, event.x+2, event.y+2), fill='black')

def save_image(event, filename='img.png'):
  x0 = canvas.winfo_rootx()
  y0 = canvas.winfo_rooty()
  x1 = x0 + canvas.winfo_width()
  y1 = y0 + canvas.winfo_height()
  im = ImageGrab.grab((x0, y0, x1, y1))
  im.save(filename)

# window
window = tk.Tk()
window.geometry('800x700')

# cavas
canvas = tk.Canvas(window, bg='white', width=800, height=600)
canvas.pack()

# events
canvas.bind('<B1-Motion>', handle_mouse)
window.bind('<Control-s>', save_image)


window.mainloop()