import numpy as np

def conv_fft(x, h):
    n = len(x) + len(h) - 1            # zero padding : évite la convolution circulaire
    return np.fft.ifft(np.fft.fft(x, n) * np.fft.fft(h, n)).real

cas = [
    ([1, 0, 2], [1, 1, 1], [1, 1, 3, 2, 2]),
    ([2, 4, 8], [0.5, 0.5], [1, 3, 6, 4]),
]

for x, h, attendu in cas:
    y1 = np.convolve(x, h)
    y2 = conv_fft(np.array(x), np.array(h))
    print("x =", x, " h =", h)
    print("  np.convolve :", y1, " somme =", y1.sum())
    print("  via FFT     :", np.round(y2, 10))
    assert np.allclose(y1, attendu) and np.allclose(y2, attendu)

# piège : sans zero padding, la convolution est circulaire (résultat faux)
x, h = np.array([1, 0, 2]), np.array([1, 1, 1])
faux = np.fft.ifft(np.fft.fft(x, len(x)) * np.fft.fft(h, len(x))).real
print("sans padding (n = len(x)) :", np.round(faux, 10), "<- faux, 3 éléments au lieu de 5")
