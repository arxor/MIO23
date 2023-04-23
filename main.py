import tkinter as tk
from tkinter import StringVar
from bracelet import Bracelet
from gui import Plot


def show_window(root):
    root.mainloop()


def change_port(bracelet, selected_com_port):
    bracelet.serial.port = selected_com_port.get()


def connect(bracelet, plot):
    bracelet.connect()
    if bracelet.serial.is_open:
        plot.generate_data()
    else:
        print("Не удалось подключиться к последовательному порту.")


def create_gui():
    bracelet = Bracelet()
    root = tk.Tk()
    root.title("Электромиографический браслет")
    plot = Plot(root)
    plot.bracelet = bracelet

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = int(screen_width / 1.5)
    window_height = int(screen_height / 1.5)

    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    frame = tk.Frame(root)
    frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    connect_button = tk.Button(frame, text="Подключиться", command=lambda: connect(bracelet, plot))
    connect_button.grid(column=0, row=0)

    com_ports = bracelet.get_ports()

    selected_com_port = StringVar()
    selected_com_port.set("Выберите порт")

    option_menu = tk.OptionMenu(frame, selected_com_port, *com_ports,
                                command=lambda v: change_port(bracelet, selected_com_port))

    option_menu.grid(column=1, row=0)
    return root


if __name__ == "__main__":
    root = create_gui()
    show_window(root)
