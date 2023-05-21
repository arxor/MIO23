import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import numpy as np
import time
import threading
from processing import *
from config import *

import tkinter as tk
from tkinter import StringVar
from bracelet import Bracelet
from config import *
from processing import *


class Plot:
    plots = []

    def __init__(self, master, stream, title, time=10, maxlen=500, update_interval=20, autoscale=0):
        # Создаем фигуру и оси
        self.fig, self.ax = plt.subplots(figsize=PLOT_FIGSIZE)
        self.ax.set_xlim([-time, 0])
        self.plots.append(self)
        self.stream = stream
        self.ax.set_title(title)
        for tick in self.ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(PLOT_FONTSIZE)  # установка размера шрифта на 10 для меток на оси x
        for tick in self.ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(PLOT_FONTSIZE)
        self.line, = self.ax.plot([], [], lw=0.5)

        self.maxlen = maxlen
        # Создаем deque для хранения данных по оси y
        self.y_data = deque([0] * self.maxlen, maxlen=self.maxlen)

        # Создаем холст для отображения графика
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)

        # Запускаем генерацию данных и обновление графика
        self.update_interval = update_interval
        self.stop = False
        self.time = time
        self.update_interval = update_interval
        self.autoscale = autoscale

    def set_pos(self, row=0, column=0, min_y=0, max_y=1023):
        self.ax.set_ylim([min_y, max_y])
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=column, row=row, padx=10, pady=10)

    def set_style(self, bg_color='white', line_color='blue', text_color='black', font_size=10, font_family='serif'):
        self.ax.set_facecolor(bg_color)  # установка цвета фона
        self.line.set_color(line_color)  # установка цвета линии
        self.fig.set_facecolor('lightblue')
        self.ax.title.set_color(text_color)  # установка цвета заголовка
        self.ax.xaxis.label.set_color(text_color)  # установка цвета меток на оси x
        self.ax.yaxis.label.set_color(text_color)  # установка цвета меток на оси y
        self.ax.tick_params(axis='both', colors=text_color,
                            labelsize=font_size)  # установка цвета и размера меток на осях
        self.ax.title.set_fontsize(font_size)  # установка размера шрифта заголовка
        self.ax.xaxis.label.set_fontsize(font_size)  # установка размера шрифта меток на оси x
        self.ax.yaxis.label.set_fontsize(font_size)  # установка размера шрифта меток на оси y
        self.ax.title.set_fontfamily(font_family)  # установка семейства шрифта заголовка
        self.ax.xaxis.label.set_fontfamily(font_family)  # установка семейства шрифта меток на оси x
        self.ax.yaxis.label.set_fontfamily(font_family)  # установка семейства шрифта меток на оси y
        self.canvas.draw()  # перерисовываем график

    def update_plot(self):
        self.y_data.append(self.stream())
        y = list(self.y_data)
        x = np.linspace(-self.time, 0, self.maxlen)

        self.line.set_xdata(np.linspace(-self.time, 0, self.maxlen))
        self.line.set_ydata(y)

        self.ax.draw_artist(self.ax.patch)
        self.ax.draw_artist(self.line)

        self.canvas.blit(self.ax.bbox)

    @classmethod
    def start_plots(cls):
        cls.stop = False
        # cls.read = threading.Thread(target=cls.read_data)
        # cls.read.start()
        # cls.update_all_plots()

    @classmethod
    def stop_plots(cls):
        for plot in cls.plots:
            cls.stop = True

    @classmethod
    def set_bracelet(cls, new_bracelet):
        cls.bracelet = new_bracelet
