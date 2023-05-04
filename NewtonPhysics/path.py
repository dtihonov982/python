class Path:
    def __init__(self):
        self.max = 100
        self.list = []
    def add(self, x, y):
        self.list.append((x, y))
        if len(self.list) > self.max:
            del self.list[0]
    def draw(self, canvas, colour='red'):
        for i in range(0, len(self.list)-1):
            p1 = self.list[i]
            p2 = self.list[i+1]
            canvas.create_line(*p1, *p2, fill=colour)

class Path2:
    def __init__(self):
        self.max = 200
        self.list = []
        self.buffer = []
        self.color = 'blue'
    def len(self):
        return len(self.list)
    def step_on(self, x, y, canvas):
        if self.len() == 0:
            self.buffer.append([x, y])
        if self.len() == 0 and len(self.buffer) == 1:
            x0 = self.buffer[0][0]
            y0 = self.buffer[0][1]
            tk_id = canvas.create_line(x0,
                                       y0,
                                       x,
                                       y,
                                       fill=self.color)
            self.list.append((x0, y0, x, y, tk_id))
            return
        if self.len() >= 1:
            #Last point
            p1 = self.list[self.len()-1]
            tk_id = canvas.create_line(p1[2],
                                       p1[3],
                                       x,
                                       y,
                                       fill=self.color)           
            self.list.append((p1[2], p1[3], x, y, tk_id))
            #Delete first line by id
            if self.len() > self.max:
                canvas.delete(self.list[0][4])
                del self.list[0]
                
class Path3:
    def __init__(self, color='blue'):
        self.last = []
        self.color = color
    def step_on(self, x, y, canvas):
        if len(self.last) == 0:
            self.last = [x, y]
            return
        if len(self.last) > 0:
            p = self.last
            canvas.create_line(p[0],
                               p[1],
                               x,
                               y,
                               fill=self.color)    
            self.last = [x, y]
            
