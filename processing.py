import numpy as np

window_size = 10
abp1_average = None
idx = 0
vals = np.zeros(window_size)

def process(bracelet):
    global abp1_average, idx, vals

    vals[idx] = bracelet.get_abp1()
    idx += 1
    if idx >= window_size:
        idx = 0
    abp1_average = np.mean(vals)
    spectrum = np.fft.fft(signal)

    # Вычисление амплитуды спектра
    amplitude = np.abs(spectrum)

    # Вычисление частотных значений
    frequencies = np.fft.fftfreq(len(signal))

    # Визуализация частотного распределения
    plt.plot(frequencies, amplitude)
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')
    plt.show()

def get_abp1_average():
    return abp1_average
