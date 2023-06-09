import json
import numpy as np
from tensorflow.keras.models import Sequential, save_model
from tensorflow.keras.layers import Dense, Dropout, LSTM, TimeDistributed, Conv1D, Bidirectional
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split


class Jesture:
    gestures = []
    prob = []
    selected_gesture = None

    def __init__(self, name):
        self.name = name
        self.gesture = {"name": self.name, "index": None, "data": [], "label": []}
        self.gestures.append(self)
        self.reindex_gestures()

    @classmethod
    def load_gestures(cls):
        try:
            with open("gestures.json", "r") as f:
                items = json.load(f)
            for i, item in enumerate(items):
                gesture = cls(item["name"])  # Создаем новый экземпляр Jesture
                gesture.gesture["data"] = item["data"]
                gesture.gesture["label"] = item["label"]
                gesture.gesture["index"] = item["index"]
        except json.decoder.JSONDecodeError:
            print("Жесты не найдены.")
            return

    def delete_recording(self, index):
        del self.gesture['data'][index]
        del self.gesture['label'][index]

    def delete_gesture(self):
        try:
            Jesture.gestures.remove(self)
            Jesture.reindex_gestures()
            if len(Jesture.gestures):
                Jesture.selected_gesture = Jesture.gestures[-1]
        except ValueError:
            print("Удаляемый жест не найден")

    @classmethod
    def reindex_gestures(cls):
        for i, gesture in enumerate(cls.gestures):
            gesture.gesture['index'] = i + 1

    @classmethod
    def save_to_file(cls):
        cls.reindex_gestures()
        with open("gestures.json", "w") as f:
            json.dump([gesture.gesture for gesture in cls.gestures], f, indent=4)

    @classmethod
    def check_name(cls, name):
        for gesture in cls.gestures:
            if gesture.gesture['name'] == name:
                return 1
        return 0

    # @classmethod
    # def sum_arrays(cls, arr):
    #     result = [0] * len(arr[0])  # Создаем новый массив из нулей с такой же длиной, как у исходного массива
    #     for sub_arr in arr:
    #         result = [max(n, m) for n, m in zip(result, sub_arr)]
    #     return result
    #
    # @classmethod
    # def convert_data(cls, data):
    #     X = []
    #     for gesture in data:
    #         for example in gesture['data']:
    #             X.append(np.transpose(example))  # Транспонирование данных
    #     return np.array(X)
    #
    # @classmethod
    # def convert_labels(cls, data):
    #     y = []
    #     for gesture in data:
    #         for example in gesture['label']:
    #             sum = cls.sum_arrays(example)
    #             example_categorical = to_categorical(sum, num_classes=3)  # Преобразование в one-hot векторы
    #             y.append(example_categorical)
    #     return np.array(y)
    #
    # @classmethod
    # def process_gestures(cls, filename):
    #     X = cls.convert_data(cls.gestures)
    #     y = cls.convert_labels(cls.gestures)
    #     return X, y

    @classmethod
    def process_gestures(cls):
        X = []
        y = []

        for gesture in cls.gestures:
            for example in gesture['data']:
                X.append(np.transpose(example))  # Транспонирование данных

            for example in gesture['label']:
                sum_array = [0] * len(
                    example[0])  # Создаем новый массив из нулей с такой же длиной, как у исходного массива
                for sub_arr in example:
                    sum_array = [max(n, m) for n, m in zip(sum_array, sub_arr)]

                example_categorical = to_categorical(sum_array, num_classes=3)  # Преобразование в one-hot векторы
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

    @classmethod
    def create_model(cls, input_shape, num_classes):
        model = Sequential()

        model.add(Conv1D(128, kernel_size=3, activation='relu', padding='same', input_shape=input_shape))
        model.add(Dropout(0.3))

        model.add(Bidirectional(LSTM(256, return_sequences=True)))
        model.add(Dropout(0.3))

        model.add(Bidirectional(LSTM(256, return_sequences=True)))
        model.add(Dropout(0.3))

        model.add(TimeDistributed(Dense(64, activation='relu')))
        model.add(Dropout(0.3))

        model.add(TimeDistributed(Dense(num_classes, activation='softmax')))

        return model

    @classmethod
    def prepare_model(cls):
        X, y = cls.process_gestures()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        input_shape = (X_train.shape[1], X_train.shape[2])
        num_classes = y_train.shape[2]

        cls.model = cls.create_model(input_shape, num_classes)
        cls.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        cls.model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)

        # Оцениваем работу модели на тестовом наборе
        test_loss, test_acc = cls.model.evaluate(X_test, y_test)
        print("Test Loss: ", test_loss)
        print("Test Accuracy: ", test_acc)

        save_path = "/"
        save_model(cls.model, save_path)
        print("Модель сохнанена.:")

    @classmethod
    def recognize(cls, d):
        data = np.array([np.transpose([list(queue)[-100:] for queue in d])])
        a = np.around(cls.model.predict(data), decimals=2)
        cls.prob = a[0][99].tolist()
        print(a[0][99])
