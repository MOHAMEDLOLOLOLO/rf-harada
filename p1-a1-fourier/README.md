# P1-A1 : transformée de Fourier d'un sinus

Signal : sin(2π·3·t), observé 1 s (1000 échantillons à 1000 Hz).

Pour chaque fréquence de test f, on calcule le centre de masse du signal enroulé :

X(f) = moyenne de x(t)·e^(-i2πft)

Résultats :
- |X(3)| = 0,5 (X(3) = -0,5j, calculé aussi à la main : -i/2)
- X(2) et X(4) de l'ordre de 1e-16, donc nuls
- le spectre (spectre.png) montre deux pics de hauteur 0,5 à +3 et -3 Hz

Lancer : python fourier_sin.py
