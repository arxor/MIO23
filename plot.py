import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from config import *
from processing import *


class Plot:
    plots = []

    def __init__(self, master, stream, channel, title="chart", maxlen=50, fft=False):
        # Создаем фигуру и оси
        self.fig, self.ax = plt.subplots(figsize=PLOT_FIGSIZE)
        self.plots.append(self)
        self.stream = stream
        self.ax.set_title(title)
        self.ax.grid(True, linestyle='--', linewidth=0.5, color='gray')
        # Увеличение числа горизонтальных линий сетки до 10


        # ????
        for tick in self.ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(PLOT_FONTSIZE)  # установка размера шрифта на 10 для меток на оси x
        for tick in self.ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(PLOT_FONTSIZE)
        self.line, = self.ax.plot([], [], lw=0.5)

        self.fft = fft
        self.maxlen = maxlen
        self.channel = channel

        # Создаем холст для отображения графика
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)

    def set_pos(self, row=0, column=0, min_y=-1, max_y=1, a=-10, b=0):
        self.a = a
        self.b = b
        self.ax.set_xlim([a, b])
        self.ax.set_ylim([min_y, max_y])
        self.ax.yaxis.set_ticks(np.linspace(self.ax.get_ylim()[0], self.ax.get_ylim()[1], 11))
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
        x = np.linspace(self.a, self.b, self.maxlen)

        self.line.set_xdata(x)
        self.line.set_ydata(self.stream(self.channel, self.maxlen))

        self.ax.draw_artist(self.ax.patch)
        self.ax.draw_artist(self.line)

        self.canvas.blit(self.ax.bbox)

    def update_fft(self, length):
        x = np.fft.fftfreq(len(self.stream(self.channel, length)), 0.004)

        self.line.set_xdata(x)
        self.line.set_ydata(self.stream(self.channel, length))

        self.ax.draw_artist(self.ax.patch)
        self.ax.draw_artist(self.line)

        self.canvas.blit(self.ax.bbox)


