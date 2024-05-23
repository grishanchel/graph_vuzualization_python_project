import queue
from Line import Line
from Node import Node

class Graph:
    def __init__(self, canvas, file_name='graph_information'):
        self.canvas = canvas
        self.file = open(f'{file_name}.txt', 'w')
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
        x = event.x
        y = event.y
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
            self.file.write(f'{i+1}:  '.join(map(str, self.adjacency_list[i])) + '\n')
        self.matrix_creation()
        self.file.write('\nMatrix\n')
        for i in range(self.counter):
            self.file.write(' '.join(map(str, self.matrix[i])) + '\n')
        self.dfs_preparation()
        self.file.write('\nAdjacency components\n')
        for i in range(len(self.adjacency_components)):
            self.file.write(f'{i+1}:  '.join(map(str, self.adjacency_components[i])) + '\n')
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

    def bfs_visualize(self, start_node):
        visited = [False] * self.counter
        q = queue
        q.put(start_node)
        while not q.empty():
            node = q.get()
            if not visited[node.number - 1]:
                self.canvas.itemconfig(node.id, fill=node.chosen_colour, outline=node.chosen_outline)
                self.canvas.update()
                visited[node.number - 1] = True
                for adjacent_node in self.adjacency_list[node.number - 1]:
                    q.put(self.node_array[adjacent_node])
                    self.canvas.itemconfig(self.line_array[(node.number - 1) * self.counter + adjacent_node].id,
                                           fill='red')
                    self.canvas.update()

    def dfs_visualize(self, start_node):
        visited = [False] * self.counter
        self.dfs_helper(start_node, visited)

    def dfs_helper(self, node, visited):
        if not visited[node.number - 1]:
            self.canvas.itemconfig(node.id, fill=node.chosen_colour, outline=node.chosen_outline)
            self.canvas.update()
            visited[node.number - 1] = True
            for adjacent_node in self.adjacency_list[node.number - 1]:
                self.canvas.itemconfig(self.line_array[(node.number - 1) * self.counter + adjacent_node].id, fill='red')
                self.canvas.update()
                self.dfs_helper(self.node_array[adjacent_node], visited)

    def dijkstra_visualize(self, start_node):
        distances = [float('inf')] * self.counter
        distances[start_node.number - 1] = 0
        visited = [False] * self.counter

        while True:
            min_distance = float('inf')
            min_node = None
            for i in range(self.counter):
                if not visited[i] and distances[i] < min_distance:
                    min_distance = distances[i]
                    min_node = i

            if min_node is None:
                break

            visited[min_node] = True
            self.canvas.itemconfig(self.node_array[min_node].id, fill=self.node_array[min_node].chosen_colour,
                                   outline=self.node_array[min_node].chosen_outline)
            self.canvas.update()

            for i, weight in enumerate(self.matrix[min_node]):
                if weight > 0 and not visited[i]:
                    new_distance = distances[min_node] + weight
                    if new_distance < distances[i]:
                        distances[i] = new_distance
                        self.canvas.itemconfig(self.line_array[min_node * self.counter + i].id, fill='red')
                        self.canvas.update()

