import tkinter as tk
from tkinter import *
from bracelet import Bracelet
from plot import plot
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')


class GUI:
    def __init__(self):
        self.bracelet = Bracelet()
        self.plot = plot()
        self.root = tk.Tk()
        self.root.title("Электромиографический браслет")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = int(screen_width / 1.5)
        window_height = int(screen_height / 1.5)

        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # root.attributes('-alpha', 0.9)
        # root.iconbitmap('./assets/pythontutorial.ico')

        self.connect = tk.Button(text="Подключиться", command=self.connect)
        self.connect.grid(column=2, row=1)

        self.com_ports = self.bracelet.get_ports()

        self.selected_com_port = StringVar()
        self.selected_com_port.set("Выберите порт")

        self.option_menu = tk.OptionMenu(self.root, self.selected_com_port, *self.com_ports,
                                         command= lambda v: self.change_port())

        self.option_menu.grid(column=1, row=1)



    def show_window(self):
        self.root.mainloop()

    def change_port(self):
        self.bracelet.serial.port = self.selected_com_port.get()

    def connect(self):
        self.bracelet.connect()
        if self.bracelet.serial.is_open:
            self.plotter()
        else:
            print("Не удалось подключиться к последовательному порту.")
    def plotter(self):
        self.plotter.animation.event_source.start()(int(self.bracelet.get_data().split()[0]))
        self.root.after(20, self.plotter)


