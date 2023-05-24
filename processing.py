import numpy as np

window_size = 10
abp1_average = None
abp1_fft = None
abp2_fft = None
idx = 0
vals = np.zeros(window_size)

def process(bracelet):
    global abp1_average, idx, vals, abp1_fft,abp2_fft
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
def abp1_get_fft():
    return abp1_fft

def abp2_get_fft():
    return abp2_fft

