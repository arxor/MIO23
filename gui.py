import tkinter as tk
from tkinter import StringVar

import processing
from plot import Plot
from config import *
from processing import *

class Application(tk.Tk):
    def __init__(self, bracelet):
        tk.Tk.__init__(self)

        # Создание экземпляра класса Bracelet
        self.bracelet = bracelet

        # Передача устройства в класс Plot
        Plot.set_bracelet(self.bracelet)

        # Название главного окна
        self.title(WINDOW_TITLE)

        # Настройки положения и размеров окна
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = int(screen_width / WINDOWSIZE_DIVIDER)
        window_height = int(screen_height / WINDOWSIZE_DIVIDER)

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2) - 50

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # При закрытии окна вызывать функцию on_closing
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Создание виджета Frame
        frame = tk.Frame(self)
        frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Создание кнопки для подключения к устройству
        connect_button = tk.Button(frame, text=BUTTON_CONNECT,
                                command=self.connect)

        # Создание выпадающего меню выбора ком-порта
        com_ports = self.bracelet.get_ports()
        selected_com_port = StringVar()
        selected_com_port.set(OPTIONMENU_COM_CHOOSE)

        if len(com_ports) == 0:
            option_menu = tk.OptionMenu(frame, selected_com_port, OPTIONMENU_NO_COM)
            option_menu.config(state='disabled')
            connect_button.config(state='disabled')
        else:
            option_menu = tk.OptionMenu(frame, selected_com_port, *com_ports,
                                        command=lambda a: self.change_port(selected_com_port))

        # Создание графиков

        self.abp1 = Plot(self, bracelet.get_abp1, PLOTTITLE_1, maxlen=50, time=1)
        self.abp2 = Plot(self, bracelet.get_abp2, PLOTTITLE_2, maxlen=50, time=1)
        self.ref = Plot(self, bracelet.get_ref, PLOTTITLE_3, maxlen=500, time=10)
        self.ax = Plot(self, bracelet.get_ax, PLOTTITLE_4, maxlen=50, time=1)
        self.ay = Plot(self, bracelet.get_ay, PLOTTITLE_5, maxlen=50, time=1)
        self.az = Plot(self, bracelet.get_az, PLOTTITLE_6, maxlen=50, time=1)
        self.gx = Plot(self, bracelet.get_gx, PLOTTITLE_7, maxlen=50, time=1)
        self.gy = Plot(self, bracelet.get_gy, PLOTTITLE_8, maxlen=50, time=1)
        self.gz = Plot(self, bracelet.get_gz, PLOTTITLE_9, maxlen=50, time=1)
        self.proceed_avg = Plot(self, processing.get_abp1_average, "middle 1", maxlen=50, time=1)

        # Настройка положения виджетов в окне
        option_menu.grid(row=1, column=1)
        connect_button.grid(row=1, column=2)

        self.abp1.set_pos(row=2, column=1)
        self.abp2.set_pos(row=2, column=2)
        self.ref.set_pos(row=2, column=3, min_y=300, max_y=700)
        self.ax.set_pos(row=3, column=1, min_y=-16384, max_y=16383)
        self.ay.set_pos(row=3, column=2, min_y=-16384, max_y=16383)
        self.az.set_pos(row=3, column=3, min_y=-16384, max_y=16383)
        self.gx.set_pos(row=4, column=1, min_y=-16384, max_y=16383)
        self.gy.set_pos(row=4, column=2, min_y=-16384, max_y=16383)
        self.gz.set_pos(row=4, column=3, min_y=-16384, max_y=16383)
        self.proceed_avg.set_pos(row=5, column=1)
        self.abp1.set_style(bg_color='white', line_color='orange', text_color='grey', font_family='fantasy')
        self.abp2.set_style()

    def connect(self):
        self.bracelet.connect()
        if self.bracelet.serial.is_open:
            self.bracelet.start_reading()
            self.interrupt()
            # Plot.start_plots()
        else:
            print(MESSAGE_CANT_CONNECT)

    def change_port(self, selected_com_port):
        self.bracelet.serial.port = selected_com_port.get()

    def on_closing(self):
        # Действия при закрытии окна
        print(MESSAGE_CLOSE_WINDOW)
        Plot.stop_plots()
        self.destroy()  # закрыть окно

    def interrupt(self):
        self.abp1.update_plot()
        self.abp2.update_plot()
        self.ref.update_plot()
        self.ax.update_plot()
        self.ay.update_plot()
        self.az.update_plot()
        self.gx.update_plot()
        self.gy.update_plot()
        self.gz.update_plot()
        self.proceed_avg.update_plot()
        self.after(15, self.interrupt)
