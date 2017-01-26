from tkinter import Tk, Canvas

class __Painter():
    def __init__(self, root):
        width = 500
        height = 500
        
        self.canvas = Canvas(root, width=width, heigh=height)
        self.canvas.pack()
        
        self.x = width / 2
        self.y = height / 2

        self.pen = False

        self.angle = 0

    def off(self):
        self.pen = False

    def on(self):
        self.pen = True

    def move(self, dx, dy):
        if self.pen == True:
            prev_x, prev_y = self.x, self.y
            
            self.x += dx
            self.y += dy

            self.canvas.create_line(prev_x, prev_y, self.x, self.y)
            
        else:
            self.x += dx
            self.y -= dy
    def turn(angle):
        self.angle += angle
            
   
__root = Tk()
__p = __Painter(__root)

def off():
    __p.off()
def on():
    __p.on()
def move(dx, dy):
    __p.move(dx, dy)
def show():
    __root.mainloop()
def turn(angle):
    __p.turn(angle)

