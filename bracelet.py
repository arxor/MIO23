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
    data = []

    def __init__(self):
        for _ in range(NUM_SIGNALS):
            self.data.append(deque([0] * 1000, maxlen=1000))
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

    def connect(self):
        if not self.serial.is_open:
            print("Подключение...")
            try:
                self.serial.open()
                print("Подключено успешно!")
            except serial.SerialException:
                print("Не удалось подключиться к браслету!")

    def disconnect(self):
        if self.serial.is_open:
            try:
                self.serial.close()
            except serial.SerialException:
                pass

    @staticmethod
    def get_ports():
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if not port.hwid.startswith("BTHENUM"):
                ports.remove(port)
            else:
                ports[ports.index(port)] = port.name
        print("Обнаружены порты: ", ports)
        return ports

    def read_data(self):
        next_call = time.time()
        self.gesture_counter = 0
        while self.serial.is_open:
            next_call += 0.02  # Следующий вызов через 20 мс

            if self.serial.in_waiting > 0:
                raw_data = self.serial.readline().decode().strip()
                all_data = [int(item) for item in re.findall(r'-?\d+', raw_data)]

                all_data += [0] * (9 - len(all_data))

                while len(all_data) > 0:
                    dta = all_data[:9]
                    all_data = all_data[9:]
                    processing.process(self)
                    for i in range(9):
                        if i == 3:
                            self.data[i].append(round(self.acc_x.process(
                                self.ma1.process(processing.normalize(dta[i], NORMALIZE_MIN[i], NORMALIZE_MAX[i]))), 3))
                        elif i == 4:
                            self.data[i].append(round(self.acc_y.process(
                                self.ma2.process(processing.normalize(dta[i], NORMALIZE_MIN[i], NORMALIZE_MAX[i]))), 3))
                        elif i == 5:
                            self.data[i].append(round(self.acc_z.process(
                                self.ma3.process(processing.normalize(dta[i], NORMALIZE_MIN[i], NORMALIZE_MAX[i]))), 3))
                        else:

                            self.data[i].append(round(processing.normalize(dta[i], NORMALIZE_MIN[i], NORMALIZE_MAX[i]), 3))

                    if self.gesture_rec_flag:
                        self.gesture_counter += 1
                        if self.gesture_counter == 100:
                            self.gesture_rec_flag = False
                            self.stop_recording()

            time_to_next_call = next_call - time.time()
            if time_to_next_call > 0:
                time.sleep(time_to_next_call)

    def start_reading(self):
        thr1 = threading.Thread(target=self.read_data)
        thr1.start()

    def start_recording(self):
        self.gesture_rec_flag = True

    def stop_recording(self):
        self.gesture_rec_flag = False
        Jesture.selected_gesture.gesture["data"].append([list(queue)[-self.gesture_counter:] for queue in self.data])
        Jesture.selected_gesture.label_gesture()
        print(Jesture.selected_gesture.gesture["data"])
        self.gesture_counter = 0

    @classmethod
    def get_data(cls, channel, n):
        return list(cls.data[channel])[-n:]
