import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import random
import numpy as np
import time
import  threading
import statistics

class Plot:
    plots = []
    data = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    bracelet = None

    def __init__(self, master, title, time=10, y_limit=1023, maxlen=500, update_interval=20):
        # Создаем фигуру и оси
        self.fig, self.ax = plt.subplots(figsize=(3, 1.8))
        self.ax.set_xlim([-time, 0])
        self.plots.append(self)

        self.ax.set_title(title)
        for tick in self.ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(5)  # установка размера шрифта на 10 для меток на оси x
        for tick in self.ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(5)
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
        self.min_y = -32768
        self.max_y = 32768
        self.delta_y = -32768
        self.last_delta_y = 32768
    def set_pos(self, row=0, column=0, min_y=0, max_y=1023):
        self.ax.set_ylim([min_y, max_y])
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=column, row=row, padx=10, pady=10)
    # Функция для обновления данных на графике
    # def update_plot(self):
    #     # Получаем последние значения данных
    #     try:
    #         self.y_data.append(self.data[0])
    #     except:
    #         pass
    #     y = list(self.y_data)
    #     x = np.linspace(-self.time, 0, self.maxlen)
    #     self.ax.set_ylim([min(y), max(y)])
    #     self.line.set_xdata(np.linspace(-self.time, 0, self.maxlen))
    #     self.line.set_ydata(self.y_data)
    #     self.ax.draw_artist(self.ax.patch)
    #     self.ax.draw_artist(self.line)
    #     self.canvas.blit(self.ax.bbox)
    #     self.canvas.get_tk_widget().after(self.update_interval, self.update_plot)

    @classmethod
    def update_all_plots(cls):
        print(cls.data)
        for plot in cls.plots:
            try:
                plot.y_data.append(cls.data[cls.plots.index(plot)])

                y = list(plot.y_data)
                x = np.linspace(-plot.time, 0, plot.maxlen)

                # plot.min_y = min(plot.y_data)
                # plot.max_y = max(plot.y_data)
                # plot.delta_y = plot.max_y - plot.min_y
                # #print(abs(plot.last_delta_y - plot.delta_y))
                # if abs(plot.last_delta_y - plot.delta_y) > 50:
                #     plot.ax.set_ylim([plot.min_y, plot.max_y])
                #     plot.canvas.draw()
                # plot.last_delta_y = plot.delta_y

                plot.line.set_xdata(np.linspace(-plot.time, 0, plot.maxlen))
                plot.line.set_ydata(y)

                plot.ax.draw_artist(plot.ax.patch)
                plot.ax.draw_artist(plot.line)

                plot.canvas.blit(plot.ax.bbox)

            except:
                while len(cls.data) < len(cls.plots):
                    #cls.data.append(statistics.mean(list(cls.plots[len(cls.data)].y_data)))
                    cls.data.append(0)
                pass
        plot.canvas.get_tk_widget().after(plot.update_interval, cls.update_all_plots)

    # @classmethod
    # def update_yaxis(cls):
    #     for plot in cls.plots:
    #         plot.ax.set_ylim([min(plot.y_data), max(plot.y_data)])
    #         plot.canvas.draw()
    #     plot.canvas.get_tk_widget().after(plot.update_interval * 100, cls.update_yaxis)
    @classmethod
    def read_data(cls):
        while cls.stop == False:
            cls.data = cls.plots[0].bracelet.get_data().split()
            for i in range(len(cls.data)):
                if all(char in '-0123456789' for char in cls.data[i]):
                    cls.data[i] = int(cls.data[i])
            time.sleep(0.01)

    @classmethod
    def start_plots(cls):
        cls.stop = False
        cls.read = threading.Thread(target=cls.read_data)
        cls.read.start()
        cls.update_all_plots()
        # cls.update_yaxis()

    @classmethod
    def stop_plots(cls):
        for plot in cls.plots:
            cls.stop = True

    @classmethod
    def set_bracelet(cls, new_bracelet):
        cls.bracelet = new_bracelet

