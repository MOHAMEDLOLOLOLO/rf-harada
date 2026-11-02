import numpy as np
x = np.array([1, 0, 2])
h = np.array([1, 1, 1])

y1 = np.convolve(x, h)                    # directe
n = len(x) + len(h) - 1                   # 5, zero padding obligatoire
y2 = np.fft.ifft(np.fft.fft(x, n) * np.fft.fft(h, n)).real

print(y1)
print(y2)
