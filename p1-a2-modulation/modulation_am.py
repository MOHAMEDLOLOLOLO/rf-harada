import numpy as np

fs = 1000
N = 1000
t = np.arange(N) / fs                      # D = 1 s

x = (1 + np.cos(2*np.pi*2*t)) * np.cos(2*np.pi*20*t)

def X(f):
    return np.mean(x * np.exp(-1j*2*np.pi*f*t))

for f in [10, 18, 20, 22, 25]:
    print(f, abs(X(f)))

import matplotlib.pyplot as plt

freqs = np.arange(0, 40.01, 0.1)
spectre = [abs(X(f)) for f in freqs]

fig, ax = plt.subplots(2, 1, figsize=(10, 7))

ax[0].plot(t[:300], x[:300], label="signal AM")
ax[0].plot(t[:300], 1 + 0.5*np.cos(2*np.pi*2*t[:300]), "r--", label="enveloppe")
ax[0].plot(t[:300], -(1 + 0.5*np.cos(2*np.pi*2*t[:300])), "r--")
ax[0].set_xlabel("t (s)"); ax[0].legend(); ax[0].grid(alpha=0.3)

ax[1].plot(freqs, spectre)
ax[1].set_xlabel("f (Hz)"); ax[1].set_ylabel("|X(f)|"); ax[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("spectre_am.png", dpi=100)
plt.show()
