class Node:
    def __init__(self, canvas, x, y, radius=30):
        from main import graph
        self.fill = 'yellow'
        self.outline = 'grey'
        self.chosen_colour = 'lime'
        self.chosen_outline = 'green'
        self.width = 2
        self.canvas = canvas
        self.radius = radius
        self.number = graph.counter
        self.x = x
        self.y = y
        self.id = self.canvas.create_oval(x - self.radius, y - self.radius,
                                          x + self.radius, y + self.radius,
                                          outline=self.outline, fill=self.fill,
                                          width=self.width)
        self.text = self.canvas.create_text(x, y, text=str(self.number))