import tkinter as tk
import tkinter.messagebox as msg
import random
from math import sqrt
import numpy as np
import time
import csv


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
        self.change_type = tk.IntVar()

        self.city_count = 0
        self.conn_count = 0
        self.selected_cities = []
        self.ovals = []
        self.lines = []
        self.gonna_move = -1
        self.gonna_move_cons = []
        self.city = {
                    "coords": (0, 0),
                    "name": "London"
        }

        self.cities = ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpeiller",
                       "Bordeaux", "Lille", "Rennas", "Reims", "Le_Havre", "Toulon", "Grenoble", "Dijon", "Angers",
                       "Villeaurbanne", "Le_Mans", "Saint-Denis"]
        self.colors = ["red", "blue", "purple", "brown", "green", "hot pink", "orange red", "black", "cyan",
                       "deep pink", "green3", "DodgerBlue3", "firebrick4", "LightPink4", "maroon", "SeaGreen3",
                       "lime green", "navy", "dark violet", "red4"]

        header = tk.Label(self.frame, text="Create Map", font='Calibri 12 bold', fg=self.h_color, bg=self.bg_color)
        header.grid(column=0, row=0)
        section = tk.Label(self.frame, text="Number of Cities", font='Calibri 12 bold', fg=self.s_color,
                           bg=self.bg_color)
        section.grid(column=0, row=1)
        cities5 = tk.Radiobutton(self.frame, text='5', variable=self.city_total, command=self.set_connections,
                                 value=5, bg=self.bg_color).grid(column=0, row=2, sticky='w')
        cities10 = tk.Radiobutton(self.frame, text='10', variable=self.city_total, command=self.set_connections,
                                  value=10, bg=self.bg_color).grid(column=0, row=2, sticky='n')
        cities20 = tk.Radiobutton(self.frame, text='20', variable=self.city_total, command=self.set_connections,
                                  value=20, bg=self.bg_color).grid(column=0, row=2, sticky='e')
        section1 = tk.Label(self.frame, text="Number of Connections", font='Calibri 12 bold', fg=self.s_color,
                            bg=self.bg_color)
        section1.grid(column=0, row=5)

        entry1 = tk.Entry(self.frame, textvariable=self.entry, background=self.bg_color)
        entry1.grid(column=0, row=6)

        section2 = tk.Label(self.frame, text="How to Create", font='Calibri 12 bold', fg=self.s_color, bg=self.bg_color)
        section2.grid(column=0, row=7)
        frame_ran = tk.Radiobutton(self.frame, text='Random', variable=self.input_type, value="Random",
                                   command=self.create_randomly, bg=self.bg_color).grid(column=0, row=8, sticky='w')
        frame_us = tk.Radiobutton(self.frame, text='User Input', variable=self.input_type, value="User",
                                  command=self.add_buttons, bg=self.bg_color).grid(column=0, row=8, sticky='e')
        section3 = tk.Label(self.frame, text="Cities and Connections", font='Calibri 12 bold', fg=self.s_color,
                            bg=self.bg_color)
        section3.grid(column=0, row=10)
        city = tk.Radiobutton(self.frame, text="Add City", variable=self.city_or_conn, command=self.binder, value=0,
                              bg=self.bg_color).grid(column=0, row=11)
        connection = tk.Radiobutton(self.frame, text="Make Connection", variable=self.city_or_conn, command=self.binder,
                                    value=1, bg=self.bg_color).grid(column=0, row=12)
        section4 = tk.Label(self.frame, text="Change Map", font='Calibri 12 bold', fg=self.s_color, bg=self.bg_color)
        section4.grid(column=0, row=13)

        move_city = tk.Radiobutton(self.frame, text='Move City', variable=self.change_type, value=0,
                                   command=self.change_map, bg=self.bg_color).grid(column=0, row=14)
        delete_city = tk.Radiobutton(self.frame, text='Delete City', variable=self.change_type, value=1,
                                     command=self.change_map, bg=self.bg_color).grid(column=0, row=15)
        delete_conn = tk.Radiobutton(self.frame, text='Delete Connection', variable=self.change_type, value=2,
                                     command=self.change_map, bg=self.bg_color).grid(column=0, row=16)

        header2 = tk.Label(self.frame, text="Algorithms", font='Calibri 12 bold', fg=self.h_color, bg=self.bg_color)
        header2.grid(column=0, row=17)

        alg1 = tk.Radiobutton(self.frame, text='A* Search', variable=self.algorithm, value=0,
                              bg=self.bg_color).grid(column=0, row=18)
        alg2 = tk.Radiobutton(self.frame, text='Best First Search', variable=self.algorithm, value=1,
                              bg=self.bg_color).grid(column=0, row=19)
        alg3 = tk.Radiobutton(self.frame, text='Depth First Search', variable=self.algorithm, value=2,
                              bg=self.bg_color).grid(column=0, row=20)
        alg4 = tk.Radiobutton(self.frame, text='Breadth First Search', variable=self.algorithm, value=3,
                              bg=self.bg_color).grid(column=0, row=21)
        section4 = tk.Label(self.frame, text="Evaluation Function", font='Calibri 12 bold', fg=self.s_color,
                            bg=self.bg_color)
        section4.grid(column=0, row=22)
        euclidean = tk.Radiobutton(self.frame, text='Euclidean', variable=self.evaluation, value=0, bg=self.bg_color). \
            grid(column=0, row=23, sticky='w')
        manhattan = tk.Radiobutton(self.frame, text='Manhattan', variable=self.evaluation, value=1, bg=self.bg_color). \
            grid(column=0, row=23, sticky='e')
        section3 = tk.Label(self.frame, text="Animation Speed", font='Calibri 12 bold', fg=self.s_color,
                            bg=self.bg_color)
        section3.grid(column=0, row=24)
        fast = tk.Radiobutton(self.frame, text='Fast', variable=self.speed, value=0, bg=self.bg_color).\
            grid(column=0, row=25, sticky='w')
        slow = tk.Radiobutton(self.frame, text='Slow', variable=self.speed, value=1, bg=self.bg_color).\
            grid(column=0, row=25, sticky='e')

        city_button = tk.Button(self.frame, text="Select Cities", bg=self.s_color, fg=self.h_color,
                                font='Calibri 12 bold', command=self.select_cities).grid(column=0, row=26,
                                                                                         sticky='e', padx=2)
        restart_button = tk.Button(self.frame, text="Restart", bg="firebrick1", fg=self.h_color,
                                   font='Calibri 12 bold', command=self.refresh_canvas).grid(column=0,
                                                                                             row=26, sticky='w')
        header3 = tk.Label(self.frame, text="Outputs", font='Calibri 12 bold', fg=self.h_color, bg=self.bg_color)
        header3.grid(column=0, row=28)

        self.output_label = tk.Label(self.frame, fg=self.h_color, bg=self.bg_color, font='Calibri 12 bold')
        self.output_label.grid(column=0, row=29)

        self.step_label = tk.Label(self.window, fg=self.h_color, bg=self.bg_color, font='Calibri 16 bold')
        self.step_label.grid(column=1, row=1)

        '''header2 = tk.Label(self.frame_list, text="", font='Calibri 14 bold', fg=self.h_color, bg=self.bg_color)
        header2.grid(column=0, row=0)

        distance_labels = tk.Label(self.frame_list, text="", font='Calibri 12 bold', fg=self.s_color, bg=self.bg_color)
        distance_labels.grid(column=0, row=1)'''
        '''button = tk.Button(self.frame, background=self.bg_color, text="Save", command=self.connection_checker())
        button.grid(column=1, row=6)'''

    def refresh_canvas(self):
        self.cities = ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpeiller",
                       "Bordeaux", "Lille", "Rennas", "Reims", "Le_Havre", "Toulon", "Grenoble", "Dijon", "Angers",
                       "Villeaurbanne", "Le_Mans", "Saint-Denis"]
        self.canvas.delete("all")
        self.ovals = []
        self.city_count = 0
        self.conn_count = 0
        self.selected_cities = []
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
        self.step_label.config(text=" ")
        self.output_label.config(text=" ")

        for i in range(len(self.ovals)):
            x, y = self.ovals[i]["coords"]
            self.canvas.create_oval(x, y, x + 10, y + 10, fill=self.c_color, outline=self.c_color)
            if self.cities[self.city_count] == "Le_Havre":
                self.canvas.create_text(x, y + 12, fill=self.h_color, font="Calibri 10", text="Le Havre",
                                        tag=self.cities[self.city_count] + "_text")
            elif self.cities[self.city_count] == "Le_Mans":
                self.canvas.create_text(x, y + 12, fill=self.h_color, font="Calibri 10", text="Le Mans",
                                        tag=self.cities[self.city_count] + "_text")
            else:
                self.canvas.create_text(x, y + 12, fill=self.h_color, font="Calibri 10",
                                        text=self.cities[self.city_count],
                                        tag=self.cities[self.city_count] + "_text")
            self.city_count += 1

        for i in range(len(self.lines)):
            x1, y1, x2, y2 = self.lines[i]["coords"]
            j = random.randint(0, len(self.colors) - 1)
            self.canvas.create_line(x1, y1, x2, y2, fill=self.colors[j])
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, fill=self.colors[j], font="Calibri 10",
                                    text=str(int(distance(x1, y1, x2, y2, 1))))
            self.conn_count += 1

    def select_cities(self):
        self.load_same()
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<Button-1>", self.dst_and_src)
        self.selected_cities = []
        msg.showinfo(title="Info", message="Click the source and destination cities.")

    def set_connections(self):
        c = self.city_total.get()
        msg.showinfo(title="Number of Connections", message="Number of connections must be between {} and {}."
                     .format(c - 1, int(c*(c - 1)/2)))

    def binder(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.bind("<Button-1>", self.create_by_input)

    def add_buttons(self):
        self.refresh_canvas()
        msg.showinfo(title="Info", message="Insert cities inside the gray frame.")

    def change_map(self):
        self.canvas.unbind("<Button-1>")
        self.gonna_move = -1
        if self.change_type.get() == 0:  # move city
            self.canvas.bind("<Button-1>", self.move_city)
        elif self.change_type.get() == 1:  # delete city
            self.canvas.bind("<Button-1>", self.delete_city)
        elif self.change_type.get() == 2:  # delete connection
            self.canvas.bind("<Button-1>", self.delete_connection)

    def find_city(self, x, y):
        i = 0
        found = False
        while i < len(self.ovals) and not found:
            x1, y1 = self.ovals[i]["coords"]
            if x1 - 1 < x < x1 + 11 and y1 - 1 < y < y1 + 11:  # it is a city
                found = True
            else:
                i += 1
        return found, i

    def find_connections(self, index):
        x, y = self.ovals[index]["coords"]
        for i in range(len(self.lines)):
            x1, y1, x2, y2 = self.lines[i]["coords"]

            if distance(x1 - 5, y1 - 5, x, y, 0) == 0 or distance(x2 - 5, y2 - 5, x, y, 0) == 0:
                # print("Bağlantı var: ", self.lines[i])
                self.gonna_move_cons.append(i)
                name = "{},{}-{},{}".format(x1, y1, x2, y2)
                self.canvas.delete(name + "_line")
                self.canvas.delete(name + "_text")

    def move_city(self, event):
        x = event.x
        y = event.y

        if self.gonna_move == -1:  # city
            found, index = self.find_city(x, y)
            if found:
                self.gonna_move = index
                self.canvas.delete(self.ovals[self.gonna_move]["name"] + "_oval")
                self.canvas.delete(self.ovals[self.gonna_move]["name"] + "_text")
                self.find_connections(index)
        else:  # destination
            self.canvas.create_oval(x, y, x + 10, y + 10, fill=self.c_color, outline=self.c_color,
                                    tag=self.ovals[self.gonna_move]["name"] + "_oval")
            if self.cities[self.gonna_move] == "Le_Havre":
                self.canvas.create_text(x, y + 12, fill=self.h_color, font="Calibri 10", text="Le Havre",
                                        tag=self.cities[self.gonna_move] + "_text")
            elif self.cities[self.gonna_move] == "Le_Mans":
                self.canvas.create_text(x, y + 12, fill=self.h_color, font="Calibri 10", text="Le Mans",
                                        tag=self.cities[self.gonna_move] + "_text")
            else:
                self.canvas.create_text(x, y + 12, fill=self.h_color, font="Calibri 10",
                                        text=self.cities[self.gonna_move],
                                        tag=self.ovals[self.gonna_move]["name"] + "_text")
            city = {"coords": (x, y), "name": self.cities[self.gonna_move]}
            old_x, old_y = self.ovals[self.gonna_move]["coords"]
            self.ovals[self.gonna_move] = city

            for i in range(len(self.gonna_move_cons)):
                k = self.gonna_move_cons[i]
                x1, y1, x2, y2 = self.lines[k]["coords"]
                if old_x + 5 == x2 and old_y + 5 == y2:
                    x2 = x1
                    y2 = y1

                j = random.randint(0, len(self.colors) - 1)
                name = "{},{}-{},{}".format(x + 5, y + 5, x2, y2)
                self.canvas.create_line(x + 5, y + 5, x2, y2, fill=self.colors[j], tag=name + "_line")
                self.canvas.create_text(int((x + x2 + 5) / 2), int((y + y2 + 5) / 2), fill=self.colors[j],
                                        font="Calibri 10", text=str(int(distance(x + 5, y + 5, x2, y2, 1))),
                                        tag=name + "_text")
                line = {"from": find_in_ovals(x, y), "to": find_in_ovals(x2 - 5, y2 - 5),
                        "coords": (x + 5, y + 5, x2, y2)}
                self.lines[k] = line
            self.gonna_move = -1
            self.gonna_move_cons = []

    def delete_city(self, event):
        x = event.x
        y = event.y

        found, index = self.find_city(x, y)
        if found:
            self.canvas.delete(self.ovals[index]["name"] + "_oval")
            if self.ovals[index]["name"] == "Le Havre":
                self.canvas.delete("Le_Havre" + "_text")
            elif self.ovals[index]["name"] == "Le Mans":
                self.canvas.delete("Le_Mans" + "_text")
            else:
                self.canvas.delete(self.ovals[index]["name"] + "_text")
            for i in range(index, self.city_count - 1):
                self.cities[i], self.cities[i+1] = self.cities[i+1], self.cities[i]
            self.city_count -= 1
            self.find_connections(index)
            del self.ovals[index]
            self.gonna_move_cons.sort(reverse=True)
            for i in range(len(self.gonna_move_cons)):
                k = self.gonna_move_cons[i]
                del self.lines[k]
                self.conn_count -= 1
            self.gonna_move_cons = []
        return

    def delete_connection(self, event):
        print("Geldim")
        x = event.x
        y = event.y
        obje = self.canvas.find_closest(x, y)

        if len(self.canvas.coords(obje)) == 4 and self.canvas.itemcget(obje, "fill") != "Magenta2":  # it's a line
            print("It's a line")
            x1, y1, x2, y2 = self.canvas.coords(obje)
            print(x1, y1, x2, y2)
            name = "{},{}-{},{}".format(int(x1), int(y1), int(x2), int(y2))
            self.canvas.delete(name + "_line")
            self.canvas.delete(name + "_text")
            i = 0
            found = False
            while i < (len(self.lines)) and not found:
                x3, y3, x4, y4 = self.lines[i]["coords"]
                if distance(x1, y1, x3, y3, 0) == 0 and distance(x2, y2, x4, y4, 0) == 0:
                    del self.lines[i]
                    print("Deleted.")
                    found = True
                    self.conn_count -= 1
                else:
                    i += 1
        return

    def overlap(self, x, y):
        overlap = False
        i = 0
        while i < len(self.ovals) and not overlap:
            x1, y1 = self.ovals[i]["coords"]
            if distance(x, y, x1, y1, 1) < 30:
                overlap = True
            i += 1

        return overlap

    def create_line(self, x1, y1, fr, x2, y2, to):
        j = random.randint(0, len(self.colors) - 1)
        name = "{},{}-{},{}".format(x1 + 5, y1 + 5, x2 + 5, y2 + 5)
        # print(name)
        self.canvas.create_line(x1 + 5, y1 + 5, x2 + 5, y2 + 5, fill=self.colors[j], tag=name + "_line")
        self.canvas.create_text((x1 + x2 + 10) / 2, (y1 + y2 + 10) / 2, fill=self.colors[j], font="Calibri 10",
                                text=str(int(distance(x1 + 5, y1 + 5, x2 + 5, y2 + 5, 1))), tag=name + "_text")
        line = {"coords": (x1 + 5, y1 + 5, x2 + 5, y2 + 5)}
        self.lines.append(line)

    def create_city(self, x, y):
        self.canvas.create_oval(x, y, x + 10, y + 10, fill=self.c_color, outline=self.c_color,
                                tag=self.cities[self.city_count] + "_oval")
        if self.cities[self.city_count] == "Le_Havre":
            self.canvas.create_text(x, y + 12, fill=self.h_color, font="Calibri 10", text="Le Havre",
                                    tag=self.cities[self.city_count] + "_text")
        elif self.cities[self.city_count] == "Le_Mans":
            self.canvas.create_text(x, y + 12, fill=self.h_color, font="Calibri 10", text="Le Mans",
                                    tag=self.cities[self.city_count] + "_text")
        else:
            self.canvas.create_text(x, y + 12, fill=self.h_color, font="Calibri 10", text=self.cities[self.city_count],
                                    tag=self.cities[self.city_count] + "_text")
        city = {"coords": (x, y), "name": self.cities[self.city_count]}
        self.ovals.append(city)

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
        # print(self.ovals)
        flags = np.zeros(self.city_total.get())
        i = 0
        while i < len(self.ovals) and self.conn_count < self.entry.get():
            if flags[i] == 0:
                to = random.randint(0, len(self.ovals) - 1)
                if i != to:
                    flags[i] = 1
                    flags[to] = 1
                    x1, y1 = self.ovals[i]["coords"]
                    x2, y2 = self.ovals[to]["coords"]
                    self.create_line(x1, y1, i, x2, y2, to)
                    self.conn_count += 1
                    i += 1
            else:
                i += 1

        while self.conn_count < self.entry.get():
            fr = random.randint(0, len(self.ovals) - 1)
            to = random.randint(0, len(self.ovals) - 1)
            if fr != to:
                x1, y1 = self.ovals[fr]["coords"]
                x2, y2 = self.ovals[to]["coords"]
                if (x1, y1, x2, y2) not in self.lines:
                    self.create_line(x1, y1, fr, x2, y2, to)
                    self.conn_count += 1
        # print(self.lines)

    def is_a_city(self, x, y):
        i = 0
        found = False
        x1 = 0
        y1 = 0
        while i < len(self.ovals) and not found:
            x1, y1 = self.ovals[i]["coords"]
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
                            self.create_line(x1, y1, find_in_ovals(x1, y1), x2, y2, find_in_ovals(x2, y2))
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
        if distance(self.x, self.y, other.x, other.y, 0) == 0:
            return True


def distance(x1, y1, x2, y2, want):
    if gui.evaluation == 0 or want == 1:  # euclidean distance
        return sqrt((x1 - x2)**2 + (y1 - y2)**2)
    else:  # manhattan distance
        return abs(x1 - x2) + abs(y1 - y2)


def find_in_ovals(x, y):
    i = 0
    while i < len(gui.ovals):
        (x1, y1) = gui.ovals[i]["coords"]
        if distance(x, y, x1, y1, 0) == 0:
            return i
        i += 1
    return -1


def append_to_stack(x, y, end_point, parent_point, index, stack, top, visited, index2):
    point = Point(x - 5, y - 5)
    point.parent = parent_point
    if index == 0 or index == 1:  # a star and best first search
        point.h = distance(x - 5, y - 5, end_point.x, end_point.y, 0)
        if index == 0:  # a star
            point.g = point.parent.g + distance(point.x, point.y, point.parent.x, point.parent.y, 1)
        point.f = point.g + point.h
    stack.append(point)
    top += 1
    visited[index2] = 1
    return top


def add_neighbours(parent_point, stack, top, visited, end_point, index):
    # find neighbours
    i = 0
    while i < len(gui.lines):
        x1, y1, x2, y2 = gui.lines[i]["coords"]
        index1 = find_in_ovals(x1 - 5, y1 - 5)
        index2 = find_in_ovals(x2 - 5, y2 - 5)

        if distance(x1 - 5, y1 - 5, parent_point.x, parent_point.y, 0) == 0 and visited[index2] == 0:
            # print("Eklenen nokta: ", x2 - 5, y2 - 5)
            top = append_to_stack(x2, y2, end_point, parent_point, index, stack, top, visited, index2)

        elif distance(x2 - 5, y2 - 5, parent_point.x, parent_point.y, 0) == 0 and visited[index1] == 0:
            # print("Eklenen nokta: ", x1 - 5, y1 - 5)
            top = append_to_stack(x1, y1, end_point, parent_point, index, stack, top, visited, index1)

        i += 1

    return top


def a_star_and_best_first_search(index, start_time):
    stack = []
    found = False
    top = 0
    (x, y) = gui.selected_cities[0]
    (end_x, end_y) = gui.selected_cities[1]

    point = Point(x, y)
    end = Point(end_x, end_y)
    start = point
    # print("Start {}, {}. End {}, {}".format(start.x, start.y, end.x, end.y))
    point.index = find_in_ovals(x, y)
    stack.append(point)  # source
    visited = np.zeros(gui.city_count)
    visited[point.index] = 1
    popped = 0
    max_element = 0

    while len(stack) > 0 and not found:
        point = stack.pop(top)
        # print("Çekilen nokta: ", point.x, point.y)
        top -= 1
        if point.equal(end):
            found = True
            print("Path found")
        else:
            top = add_neighbours(point, stack, top, visited, end, index)
            stack.sort(key=lambda point: point.f, reverse=True)  # sort max to min by h(n)
            if len(stack) > max_element:
                max_element = len(stack)
            # print("Stack boyutu:", len(stack))
            popped += 1

    if found:
        total_distance, step_size = paint(point, start, max_element, popped)
        return total_distance, step_size, max_element, popped, time.time() - start_time
    else:
        message = "Path is not exist."
        gui.step_label.config(text=message)
    return 0, 0, 0, 0, time.time() - start_time


def depth_first_search(start_time):
    stack = []
    found = False
    top = 0
    (x, y) = gui.selected_cities[0]
    (end_x, end_y) = gui.selected_cities[1]

    point = Point(x, y)
    end = Point(end_x, end_y)
    start = point
    # print("Start {}, {}. End {}, {}".format(start.x, start.y, end.x, end.y))
    point.index = find_in_ovals(x, y)
    stack.append(point)  # source
    visited = np.zeros(gui.city_count)
    visited[point.index] = 1
    popped = 0
    max_element = 0

    while len(stack) > 0 and not found:
        point = stack.pop(top)
        # print("Çekilen nokta: ", point.x, point.y)
        top -= 1
        if point.equal(end):
            found = True
            print("Path found")
        else:
            top = add_neighbours(point, stack, top, visited, end, 2)
            if len(stack) > max_element:
                max_element = len(stack)
            # print("Stack boyutu:", len(stack))
            popped += 1

    if found:
        total_distance, step_size = paint(point, start, max_element, popped)
        return total_distance, step_size, max_element, popped, time.time() - start_time
    else:
        message = "Path is not exist."
        gui.step_label.config(text=message)
    return 0, 0, 0, 0, time.time() - start_time


def breadth_first_search(start_time):
    queue = []
    found = False
    rear = 0
    front = 0
    (x, y) = gui.selected_cities[0]
    (end_x, end_y) = gui.selected_cities[1]

    point = Point(x, y)
    end = Point(end_x, end_y)
    start = point
    # print("Start {}, {}. End {}, {}".format(start.x, start.y, end.x, end.y))
    point.index = find_in_ovals(x, y)
    queue.append(point)  # source
    visited = np.zeros(gui.city_count)
    visited[point.index] = 1
    popped = 0
    max_element = 0

    while len(queue) > 0 and not found:
        point = queue[front]
        # print("Çekilen nokta: ", point.x, point.y)
        rear -= 1
        if point.equal(end):
            found = True
            print("Path found")
        else:
            top = add_neighbours(point, queue, rear, visited, end, 2)
            if len(queue) > max_element:
                max_element = len(queue)
            # print("Stack boyutu:", len(queue))
            popped += 1
        front += 1

    if found:
        total_distance, step_size = paint(point, start, max_element, popped)
        return total_distance, step_size, max_element, popped, time.time() - start_time
    else:
        message = "Path is not exist."
        gui.step_label.config(text=message)
    return 0, 0, 0, 0, time.time() - start_time


def paint(point, start, max_element, pops):
    path = []
    step_size = 0
    total_distance = 0
    delay = 0.3
    if gui.speed.get() == 0:  # fast
        delay = 0.2
    elif gui.speed.get() == 1:
        delay = 0.5

    while not point.equal(start):
        path.append(point)
        total_distance += distance(point.x, point.y, point.parent.x, point.parent.y, 1)
        point = point.parent
        step_size += 1

    message = "Step Size: {}, Distance: {}".format(step_size, int(total_distance))
    message2 = "Maximum Stack Size: {}\nNumber of Pops: {}".format(max_element, pops)
    gui.step_label.config(text=message)
    gui.output_label.config(text=message2)

    for i in range(len(path) - 1, -1, -1):
        gui.canvas.create_line(path[i].x + 5, path[i].y + 5, path[i].parent.x + 5, path[i].parent.y + 5,
                               width=3, fill="yellow")
        gui.window.update()
        time.sleep(delay)

    return total_distance, step_size


def run():
    if gui.conn_count < gui.city_total.get() - 1:
        msg.showerror(title="Connection Count Error", message="The number of connections is {} it's less than threshold"
                                                              " {}.".format(gui.conn_count, gui.city_total.get() - 1))
        return
    elif gui.city_count + 1 < gui.city_total.get():
        msg.showerror(title="City Count Error", message="The number of cities is {} but it's supposed to be {}.".
                      format(gui.city_count, gui.city_total.get()))
        return
    elif gui.conn_count < gui.entry.get() - 1:
        msg.showinfo(title="Connection Count Info", message="The number connections is {} but it's supposed to be {}."
                     .format(gui.conn_count, gui.entry.get()))
    start = time.time()
    if gui.algorithm.get() == 0:  # a *
        total_distance, step_size, max_element, popped, total_time = a_star_and_best_first_search(0, start)
    elif gui.algorithm.get() == 1:  # best first search
        total_distance, step_size, max_element, popped, total_time = a_star_and_best_first_search(1, start)
    elif gui.algorithm.get() == 2:
        total_distance, step_size, max_element, popped, total_time = depth_first_search(start)
    elif gui.algorithm.get() == 3:
        total_distance, step_size, max_element, popped, total_time = breadth_first_search(start)
    else:
        msg.showerror(title="Algorithm Selection Error", message="You did not choose the algorithm.")

    return total_distance, step_size, max_element, popped, total_time


def select_indices():
    index1 = random.randint(0, gui.city_total.get() - 1)
    index2 = index1

    neighbours = []
    i = 0
    x, y = gui.ovals[index1]["coords"]
    while i < len(gui.lines):  # find neighbours
        x1, y1, x2, y2 = gui.lines[i]["coords"]
        if distance(x, y, x1 - 5, y1 - 5, 0) == 0:
            neighbours.append((x2 - 5, y2 - 5))
        elif distance(x, y, x2 - 5, y2 - 5, 0) == 0:
            neighbours.append((x1 - 5, y1 - 5))
        i += 1

    index2 = random.randint(0, gui.city_total.get() - 1)
    x1, y1 = gui.ovals[index2]["coords"]
    while index1 == index2 or (x1, y1) in neighbours:  # işimizi şansa bırakmıyoruz
        index2 = random.randint(0, gui.city_total.get() - 1)
        x1, y1 = gui.ovals[index2]["coords"]
    print("Selected: ", x, y, x1, y1)
    gui.selected_cities.append((x, y))
    gui.selected_cities.append((x1, y1))


def test():
    gui.city_total.set(20)
    gui.entry.set(40)

    with open('test_outputs.csv', 'w', newline='') as file:
        fieldnames = ['algorithm', 'distance', "step size", "max element", "popped", "time"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(100):
            print("Adım:", i)
            gui.create_randomly()
            gui.selected_cities = []
            select_indices()
            accepted = 0
            for j in range(6):
                if j == 0:
                    gui.algorithm.set(0)
                    gui.evaluation.set(0)
                    total_distance, step_size, max_element, popped, total_time = run()
                    accepted = total_distance
                    writer.writerow({"algorithm": "A* with Euclidean", "distance": accepted / total_distance , "step size": step_size,
                                  "max element": max_element, "popped": popped, "time": total_time})

                elif j == 1:
                    gui.algorithm.set(0)
                    gui.evaluation.set(1)
                    total_distance, step_size, max_element, popped, total_time = run()
                    writer.writerow({"algorithm": "A* with Manhattan", "distance": accepted / total_distance , "step size": step_size,
                                     "max element": max_element, "popped": popped, "time": total_time})

                elif j == 2:
                    gui.algorithm.set(1)
                    gui.evaluation.set(0)
                    total_distance, step_size, max_element, popped, total_time = run()
                    writer.writerow({"algorithm": "BFS with Euclidean", "distance": accepted / total_distance,
                                     "step size": step_size, "max element": max_element, "popped": popped, "time": total_time})

                elif j == 3:
                    gui.algorithm.set(1)
                    gui.evaluation.set(1)
                    total_distance, step_size, max_element, popped, total_time = run()
                    writer.writerow({"algorithm": "BFS with Manhattan", "distance": accepted / total_distance, "step size": step_size,
                                     "max element": max_element, "popped": popped, "time": total_time})

                elif j == 4:
                    gui.algorithm.set(2)
                    total_distance, step_size, max_element, popped, total_time = run()
                    writer.writerow({"algorithm": "DFS", "distance": accepted / total_distance, "step size": step_size,
                                     "max element": max_element, "popped": popped, "time": total_time})

                elif j == 5:
                    gui.algorithm.set(3)
                    total_distance, step_size, max_element, popped, total_time = run()
                    writer.writerow({"algorithm": "Breadth FS", "distance": accepted / total_distance, "step size": step_size,
                                     "max element": max_element, "popped": popped, "time": total_time})


if __name__ == "__main__":
    root = tk.Tk()
    gui = Gui()
    # test()
    root.mainloop()
