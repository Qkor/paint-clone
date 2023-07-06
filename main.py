import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageGrab, ImageTk


def brush(event):
  canvas.create_oval((event.x-brush_size.get()/2, event.y-brush_size.get()/2, event.x+brush_size.get()/2, event.y+brush_size.get()/2), fill='black')

def line(end_position, preview=False):
  if(preview):
    global canvas_image
    canvas_image = ImageTk.PhotoImage(current_image)
    canvas.create_image((0,0),image=canvas_image, anchor=tk.NW)
  canvas.create_line((start_position[0], start_position[1], end_position.x, end_position.y), width=brush_size.get())

def handle_mouse_press(event):
  global start_position
  global current_image
  current_image = get_current_image()
  start_position = (event.x, event.y)
  

def handle_mouse_release(event):
  match selected_tool.get():
    case 'line':
      line(event)
    case _:
      pass

def handle_mouse_motion(event):
  match selected_tool.get():
    case 'brush':
      brush(event)
    case 'line':
      line(event, preview=True)
    case _:
      pass

def get_current_image():
  x0 = canvas.winfo_rootx()
  y0 = canvas.winfo_rooty()
  x1 = x0 + canvas.winfo_width()
  y1 = y0 + canvas.winfo_height()
  return ImageGrab.grab((x0, y0, x1, y1))

def save_image(event, filename='img.png'):
  im = get_current_image()
  im.save(filename)

# window
window = tk.Tk()
window.geometry('800x700')

# variables
brush_size = tk.IntVar()
selected_tool = tk.StringVar()
start_position = (0,0)
current_image = None
canvas_image = None

# widgets
canvas = tk.Canvas(window, bg='white', width=800, height=600)
canvas.pack()
current_image = get_current_image()

tk.Label(text='brush size').pack()
brush_size_entry = tk.Entry(textvariable=brush_size)
brush_size_entry.pack()

tk.Label(text='tool').pack()
tool_entry = tk.Entry(textvariable=selected_tool)
tool_entry.pack()

# events
canvas.bind('<B1-Motion>', handle_mouse_motion)
canvas.bind('<ButtonPress-1>', handle_mouse_press)
canvas.bind('<ButtonRelease-1>', handle_mouse_release)
window.bind('<Control-s>', save_image)


window.mainloop()