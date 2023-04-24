import serial
import serial.tools.list_ports
import time

class Bracelet:
    def __init__(self):
        self.serial = serial.Serial()

        self.serial.baudrate = 57600
        self.serial.port = None
        self.serial.timeout = 0.05

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

    def get_data(self):
        if not self.serial.is_open:
            self.connect()
        return self.serial.readline().decode().strip()

