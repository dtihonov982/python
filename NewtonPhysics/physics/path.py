class Path:
    def __init__(self, x, y, max_len = 200, color = 'blue'):
        self.max_len = max_len
        self.lines = [(x, y, None)]
        self.color = color
        
    def len(self):
        return len(self.lines)
    
    def step_on(self, x, y, canvas):
        #Отрисовать новую линию, ближайшую к точке (x, y)
        prev = self.lines[-1]
        x0 = prev[0]
        y0 = prev[1]
        tk_id = canvas.create_line(x0, y0, x, y, fill=self.color)
        self.lines.append((x, y, tk_id))

        #Промежуточные линии остаются на холсте без изменений
        
        #Если длина превысила максимальное значение
        if self.len() > self.max_len:
            canvas.delete(self.lines[1][2])
            #удалить дальную линию с нулевым индексом
            del self.lines[0]
