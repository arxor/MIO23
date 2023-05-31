import processing
from plot import *
from config import *
from recognition import Jesture
import tkinter as tk
from tkinter import StringVar


class Application(tk.Tk):
    def __init__(self, bracelet):
        tk.Tk.__init__(self)

        # Создание экземпляра класса Bracelet
        self.bracelet = bracelet

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
        # Создание кнопок записи жестов
        start_recording_button = tk.Button(frame, text="Начать запись", command=self.bracelet.start_recording)
        stop_recording_button = tk.Button(frame, text="Окончить запись", command=self.bracelet.stop_recording)

        rec_button = tk.Button(frame, text="Распознать", command=self.rec)

        self.plots = []

        # Создание графиков
        for i in range(NUM_SIGNALS):
            if i <= 8:
                self.plots.append(Plot(self, bracelet.get_data, i, CHANNELS[i]))
                self.plots[i].set_pos(row=i // 3 + 2, column=i % 3)

            else:
                self.plots.append(Plot(self, bracelet.get_data, i, CHANNELS[i], fft=True))
                self.plots[i].set_pos(row=i // 3 + 2, column=i % 3, min_y=0, max_y=50, a=0, b=150)



        # Настройка положения виджетов в окне
        option_menu.grid(row=0, column=0)
        connect_button.grid(row=0, column=1)

        start_recording_button.grid(row=0, column=2)
        stop_recording_button.grid(row=0, column=3)

        rec_button.grid(row=0, column=4)

    def connect(self):
        self.bracelet.connect()
        if self.bracelet.serial.is_open:
            self.bracelet.start_reading()
            self.interrupt()
        else:
            print(MESSAGE_CANT_CONNECT)

    def change_port(self, selected_com_port):
        self.bracelet.serial.port = selected_com_port.get()

    def on_closing(self):
        # Действия при закрытии окна
        print(MESSAGE_CLOSE_WINDOW)
        self.bracelet.disconnect()
        self.destroy()  # закрыть окно

    def interrupt(self):
        for i in range(11):
            if i <= 8:
                self.plots[i].update_plot()
            else:
                self.plots[i].update_fft(self.bracelet.gesture_counter)
        # self.proceed_avg.update_plot()
        self.after(15, self.interrupt)
    def rec(self):
        Jesture.recognize(Jesture)
        self.after(20, self.rec)
