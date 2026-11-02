import numpy as np
import matplotlib.pyplot as plt

fs = 1000
D = 2.0
t = np.arange(int(fs*D)) / fs

porteuse = np.cos(2*np.pi*100*t)*3

# --- défauts cachés : à identifier ---
x = porteuse * (1 + 0.1*np.cos(2*np.pi*7*t))   # défaut 1
x += 0.05*np.cos(2*np.pi*300*t)                # défaut 2
x += 0.03*np.cos(2*np.pi*173*t)                # défaut 3
x += 0.02*np.random.randn(len(t))              # défaut 4

X = np.fft.rfft(x) / len(x) * 2
f = np.fft.rfftfreq(len(x), 1/fs)

plt.figure(figsize=(10, 4))
plt.plot(f, np.abs(X))
plt.xlim(0, 500)
plt.xlabel("f (Hz)"); plt.ylabel("amplitude")
plt.grid(alpha=0.3)
plt.savefig("spectre_defauts.png", dpi=100)
plt.show()
