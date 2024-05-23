class Line:
    def __init__(self, canvas, x0, y0, x1, y1):
        self.canvas = canvas
        self.normal_colour = 'black'
        self.chosen_colour = 'cyan'
        self.width = 2
        self.x0, self.y0 = x0, y0
        self.x1, self.y1 = x1, y1
        self.id = self.canvas.create_line(self.x0, self.y0,
                                          self.x1, self.y1,
                                          fill=self.normal_colour,
                                          width=self.width)
        self.canvas.lower(self.id)
