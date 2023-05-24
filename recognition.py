import numpy as np

from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

import processing


# from fastdtw import fastdtw
# from scipy.spatial.distance import euclidean
#
# # Примеры жестов, которые будут использоваться для обучения
# # Каждый жест - это временная последовательность 3D-координат
# gestures = {
#     'жест1': np.array([/* data */]),
#     'жест2': np.array([/* data */]),
#     # Добавьте больше жестов здесь...
# }
#
# # Входной жест, который мы хотим распознать
# input_gesture = np.array([/* data */])
#
# # Расчет DTW расстояния между входным жестом и каждым обучающим жестом
# distances = {}
# for gesture_name, gesture_data in gestures.items():
#     distance, _ = fastdtw(input_gesture, gesture_data, dist=euclidean)
#     distances[gesture_name] = distance
#
# # Определение наиболее подходящего жеста
# best_match = min(distances, key=distances.get)
# print('Наиболее подходящий жест:', best_match)
class Jesture:
    items = []
    bracelet = None  # Добавляем новый атрибут класса для хранения bracelet

    @classmethod
    def set_bracelet(cls, bracelet):
        cls.bracelet = bracelet

    def __init__(self):
        self.gesture_temp = []
        self.items.append(self)
        self.abp1 = None
        self.abp2 = None
        self.ref = None
        self.ax = None
        self.ay = None
        self.az = None
        self.gx = None
        self.gy = None
        self.gz = None


    def convert(self):
        self.abp1 = np.array([list[0] for list in self.gesture_temp])
        self.abp2 = np.array([list[1] for list in self.gesture_temp])
        self.ref = np.array([list[2] for list in self.gesture_temp])
        self.ax = np.array([list[3] for list in self.gesture_temp])
        self.ay = np.array([list[4] for list in self.gesture_temp])
        self.az = np.array([list[5] for list in self.gesture_temp])
        self.gx = np.array([list[6] for list in self.gesture_temp])
        self.gy = np.array([list[7] for list in self.gesture_temp])
        self.gz = np.array([list[8] for list in self.gesture_temp])

    def recognize(cls):
        # Создаем входной жест из текущих данных сенсора


        # Вычисляем расстояние DTW между входным жестом и каждым известным жестом
        for jest in cls.items:
            input_gesture = np.array(
                # cls.bracelet.get_abp1(len(jest.abp1)),
                # cls.bracelet.get_abp2(len(jest.abp1)),
                # cls.bracelet.get_ref(len(jest.abp1)),
                 cls.bracelet.get_ay(len(jest.abp1))
                # cls.bracelet.get_ay(len(jest.abp1)),
                # cls.bracelet.get_az(len(jest.abp1)),
                # cls.bracelet.get_gx(len(jest.abp1)),
                # cls.bracelet.get_gy(len(jest.abp1)),
                # cls.bracelet.get_gz(len(jest.abp1))
            )
            jesture_data = np.array(
                # jest.abp1,
                # jest.abp2,
                # jest.ref,
                jest.ay
                # jest.ay,
                # jest.az,
                # jest.gx,
                # jest.gy,
                # jest.gz
            )

            distance, _ = fastdtw(input_gesture, jesture_data, dist=euclidean)
            print(f"Расстояние до жеста {jest}: {distance}")
