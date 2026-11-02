import numpy as np
import matplotlib.pyplot as plt

x = np.zeros(40)
x[5:12] = [1, 5, 3, 4, 3, 2, 1]        # une petite bosse, échantillons 5 à 11

h = np.zeros(11)
h[0] = 0.5
h[10] = 1.0                             # retard de 10 échantillons : y[n] = x[n-10]

y = np.convolve(x, h)[:len(x)]

print("x non nul aux indices :", np.nonzero(x)[0])
print("y non nul aux indices :", np.nonzero(y)[0])
print("somme x =", x.sum(), " somme y =", y.sum())

fig, ax = plt.subplots(3, 1, figsize=(9, 7), sharex=True)
ax[0].stem(x, basefmt=" ");  ax[0].set_ylabel("x[n]  entrée")
ax[1].stem(h, basefmt=" ", linefmt="tab:green", markerfmt="o"); ax[1].set_ylabel("h[n]")
ax[2].stem(y, basefmt=" ", linefmt="tab:red", markerfmt="o");   ax[2].set_ylabel("y[n]  sortie")
ax[2].set_xlabel("n (échantillons)")
for a in ax: a.grid(alpha=0.3)
plt.tight_layout(); plt.savefig("retard10.png", dpi=100)
plt.tight_layout()
plt.savefig("retard10.png", dpi=100)
plt.show()
