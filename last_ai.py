import tkinter as tk
from queue import Queue

romania_map = {
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Zerind': [('Arad', 75), ('Oradea', 71)],
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
    'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
    'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
    'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
    'Bucharest': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 40), ('Urziceni', 45)],
    'Giurgiu': [('Bucharest', 90)],
    'Urziceni': [('Bucharest', 85), ('Vaslui', 142), ('Hirsova', 98)],
    'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
    'Iasi': [('Vaslui', 92), ('Neamt', 87)],
    'Neamt': [('Iasi', 87)],
    'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
    'Eforie': [('Hirsova', 86)]
}


class RomaniaMapGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Romania Map")

        self.canvas = tk.Canvas(self.root, width=850, height=450, bg="white")
        self.canvas.pack()

        self.source_label = tk.Label(self.root, text="Source", font=25)
        self.source_label.pack(pady=10)
        self.source_var = tk.StringVar(root)
        self.source_var.set('Select')  # Default source city
        self.source_dropdown = tk.OptionMenu(root, self.source_var, *romania_map.keys())
        self.source_dropdown.pack()

        self.destination_label = tk.Label(self.root, text="Destination", font=25)
        self.destination_label.pack(pady=10)
        self.destination_var = tk.StringVar(root)
        self.destination_var.set('Select')  # Default destination city
        self.destination_dropdown = tk.OptionMenu(root, self.destination_var, *romania_map.keys())
        self.destination_dropdown.pack()
        
        submit_button = tk.Button(root, text="Submit", command=self.visualize_bfs, font=("Arial", 14, "bold"), bg="blue", fg="white", relief="raised", padx=10, pady=5)
        submit_button.pack(pady=10)


        self.source_city = None
        self.destination_city = None

        self.draw_romania_map()

    def draw_romania_map(self):
        city_coordinates = self.get_city_coordinates()

        for city, (x, y) in city_coordinates.items():
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="black", outline="black")
            self.canvas.create_text(x, y + 20, text=city, font=("Arial", 10))

        for city, neighbors in romania_map.items():
            for neighbor, _ in neighbors:
                start_x, start_y = city_coordinates[city]
                end_x, end_y = city_coordinates[neighbor]
                self.canvas.create_line(start_x, start_y, end_x, end_y)

    def visualize_bfs(self):
        source_city = self.source_var.get()
        destination_city = self.destination_var.get()

        self.source_city = source_city
        self.destination_city = destination_city
        
        path = self.bfs(romania_map, source_city, destination_city)
        if path:
            self.highlight_path_with_delay(path)
            self.highlight_path(path)

    def bfs(self, graph, source, destination):
        queue = Queue()
        frontier = [source]
        explored = []
        queue.put([source])
        visited = set([source])
        print("Frontier:", frontier)
        print("Explored:", explored)

        while not queue.empty():
            path = queue.get()
            current_city = path[-1]
            current = frontier.pop(0)
            explored.append(current)

            if current_city == destination:
                print("Frontier:", frontier)
                print("Explored:", explored)
                print("Congratulations!! Goal node found:)")
                return path

            neighbors = graph[current_city]
            for neighbor, _ in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    frontier.append(neighbor)
                    queue.put(new_path)
            
            print("Frontier:", frontier)
            print("Explored:", explored)
            self.highlight_neighbors(current_city, frontier, explored)
            self.root.update()
            self.root.after(1000)

        return None

    def highlight_neighbors(self, current_city, frontier, explored):
        self.canvas.delete("highlight")
        city_coordinates = self.get_city_coordinates()

        for city in frontier:
            self.canvas.create_oval(
                city_coordinates[city][0] - 10,
                city_coordinates[city][1] - 10,
                city_coordinates[city][0] + 10,
                city_coordinates[city][1] + 10,
                fill="yellow",
                outline="black",
                tags="highlight"
            )

        for city in explored:
            self.canvas.create_oval(
                city_coordinates[city][0] - 10,
                city_coordinates[city][1] - 10,
                city_coordinates[city][0] + 10,
                city_coordinates[city][1] + 10,
                fill="light blue",
                outline="black",
                tags="highlight"
            )

    def highlight_path_with_delay(self, path):
        self.canvas.delete("path")
        city_coordinates = self.get_city_coordinates()

        for i, city in enumerate(path):
            self.canvas.create_oval(
                city_coordinates[city][0] - 13,
                city_coordinates[city][1] - 13,
                city_coordinates[city][0] + 13,
                city_coordinates[city][1] + 13,
                fill="yellow",
                outline="green",
                tags="path"
            )

            if i > 0:
                start_city = path[i - 1]
                end_city = path[i]
                start_x, start_y = city_coordinates[start_city]
                end_x, end_y = city_coordinates[end_city]
                self.canvas.create_line(start_x, start_y, end_x, end_y, fill="red", width=4, tags="path")
                self.root.update()
                self.root.after(1000)

    def highlight_path(self, path):
        self.canvas.delete("path")
        city_coordinates = self.get_city_coordinates()

        for i in range(len(path) - 1):
            start_city = path[i]
            end_city = path[i + 1]
            start_x, start_y = city_coordinates[start_city]
            end_x, end_y = city_coordinates[end_city]
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill="red", width=3, tags="path")

        self.canvas.create_oval(
            city_coordinates[self.source_city][0] - 15,
            city_coordinates[self.source_city][1] - 15,
            city_coordinates[self.source_city][0] + 15,
            city_coordinates[self.source_city][1] + 15,
            fill="blue",
            outline="blue",
            tags="path"
        )

        self.canvas.create_oval(
            city_coordinates[self.destination_city][0] - 15,
            city_coordinates[self.destination_city][1] - 15,
            city_coordinates[self.destination_city][0] + 15,
            city_coordinates[self.destination_city][1] + 15,
            fill="green",
            outline="blue",
            tags="path"
        )

    def get_city_coordinates(self):
        coordinates = {
            'Arad': (100, 100),
            'Zerind': (125, 60),
            'Oradea': (150, 15),
            'Timisoara': (110, 200),
            'Lugoj': (193, 225),
            'Mehadia': (200, 272),
            'Drobeta': (197, 313),
            'Sibiu': (250, 145),
            'Fagaras': (357, 150),
            'Rimnicu Vilcea': (280, 194),
            'Craiova': (305, 330),
            'Pitesti': (390, 242),
            'Bucharest': (490, 290),
            'Giurgiu': (460, 350),
            'Urziceni': (560, 260),
            'Vaslui': (625, 156),
            'Iasi': (580, 87),
            'Neamt': (496, 54),
            'Hirsova': (656, 262),
            'Eforie': (690, 323)
        }
        return coordinates

root = tk.Tk()
root.title("Romania Map")


window_width = 900
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")


root.configure(bg="white")



RomaniaMapGUI(root)
root.mainloop()