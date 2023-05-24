import time

import numpy
import serial
import serial.tools.list_ports

import processing
from config import *
from collections import deque

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

    def connect(self):
        if not self.serial.is_open:
            try:
                self.serial.open()
            except:
                pass

    def get_ports(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if not port.hwid.startswith("BTHENUM"):
                ports.remove(port)
            else:
                ports[ports.index(port)] = port.name
        print(ports)
        return ports

    def read_data(self):
        while self.serial.is_open:
            self.data = self.serial.readline().decode().strip().split()
            for i in range(len(self.data)):
                if all(char in '-0123456789' for char in self.data[i]):
                    self.data[i] = int(self.data[i])
            while len(self.data) < 9:
                self.data.append(0)
            print(self.data)
            self.abp1.append(self.data[0])
            self.abp2.append(self.data[1])
            self.ref.append(self.data[2])
            self.ax.append(self.data[3])
            self.ay.append(self.data[4])
            self.az.append(self.data[5])
            self.gx.append(self.data[6])
            self.gy.append(self.data[7])
            self.gz.append(self.data[8])
            processing.process(self)
            time.sleep(0.01)

    def start_reading(self):
        thr1 = threading.Thread(target=self.read_data)
        thr1.start()

    def get_abp1(self, n):
        return list(self.abp1)[-n:]

    def get_abp2(self, n):
        return list(self.abp2)[-n:]

    def get_ref(self, n):
        return list(self.ref)[-n:]

    def get_ax(self, n):
        return list(self.ax)[-n:]

    def get_ay(self, n):
        return list(self.ay)[-n:]

    def get_az(self, n):
        return list(self.az)[-n:]

    def get_gx(self, n):
        return list(self.gx)[-n:]

    def get_gy(self, n):
        return list(self.gy)[-n:]

    def get_gz(self, n):
        return list(self.gz)[-n:]
