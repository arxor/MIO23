"""
Модуль, содержащий класс Jesture, который обрабатывает, сохраняет и загружает жесты.
Также этот класс обучает модель для распознавания жестов на основе данных, собранных с браслета.
"""
import json
import numpy as np
from tensorflow.keras.models import Sequential, save_model, load_model
from tensorflow.keras.layers import Dense, Dropout, LSTM, TimeDistributed, Conv1D, Bidirectional
from tensorflow.keras.utils import to_categorical
from keras.regularizers import l2
import os
import threading


class Jesture:
    """
        Класс, представляющий жест, с возможностью загрузки, сохранения, обработки и обучения модели.

        Атрибуты:
        gestures : список всех жестов.
        prob : список вероятностей для каждого жеста.
        selected_gesture : текущий выбранный жест.
    """
    gestures = []
    prob = []
    selected_gesture = None

    def __init__(self, name):
        """
        Инициализация объекта Jesture с заданным именем.

        Параметры:
        name (str): имя жеста.
        """
        self.name = name
        self.gesture = {"name": self.name, "index": None, "data": []}
        self.gestures.append(self)
        self.reindex_gestures()

    @classmethod
    def load_gestures(cls):
        """
        Загрузка жестов из файла.
        Если файл не найден или содержит недействительные данные, выводится сообщение об ошибке.
        """
        try:
            with open("gestures.json", "r") as f:
                items = json.load(f)
            for i, item in enumerate(items):
                gesture = cls(item["name"])
                gesture.gesture["data"] = item["data"]
                gesture.gesture["index"] = item["index"]
        except json.decoder.JSONDecodeError:
            print("Жесты не найдены.")
            return

    def add_recording(self, data):
        """
        Добавление новой записи данных для этого жеста в файл "gestures.json".

        Параметры:
        data (list): список с данными для записи.
        """
        try:
            with open("gestures.json", "r") as f:
                gestures = json.load(f)
        except FileNotFoundError:
            gestures = []

        for gest in gestures:
            if gest["name"] == self.name:
                gest["data"].append(data)
                self.gesture["data"].append(data)
                print("Жест записан. Запись ", len(gest["data"]))

        with open("gestures.json", "w") as f:
            json.dump(gestures, f, indent=4)

    def delete_recording(self, index):
        """
        Удаление записи данных из этого жеста по указанному индексу.

        Параметры:
        index (int): индекс записи для удаления.
        """
        del self.gesture['data'][index]

    def delete_gesture(self):
        """
        Удаление этого жеста из списка жестов.
        """
        try:
            Jesture.gestures.remove(self)
            Jesture.reindex_gestures()
            if len(Jesture.gestures):
                Jesture.selected_gesture = Jesture.gestures[-1]
        except ValueError:
            print("Удаляемый жест не найден")

    @classmethod
    def reindex_gestures(cls):
        """
        Переиндексация всех жестов в списке жестов (нужно после удаления, так как один из индексов исчезает)
        """
        for i, gesture in enumerate(cls.gestures):
            gesture.gesture['index'] = i + 1

    @classmethod
    def save_to_file(cls):
        """
        Сохранение всех жестов в файл.
        """
        cls.reindex_gestures()
        with open("gestures.json", "w") as f:
            json.dump([gesture.gesture for gesture in cls.gestures], f, indent=4)

    @classmethod
    def check_name(cls, name):
        """
        Проверка, существует ли уже жест с заданным именем.

        Параметры:
        name (str): имя жеста для проверки.

        Возвращает:
        int : 1, если имя уже существует, 0 в противном случае.
        """
        for gesture in cls.gestures:
            if gesture.gesture['name'] == name:
                return 1
        return 0

    @classmethod
    def process_gestures(cls):
        """
        Обработка всех данных жестов и преобразование их в формат, подходящий для обучения модели.

        Возвращает:
        tuple : кортеж из двух массивов numpy, X - данные, y - метки.
        """
        X = []
        y = []

        for gesture in cls.gestures:
            for example in gesture.gesture['data']:
                X.append(np.transpose(example))

            for example in gesture.gesture['data']:
                example_categorical = to_categorical(gesture.gesture['index'],
                                                     num_classes=len(
                                                         cls.gestures) + 1)  # в one-hot векторы
                y.append(example_categorical)

        return np.array(X), np.array(y)

    # @classmethod
    # def create_model(cls, input_shape, num_classes):
    #     model = Sequential()
    #
    #     model.add(Conv1D(64, kernel_size=3, activation='relu', padding='same', input_shape=input_shape))
    #     model.add(Dropout(0.2))
    #
    #     model.add(LSTM(128, return_sequences=True))
    #     model.add(Dropout(0.2))
    #
    #     model.add(LSTM(128, return_sequences=True))
    #     model.add(Dropout(0.2))
    #
    #     model.add(TimeDistributed(Dense(32, activation='relu')))
    #     model.add(Dropout(0.2))
    #
    #     model.add(TimeDistributed(Dense(num_classes, activation='softmax')))
    #
    #     return model

    # @classmethod
    # def create_model(cls, input_shape, num_classes):
    #     model = Sequential()
    #
    #     model.add(Conv1D(64, kernel_size=3, activation='relu', padding='same', input_shape=input_shape))
    #     model.add(Dropout(0.3))
    #
    #     model.add(Bidirectional(LSTM(128, return_sequences=True)))
    #     model.add(Dropout(0.3))
    #
    #     model.add(Bidirectional(LSTM(128, return_sequences=True)))
    #     model.add(Dropout(0.3))
    #
    #     model.add(TimeDistributed(Dense(32, activation='relu')))
    #     model.add(Dropout(0.3))
    #
    #     model.add(TimeDistributed(Dense(num_classes, activation='softmax')))
    #
    #     return model

    # @classmethod
    # def create_model(cls, input_shape, num_classes):
    #     model = Sequential()
    #
    #     model.add(Conv1D(64, kernel_size=3, activation='relu', padding='same', input_shape=input_shape))
    #     model.add(Dropout(0.3))
    #
    #     model.add(Bidirectional(LSTM(128, return_sequences=True)))
    #     model.add(Dropout(0.3))
    #
    #     model.add(Bidirectional(LSTM(128)))
    #     model.add(Dropout(0.3))
    #
    #     model.add(Dense(32, activation='relu'))
    #     model.add(Dropout(0.3))
    #
    #     model.add(Dense(num_classes, activation='softmax'))
    #
    #     return model

    @classmethod
    def create_model(cls, input_shape, num_classes):
        """
        Создает модель для распознавания жестов.

        Параметры:
        input_shape (tuple): форма входных данных.
        num_classes (int): количество классов (жестов).

        Возвращает:
        model: модель Sequential.
        """
        model = Sequential()

        model.add(Conv1D(128, kernel_size=3, activation='relu', padding='same', input_shape=input_shape))
        model.add(Dropout(0.5))

        model.add(Conv1D(128, kernel_size=3, activation='relu', padding='same'))
        model.add(Dropout(0.5))

        model.add(Bidirectional(LSTM(256, return_sequences=True)))
        model.add(Dropout(0.5))

        model.add(Bidirectional(LSTM(256, return_sequences=True)))
        model.add(Dropout(0.5))

        model.add(Bidirectional(LSTM(256)))
        model.add(Dropout(0.5))

        model.add(Dense(64, activation='relu'), kernel_regularizer=l2(0.01))
        model.add(Dropout(0.5))

        model.add(Dense(16, activation='relu'))
        model.add(Dropout(0.5))

        model.add(Dense(num_classes, activation='softmax'))

        return model

    @classmethod
    def prepare_model(cls):
        """
        Подготавливает модель для обучения. Создает и компилирует модель,
        затем запускает поток для обучения модели.
        """
        X, y = cls.process_gestures()

        input_shape = (X.shape[1], X.shape[2])
        num_classes = len(cls.gestures) + 1

        cls.model = cls.create_model(input_shape, num_classes)
        cls.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        train_thread = threading.Thread(target=cls.train_model, args=(X, y))
        train_thread.start()

    @classmethod
    def train_model(cls, X, Y):
        """
        Обучает модель на заданных данных.

        Параметры:
        X (numpy.array): данные для обучения.
        Y (numpy.array): метки для обучения.
        """

        cls.model.fit(X, Y, epochs=100, batch_size=64, validation_split=0.2)

        save_path = os.path.join(os.getcwd(), 'my_model.h5')
        save_model(cls.model, save_path)
        print("Модель сохранена.")

    @classmethod
    def load_model(cls):
        """
        Загружает модель из файла. Если файл не найден, выводит сообщение об ошибке.
        """
        model_path = 'my_model.h5'
        if os.path.exists(model_path):
            cls.model = load_model(model_path)
            print("Модель загружена.")
        else:
            print("Модель не найдена.")

    @classmethod
    def delete_model(cls):
        """
        Удаляет модель из файла 'my_model.h5'. Если файл не найден, выводит сообщение об ошибке.
        """
        model_path = 'my_model.h5'
        if os.path.exists(model_path):
            os.remove(model_path)
            print("Модель удалена.")
        else:
            print("Модель не найдена.")

    @classmethod
    def recognize(cls, d):
        """
        Распознает жест, основываясь на предоставленных данных.

        Параметры:
        d (list): данные для распознавания жеста.

        Выводит:
        list: список вероятностей для каждого жеста.
        """
        data = np.array([np.transpose([list(queue)[-70:] for queue in d])])
        a = np.around(cls.model.predict(data), decimals=2)
        cls.prob = a[0].tolist()
        print(a[0])
