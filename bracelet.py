"""
Модуль, содержащий класс Bracelet, который используется для подключения, чтения данных и обработки данных
с браслета через последовательный порт.

Также включает в себя функции записи движений для жестов.
"""

import time

import serial
import serial.tools.list_ports
import re

import processing
from config import *
from collections import deque
from recognition import Jesture
import threading


class Bracelet:
    """
        Класс, представляющий браслет, подключенный через последовательный порт.
        Он обеспечивает подключение, чтение данных, их обработку и распознавание жестов.

        Атрибуты:
        data : список очередей, содержащих данные от браслета.
    """
    data = []

    def __init__(self):
        """
        Инициализация объекта Bracelet и экземпляров классов для обработки данных.
        """
        for _ in range(NUM_SIGNALS):
            self.data.append(deque([0] * 70, maxlen=70))
        self.serial = serial.Serial()
        self.serial.baudrate = COM_BAUD
        self.serial.port = None
        self.serial.timeout = COM_TIMEOUT
        self.gesture_rec_flag = False
        self.gesture_counter = 0

        self.acc_x = processing.Accelerometer()
        self.acc_y = processing.Accelerometer()
        self.acc_z = processing.Accelerometer()

        self.ma1 = processing.MovingAverage(3)
        self.ma2 = processing.MovingAverage(3)
        self.ma3 = processing.MovingAverage(3)

        self.ed1 = processing.EnvelopeDetector()
        self.ed2 = processing.EnvelopeDetector()

    def connect(self):
        """
        Подключение к браслету через последовательный порт.
        """
        if not self.serial.is_open:
            print("Подключение...")
            try:
                self.serial.open()
                print("Подключено успешно!")
            except serial.SerialException:
                print("Не удалось подключиться к браслету!")

    def disconnect(self):
        """
        Отключение от браслета, закрытие последовательного порта.
        """
        if self.serial.is_open:
            try:
                self.serial.close()
            except serial.SerialException:
                pass

    @staticmethod
    def get_ports():
        """
        Метод, возвращающий список доступных последовательных портов.

        Возвращает:
        list : Список доступных портов.
        """
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if not port.hwid.startswith("BTHENUM"):
                ports.remove(port)
            else:
                ports[ports.index(port)] = port.name
        print("Обнаружены порты: ", ports)
        return ports

    def read_data(self):
        """
        Чтение и обработка данных с браслета в реальном времени.
        Обработка включает в себя нормализацию, вычисление скользящего среднего, расчет разницы значений и детектор огибающей.
        """
        next_call = time.time()
        self.gesture_counter = 0
        while self.serial.is_open:
            next_call += 0.02

            if self.serial.in_waiting > 0:
                raw_data = self.serial.readline().decode().strip()
                all_data = [int(item) for item in re.findall(r'-?\d+', raw_data)]

                all_data += [0] * (9 - len(all_data))

                while len(all_data) > 0:
                    dta = all_data[:9]
                    all_data = all_data[9:]
                    processing.process(self)
                    for i in range(9):
                        if i == 0:
                            self.data[i].append(round(
                                self.ed1.process(processing.normalize(dta[i], NORMALIZE_MIN[i], NORMALIZE_MAX[i])), 1))
                        elif i == 1:
                            self.data[i].append(round(
                                self.ed2.process(processing.normalize(dta[i], NORMALIZE_MIN[i], NORMALIZE_MAX[i])), 1))
                        elif i == 3:
                            self.data[i].append(round(self.acc_x.process(
                                self.ma1.process(processing.normalize(dta[i], NORMALIZE_MIN[i], NORMALIZE_MAX[i]))), 1))
                        elif i == 4:
                            self.data[i].append(round(self.acc_y.process(
                                self.ma2.process(processing.normalize(dta[i], NORMALIZE_MIN[i], NORMALIZE_MAX[i]))), 1))
                        elif i == 5:
                            self.data[i].append(round(self.acc_z.process(
                                self.ma3.process(processing.normalize(dta[i], NORMALIZE_MIN[i], NORMALIZE_MAX[i]))), 1))
                        else:

                            self.data[i].append(
                                round(processing.normalize(dta[i], NORMALIZE_MIN[i], NORMALIZE_MAX[i]), 1))

                    if self.gesture_rec_flag:
                        self.gesture_counter += 1
                        if self.gesture_counter == 70:
                            self.gesture_rec_flag = False
                            self.stop_recording()

            time_to_next_call = next_call - time.time()
            if time_to_next_call > 0:
                time.sleep(time_to_next_call)

    def start_reading(self):
        """
        Запуск потока для чтения и обработки данных с браслета.
        """
        thr1 = threading.Thread(target=self.read_data)
        thr1.start()

    def start_recording(self):
        """
        Начало записи данных для распознавания жестов.
        """
        self.gesture_rec_flag = True

    def stop_recording(self):
        """
        Остановка записи данных и передача последнего сегмента данных в объект жеста для распознавания жестов.
        """
        self.gesture_rec_flag = False
        Jesture.selected_gesture.add_recording([list(queue)[-70:] for queue in self.data])
        self.gesture_counter = 0

    @classmethod
    def get_data(cls, channel, n):
        """
        Метод, возвращающий последние n элементов данных из заданного канала.

        Параметры:
        channel (int): номер канала для получения данных.
        n (int): количество элементов данных, которые следует вернуть.

        Возвращает:
        list : список последних n элементов данных.
        """
        return list(cls.data[channel])[-n:]
