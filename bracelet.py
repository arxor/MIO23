import time

import numpy
import serial
import serial.tools.list_ports

import processing
from config import *

import threading

class Bracelet:
    data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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
            processing.process(self)
            time.sleep(0.01)

    def start_reading(self):
        thr1 = threading.Thread(target=self.read_data)
        thr1.start()

    def get_abp1(self):
        return self.data[0]

    def get_abp2(self):
        return self.data[1]

    def get_ref(self):
        return self.data[2]

    def get_ax(self):
        return self.data[3]

    def get_ay(self):
        return self.data[4]

    def get_az(self):
        return self.data[5]

    def get_gx(self):
        return self.data[6]

    def get_gy(self):
        return self.data[7]

    def get_gz(self):
        return self.data[8]
