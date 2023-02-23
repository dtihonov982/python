from tkinter import *

root = Tk()
root.minsize(width = 500, height=400)


history = []
var = StringVar()
a_label = Label(root, textvariable = var).pack()

def keyup(e):
    global history
    if e.keycode in history:
        history.pop(history.index(e.keycode))

        var.set(str(history))
    
def keydown(e):
    global history
    if not e.keycode in history:
        history.append(e.keycode)
        var.set(str(history))

 
root.bind('<KeyPress>', keydown)
root.bind('<KeyRelease>', keyup)

root.mainloop() 
