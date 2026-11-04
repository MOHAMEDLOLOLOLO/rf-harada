# Fiche : spectre d'un signal modulé en amplitude (AM)

## 1. À quoi ça sert

Une modulation d'amplitude fait varier lentement l'amplitude d'une porteuse. Le même calcul (un produit de deux cosinus) décrit :
- un **mélangeur** RF : il multiplie le signal par un oscillateur local et crée des fréquences somme et différence ;
- un **défaut** sur un signal : un ripple d'alimentation ou une modulation parasite à la fréquence f_m crée des raies à f_c ± f_m. L'écart entre la raie et la porteuse donne la fréquence du coupable.

## 2. Le signal

```
s(t) = (1 + m cos(2 pi f_m t)) * cos(2 pi f_c t)
```

- f_c : porteuse. f_m : fréquence de modulation. m : indice de modulation (0 à 1).
- Le terme entre parenthèses est l'enveloppe : l'amplitude de la porteuse varie entre 1 - m et 1 + m.

## 3. Dérivation à la main

Formule du produit de cosinus (déduite d'Euler, cos a = (e^{ia} + e^{-ia})/2) :

```
cos a * cos b = 1/2 [ cos(a - b) + cos(a + b) ]
```

On développe :

```
s(t) = cos(2 pi f_c t) + m cos(2 pi f_m t) cos(2 pi f_c t)
     = cos(2 pi f_c t)
       + (m/2) cos(2 pi (f_c - f_m) t)
       + (m/2) cos(2 pi (f_c + f_m) t)
```

Trois cosinus : la porteuse (amplitude 1) et deux raies latérales (amplitude m/2 chacune) en f_c - f_m et f_c + f_m.

## 4. Passage au spectre (convention)

Avec la mesure X(f) = moyenne de x(t) e^{-i 2 pi f t} (bilatérale), un cosinus d'amplitude A donne un pic de hauteur **A/2** en f et en -f.

| Raie | Amplitude du cosinus | |X(f)| mesuré |
|---|---|---|
| porteuse f_c | 1 | 0.5 |
| f_c - f_m | m/2 | m/4 |
| f_c + f_m | m/2 | m/4 |

Avec f_c = 20 Hz, f_m = 2 Hz : m = 0.5 donne 0.125 aux fréquences 18 et 22 Hz ; m = 1 donne 0.25.

Attention aux conventions : avec `2*np.abs(np.fft.rfft(x))/N` (spectre unilatéral), la porteuse vaut 1 et les raies m/2. Le facteur 2 entre les deux est une source d'erreur fréquente.

## 5. Résultats (voir `modulation_am.py`)

Fenêtre D = 1 s, fs = 1000 Hz, f_c = 20 Hz, f_m = 2 Hz.

| f (Hz) | m = 0.5 | m = 1 |
|---|---|---|
| 10 | ~1e-16 | ~1e-16 |
| 18 | 0.125 | 0.25 |
| 20 | 0.5 | 0.5 |
| 22 | 0.125 | 0.25 |
| 25 | ~1e-16 | ~1e-16 |

Les valeurs mesurées coïncident avec la dérivation à la main.

## 6. Pourquoi tant de pics sur la figure (fuite spectrale)

Le signal n'a que 3 fréquences, mais il n'est observé que pendant D = 1 s. Chaque raie apparaît comme un sinus cardinal de largeur 1/D = 1 Hz, dont les lobes secondaires s'annulent aux fréquences entières à partir de la raie. Les petits pics de `spectre_am.png` sont ces lobes, pas de vraies fréquences. Le script ne mesure qu'à des fréquences entières (10, 18, 20, 22, 25), exactement là où les lobes valent 0. Avec un pas de 0.1 Hz, ils apparaissent. Avec D = 4 s, les pics sont 4 fois plus étroits.

## 7. Lire un spectre : retrouver la source d'un défaut

Signal de test (`spectre_defauts.png`) : porteuse 100 Hz, ripple à 7 Hz (m = 0.1), brouilleurs à 173 Hz et 300 Hz, bruit. Amplitudes unilatérales attendues : 1 à 100 Hz, 0.05 à 93 et 107 Hz, 0.03 à 173 Hz, 0.05 à 300 Hz.

| Élément | Forme | Position | Test pour l'identifier |
|---|---|---|---|
| Porteuse | pic étroit | f_c (connue) | elle suit quand on change f_c |
| Raies latérales | deux pics symétriques | f_c ± f_m | elles suivent l'amplitude de la porteuse : produit porteuse x modulation. L'écart f_m désigne la source |
| Harmonique | pic | n x f_c | elle bouge de n fois le changement de f_c |
| Brouilleur | pic | sans lien entier avec f_c | il ne bouge pas quand on change f_c |
| Bruit | plancher continu | toutes fréquences | il baisse de 10 log10(RBW1/RBW2) dB si la bande d'analyse diminue |

Le test s'applique quand on peut faire varier un paramètre. Sur un signal reçu qu'on ne contrôle pas, on s'appuie sur les relations de fréquence (n x f_c, f_c ± f_m).

## 8. Pièges rencontrés

- **Enveloppe tracée avec un autre m que le signal** : utiliser une variable `m` partagée.
- **Fréquences de test hors de la grille 1/D** : fuite spectrale. Choisir des fréquences multiples de 1/D, ou allonger D.
- **Facteur 2** entre spectre bilatéral (mean) et unilatéral (2|rfft|/N).
- **fs et f_c** : fs est le réglage de la mesure (échantillons par seconde), f_c est une propriété du signal. Il faut fs > 2 f_c pour voir f_c.

## 9. Reproduire

```
python modulation_am.py      # affiche |X(f)| aux 5 fréquences de test
```
