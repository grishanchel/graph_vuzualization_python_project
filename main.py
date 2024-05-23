from tkinter import Tk, Canvas
import Graph

tk = Tk()
print(chr(27) + "[2J")
tk.title("Graph")
tk.geometry('1000x500')

cv = Canvas(tk, width=1300, height=700, bg="white")
cv.pack()
graph = Graph.Graph(cv)

tk.bind("<Double-Button-1>", lambda event: graph.node_creation(event))
tk.bind("<Button-1>", lambda event: graph.node_selection(event))
tk.bind("<B3-Motion>", lambda event: graph.node_moving(event))
tk.bind("<d>", lambda event: graph.delete_node())
tk.bind("<p>", lambda event: graph.graph_output())

tk.resizable(False, False)
tk.mainloop()

start_node = graph.node_array[0]  # Specify the start node for algorithms
graph.bfs_visualize(start_node)   # Visualize BFS
graph.dfs_visualize(start_node)   # Visualize DFS
graph.dijkstra_visualize(start_node)  # Visualize Dijkstra's algorithm
