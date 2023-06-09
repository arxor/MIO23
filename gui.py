import tkinter

import processing
from plot import *
from config import *
from recognition import Jesture
import tkinter as tk
from tkinter import ttk, StringVar


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
        self.resizable(False, False)

        # При закрытии окна вызывать функцию on_closing
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Создание фрейма для элементов управления
        control_frame = tk.Frame(self)
        control_frame.grid(row=0, column=0, sticky="nsew")

        # Создание фрейма для графиков
        plot_frame = tk.Frame(self)
        plot_frame.grid(row=0, column=1, sticky="nsew")

        # Элементы управления, размещенные в control_frame
        connect_button = tk.Button(control_frame, text=BUTTON_CONNECT, command=self.connect)
        com_ports = self.bracelet.get_ports()
        selected_com_port = StringVar()
        selected_com_port.set(OPTIONMENU_COM_CHOOSE)

        option_menu = tk.OptionMenu(control_frame, selected_com_port, *com_ports,
                                    command=lambda a: self.change_port(selected_com_port))
        start_recording_button = tk.Button(control_frame, text="Начать запись",
                                           command=lambda: self.bracelet.start_recording(self.choosen_gesture))
        stop_recording_button = tk.Button(control_frame, text="Окончить запись", command=self.bracelet.stop_recording)
        rec_button = tk.Button(control_frame, text="Распознать", command=self.prep)

        # Расположение элементов управления
        option_menu.grid(row=0, column=0)
        connect_button.grid(row=0, column=1)
        start_recording_button.grid(row=0, column=2)
        stop_recording_button.grid(row=0, column=3)
        rec_button.grid(row=0, column=4)

        gestures = Jesture.get_gestures()

        lb_choose_gesture = tk.Label(control_frame, text="Выберите жест: ")
        lb_choose_gesture.grid(row=3, column=0)

        self.selected_gesture = StringVar()
        self.selected_gesture.set("___")

        self.gesture_names = self.convert_gestures_data_for_table()[1]
        self.opt_menu_gesture = tk.OptionMenu(control_frame, self.selected_gesture, self.gesture_names)
        self.opt_menu_gesture.grid(row=3, column=1)

        self.table1 = Table(control_frame, self.convert_gestures_data_for_table(),
                            ['ID', 'Название жеста', 'Число записей'], row=1, column=0)

        del_gesture_button = tk.Button(control_frame, text="Удалить жест",
                                       command=lambda: (
                                           Jesture.delete_gesture(
                                               self.selected_gesture.get()),
                                           self.table1.update_table(self.convert_gestures_data_for_table())))

        del_gesture_button.grid(row=3, column=3)

        choose_gesture_button = tk.Button(control_frame, text="Выбрать", command=lambda: (
        self.select_gesture(), self.table2.update_table(self.get_gesture_recordings_list())))
        choose_gesture_button.grid(row=3, column=2)

        self.choosen_gesture = None

        tk.Label(control_frame, text="Новый жест:").grid(row=4, column=0)
        new_gesture_entry = tk.Entry(control_frame)
        new_gesture_entry.grid(row=4, column=1)
        new_gesture_button = tk.Button(control_frame, text="Создать", command=lambda: (
            Jesture.add_gesture(new_gesture_entry.get()),
            self.table1.update_table(self.convert_gestures_data_for_table()),
            self.selected_gesture.set(self.selected_gesture)
        ))
        new_gesture_button.grid(row=4, column=2)

        self.circle_frame = tk.Frame(control_frame)
        self.circle_frame.grid(row=8, column=0, columnspan=4, rowspan=2)
        self.circles = []
        self.circles.append(ProbabilityCircle(self.circle_frame, probability=0, name="NO"))
        self.circles[0].grid(row=0, column=0)

        self.table2 = Table(control_frame, self.get_gesture_recordings_list(self.selected_gesture), columns=["ID"],
                            row=5, column=0)

        # графики, размещенные в plot_frame
        self.plots = []
        for i in range(NUM_SIGNALS):
            if i <= 8:
                self.plots.append(Plot(plot_frame, bracelet.get_data, i, CHANNELS[i]))
                self.plots[i].set_pos(row=i // 3 + 2, column=i % 3)

            else:
                self.plots.append(Plot(plot_frame, bracelet.get_data, i, CHANNELS[i], fft=True))
                self.plots[i].set_pos(row=i // 3 + 2, column=i % 3, min_y=0, max_y=50, a=0, b=150)

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
        self.after(15, self.interrupt)

    def prep(self):
        Jesture.prepare_model()
        gestures = Jesture.get_gestures()
        for i in range(0, len(gestures)):
            self.circles.append(ProbabilityCircle(self.circle_frame, probability=0, name=gestures[i]['name']))
            self.circles[i + 1].grid(row=(i + 1) // 4, column=(i + 1) % 4)
        self.rec()

    def rec(self):
        Jesture.recognize(self.bracelet.data)
        for i in range(0, len(self.circles)):
            self.circles[i].update_probability(Jesture.prob[i])
        self.after(100, self.rec)

    def select_gesture(self):
        self.choosen_gesture = self.selected_gesture.get()

    def convert_gestures_data_for_table(self):
        gestures = Jesture.get_gestures()
        if len(gestures):
            gesture_ids = [gesture["index"] for gesture in gestures]
            gesture_names = [gesture["name"] for gesture in gestures]
            gesture_recordings_num = [len(gesture["data"]) for gesture in gestures]
        else:
            gesture_ids = []
            gesture_names = []
            gesture_recordings_num = []
        return [gesture_ids, gesture_names, gesture_recordings_num]

    def get_gesture_recordings_list(self, gesture_name):
        gestures = Jesture.get_gestures()
        for i, gesture in enumerate(gestures):
            if gesture['name'] == gesture_name:
                return [range(0, len(gesture['data'])),gesture['data']]
        else:
            print("Gesture not found.")
            return []


class ProbabilityCircle(tk.Canvas):
    def __init__(self, master, probability, size=100, name=""):
        super().__init__(master, width=size, height=size)
        self.probability = probability
        self.size = size
        self.name = name
        self.text_id = None
        self.update_color()

    def update_probability(self, probability):
        self.probability = probability
        self.update_color()

    def update_color(self):
        # Преобразование вероятности в диапазон 0 - 255 для RGB
        green = int(self.probability * 255)
        red = 255 - green
        blue = 0

        # Преобразование RGB в шестнадцатеричную строку
        color = '#%02x%02x%02x' % (red, green, blue)

        self.delete("all")
        self.create_oval(0, 0, self.size, self.size, fill=color)

        text = f"{self.probability:.2f}"
        self.text_id = self.create_text(self.size // 2, self.size // 2, text=text)

        name_text = self.create_text(self.size // 2, self.size - 10, text=self.name)


class Table:
    def __init__(self, master, data, columns, row, column):
        self.master = master
        self.data = data
        self.columns = columns

        self.frame = tk.Frame(master)
        self.frame.grid(row=row, column=column, columnspan=4, rowspan=2, sticky="nsew", pady=10)

        self.update_table(self.data)

    def update_table(self, data):
        self.data = list(zip(*data))  # Transpose data

        for widget in self.frame.winfo_children():
            widget.destroy()

        for i, column in enumerate(self.columns):
            tk.Label(self.frame, text=column).grid(row=0, column=i)

        for i, item in enumerate(self.data):
            for j, d in enumerate(item):
                tk.Label(self.frame, text=d).grid(row=i + 1, column=j)
