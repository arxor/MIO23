import tkinter
import sys
import processing
from plot import *
from config import *
from recognition import Jesture
import tkinter as tk
from tkinter import ttk, StringVar


class Application(tk.Tk):
    def __init__(self, bracelet):
        tk.Tk.__init__(self)

        self.bracelet = bracelet

        self.set_initial_configuration()
        self.set_style()

        self.control_frame = self.create_control_frame()
        self.plot_frame = self.create_plot_frame()
        console = Console(self, row=1, column=0, columnspan=2)

        self.create_control_elements(self.control_frame)
        self.create_plot_elements(self.plot_frame)

    def set_initial_configuration(self):
        Jesture.load_gestures()
        if len(Jesture.gestures):
            Jesture.selected_gesture = Jesture.gestures[-1]

        self.title(WINDOW_TITLE)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = int(screen_width / WINDOWSIZE_DIVIDER)
        window_height = int(screen_height / WINDOWSIZE_DIVIDER)

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2) - 50

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(False, False)
        self.configure(background=LIGHT_GREY)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_control_frame(self):
        control_frame = ttk.Frame(self, style='Custom.TFrame')
        control_frame.grid(row=0, column=0, sticky="nsew")
        return control_frame

    def create_plot_frame(self):
        plot_frame = ttk.Frame(self, style='Custom.TFrame')
        plot_frame.grid(row=0, column=1, sticky="nsew")
        return plot_frame

    def create_control_elements(self, control_frame):
        ttk.Button(self.control_frame, text="Подключиться", command=self.connect, style='Custom.TButton').grid(row=0,
                                                                                                               column=1)
        ttk.Button(self.control_frame, text="Начать запись", command=lambda: self.bracelet.start_recording(),
                   style='Custom.TButton').grid(row=0, column=2, sticky="nsew")
        ttk.Button(self.control_frame, text="Окончить запись", command=self.bracelet.stop_recording,
                   style='Custom.TButton').grid(row=0, column=3, sticky="nsew")
        ttk.Button(self.control_frame, text="Обучить модель", command=self.prep, style='Custom.TButton').grid(row=0,
                                                                                                          column=4, sticky="nsew")
        ttk.Button(self.control_frame, text="Удалить жест", command=self.del_gesture, style='Custom.TButton').grid(
            row=3, column=2, pady=10, sticky="nsew")
        ttk.Button(self.control_frame, text="Создать", command=self.new_gesture, style='Custom.TButton').grid(row=4,
                                                                                                              column=2, sticky="nsew")

        # Создание выпадающего списка com портов
        selected_com_port = StringVar()
        selected_com_port.set("Выберите порт")
        option_menu = ttk.Combobox(self.control_frame, state="readonly", textvariable=selected_com_port,
                                   values=self.bracelet.get_ports(), style="Custom.TCombobox", width=14)
        option_menu.bind("<<ComboboxSelected>>", lambda a: self.change_port(selected_com_port))
        option_menu.grid(row=0, column=0, sticky="nsew")

        # Создание таблиц
        self.table1 = Table(self.control_frame, self.convert_gestures_data_for_table(),
                            ['Номер жеста', 'Название жеста', 'Число записей'], row=1, column=1)
        self.table2 = Table(self.control_frame, self.get_gesture_recordings_list(Jesture.selected_gesture),
                            columns=["Номер записи", "Длина записи"], row=5, column=1)

        # Создание элементов управления для выбора и создания жестов
        ttk.Label(self.control_frame, text="Выберите жест: ", style='Custom.TLabel').grid(row=3, column=0)
        ttk.Label(self.control_frame, text="Новый жест:", style='Custom.TLabel').grid(row=4, column=0)
        self.new_gesture_entry = ttk.Entry(self.control_frame, style='Custom.TEntry',width=12)
        self.new_gesture_entry.grid(row=4, column=1)

        self.selected_gesture = StringVar()
        self.selected_gesture.set("")
        self.selected_gesture.trace("w", self.select_gesture)

        self.gesture_names = self.convert_gestures_data_for_table()[1]
        if not self.gesture_names:  # если нет ни одного жеста
            self.gesture_names.append(" ")

        self.opt_menu_gesture = ttk.Combobox(self.control_frame, state="readonly", textvariable=self.selected_gesture,
                                             values=self.gesture_names, style="Custom.TCombobox", width=10)
        self.update_option_menu()
        self.opt_menu_gesture.grid(row=3, column=1)

        # Создание кругов вероятности
        self.circle_frame = ttk.Frame(self.control_frame, style='Custom.TFrame')
        self.circle_frame.grid(row=8, column=0, columnspan=4, rowspan=2, sticky="nsew", pady=30)
        self.circles = [ProbabilityCircle(self.circle_frame, probability=0, name="NO")]
        self.circles[0].grid(row=0, column=0)

    def create_plot_elements(self, plot_frame):
        # графики, размещенные в plot_frame
        self.plots = []
        for i in range(NUM_SIGNALS):
            if i <= 8:
                self.plots.append(Plot(plot_frame, self.bracelet.get_data, i, CHANNELS[i]))
                self.plots[i].set_pos(row=i // 3 + 2, column=i % 3)

            else:
                self.plots.append(Plot(plot_frame, self.bracelet.get_data, i, CHANNELS[i], fft=True))
                self.plots[i].set_pos(row=i // 3 + 2, column=i % 3, min_y=0, max_y=50, a=0, b=150)

    def set_style(self):
        style = ttk.Style(self)

        style.theme_create('Custom', parent='alt',
                           settings={
                               'TCombobox':
                                   {
                                       'configure':
                                           {
                                               'selectbackground': ACCENT_COLOR,
                                               'fieldbackground': LIGHT_GREY,
                                               'background': LIGHT_GREY,
                                               'foreground': ACCENT_COLOR
                                           }
                                   },
                               'TButton':
                                   {
                                       'configure':
                                           {
                                               'background': LIGHT_GREY,
                                               'foreground': ACCENT_COLOR
                                           },
                                       'map':
                                           {
                                               'background': [('active', DARK_GREY)]
                                           }
                                   },
                               'TFrame':
                                   {
                                       'configure':
                                           {
                                               'background': DARK_GREY
                                           }
                                   },
                               'TEntry':
                                   {
                                       'configure':
                                           {
                                               'fieldbackground': DARK_GREY,
                                               'foreground': ACCENT_COLOR
                                           }
                                   },
                               'TLabel':
                                   {
                                       'configure':
                                           {
                                               'background': DARK_GREY,
                                               'foreground': ACCENT_COLOR
                                           }
                                   }
                           }
                           )
        style.theme_use('Custom')

    def connect(self):
        self.bracelet.connect()
        if self.bracelet.serial.is_open:
            self.bracelet.start_reading()
            self.interrupt()

    def change_port(self, selected_com_port):
        self.bracelet.serial.port = selected_com_port.get()

    def on_closing(self):
        # Действия при закрытии окна
        Jesture.save_to_file()
        print("Закрытие приложения.")
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

    def update_option_menu(self):
        if not self.gesture_names:
            self.gesture_names.append(" ")
            self.opt_menu_gesture.config(state="disabled")
        else:
            if len(Jesture.gestures) >= 1 and " " in self.gesture_names:
                self.gesture_names.remove(" ")
                self.opt_menu_gesture.config(state="normal")
        self.opt_menu_gesture['values'] = self.gesture_names
        self.opt_menu_gesture.current(0)  # Если вы хотите установить первый элемент из списка в качестве выбранного значения

    def new_gesture(self):
        name = self.new_gesture_entry.get()
        if Jesture.check_name(name):
            print("Такой жест уже существует")
        else:
            Jesture.selected_gesture = Jesture(name)
            self.selected_gesture.set(name)
            self.gesture_names.append(Jesture.selected_gesture.gesture["name"])
            self.update_option_menu()
            self.table1.update_table(self.convert_gestures_data_for_table())

    def del_gesture(self):
        if len(Jesture.gestures):
            gesture_name = Jesture.selected_gesture.gesture["name"]
            Jesture.delete_gesture(Jesture.selected_gesture)

            if gesture_name in self.gesture_names:
                self.gesture_names.remove(gesture_name)
            if len(self.gesture_names):
                self.selected_gesture.set(self.gesture_names[0])
            else:
                self.selected_gesture.set("")
            self.update_option_menu()
            self.table1.update_table(self.convert_gestures_data_for_table())
        else:
            print("Нет жестов для удаления.")

    def select_gesture(self, name=None, index=None, mode=None):
        selected_name = self.selected_gesture.get()
        for gesture in Jesture.gestures:
            if gesture.name == selected_name:
                Jesture.selected_gesture = gesture
                break
        self.table2.update_table(self.get_gesture_recordings_list(Jesture.selected_gesture))

    def convert_gestures_data_for_table(self):
        gestures = Jesture.gestures
        if len(gestures):
            gesture_ids = [gesture.gesture["index"] for gesture in gestures]
            gesture_names = [gesture.gesture["name"] for gesture in gestures]
            gesture_recordings_num = [len([gesture.gesture["data"]]) if gesture.gesture["data"] else 0 for gesture in gestures]
        else:
            gesture_ids = []
            gesture_names = []
            gesture_recordings_num = []
        return [gesture_ids, gesture_names, gesture_recordings_num]

    def get_gesture_recordings_list(self, gesture):
        if len(Jesture.gestures):
            return [range(0, len([gesture.gesture['data']])), [len(channel) for channel in gesture.gesture["data"]]]
        else:
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
        self.create_rectangle(0, 0, self.size, self.size, fill=color)

        text = f"{self.probability:.2f}"
        self.text_id = self.create_text(self.size // 2, self.size // 2, text=text)

        name_text = self.create_text(self.size // 2, self.size - 10, text=self.name)


class Table:
    def __init__(self, master, data, columns, row, column):
        self.master = master
        self.data = data
        self.columns = columns

        self.frame = ttk.Frame(master, style="Custom.TFrame")
        self.frame.grid(row=row, column=column, columnspan=4, rowspan=2, sticky="nsew", pady=20)

        self.update_table(self.data)

    def update_table(self, data):
        self.data = list(zip(*data))  # Transpose data

        for widget in self.frame.winfo_children():
            widget.destroy()

        for i, column in enumerate(self.columns):
            ttk.Label(self.frame, text=column, style="Custom.TLabel").grid(row=0, column=i, padx=5)

        for i, item in enumerate(self.data):
            for j, d in enumerate(item):
                ttk.Label(self.frame, text=d, style="Custom.TLabel").grid(row=i + 1, column=j, padx=5)


class Console(tk.Text):
    def __init__(self, master=None, **kwargs):
        row = kwargs.pop('row', None)
        column = kwargs.pop('column', None)
        columnspan = kwargs.pop('columnspan', None)
        tk.Text.__init__(self, master, height=6, background=LIGHT_GREY, foreground=ACCENT_COLOR, **kwargs)
        sys.stdout = self

        self.grid(row=row, column=column, columnspan=columnspan, sticky="nsew")

    def write(self, txt):
        self.insert(tk.END, str(txt))
        self.see(tk.END)
        self.update_idletasks()

    def flush(self):
        pass
