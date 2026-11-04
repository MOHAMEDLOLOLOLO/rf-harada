# Fiche : transformée de Fourier d'un signal

## 1. À quoi ça sert

La transformée de Fourier dit quelles fréquences composent un signal, et avec quelle amplitude et quelle phase. En RF : lire un spectre (porteuse, harmoniques, brouilleurs, bruit), prédire l'effet d'un filtre (Y = H x X), concevoir l'OFDM. Elle sert aussi dans un analyseur de spectre, une FFT d'oscilloscope et en FPGA (FFT IP).

## 2. Rappels utilisés

- Euler : e^{i t} = cos t + i sin t. Donc cos t = (e^{it} + e^{-it}) / 2 et sin t = (e^{it} - e^{-it}) / (2i).
- Puissances de i : i^2 = -1, i^3 = -i, i^4 = 1. e^{i 2 pi k} = 1 pour tout entier k.
- Intégrale = limite d'une somme de rectangles. Valeur moyenne d'une fonction sur une durée D : (1/D) x intégrale de f(t) dt sur [0, D].
- Moyenne d'un sinus sur un nombre entier de périodes : 0.

## 3. Définition

```
X(f) = (1/D) * integrale de 0 a D de  x(t) e^{-i 2 pi f t} dt
```

On multiplie le signal par une exponentielle qui tourne à la fréquence -f, puis on fait la moyenne. Si x contient la fréquence f, le produit contient un terme constant qui ne s'annule pas dans la moyenne : X(f) est grand. Sinon, les termes tournent dans tous les sens et la moyenne est proche de 0.

Règle : un terme e^{i 2 pi k t} a pour moyenne 0 sur [0, D] si k D est un entier non nul, et 1 si k = 0.

## 4. Calcul à la main : sin(2 pi 3 t) sur D = 1 s

```
sin(2 pi 3 t) = (e^{i 2 pi 3 t} - e^{-i 2 pi 3 t}) / (2i)
X(f) = (1/(2i)) * moyenne de [ e^{i 2 pi (3-f) t} - e^{-i 2 pi (3+f) t} ]
```

- f = 3 : le premier terme vaut 1, le second a pour moyenne 0. X(3) = 1/(2i) = **-i/2**.
- f = -3 : X(-3) = **+i/2**.
- f = 2 ou 4 : les deux termes ont une fréquence entière non nulle, donc X = 0.

Un sinus d'amplitude A donne |X(+-f0)| = A/2 (l'amplitude est partagée entre +f0 et -f0). Pour un signal réel, X(-f) est le conjugué de X(f). Une fréquence négative n'a pas de sens physique : c'est la moitié du même cosinus ou sinus.

## 5. Version discrète (voir `fourier_sin.py`)

```python
fs = 1000; N = 1000
t = np.arange(N) / fs
x = np.sin(2*np.pi*3*t)
def X(f): return np.mean(x * np.exp(-1j*2*np.pi*f*t))
```

`np.mean` remplace (1/D) x intégrale : on moyenne les N échantillons du produit.

| f (Hz) | X(f) | |X(f)| |
|---|---|---|
| 2 | ~0 (1e-17) | 0 |
| 3 | -0.5 i | 0.5 |
| 4 | ~0 (1e-17) | 0 |

Le spectre tracé de -10 à 10 Hz (pas 0,1) montre deux pics de hauteur 0,5 en +3 et -3 Hz (`spectre.png`).

## 6. Durée d'observation, fuite spectrale, fenêtres

Le résultat est exact seulement si f est un multiple de 1/D (la grille des fréquences). Sinon, le signal n'accomplit pas un nombre entier de périodes pendant l'observation, et le calcul fuit sur les fréquences voisines.

| Mesure | Valeur |
|---|---|
| N = 1000 (D = 1 s), f = 2,5 Hz (hors grille) | \|X\| = 0.347 |
| N = 1300 (D = 1,3 s), sans fenêtre : f = 3 / 2 / 4 | 0.5096 / 0.1195 / 0.0948 |
| N = 1300, fenêtre de Hann : f = 3 / 2 / 4 | 0.4998 / 0.1443 / 0.1438 |

Lecture :
- La résolution en fréquence est 1/D. Observer plus longtemps rend les pics plus étroits.
- Une fréquence inconnue ne tombe pas sur la grille : le pic est quand même visible, avec une valeur légèrement fausse et des lobes secondaires.
- La fenêtre de Hann ramène la valeur du pic plus près de 0,5 et réduit les lobes loin du pic, au prix d'un pic principal plus large. À 1 Hz du pic, elle ne baisse pas la valeur (0,144 contre 0,119 et 0,095).

## 7. Pièges rencontrés

- Une fréquence négative n'est pas un phénomène physique : le spectre d'un signal réel est symétrique.
- Un résultat de l'ordre de 1e-16 est un zéro numérique, pas un vrai signal.
- Fréquence testée et fréquence du signal doivent être des multiples de 1/D pour un résultat sans fuite.
- Un sinus de 3 Hz donne 0,5 et non 1 : l'amplitude est partagée entre +3 et -3 Hz.

## 8. Reproduire

```
python fourier_sin.py      # affiche X(2), X(3), X(4) et trace spectre.png
```
