import tkinter as tk
import tkinter.messagebox as msg
import random
from math import sqrt
import numpy as np


class Gui:
    def __init__(self):
        self.window = root
        self.window.title("Path Finder")

        self.bg_color = "pink"
        self.h_color = "navy"
        self.s_color = "RoyalBlue2"
        self.c_color = "MediumOrchid1"
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
        self.selected_cities = []
        self.cities = ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpeiller",
                       "Bordeaux", "Lille", "Rennas", "Reims", "Le Havre", "Toulon", "Grenoble", "Dijon", "Angers",
                       "Villeaurbanne", "Le Mans", "Saint-Denis"]
        self.colors = ["red", "blue", "purple", "brown", "green", "hot pink", "orange red", "black", "cyan",
                       "deep pink", "green3", "DodgerBlue3", "firebrick4", "LightPink4", "maroon", "SeaGreen3",
                       "lime green", "navy", "dark violet", "red4", "magenta2"]
        self.city_count = 0
        self.conn_count = 0
        self.ovals = []
        self.distances = []
        self.city_dict = {"City1": "Paris", "City2": "Lion", "Distance": 0}
        self.entry = tk.IntVar()
        self.lines = []
        self.painted = None

        header = tk.Label(self.frame, text="Create Map", font='Calibri 14 bold', fg=self.h_color, bg=self.bg_color)
        header.grid(column=0, row=0)
        section = tk.Label(self.frame, text="Number of Cities", font='Calibri 12 bold', fg=self.s_color, bg=self.bg_color)
        section.grid(column=0, row=1)
        cities5 = tk.Radiobutton(self.frame, text='5 cities', variable=self.city_total, command=self.set_connections, value=5, bg=self.bg_color).grid(column=0, row=2)
        cities10 = tk.Radiobutton(self.frame, text='10 cities', variable=self.city_total, command=self.set_connections, value=10, bg=self.bg_color).grid(column=0, row=3)
        cities20 = tk.Radiobutton(self.frame, text='20 cities', variable=self.city_total, command=self.set_connections, value=20, bg=self.bg_color).grid(column=0, row=4)
        section1 = tk.Label(self.frame, text="Number of Connections:", font='Calibri 12 bold', fg=self.s_color,
                            bg=self.bg_color)
        section1.grid(column=0, row=5)

        entry1 = tk.Entry(self.frame, textvariable=self.entry, background=self.bg_color)
        entry1.grid(column=0, row=6)

        '''header2 = tk.Label(self.frame_list, text="", font='Calibri 14 bold', fg=self.h_color, bg=self.bg_color)
        header2.grid(column=0, row=0)

        distance_labels = tk.Label(self.frame_list, text="", font='Calibri 12 bold', fg=self.s_color, bg=self.bg_color)
        distance_labels.grid(column=0, row=1)'''
        '''button = tk.Button(self.frame, background=self.bg_color, text="Save", command=self.connection_checker())
        button.grid(column=1, row=6)'''

        section2 = tk.Label(self.frame, text="How to Create", font='Calibri 12 bold', fg=self.s_color, bg=self.bg_color)
        section2.grid(column=0, row=7)
        frame_ran = tk.Radiobutton(self.frame, text='Random', variable=self.input_type, value="Random",
                                   command=self.create_randomly, bg=self.bg_color).grid(column=0, row=8)
        frame_us = tk.Radiobutton(self.frame, text='User Input', variable=self.input_type, value="User",
                                  command=self.add_buttons, bg=self.bg_color).grid(column=0, row=9)

        # button = tk.Button(self.frame, text="RUN", command=create_population).grid(column=1, row=3, sticky='nsew', padx=2)
        '''
        self.generation_label = tk.Label(self.window, font='Calibri 16 bold')
        self.generation_label.grid(column=1, row=1)
        
        '''

    def set_connections(self):
        c = self.city_total.get()
        msg.showinfo(title="Number of Connections", message="Number of connections must be between {} and {}."
                     .format(c - 1, int(c*(c - 1)/2)))

    def refresh_canvas(self):
        self.canvas.delete("all")
        self.ovals = []
        self.canvas.create_line(20, 20, 20, 680, fill="gray")
        self.canvas.create_line(20, 20, 680, 20, fill="gray")
        self.canvas.create_line(680, 20, 680, 680, fill="gray")
        self.canvas.create_line(680, 680, 20, 680, fill="gray")

    def add_buttons(self):
        self.refresh_canvas()
        self.canvas.bind("<Button-1>", self.create_by_input)
        section3 = tk.Label(self.frame, text="Cities and Connections", font='Calibri 12 bold', fg=self.s_color, bg=self.bg_color)
        section3.grid(column=0, row=10)
        city = tk.Radiobutton(self.frame, text="Add City", variable=self.city_or_conn, value=0, bg=self.bg_color).grid(column=0, row=11)
        connection = tk.Radiobutton(self.frame, text="Make Connection", variable=self.city_or_conn, value=1, bg=self.bg_color).grid(column=0, row=12)
        msg.showinfo(title="Bilgi", message="Engel koymak istediğiniz kutuların üzerine tıklayınız.")

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

    def create_city(self, x, y, i):
        self.canvas.create_oval(x, y, x + 10, y + 10, fill=self.c_color, outline=self.c_color)
        self.ovals.append((x, y))
        self.canvas.create_text(x, y + 12, fill=self.h_color, font="Calibri 10", text=self.cities[i])

    def create_randomly(self):
        self.refresh_canvas()
        x = 0
        y = 0
        i = 0

        # add cities
        while i < (self.city_total.get()):
            x = random.randint(30, 670)
            y = random.randint(30, 670)

            if not self.overlap(x, y):
                self.create_city(x, y, i)
                i += 1

        # make connections
        flags = np.zeros(self.city_total.get())

        i = 0
        if self.entry.get() < self.city_total.get() - 1 or self.entry.get() > self.city_total.get() * (self.city_total.get() - 1) / 2:
            msg.showerror(title="Connection Number Error", message="Number of connections are not in the interval.")
            return

        while i < len(self.ovals):
            if flags[i] == 0:
                to = random.randint(0, len(self.ovals) - 1)
                if i != to:
                    flags[i] = 1
                    x1, y1 = self.ovals[i]
                    x2, y2 = self.ovals[to]
                    self.create_line(x1, y1, x2, y2)
                    self.conn_count += 1
                    i += 1

        while self.conn_count < int(self.entry.get()) + 1:
            fr = random.randint(0, len(self.ovals) - 1)
            to = random.randint(0, len(self.ovals) - 1)
            if fr != to:
                x1, y1 = self.ovals[fr]
                x2, y2 = self.ovals[to]
                if (x1, y1, x2, y2) not in self.lines:
                    self.create_line(x1, y1, x2, y2)
                    self.conn_count += 1
        return

    def is_a_city(self, x, y):
        i = 0
        found = False
        while i < len(self.ovals) and not found:
            x1, y1 = self.ovals[i]
            if x1 - 1 < x < x1 + 11 and y1 - 1 < y < y1 + 11:  # çakışma var
                found = True
            i += 1
        return found, x1, y1

    def create_by_input(self, event):
        x = event.x
        y = event.y
        if self.city_or_conn.get() == 0:  # city
            if self.city_count < self.city_total.get():
                if not self.overlap(x, y):
                    self.create_city(x, y, self.city_count)
                    self.city_count += 1
            else:
                msg.showerror(title="Number of Cities", message="Number of cities completed.")

        elif self.city_or_conn.get() == 1:  # connection
            if self.conn_count < int(self.entry.get()):
                flag, x, y = self.is_a_city(x, y)
                if flag and (len(self.selected_cities) == 0 or len(self.selected_cities) == 1 and self.selected_cities[0] != (x, y)):
                    self.selected_cities.append((x, y))
                    if len(self.selected_cities) == 2:
                        (x1, y1) = self.selected_cities[0]
                        (x2, y2) = self.selected_cities[1]
                        if (x1, y1, x2, y2) not in self.lines:
                            self.create_line(x1, y1, x2, y2)
                            self.conn_count += 1
                        self.selected_cities = []
            else:
                msg.showerror(title="Number of Connections", message="Number of connections completed.")
        return


def euclidean_distance(x1, y1, x2, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)


if __name__ == "__main__":
    root = tk.Tk()
    gui = Gui()
    root.mainloop()