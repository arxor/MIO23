import json
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, TimeDistributed, Conv1D
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split


class Jesture:
    items = []

    def __init__(self):
        self.items.append(self)
        self.name = "кулак"
        self.data = None
        self.label = []

    def save_to_file(self):
        try:
            with open("gestures.json", "r") as f:
                gestures = json.load(f)
        except json.decoder.JSONDecodeError:
            gestures = []

        for gesture in gestures:
            if gesture['name'] == self.name:
                index = gesture['index']
                break
        else:
            index = len(gestures) + 1

        self.label_gesture(index, 1, 10)

        for gesture in gestures:
            if gesture['name'] == self.name:
                gesture['data'].append(self.data)
                gesture['label'].append(self.label)
                break
        else:
            save = {"name": self.name, "index": index, "data": [self.data], "label": [self.label]}
            gestures.append(save)

        with open("gestures.json", "w") as f:
            json.dump(gestures, f, indent=4)

    def label_gesture(self, gesture_index, rest_threshold_ratio, transition_samples, min_threshold=0.1):
        for signal in self.data:
            labeled_signal = [0] * len(signal)

            # Рассчитаем среднее значение и стандартное отклонение сигнала
            mean_signal = np.mean(signal)
            std_signal = np.std(signal)

            # Установим адаптивный порог как множитель стандартного отклонения выше среднего
            threshold = mean_signal + rest_threshold_ratio * std_signal

            # Установим минимальный порог
            if threshold < min_threshold:
                threshold = min_threshold

            # Пометьте сигнал, где он превышает порог
            for i in range(transition_samples, len(signal) - transition_samples):
                if any(abs(val) > threshold for val in signal[i - transition_samples:i + transition_samples + 1]):
                    labeled_signal[i] = gesture_index

            self.label.append(labeled_signal)

    @classmethod
    def sum_arrays(cls, arr):
        result = [0] * len(arr[0])  # Создаем новый массив из нулей с такой же длиной, как у исходного массива
        for sub_arr in arr:
            result = [max(n, m) for n, m in zip(result, sub_arr)]
        return result

    @classmethod
    def convert_data(cls, data):
        X = []
        for gesture in data:
            for example in gesture['data']:
                X.append(np.transpose(example))  # Транспонирование данных
        return np.array(X)

    @classmethod
    def convert_labels(cls, data):
        y = []
        for gesture in data:
            for example in gesture['label']:
                sum = cls.sum_arrays(example)
                example_categorical = to_categorical(sum, num_classes=3)  # Преобразование в one-hot векторы
                y.append(example_categorical)
        return np.array(y)

    @classmethod
    def process_gestures(cls, filename):
        with open(filename, 'r') as f:
            data = json.load(f)

        X = cls.convert_data(data)
        y = cls.convert_labels(data)
        return X, y

    @classmethod
    def create_model(cls, input_shape, num_classes):
        model = Sequential()

        model.add(Conv1D(64, kernel_size=3, activation='relu', padding='same', input_shape=input_shape))
        model.add(Dropout(0.2))

        model.add(LSTM(128, return_sequences=True))
        model.add(Dropout(0.2))

        model.add(LSTM(128, return_sequences=True))
        model.add(Dropout(0.2))

        model.add(TimeDistributed(Dense(32, activation='relu')))
        model.add(Dropout(0.2))

        model.add(TimeDistributed(Dense(num_classes, activation='softmax')))

        return model

    @classmethod
    def prepare_model(cls):
        X, y = cls.process_gestures("gestures.json")
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

    @classmethod
    def recognize(cls, d):
        data = np.array([np.transpose([list(queue)[-100:] for queue in d])])
        print(np.around(cls.model.predict(data), decimals=2))
