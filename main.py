import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageGrab, ImageTk
from tkinter.colorchooser import askcolor

def choose_color():
  global selected_color
  global color_button
  selected_color = askcolor()[1]
  color_button.config(bg = selected_color, activebackground = selected_color)

def set_previous_image():
  global canvas_image
  canvas_image = ImageTk.PhotoImage(image)
  canvas.create_image((0,0),image=canvas_image, anchor=tk.NW)

def brush(event):
  canvas.create_oval((event.x-brush_size.get()/2, event.y-brush_size.get()/2, event.x+brush_size.get()/2, event.y+brush_size.get()/2), fill=selected_color, outline=selected_color)

def shape(end_position, preview=False, type='line'):
  if(preview):
    set_previous_image()
  match type:
    case 'line':
      canvas.create_line((start_position[0], start_position[1], end_position.x, end_position.y), width=brush_size.get(), fill=selected_color)
    case 'rectangle':
      canvas.create_rectangle((start_position[0], start_position[1], end_position.x, end_position.y), outline=selected_color, width=brush_size.get())

def handle_mouse_press(event):
  # if(selected_tool.get() == 'brush'):
  #   brush(event)
  global start_position
  global image
  image = get_current_image()
  start_position = (event.x, event.y)

def handle_mouse_release(event):
  match selected_tool.get():
    case 'line':
      shape(event, type='line')
    case 'rectangle':
      shape(event, type='rectangle')
    case _:
      pass

def handle_mouse_motion(event):
  match selected_tool.get():
    case 'brush':
      brush(event)
    case 'line':
      shape(event, type='line', preview=True)
    case 'rectangle':
      shape(event, type='rectangle', preview=True)
    case _:
      pass

def get_current_image():
  x0 = canvas.winfo_rootx()
  y0 = canvas.winfo_rooty()
  x1 = x0 + canvas.winfo_width()
  y1 = y0 + canvas.winfo_height()
  return ImageGrab.grab((x0, y0, x1, y1))

def save_image(filename='img.png'):
  im = get_current_image()
  im.save(filename)

# window
window = tk.Tk()
window.geometry('1000x600')
window.title('Simple Paint')

# variables
brush_size = tk.IntVar(window, 5)
selected_tool = tk.StringVar(window, 'brush')
selected_color = '#000000'
start_position = (0,0)
image = None
canvas_image = None
color = (0,0,0)

# widgets
tools_frame = tk.Frame(window)
tools_frame.pack(side='left', fill=tk.BOTH)

canvas = tk.Canvas(window, bg='white', width=800, height=600)
canvas.pack(side='top', anchor=tk.NW)
image = get_current_image()

tk.Label(tools_frame, text='brush size').pack(side='top')
brush_size_selection = ttk.Combobox(tools_frame, textvariable=brush_size)
brush_size_selection['values'] = tuple(range(1,21))
brush_size_selection.pack(side='top')

tk.Label(tools_frame, text='tool').pack(side='top')
tool_selection = ttk.Combobox(tools_frame, textvariable=selected_tool)
tool_selection['values'] = ('brush', 'line', 'rectangle')
tool_selection.pack(side='top')

tk.Label(tools_frame, text='color').pack(side='top')
color_button = tk.Button(tools_frame, command=choose_color, bg=selected_color, activebackground=selected_color)
color_button.pack(side='top')


menu = tk.Menu()
menu.add_command(label = 'save', command = save_image)
window.configure(menu=menu)




# events
canvas.bind('<B1-Motion>', handle_mouse_motion)
canvas.bind('<ButtonPress-1>', handle_mouse_press)
canvas.bind('<ButtonRelease-1>', handle_mouse_release)
window.bind('<Control-s>', lambda e: save_image())


window.mainloop()