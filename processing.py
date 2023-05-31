import numpy as np
from scipy.signal import hilbert
from config import *
from collections import deque

window_size = 10
abp1_average = None
abp1_fft = None
abp2_fft = None
idx = 0
vals = np.zeros(window_size)


def process(bracelet):
    bracelet.data[9] = np.abs(np.fft.fft(np.array(list(bracelet.get_data(0, bracelet.gesture_counter)))))
    bracelet.data[10] = np.abs(np.fft.fft(np.array(list(bracelet.get_data(1, bracelet.gesture_counter)))))

class EnvelopeDetector:
    def __init__(self, buffer_size=10):
        self.buffer = []
        self.buffer_size = buffer_size

    def process(self, value):
        # Добавляем новое значение в буфер
        self.buffer.append(value)

        # Если буфер превысил максимальный размер, удаляем самое старое значение
        if len(self.buffer) > self.buffer_size:
            self.buffer = self.buffer[1:]

        # Применяем фильтр Хилберта к буферу
        analytic_signal = hilbert(self.buffer)

        # Вычисляем огибающую как амплитуду аналитического сигнала
        envelope = np.abs(analytic_signal)

        # Возвращаем последнее значение огибающей
        return envelope[-1]


class MovingAverage:
    def __init__(self, window_size):
        self.window_size = window_size
        self.values = []

    def process(self, value):
        self.values.append(value)
        if len(self.values) > self.window_size:
            self.values = self.values[-self.window_size:]
        return sum(self.values) / len(self.values)


class Accelerometer:
    def __init__(self):
        self.previous_value = None

    def process(self, current_value):
        if self.previous_value is None:
            # Если предыдущего значения нет, сохраняем текущее значение и возвращаем 0
            self.previous_value = current_value
            return 0
        else:
            # Вычисляем разницу между текущим и предыдущим значениями
            diff = current_value - self.previous_value
            self.previous_value = current_value
            return diff


def normalize(value, from_min, from_max, to_min=-1, to_max=1):
    from_range = from_max - from_min
    to_range = to_max - to_min
    scaled_value = (value - from_min) / from_range
    return to_min + (scaled_value * to_range)
