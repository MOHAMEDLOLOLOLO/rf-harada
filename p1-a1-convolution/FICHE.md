# Fiche : convolution, systèmes linéaires invariants et lien avec Fourier

## 1. À quoi ça sert

Un système linéaire invariant dans le temps (LTI) est un système dont la sortie se calcule à partir de son entrée sans connaître son intérieur : il suffit de savoir ce qu'il fait à une impulsion. Filtres, amplis dans leur zone linéaire, câbles, canaux radio avec échos : en première approximation, ce sont des systèmes LTI.

Cette fiche répond à trois questions :
1. Comment prédire la sortie d'un système à partir de sa réponse impulsionnelle h ? (convolution)
2. Pourquoi la fréquence simplifie-t-elle ce calcul ? (Fourier)
3. À quoi ça sert en RF ?

## 2. La convolution

Entrée x[n], réponse impulsionnelle h[k] (la sortie quand l'entrée est une impulsion unité δ[n]) :

```
y[n] = somme sur k de  h[k] * x[n-k]        (noté y = x * h)
```

Démarche : x est une somme d'impulsions décalées et pondérées (x[n] = somme de x[k] δ[n-k]). Par linéarité et invariance dans le temps, chaque impulsion produit une copie décalée et pondérée de h. La sortie est la somme de ces copies.

Lecture de h : la position dans h est un retard. h[k] pondère l'entrée vue k échantillons plus tôt.

Exemples (voir `convolution.py` et `retard10.py`) :

| Système | h | Effet |
|---|---|---|
| Gain | [2] | y = 2x |
| Retard de 10 échantillons | 10 zéros puis un 1 (le 1 à la position 10) | y[n] = x[n-10] |
| Écho | [1, 0, ..., 0, 0.5] | le signal plus une copie retardée et atténuée |
| Moyenne sur L points | L fois 1/L | passe-bas, zéro de gain à fs/L |

Vérification à la main : x = [1, 0, 2], h = [1, 1, 1] donne y = [1, 1, 3, 2, 2]. La longueur vaut len(x) + len(h) - 1 = 5. La somme de y est le produit des sommes (3 x 3 = 9).

## 3. Pourquoi passer en fréquences

Choisissons comme entrée une exponentielle complexe x[n] = e^{i w n}, avec w = 2 pi f / fs.

```
y[n] = somme_k h[k] e^{i w (n-k)}
     = e^{i w n} * somme_k h[k] e^{-i w k}
     = H(w) * x[n]
```

Un retard de k échantillons multiplie e^{i w n} par le nombre constant e^{-i w k} (module 1 : c'est une rotation dans le plan complexe). Pour toute autre forme d'onde, un décalage mélange des fonctions différentes. L'exponentielle complexe traverse donc un système LTI en étant seulement multipliée par un nombre complexe :

```
H(w) = somme_k h[k] e^{-i w k}      (transformée de Fourier de h)
```

- |H(w)| : facteur sur l'amplitude à cette fréquence.
- arg H(w) : décalage de phase.

Tout signal étant une somme d'exponentielles (transformée de Fourier), et le système étant linéaire :

```
Y(f) = H(f) * X(f)       (convolution dans le temps = produit dans les fréquences)
```

Démonstration : avec m = n - k, la somme double de la transformée de y se sépare en deux sommes indépendantes, celle de h et celle de x.

## 3 bis. Cas du filtre RC (fc = 10 Hz)

```
H(f) = 1 / (1 + i f/fc)        |H(f)| = 1 / sqrt(1 + (f/fc)^2)
```

| f | |H(f)| |
|---|---|
| 3 Hz | 0.958 |
| 10 Hz | 0.707 |
| 30 Hz | 0.316 |

Pour une entrée sin(2 pi 3 t) + sin(2 pi 30 t), la sortie vaut environ 0.958 sin(2 pi 3 t + phi1) + 0.316 sin(2 pi 30 t + phi2) : chaque pic du spectre est multiplié par |H| à sa fréquence. C'est ce que montre la 3e colonne de `tracer_systemes.png`.

## 4. Usages en RF

- **Filtrage** : on choisit |H(f)| (garder une bande, couper le reste), on en déduit h (filtres FIR/IIR, pilier P2-A6).
- **Canal multitrajet** : le canal est un h avec plusieurs échos. Dans les fréquences, |H(f)| oscille (pour un écho de retard tau, la période de l'ondulation est 1/tau).
- **OFDM** (Wi-Fi, 5G) : l'émetteur place un symbole sur chaque fréquence (IFFT), le canal multiplie chaque fréquence par H(f), le récepteur divise par l'estimation de H(f) (égalisation à un coefficient par sous-porteuse).
- **Diagnostic d'un signal mesuré** : le spectre montre quelles fréquences composent le signal (porteuse, harmoniques, raies latérales d'un ripple, brouilleurs, plancher de bruit). Un défaut qui dure et oscille se lit dans le spectre ; un défaut localisé dans le temps (décalage, impulsion) se lit dans le temps.
- **Coût de calcul** : convolution directe N x M multiplications ; via FFT de l'ordre de N log N. Pour les filtres courts ou le temps réel, la forme directe reste la plus simple.

## 5. Pièges rencontrés

- **Zero padding** : pour obtenir la convolution linéaire via FFT, il faut des FFT de longueur len(x) + len(h) - 1. Avec n = len(x), la FFT calcule une convolution circulaire : pour x = [1, 0, 2] et h = [1, 1, 1], elle donne [3, 3, 3] au lieu de [1, 1, 3, 2, 2].
- **Discrétisation d'un RC** : échantillonner simplement l'exponentielle sur-estime le gain (0.988 au lieu de 0.958 à 3 Hz). Il faut h[k] = (1 - a) a^k avec a = exp(-1/(fs tau)).
- **Régime établi** : le spectre du tracé est calculé sur la dernière seconde, pour exclure le démarrage (transitoire).
- **Retard pur** : |H(f)| = 1 à toutes les fréquences, le spectre d'amplitude ne le montre pas. Seule la phase (pente -2 pi f d / fs) change.

## 6. Reproduire

```
python convolution.py        # vérifie les cas chiffrés, direct vs FFT
python retard10.py           # retard de 10 échantillons
python tracer_systemes.py    # 5 systèmes : h, entrée/sortie, spectres
```

## 7. Suite

Laplace généralise Fourier (s = sigma + i w au lieu de i w). La fonction de transfert H(s) = V_out / V_in d'un RC vaut 1 / (1 + s RC) ; son pôle s = -1/RC donne la stabilité et le régime transitoire (v_out = 1 - e^{-t/RC} pour un échelon). Cette partie sera ajoutée après validation des exercices.
