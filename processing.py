"""
Модуль для обработки данных каналов электромиографа и акселерометра.

Он включает в себя фильтры, быстрое преобразование Фурье и нормализацию данных.
"""

import numpy as np


def process(bracelet):
    """
    Обрабатывает данные с браслета, применяя быстрое преобразование Фурье.

    Параметры:
    bracelet : Объект браслета.
    """
    bracelet.data[9] = np.round(np.abs(np.fft.fft(np.array(list(bracelet.get_data(0, 70))))), 1)
    bracelet.data[10] = np.round(np.abs(np.fft.fft(np.array(list(bracelet.get_data(1, 70))))), 1)


class EnvelopeDetector:
    """
    Класс для огибающей сигнала.

    Параметры:
    smoothing_factor (float): Коэффициент сглаживания.
    integral_window (int): Размер окна.
    integral_threshold (int): Пороговое значение для нахождения суммы (интеграла).
    """

    def __init__(self, smoothing_factor=0.3, integral_window=10, integral_threshold=5):
        self.smoothing_factor = smoothing_factor
        self.integral_window = integral_window
        self.integral_threshold = integral_threshold
        self.envelope = 0.0
        self.values_buffer = []

    def process(self, value):
        """
        Обрабатывает значение.

        Параметры:
        value : Значение для обработки.

        Возвращает:
        float : Обновленное значение огибающей, если сумма значений в буфере больше порогового значения.
                В противном случае возвращается 0.0.
        """
        abs_value = abs(value)

        self.envelope = (1.0 - self.smoothing_factor) * self.envelope + self.smoothing_factor * abs_value

        self.values_buffer.append(abs_value)

        if len(self.values_buffer) > self.integral_window:
            self.values_buffer = self.values_buffer[-self.integral_window:]

        if sum(self.values_buffer) < self.integral_threshold:
            return 0.0
        else:
            return self.envelope


class MovingAverage:
    """
       Класс для вычисления скользящего среднего.

       Параметры:
       window_size (int): Размер окна.
    """

    def __init__(self, window_size):
        self.window_size = window_size
        self.values = []

    def process(self, value):
        """
        Обрабатывает значение, обновляя список значений и возвращая текущее скользящее среднее.

        Параметры:
        value : Значение для обработки.

        Возвращает:
        float : Текущее скользящее среднее.
        """
        self.values.append(value)
        if len(self.values) > self.window_size:
            self.values = self.values[-self.window_size:]
        return sum(self.values) / len(self.values)


class Accelerometer:
    """
    Класс для обработки данных акселерометра (для вычисления разницы между текущим и предыдущим значением).
    """

    def __init__(self):
        self.previous_value = None

    def process(self, current_value):
        """
        Обрабатывает текущее значение, вычисляя разницу между ним и предыдущим значением.

        Параметры:
        current_value : Текущее значение для обработки.

        Возвращает:
        int : Разница между текущим и предыдущим значением.
        """

        if self.previous_value is None:
            self.previous_value = current_value
            return 0
        else:
            diff = current_value - self.previous_value
            self.previous_value = current_value
            return diff


def normalize(value, from_min, from_max, to_min=-1, to_max=1):
    """
    Нормализует значение в заданном диапазоне.

    Параметры:
    value : Значение для нормализации.
    from_min, from_max : Исходный диапазон значений.
    to_min, to_max : Конечный диапазон значений.

    Возвращает:
    float : Нормализованное значение.
    """
    from_range = from_max - from_min
    to_range = to_max - to_min
    scaled_value = (value - from_min) / from_range
    return to_min + (scaled_value * to_range)
