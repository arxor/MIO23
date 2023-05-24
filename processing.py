import numpy as np
from collections import deque
window_size = 10
abp1_average = None
abp1_fft = None
abp2_fft = None
idx = 0
vals = np.zeros(window_size)


def process(bracelet):
    global abp1_average, idx, vals, abp1_fft, abp2_fft
    abp1_fft = np.fft.fft(bracelet.get_abp1(50))
    abp2_fft = np.fft.fft(bracelet.get_abp2(50))


#     vals[idx] = bracelet.get_abp1()
#     idx += 1
#     if idx >= window_size:
#         idx = 0
#     abp1_average = np.mean(vals)
#
#
# def get_abp1_average():
#     return abp1_average
# def envelope_detector(new_value, buffer_size=10):
#     if not hasattr(envelope_detector, "buffer"):
#         envelope_detector.buffer = [0] * buffer_size
#
#     envelope_detector.buffer.pop(0)
#     envelope_detector.buffer.append(abs(new_value))
#     return sum(envelope_detector.buffer) / len(envelope_detector.buffer)
class EnvelopeDetector:
    def __init__(self, buffer_size=5, decay_factor=0.9):
        self.buffer_size = buffer_size
        self.decay_factor = decay_factor
        self.buffer = [0] * buffer_size
        self.peak = 0

    def process(self, new_value):
        # Обновляем пик, если новое значение выше текущего пика
        if abs(new_value) > self.peak:
            self.peak = abs(new_value)

        # Обновляем буфер
        self.buffer.pop(0)
        self.buffer.append(self.peak)

        # Постепенно уменьшаем значение пика
        self.peak *= self.decay_factor

        # Возвращаем среднее значение буфера в качестве огибающей
        return sum(self.buffer) / len(self.buffer)

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


class StreamingNormalization:
    def __init__(self, window_size):
        self.window = deque(maxlen=window_size)

    def normalize(self, value):
        self.window.append(value)
        mean = np.mean(self.window)
        std = np.std(self.window)
        return (value - mean) / std if std != 0 else value

def abp1_get_fft():
    return abp1_fft


def abp2_get_fft():
    return abp2_fft
