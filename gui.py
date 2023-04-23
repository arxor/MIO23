import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import random
import numpy as np

class Plot:
    def __init__(self, master, title, x_limit=500, y_limit=1023, maxlen=500, update_interval=10, bracelet=None):
        # Создаем фигуру и оси
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.ax.set_xlim([-10, 0])
        #self.ax.set_ylim([0, y_limit])

        self.ax.set_title(title)
        self.line, = self.ax.plot([], [], lw=0.5, marker='o')

        self.maxlen = maxlen
        # Создаем deque для хранения данных по оси y
        self.y_data = deque([0] * self.maxlen, maxlen=self.maxlen)

        # Создаем холст для отображения графика
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().grid(column=1, row=2)

        # Запускаем генерацию данных и обновление графика
        self.update_interval = update_interval
        self.bracelet = bracelet
    # Функция для обновления данных на графике
    def update_plot(self):
        # Получаем последние значения данных
        y = list(self.y_data)
        x = np.linspace(-10, 0, self.maxlen)
        self.ax.set_ylim([min(y), max(y)])
        self.line.set_data(x, y)
        # Перерисовываем график
        self.canvas.draw()
        # Запускаем таймер на update_interval мс для обновления графика
        self.canvas.get_tk_widget().after(self.update_interval, self.update_plot)

    # Функция для генерации новых данных
    def generate_data(self):
        # Генерируем новое значение и добавляем его в очередь
        new_value = int(self.bracelet.get_data().split()[1])
        print(new_value)
        self.y_data.append(new_value)
        # Запускаем таймер на update_interval мс для генерации новых данных
        self.canvas.get_tk_widget().after(self.update_interval, self.generate_data)

    def clear_data(self):
        self.y_data = deque([0] * self.maxlen, maxlen=self.maxlen)
