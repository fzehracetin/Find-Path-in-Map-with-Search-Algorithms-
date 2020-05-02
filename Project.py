import tkinter as tk
import tkinter.messagebox as msg
import random
from math import sqrt
import numpy as np
import time


class Gui:
    def __init__(self):
        self.window = root
        self.window.title("Path Finder")
        self.bg_color = "pink"
        self.h_color = "navy"
        self.s_color = "RoyalBlue2"
        self.c_color = "Magenta2"
        self.window.configure(bg=self.bg_color)

        self.canvas_size = 700  # canvas
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, background="white")
        self.canvas.grid(column=1, row=0)
        self.refresh_canvas()

        self.frame = tk.Frame(self.window, bg=self.bg_color)
        self.frame.grid(row=0, column=0, sticky="n")

        self.frame_list = tk.Frame(self.window, bg=self.bg_color)
        self.frame_list.grid(row=0, column=2, sticky="n")

        self.city_total = tk.IntVar()
        self.input_type = tk.StringVar()
        self.city_or_conn = tk.IntVar()
        self.algorithm = tk.IntVar()
        self.entry = tk.IntVar()
        self.dst_src = tk.IntVar()
        self.speed = tk.IntVar()
        self.evaluation = tk.IntVar()

        self.city_count = 0
        self.conn_count = 0
        self.selected_cities = []
        self.ovals = []
        self.distances = []
        self.lines = []
        self.city_dict = {"City1": "Paris", "City2": "Lion", "Distance": 0}

        self.cities = ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpeiller",
                       "Bordeaux", "Lille", "Rennas", "Reims", "Le Havre", "Toulon", "Grenoble", "Dijon", "Angers",
                       "Villeaurbanne", "Le Mans", "Saint-Denis"]
        self.colors = ["red", "blue", "purple", "brown", "green", "hot pink", "orange red", "black", "cyan",
                       "deep pink", "green3", "DodgerBlue3", "firebrick4", "LightPink4", "maroon", "SeaGreen3",
                       "lime green", "navy", "dark violet", "red4", "magenta2"]

        header = tk.Label(self.frame, text="Create Map", font='Calibri 14 bold', fg=self.h_color, bg=self.bg_color)
        header.grid(column=0, row=0)
        section = tk.Label(self.frame, text="Number of Cities", font='Calibri 12 bold', fg=self.s_color,
                           bg=self.bg_color)
        section.grid(column=0, row=1)
        cities5 = tk.Radiobutton(self.frame, text='5 cities', variable=self.city_total, command=self.set_connections,
                                 value=5, bg=self.bg_color).grid(column=0, row=2)
        cities10 = tk.Radiobutton(self.frame, text='10 cities', variable=self.city_total, command=self.set_connections,
                                  value=10, bg=self.bg_color).grid(column=0, row=3)
        cities20 = tk.Radiobutton(self.frame, text='20 cities', variable=self.city_total, command=self.set_connections,
                                  value=20, bg=self.bg_color).grid(column=0, row=4)
        section1 = tk.Label(self.frame, text="Number of Connections", font='Calibri 12 bold', fg=self.s_color,
                            bg=self.bg_color)
        section1.grid(column=0, row=5)

        entry1 = tk.Entry(self.frame, textvariable=self.entry, background=self.bg_color)
        entry1.grid(column=0, row=6)

        section2 = tk.Label(self.frame, text="How to Create", font='Calibri 12 bold', fg=self.s_color, bg=self.bg_color)
        section2.grid(column=0, row=7)
        frame_ran = tk.Radiobutton(self.frame, text='Random', variable=self.input_type, value="Random",
                                   command=self.create_randomly, bg=self.bg_color).grid(column=0, row=8)
        frame_us = tk.Radiobutton(self.frame, text='User Input', variable=self.input_type, value="User",
                                  command=self.add_buttons, bg=self.bg_color).grid(column=0, row=9)

        header2 = tk.Label(self.frame, text="Algorithms", font='Calibri 14 bold', fg=self.h_color, bg=self.bg_color)
        header2.grid(column=0, row=13)

        alg1 = tk.Radiobutton(self.frame, text='A* Search', variable=self.algorithm, value=0,
                              bg=self.bg_color).grid(column=0, row=14)
        alg2 = tk.Radiobutton(self.frame, text='Best First Search', variable=self.algorithm, value=1,
                              bg=self.bg_color).grid(column=0, row=15)
        alg3 = tk.Radiobutton(self.frame, text='Depth First Search', variable=self.algorithm, value=2,
                              bg=self.bg_color).grid(column=0, row=16)
        alg4 = tk.Radiobutton(self.frame, text='Breadth First Search', variable=self.algorithm, value=3,
                              bg=self.bg_color).grid(column=0, row=17)
        section4 = tk.Label(self.frame, text="Evaluation Function", font='Calibri 12 bold', fg=self.s_color,
                            bg=self.bg_color)
        section4.grid(column=0, row=18)
        euclidean = tk.Radiobutton(self.frame, text='Euclidean', variable=self.evaluation, value=0, bg=self.bg_color). \
            grid(column=0, row=19, sticky='w')
        manhattan = tk.Radiobutton(self.frame, text='Manhattan', variable=self.evaluation, value=1, bg=self.bg_color). \
            grid(column=0, row=19, sticky='e')
        section3 = tk.Label(self.frame, text="Animation Speed", font='Calibri 12 bold', fg=self.s_color,
                            bg=self.bg_color)
        section3.grid(column=0, row=20)
        fast = tk.Radiobutton(self.frame, text='Fast', variable=self.speed, value=0, bg=self.bg_color).\
            grid(column=0, row=21, sticky='w')
        slow = tk.Radiobutton(self.frame, text='Slow', variable=self.speed, value=1, bg=self.bg_color).\
            grid(column=0, row=21, sticky='e')

        city_button = tk.Button(self.frame, text="Select Cities", bg=self.s_color, fg=self.h_color,
                                font='Calibri 12 bold', command=self.select_cities).grid(column=0, row=22,
                                                                                         sticky='nsew', padx=2)
        restart_button = tk.Button(self.frame, text="Restart", bg="firebrick1", fg=self.h_color,
                                   font='Calibri 12 bold', command=self.refresh_canvas).grid(column=0,
                                                                                             row=23, sticky='w')
        continue_button = tk.Button(self.frame, text="Continue", bg=self.s_color, fg=self.h_color,
                                    font='Calibri 12 bold', command=self.load_same).grid(column=0, row=23, sticky='e')



        self.step_label = tk.Label(self.window, fg=self.h_color, bg=self.bg_color, font='Calibri 16 bold')
        self.step_label.grid(column=1, row=1)

        '''header2 = tk.Label(self.frame_list, text="", font='Calibri 14 bold', fg=self.h_color, bg=self.bg_color)
        header2.grid(column=0, row=0)

        distance_labels = tk.Label(self.frame_list, text="", font='Calibri 12 bold', fg=self.s_color, bg=self.bg_color)
        distance_labels.grid(column=0, row=1)'''
        '''button = tk.Button(self.frame, background=self.bg_color, text="Save", command=self.connection_checker())
        button.grid(column=1, row=6)'''

    def refresh_canvas(self):
        self.canvas.delete("all")
        self.ovals = []
        self.city_count = 0
        self.conn_count = 0
        self.selected_cities = []
        self.distances = []
        self.lines = []
        self.canvas.create_line(20, 20, 20, 680, fill="gray")
        self.canvas.create_line(20, 20, 680, 20, fill="gray")
        self.canvas.create_line(680, 20, 680, 680, fill="gray")
        self.canvas.create_line(680, 680, 20, 680, fill="gray")

    def load_same(self):
        self.canvas.delete("all")
        self.city_count = 0
        self.conn_count = 0
        self.canvas.create_line(20, 20, 20, 680, fill="gray")
        self.canvas.create_line(20, 20, 680, 20, fill="gray")
        self.canvas.create_line(680, 20, 680, 680, fill="gray")
        self.canvas.create_line(680, 680, 20, 680, fill="gray")

        for i in range(len(self.ovals)):
            x, y = self.ovals[i]
            self.canvas.create_oval(x, y, x + 10, y + 10, fill=self.c_color, outline=self.c_color)
            self.canvas.create_text(x, y + 12, fill=self.h_color, font="Calibri 10", text=self.cities[self.city_count])
            self.city_count += 1

        for i in range(len(self.lines)):
            x1, y1, x2, y2 = self.lines[i]
            j = random.randint(0, len(self.colors) - 1)
            self.canvas.create_line(x1, y1, x2, y2, fill=self.colors[j])
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, fill=self.colors[j], font="Calibri 10",
                                    text=str(int(euclidean_distance(x1, y1, x2, y2))))
            self.conn_count += 1

    def select_cities(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<Button-1>", self.dst_and_src)
        self.selected_cities = []
        msg.showinfo(title="Info", message="Click the source and destination cities.")

    def set_connections(self):
        c = self.city_total.get()
        msg.showinfo(title="Number of Connections", message="Number of connections must be between {} and {}."
                     .format(c - 1, int(c*(c - 1)/2)))

    def add_buttons(self):
        self.refresh_canvas()
        self.canvas.bind("<Button-1>", self.create_by_input)
        section3 = tk.Label(self.frame, text="Cities and Connections", font='Calibri 12 bold', fg=self.s_color,
                            bg=self.bg_color)
        section3.grid(column=0, row=10)
        city = tk.Radiobutton(self.frame, text="Add City", variable=self.city_or_conn, value=0, bg=self.bg_color).\
            grid(column=0, row=11)
        connection = tk.Radiobutton(self.frame, text="Make Connection", variable=self.city_or_conn, value=1,
                                    bg=self.bg_color).grid(column=0, row=12)
        msg.showinfo(title="Info", message="Insert cities inside the gray frame.")

    def overlap(self, x, y):
        overlap = False
        i = 0
        while i < len(self.ovals) and not overlap:
            x1, y1 = self.ovals[i]
            if euclidean_distance(x, y, x1, y1) < 30:
                overlap = True
            i += 1

        return overlap

    def create_line(self, x1, y1, x2, y2):
        j = random.randint(0, len(self.colors) - 1)

        self.canvas.create_line(x1 + 5, y1 + 5, x2 + 5, y2 + 5, fill=self.colors[j])
        self.canvas.create_text((x1 + x2 + 10) / 2, (y1 + y2 + 10) / 2, fill=self.colors[j], font="Calibri 10",
                                text=str(int(euclidean_distance(x1 + 5, y1 + 5, x2 + 5, y2 + 5))))
        self.lines.append((x1 + 5, y1 + 5, x2 + 5, y2 + 5))

        # uzaklıkları yazdırmayı sonraya saldım
        '''city1 = self.canvas.find_closest(x1 + 12, y1 + 12)
        city2 = self.canvas.find_closest(x2 + 12, y2 + 12)
        print("City1", city1.itemcget(city1, "text"))'''

        # self.city_dict["City1"] = city1.get()

    def create_city(self, x, y):
        self.canvas.create_oval(x, y, x + 10, y + 10, fill=self.c_color, outline=self.c_color)
        self.canvas.create_text(x, y + 12, fill=self.h_color, font="Calibri 10", text=self.cities[self.city_count])
        self.ovals.append((x, y))

    def create_randomly(self):
        self.refresh_canvas()
        x = 0
        y = 0
        i = 0
        # add cities
        while self.city_count < (self.city_total.get()):
            x = random.randint(30, 670)
            y = random.randint(30, 670)

            if not self.overlap(x, y):
                self.create_city(x, y)
                self.city_count += 1

        if self.entry.get() < self.city_total.get() - 1 or self.entry.get() > self.city_total.get() * \
                (self.city_total.get() - 1) / 2:
            msg.showerror(title="Connection Number Error", message="Number of connections are not in the interval.")
            return
        # make connections
        flags = np.zeros(self.city_total.get())
        i = 0
        while i < len(self.ovals) and self.conn_count < self.entry.get():
            if flags[i] == 0:
                to = random.randint(0, len(self.ovals) - 1)
                if i != to:
                    flags[i] = 1
                    flags[to] = 1
                    x1, y1 = self.ovals[i]
                    x2, y2 = self.ovals[to]
                    self.create_line(x1, y1, x2, y2)
                    self.conn_count += 1
                    i += 1
            else:
                i += 1

        while self.conn_count < self.entry.get():
            fr = random.randint(0, len(self.ovals) - 1)
            to = random.randint(0, len(self.ovals) - 1)
            if fr != to:
                x1, y1 = self.ovals[fr]
                x2, y2 = self.ovals[to]
                if (x1, y1, x2, y2) not in self.lines:
                    self.create_line(x1, y1, x2, y2)
                    self.conn_count += 1

    def is_a_city(self, x, y):
        i = 0
        found = False
        x1 = 0
        y1 = 0
        while i < len(self.ovals) and not found:
            x1, y1 = self.ovals[i]
            if x1 - 1 < x < x1 + 11 and y1 - 1 < y < y1 + 11:  # it is a city
                found = True
            i += 1
        return found, x1, y1

    def create_by_input(self, event):
        x = event.x
        y = event.y
        if self.city_or_conn.get() == 0:  # city
            if self.city_count < self.city_total.get():
                if not self.overlap(x, y):
                    self.create_city(x, y)
                    self.city_count += 1
            else:
                msg.showerror(title="Error", message="Number of cities completed.")

        elif self.city_or_conn.get() == 1:  # connection
            if self.conn_count < int(self.entry.get()):
                flag, x, y = self.is_a_city(x, y)
                if flag and (len(self.selected_cities) == 0 or len(self.selected_cities) == 1
                             and self.selected_cities[0] != (x, y)):
                    self.selected_cities.append((x, y))
                    if len(self.selected_cities) == 2:
                        (x1, y1) = self.selected_cities[0]
                        (x2, y2) = self.selected_cities[1]
                        if (x1, y1, x2, y2) not in self.lines:
                            self.create_line(x1, y1, x2, y2)
                            self.conn_count += 1
                        self.selected_cities = []
            else:
                msg.showerror(title="Error", message="Number of connections completed.")

    def dst_and_src(self, event):
        x = event.x
        y = event.y
        flag, x, y = self.is_a_city(x, y)
        if flag and (len(self.selected_cities) == 0 or len(self.selected_cities) == 1
                     and self.selected_cities[0] != (x, y)):
            self.selected_cities.append((x, y))
            msg.showinfo(title="Info", message="City selected.")
            if len(self.selected_cities) == 2:
                run()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.index = 0
        self.parent = None

    def equal(self, other):
        if euclidean_distance(self.x, self.y, other.x, other.y) == 0:
            return True


def euclidean_distance(x1, y1, x2, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)


def find_in_ovals(x, y):
    i = 0
    while i < len(gui.ovals):
        (x1, y1) = gui.ovals[i]
        if euclidean_distance(x, y, x1, y1) == 0:
            return i
        i += 1
    return -1


def append_to_stack(x, y, end_point, parent_point, index, stack, top, visited, index2):
    point = Point(x - 5, y - 5)
    point.parent = parent_point
    if index == 0 or index == 1:  # a star and best first search
        point.h = euclidean_distance(x - 5, y - 5, end_point.x, end_point.y)
        if index == 0:  # a star
            point.g = point.parent.g + euclidean_distance(point.x, point.y, point.parent.x, point.parent.y)
        point.f = point.g + point.h
    stack.append(point)
    top += 1
    visited[index2] = 1
    return top


def add_neighbours(parent_point, stack, top, visited, end_point, index):
    # find neighbours
    i = 0
    while i < len(gui.lines):
        x1, y1, x2, y2 = gui.lines[i]
        index1 = find_in_ovals(x1 - 5, y1 - 5)
        index2 = find_in_ovals(x2 - 5, y2 - 5)

        if euclidean_distance(x1 - 5, y1 - 5, parent_point.x, parent_point.y) == 0 and visited[index2] == 0:
            print("Eklenen nokta: ", x2 - 5, y2 - 5)
            top = append_to_stack(x2, y2, end_point, parent_point, index, stack, top, visited, index2)

        elif euclidean_distance(x2 - 5, y2 - 5, parent_point.x, parent_point.y) == 0 and visited[index1] == 0:
            print("Eklenen nokta: ", x1 - 5, y1 - 5)
            top = append_to_stack(x1, y1, end_point, parent_point, index, stack, top, visited, index1)

        i += 1

    return top


def a_star_and_best_first_search(index):
    stack = []
    found = False
    top = 0
    (x, y) = gui.selected_cities[0]
    (end_x, end_y) = gui.selected_cities[1]

    point = Point(x, y)
    end = Point(end_x, end_y)
    start = point
    print("Start {}, {}. End {}, {}".format(start.x, start.y, end.x, end.y))
    point.index = find_in_ovals(x, y)
    stack.append(point)  # source
    visited = np.zeros(gui.city_count)
    visited[point.index] = 1
    popped = 0
    max_element = 0

    while len(stack) > 0 and not found:
        point = stack.pop(top)
        print("Çekilen nokta: ", point.x, point.y)
        top -= 1
        if point.equal(end):
            found = True
            print("Path found")
        else:
            top = add_neighbours(point, stack, top, visited, end, index)
            stack.sort(key=lambda point: point.f, reverse=True)  # sort max to min by h(n)
            if len(stack) > max_element:
                max_element = len(stack)
            print("Stack boyutu:", len(stack))
            popped += 1

    if found:
        paint(point, start, max_element)
    else:
        print("Yol yok")
    return


def depth_first_search():
    stack = []
    found = False
    top = 0
    (x, y) = gui.selected_cities[0]
    (end_x, end_y) = gui.selected_cities[1]

    point = Point(x, y)
    end = Point(end_x, end_y)
    start = point
    print("Start {}, {}. End {}, {}".format(start.x, start.y, end.x, end.y))
    point.index = find_in_ovals(x, y)
    stack.append(point)  # source
    visited = np.zeros(gui.city_count)
    visited[point.index] = 1
    popped = 0
    max_element = 0

    while len(stack) > 0 and not found:
        point = stack.pop(top)
        print("Çekilen nokta: ", point.x, point.y)
        top -= 1
        if point.equal(end):
            found = True
            print("Path found")
        else:
            top = add_neighbours(point, stack, top, visited, end, 2)
            if len(stack) > max_element:
                max_element = len(stack)
            print("Stack boyutu:", len(stack))
            popped += 1

    if found:
        paint(point, start, max_element)
    else:
        print("Yol yok")
    return


def breadth_first_search():
    queue = []
    found = False
    rear = 0
    front = 0
    (x, y) = gui.selected_cities[0]
    (end_x, end_y) = gui.selected_cities[1]

    point = Point(x, y)
    end = Point(end_x, end_y)
    start = point
    print("Start {}, {}. End {}, {}".format(start.x, start.y, end.x, end.y))
    point.index = find_in_ovals(x, y)
    queue.append(point)  # source
    visited = np.zeros(gui.city_count)
    visited[point.index] = 1
    popped = 0
    max_element = 0

    while len(queue) > 0 and not found:
        point = queue[front]
        print("Çekilen nokta: ", point.x, point.y)
        rear -= 1
        if point.equal(end):
            found = True
            print("Path found")
        else:
            top = add_neighbours(point, queue, rear, visited, end, 2)
            if len(queue) > max_element:
                max_element = len(queue)
            print("Stack boyutu:", len(queue))
            popped += 1
        front += 1

    if found:
        paint(point, start, max_element)
    else:
        print("Yol yok")
    return


def paint(point, start, max_element):
    path = []
    total_distance = 0
    delay = 0.3
    if gui.speed.get() == 0:  # fast
        delay = 0.2
    elif gui.speed.get() == 1:
        delay = 0.5

    while not point.equal(start):
        path.append(point)
        point = point.parent

    for i in range(len(path) - 1, -1, -1):
        gui.canvas.create_line(path[i].x + 5, path[i].y + 5, path[i].parent.x + 5, path[i].parent.y + 5,
                               width=3, fill="yellow")
        gui.window.update()
        time.sleep(delay)


def run():
    print(gui.conn_count, gui.entry.get())
    if gui.conn_count < gui.entry.get():
        msg.showerror(title="Connection Count Error", message="The number of connections is {} but it's supposed "
                                                              "to be {}.".format(gui.conn_count, gui.entry.get()))
        return
    elif gui.city_count + 1 < gui.city_total.get():
        msg.showerror(title="City Count Error", message="The number of cities is {} but it's supposed to be {}.".
                      format(gui.city_count, gui.city_total.get()))
        return

    if gui.algorithm.get() == 0:  # a *
        a_star_and_best_first_search(0)
    elif gui.algorithm.get() == 1:  # best first search
        a_star_and_best_first_search(1)
    elif gui.algorithm.get() == 2:
        depth_first_search()
    elif gui.algorithm.get() == 3:
        breadth_first_search()
    else:
        msg.showerror(title="Algorithm Selection Error", message="You did not choose the algorithm.")

    return


if __name__ == "__main__":
    root = tk.Tk()
    gui = Gui()
    root.mainloop()
