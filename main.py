import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageGrab, ImageTk, ImageDraw
from tkinter.colorchooser import askcolor

def choose_color():
  global selected_color
  global color_button
  selected_color = askcolor()[1]
  color_button.config(bg = selected_color, activebackground = selected_color)

def display_image_on_canvas(temporary=False):
  canvas.delete("all")
  global canvas_image
  if(temporary): canvas_image = ImageTk.PhotoImage(temp_img)
  else: canvas_image = ImageTk.PhotoImage(image)
  canvas.create_image((0,0),image=canvas_image, anchor=tk.NW)

def clear_image():
  canvas.delete("all")
  canvas.config(width=800, height=600)
  global filename
  filename = ''

def brush(event):
  drawingTool = ImageDraw.Draw(image)
  drawingTool.ellipse((event.x-brush_size.get()/2, event.y-brush_size.get()/2, event.x+brush_size.get()/2, event.y+brush_size.get()/2), fill=selected_color, outline=(0,0,0))
  display_image_on_canvas()

def shape(end_position, preview=False, type='line'):
  global temp_img
  temp_img = image.copy()
  if preview: drawingTool = ImageDraw.Draw(temp_img)
  else: drawingTool = ImageDraw.Draw(image)
  match type:
    case 'line':
      drawingTool.line((start_position[0], start_position[1], end_position[0], end_position[1]), width=brush_size.get(),fill=selected_color)
    case 'rectangle':
      if start_position[0] < end_position[0]:
        drawingTool.rectangle((start_position[0], start_position[1], end_position[0], end_position[1]), outline=selected_color, width=brush_size.get())
      else:
        drawingTool.rectangle((end_position[0], end_position[1], start_position[0], start_position[1]), outline=selected_color, width=brush_size.get())

  display_image_on_canvas(temporary=preview)

def handle_mouse_press(event):
  global start_position
  start_position = (event.x, event.y)

def handle_mouse_release(event):
  match selected_tool.get():
    case 'line':
      shape((event.x,event.y), type='line')
    case 'rectangle':
      shape((event.x,event.y), type='rectangle')
    case _:
      pass

def handle_mouse_motion(event):
  match selected_tool.get():
    case 'brush':
      brush(event)
    case 'line':
      shape((event.x,event.y), type='line', preview=True)
    case 'rectangle':
      shape((event.x,event.y), type='rectangle', preview=True)
    case _:
      pass

def save_image_as():
  global filename
  filename = filedialog.asksaveasfilename()
  try:
    image.save(filename)
  except:
    tk.messagebox.showerror(window, message='Could not save the file')

def save_image():
  if not len(filename):
    save_image_as()
  else:
    try:
      image.save(filename)
    except:
      tk.messagebox.showerror(window, message='Could not save the file')

def load_image():
  global filename
  filename = filedialog.askopenfilename()
  try:
    global image
    image = Image.open(filename)
    canvas.config(width=image.width, height=image.height)
    display_image_on_canvas()
  except:
    tk.messagebox.showerror(window, message='Could not open the file')

# window
window = tk.Tk()
window.geometry('1000x600')
window.title('Simple Paint')

# variables
filename = ''
brush_size = tk.IntVar(window, 5)
selected_tool = tk.StringVar(window, 'brush')
selected_color = '#000000'
start_position = (0,0)
color = (0,0,0)


# widgets
tools_frame = tk.Frame(window)
tools_frame.pack(side='left', fill=tk.BOTH)

canvas = tk.Canvas(window, bg='white', width=800, height=600)
canvas.pack(side='top', anchor=tk.NW)

tk.Label(tools_frame, text='size').pack(side='top')
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
menu.add_command(label = 'New', command = clear_image)
menu.add_command(label = 'Open', command = load_image)
menu.add_command(label = 'Save as', command = save_image_as)
menu.add_command(label = 'Save', command = save_image)
window.configure(menu=menu)


# events
canvas.bind('<B1-Motion>', handle_mouse_motion)
canvas.bind('<ButtonPress-1>', handle_mouse_press)
canvas.bind('<ButtonRelease-1>', handle_mouse_release)
window.bind('<Control-s>', lambda e: save_image())
window.bind('<Control-o>', lambda e: load_image())
window.bind('<Control-n>', lambda e: clear_image())

# image
image = Image.new('RGB', (800, 600), (255, 255, 255))
temp_img = image.copy()
display_image_on_canvas()

window.mainloop()