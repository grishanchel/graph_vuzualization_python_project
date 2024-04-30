from tkinter import Tk, Canvas


class Graph:
    def __init__(self, canvas, file_name='graph_information'):
        self.canvas = canvas
        self.file = open(str(file_name) + '.txt', 'w')
        self.adjacency_components = []
        self.adjacency_list = []
        self.matrix = []
        self.node_array = []
        self.line_array = []
        self.queue = []
        self.counter = 0

    def node_creation(self, event):
        self.adjacency_list.append([])
        self.counter += 1
        self.node_array += [Node(self.canvas, event.x, event.y)]

    def node_selection(self, event):
        x, y = event.x, event.y
        for node in self.node_array:
            if node.x - node.radius <= x <= node.x + node.radius and node.y - node.radius <= y <= node.y + node.radius:
                self.canvas.itemconfig(node.id, fill=node.chosen_colour, outline=node.chosen_outline)
                self.queue.append(node)
                break
        if len(self.queue) == 2:
            self.adjacency_list[self.queue[0].number - 1] += [self.queue[1].number - 1]
            self.adjacency_list[self.queue[1].number - 1] += [self.queue[0].number - 1]
            self.line_creation()

    def line_creation(self):
        self.line_array += [Line(self.canvas, self.queue[0].x, self.queue[0].y, self.queue[1].x, self.queue[1].y)]
        self.canvas.itemconfig(self.queue[0].id, fill=self.queue[0].fill, outline=self.queue[0].outline)
        self.canvas.itemconfig(self.queue[1].id, fill=self.queue[1].fill, outline=self.queue[1].outline)
        self.queue = []

    def node_moving(self, event):
        x, y = event.x, event.y
        for node in self.node_array:
            if node.x - node.radius <= x <= node.x + node.radius and node.y - node.radius <= y <= node.y + node.radius:
                self.canvas.move(node.id, x - node.x, y - node.y)
                self.canvas.move(node.text, x - node.x, y - node.y)
                node.x = x
                node.y = y
        for line in self.line_array:
            if line.x0 - 30 <= x <= line.x0 + 30 and line.y0 - 30 <= y <= line.y0 + 30:
                line.x0, line.y0 = x, y
                self.canvas.coords(line.id, line.x0, line.y0, line.x1, line.y1)
            if line.x1 - 30 <= x <= line.x1 + 30 and line.y1 - 30 <= y <= line.y1 + 30:
                line.x1, line.y1 = x, y
                self.canvas.coords(line.id, line.x0, line.y0, line.x1, line.y1)

    def delete_node(self):
        node = self.queue[0]
        temp_array = []
        for line in self.line_array:
            flag = True
            if line.x0 - 30 <= node.x <= line.x0 + 30 and line.y0 - 30 <= node.y <= line.y0 + 30:
                self.canvas.delete(line.id)
                flag = False
            if line.x1 - 30 <= node.x <= line.x1 + 30 and line.y1 - 30 <= node.y <= line.y1 + 30:
                self.canvas.delete(line.id)
                flag = False
            if flag:
                temp_array.append(line)
        for i in self.adjacency_list[node.number - 1]:
            self.adjacency_list[i].remove(node.number - 1)
        self.adjacency_list[node.number - 1] = []
        self.line_array = temp_array
        self.canvas.delete(self.queue[0].text)
        self.canvas.delete(self.queue[0].id)
        self.node_array.remove(node)
        self.queue = []

    def matrix_creation(self):
        self.matrix = [[0] * len(self.adjacency_list) for _ in range(len(self.adjacency_list))]
        for i in range(len(self.adjacency_list)):
            for j in range(len(self.adjacency_list[i])):
                self.matrix[i][self.adjacency_list[i][j]] = 1

    def graph_output(self):
        self.file.write('Adjacency list\n')
        for i in range(len(self.adjacency_list)):
            self.file.write(str(i + 1) + ': ' + ' '.join(map(str, self.adjacency_list[i])) + '\n')
        self.matrix_creation()
        self.file.write('\nMatrix\n')
        for i in range(self.counter):
            self.file.write(' '.join(map(str, self.matrix[i])) + '\n')
        self.dfs_preparation()
        self.file.write('\nAdjacency components\n')
        for i in range(len(self.adjacency_components)):
            self.file.write(str(i + 1) + ': ' + ' '.join(map(str, self.adjacency_components[i])) + '\n')
        self.file.close()

    def dfs_preparation(self):
        mark = [True] * self.counter
        for i in range(self.counter):
            if mark[i]:
                self.adjacency_components.append(self.dfs(mark, [], i))

    def dfs(self, mark, stack, u):
        mark[u] = False
        stack.append(u + 1)
        # print(u, self.adjacency_list[u])
        for i in range(len(self.adjacency_list[u])):
            v = self.adjacency_list[u][i]
            if mark[v]:
                stack = self.dfs(mark, stack, v)
                # print(stack)
        return stack


class Node:
    def __init__(self, canvas, x, y, radius=30):
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


tk = Tk()
print(chr(27) + "[2J")
tk.title("Graph")
tk.geometry('1000x500')

cv = Canvas(tk, width=1300, height=700, bg="white")
cv.pack()
graph = Graph(cv)

tk.bind("<Double-Button-1>", lambda event: graph.node_creation(event))
tk.bind("<Button-1>", lambda event: graph.node_selection(event))
tk.bind("<B3-Motion>", lambda event: graph.node_moving(event))
tk.bind("<d>", lambda event: graph.delete_node())
tk.bind("<p>", lambda event: graph.graph_output())

tk.resizable(False, False)
tk.mainloop()
