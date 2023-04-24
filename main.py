import tkinter as tk
from tkinter import StringVar

from bracelet import Bracelet
from gui import Plot
from config import *


def show_window(root):
    root.mainloop()


def change_port(bracelet, selected_com_port):
    bracelet.serial.port = selected_com_port.get()


def connect(bracelet):
    bracelet.connect()
    if bracelet.serial.is_open:
        Plot.start_plots()
    else:
        print(MESSAGE_CANT_CONNECT)


def on_closing():
    # Действия при закрытии окна
    print(MESSAGE_CLOSE_WINDOW)
    Plot.stop_plots()
    root.destroy()  # закрыть окно


def create_gui():
    # Создание экземпляра класса Bracelet
    bracelet = Bracelet()

    # Передача устройства в класс Plot
    Plot.set_bracelet(bracelet)

    # Создание главного окна
    root = tk.Tk()
    # Название главного окна
    root.title(WINDOW_TITLE)
    # Настройки положения и размеров окна
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = int(screen_width / WINDOWSIZE_DIVIDER)
    window_height = int(screen_height / WINDOWSIZE_DIVIDER)

    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2) - 50

    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    # При закрытии окна вызывать функцию on_closing
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Создание виджета Frame
    frame = tk.Frame(root)
    frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    # Создание кнопки для подключения к устройству
    connect_button = tk.Button(frame, text=BUTTON_CONNECT,
                               command=lambda: connect(bracelet))

    # Создание выпадающего меню выбора ком-порта
    com_ports = bracelet.get_ports()
    selected_com_port = StringVar()
    selected_com_port.set(OPTIONMENU_COM_CHOOSE)

    if len(com_ports) == 0:
        option_menu = tk.OptionMenu(frame, selected_com_port, OPTIONMENU_NO_COM)
        option_menu.config(state='disabled')
        connect_button.config(state='disabled')
    else:
        option_menu = tk.OptionMenu(frame, selected_com_port, *com_ports,
                                    command=lambda a: change_port(bracelet, selected_com_port))

    # Создание графиков
    abp1 = Plot(root, PLOTTITLE_1, maxlen=50, time=1)
    abp2 = Plot(root, PLOTTITLE_2, maxlen=50, time=1)
    ref = Plot(root, PLOTTITLE_3, maxlen=500, time=10)
    ax = Plot(root, PLOTTITLE_4, maxlen=50, time=1)
    ay = Plot(root, PLOTTITLE_5, maxlen=50, time=1)
    az = Plot(root, PLOTTITLE_6, maxlen=50, time=1)
    gx = Plot(root, PLOTTITLE_7, maxlen=50, time=1)
    gy = Plot(root, PLOTTITLE_8, maxlen=50, time=1)
    gz = Plot(root, PLOTTITLE_9, maxlen=50, time=1)

    # Настройка положения виджетов в окне
    option_menu.grid(row=1, column=1)
    connect_button.grid(row=1, column=2)

    abp1.set_pos(row=2, column=1)
    abp2.set_pos(row=2, column=2)
    ref.set_pos(row=2, column=3, min_y=300, max_y=700)
    ax.set_pos(row=3, column=1, min_y=-16384, max_y=16383)
    ay.set_pos(row=3, column=2, min_y=-16384, max_y=16383)
    az.set_pos(row=3, column=3, min_y=-16384, max_y=16383)
    gx.set_pos(row=4, column=1, min_y=-16384, max_y=16383)
    gy.set_pos(row=4, column=2, min_y=-16384, max_y=16383)
    gz.set_pos(row=4, column=3, min_y=-16384, max_y=16383)

    return root


if __name__ == "__main__":
    root = create_gui()
    show_window(root)
