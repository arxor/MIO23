import tkinter as tk
from tkinter import *
from bracelet import Bracelet
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import numpy as np
from collections import deque
matplotlib.use('TkAgg')



class Plot:
    def __init__(self, master):
        self.bracelet = None
        self.master = master
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim([-10, 0])
        self.ax.set_ylim([0, 1023])
        self.line, = self.ax.plot([], [], lw=2) # lw = line width
        self.y_data = deque([0] * 500, maxlen=500)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().grid(row=2, column=1)
        self.update_interval = 50
        self.animation = None

    def update(self):
        y = list(self.y_data)
        x = np.linspace(-10, 0, 500)
        self.line.set_data(x, y)
        # Перерисовываем график
        self.canvas.draw()

    def generate_data(self):
        if self.animation:
            # Генерируем новое значение и добавляем его в очередь)
            new_data = int(self.bracelet.get_data().split()[0])
            print(new_data)
            self.y_data.append(new_data)
            # Вызываем функцию обновления графика
            self.update()
            # Запускаем таймер на 50 мс
            #self.master.after(self.update_interval, self.generate_data)
