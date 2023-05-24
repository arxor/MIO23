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
    data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    abp1 = deque([0] * 1000, maxlen=1000)
    abp2 = deque([0] * 1000, maxlen=1000)
    ref = deque([0] * 1000, maxlen=1000)
    ax = deque([0] * 1000, maxlen=1000)
    ay = deque([0] * 1000, maxlen=1000)
    az = deque([0] * 1000, maxlen=1000)
    gx = deque([0] * 1000, maxlen=1000)
    gy = deque([0] * 1000, maxlen=1000)
    gz = deque([0] * 1000, maxlen=1000)

    def __init__(self):
        self.serial = serial.Serial()
        self.serial.baudrate = COM_BAUD
        self.serial.port = None
        self.serial.timeout = COM_TIMEOUT
        self.gesture_rec_flag = False
        Jesture.set_bracelet(self)

        self.env1 = processing.EnvelopeDetector()
        self.env2 = processing.EnvelopeDetector()

        self.acc_x = processing.Accelerometer()
        self.acc_y = processing.Accelerometer()
        self.acc_z = processing.Accelerometer()

        self.n0 = processing.StreamingNormalization(50)
        self.n1 = processing.StreamingNormalization(50)
        self.n2 = processing.StreamingNormalization(50)
        self.n3 = processing.StreamingNormalization(50)
        self.n4 = processing.StreamingNormalization(50)
        self.n5 = processing.StreamingNormalization(50)
        self.n6 = processing.StreamingNormalization(50)
        self.n7 = processing.StreamingNormalization(50)
        self.n8 = processing.StreamingNormalization(50)

    def connect(self):
        if not self.serial.is_open:
            try:
                self.serial.open()
            except serial.SerialException:
                pass

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
        print(ports)
        return ports

    def read_data(self):
        next_call = time.time()
        while self.serial.is_open:
            next_call += 0.02  # Следующий вызов через 20 мс

            if self.serial.in_waiting > 0:
                raw_data = self.serial.readline().decode().strip()
                all_data = [int(item) for item in re.findall(r'-?\d+', raw_data)]

                all_data += [0] * (NUM_CHANNELS - len(all_data))

                while len(all_data) > 0:

                    self.data = all_data[:NUM_CHANNELS]  # Take the first NUM_CHANNELS numbers
                    all_data = all_data[NUM_CHANNELS:]  # Leave the rest

                    if self.gesture_rec_flag:
                        Jesture.items[-1].gesture_temp.append(self.data)
                    self.abp1.append(self.n0.normalize(self.data[0] - self.data[2]))
                    self.abp2.append(self.n1.normalize(self.data[1] - self.data[2]))
                    self.ref.append(self.data[2])
                    self.ax.append(self.n3.normalize(self.data[3]))
                    self.ay.append(self.n4.normalize(self.data[4]))
                    self.az.append(self.n5.normalize(self.data[5]))
                    self.gx.append(self.n6.normalize(self.data[6]))
                    self.gy.append(self.n7.normalize(self.data[7]))
                    self.gz.append(self.n8.normalize(self.data[8]))
                    processing.process(self)

            time_to_next_call = next_call - time.time()
            if time_to_next_call > 0:
                time.sleep(time_to_next_call)

    def start_reading(self):
        thr1 = threading.Thread(target=self.read_data)
        thr1.start()

    def start_recording(self):
        j = Jesture()
        self.gesture_rec_flag = True

    def stop_recording(self):
        self.gesture_rec_flag = False
        if len(Jesture.items) == 0:
            print("Нет жестов")
        else:
            Jesture.items[-1].convert()
            print(Jesture.items[-1].abp1)
            print(Jesture.items[-1].gesture_temp)

    @classmethod
    def get_abp1(cls, n):
        return list(cls.abp1)[-n:]

    @classmethod
    def get_abp2(cls, n):
        return list(cls.abp2)[-n:]

    @classmethod
    def get_ref(cls, n):
        return list(cls.ref)[-n:]

    @classmethod
    def get_ax(cls, n):
        return list(cls.ax)[-n:]

    @classmethod
    def get_ay(cls, n):
        return list(cls.ay)[-n:]

    @classmethod
    def get_az(cls, n):
        return list(cls.az)[-n:]

    @classmethod
    def get_gx(cls, n):
        return list(cls.gx)[-n:]

    @classmethod
    def get_gy(cls, n):
        return list(cls.gy)[-n:]

    @classmethod
    def get_gz(cls, n):
        return list(cls.gz)[-n:]
