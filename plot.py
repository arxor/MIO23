from bracelet import Bracelet
import numpy as np
import time
from collections import deque
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
)

class plot:
    def __init__(self):
        self.bracelet = Bracelet()
        self.d1 = deque([0]*500, maxlen=500)
        self.x = np.linspace(-10, 0, 500)
        matplotlib.use('TkAgg')
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.figure_canvas = FigureCanvasTkAgg(self.figure)
        self.axes = self.figure.add_subplot()
        self.axes.plot(self.x, self.d1)
        self.figure_canvas.get_tk_widget().grid(column=3, row=1)

    def update(self, dy):
        start_time = time.time()

        self.d1.append(dy)
        self.axes.clear()
        #self.axes.plot(self.x, self.d1)
        #self.figure_canvas.draw()

        print("--- %s seconds ---" % (time.time() - start_time))


