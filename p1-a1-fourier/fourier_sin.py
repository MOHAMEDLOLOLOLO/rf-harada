import numpy as np
import matplotlib.pyplot as plt

fs = 1000                       # fréquence d'échantillonnage (Hz)
N = 1000                        # nombre d'échantillons, durée D = 1 s
t = np.arange(N) / fs
x = np.sin(2*np.pi*3*t)         # sinus à 3 Hz

def X(f):
    return np.mean(x * np.exp(-1j*2*np.pi*f*t))   # moyenne de x(t)·e^(-i2πft)

for f in [2, 3, 4]:
    print(f, X(f), abs(X(f)))

freqs = np.arange(-10, 10.01, 0.1)
spectre = np.array([abs(X(f)) for f in freqs])

plt.plot(freqs, spectre)
plt.xlabel("f (Hz)")
plt.ylabel("|X(f)|")
plt.grid()
plt.savefig("spectre.png", dpi=150)   # enregistre la figure
plt.show()
