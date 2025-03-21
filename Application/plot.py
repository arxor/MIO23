"""
Модуль для построения графиков с помощью matplotlib.

В этом модуле представлен класс Plot для отображения графиков в приложении Tkinter.
Графики используются для отображения данных в реальном времени.
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Application.config import *
from Application.processing import *


class Plot:
    """
    Класс Plot представляет собой интерфейс для построения и обновления графиков в приложении Tkinter.
    """

    plots = []

    def __init__(self, master, stream, channel, title="chart", maxlen=50, fft=False):
        """
        Инициализация объекта класса Plot.

        master: родительский виджет, на котором будет отображаться график.
        stream: поток данных для отображения.
        channel: канал данных для отображения.
        title: заголовок графика.
        maxlen: максимальная длина данных для отображения.
        fft: флаг для включения преобразования Фурье.
        """
        # фигура и оси
        self.fig, self.ax = plt.subplots(figsize=PLOT_FIGSIZE)
        self.plots.append(self)
        self.stream = stream
        self.ax.set_title(title)
        self.ax.grid(True, linestyle="--", linewidth=0.5, color="gray")

        # шрифт
        for tick in self.ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(PLOT_FONTSIZE)
        for tick in self.ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(PLOT_FONTSIZE)
        (self.line,) = self.ax.plot([], [], lw=0.5)

        self.fft = fft
        self.maxlen = maxlen
        self.channel = channel

        # холст для отображения графика
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.set_style()

    def set_pos(self, row=0, column=0, min_y=-1, max_y=1, a=-10, b=0):
        """
        Устанавливает позицию графика на холсте.

        row - номер строки для размещения графика (по умолчанию 0).
        column - номер столбца для размещения графика (по умолчанию 0).
        min_y - минимальное значение оси Y (по умолчанию -1).
        max_y - максимальное значение оси Y (по умолчанию 1).
        a - начальное значение оси X (по умолчанию -10).
        b - конечное значение оси X (по умолчанию 0).
        """
        self.a = a
        self.b = b
        self.ax.set_xlim([a, b])
        self.ax.set_ylim([min_y, max_y])

        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=column, row=row, padx=2, pady=2)

    def set_style(
        self,
        face_color=LIGHT_GREY,
        bg_color=DARK_GREY,
        line_color=ACCENT_COLOR,
        text_color=ACCENT_COLOR,
        font_size=6,
        title_font_size=8,
        font_family="serif",
    ):
        """
        Устанавливает стиль графика.

        face_color - цвет фона графика (по умолчанию LIGHT_GREY).
        bg_color - цвет фона холста (по умолчанию DARK_GREY).
        line_color - цвет линии графика (по умолчанию ACCENT_COLOR).
        text_color - цвет текста на графике (по умолчанию ACCENT_COLOR).
        font_size - размер шрифта меток на графике (по умолчанию 6).
        title_font_size - размер шрифта заголовка графика (по умолчанию 8).
        font_family - семейство шрифта для текста на графике (по умолчанию 'serif').
        """
        self.ax.set_facecolor(face_color)
        self.line.set_color(line_color)
        self.fig.set_facecolor(bg_color)
        self.ax.title.set_color(text_color)
        self.ax.xaxis.label.set_color(text_color)
        self.ax.yaxis.label.set_color(text_color)
        self.ax.tick_params(axis="both", colors=text_color, labelsize=font_size)
        self.ax.title.set_fontsize(title_font_size)
        self.ax.xaxis.label.set_fontsize(font_size)
        self.ax.yaxis.label.set_fontsize(font_size)
        self.ax.title.set_fontfamily(font_family)
        self.ax.xaxis.label.set_fontfamily(font_family)
        self.ax.yaxis.label.set_fontfamily(font_family)
        self.canvas.draw()

    def update_plot(self):
        """
        Обновляет данные на графике.
        """
        x = np.linspace(self.a, self.b, self.maxlen)

        self.line.set_xdata(x)
        self.line.set_ydata(self.stream(self.channel, self.maxlen))

        self.ax.draw_artist(self.ax.patch)
        self.ax.draw_artist(self.line)

        self.canvas.blit(self.ax.bbox)

    def update_fft(self, length):
        """
        Обновляет данные на графике с использованием преобразования Фурье.

        length - длина данных для преобразования Фурье.
        """
        x = np.fft.fftfreq(len(self.stream(self.channel, length)), 0.004)

        self.line.set_xdata(x)
        self.line.set_ydata(self.stream(self.channel, length))

        self.ax.draw_artist(self.ax.patch)
        self.ax.draw_artist(self.line)

        self.canvas.blit(self.ax.bbox)
