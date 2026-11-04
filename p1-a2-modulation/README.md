# P1-A2 : spectre d'un signal modulé en amplitude

Dérivation à la main du spectre d'un signal AM, puis vérification numérique.

## Contenu
- `FICHE.md` : fiche explicative (dérivation, conventions, fuite spectrale, lecture d'un spectre).
- `modulation_am.py` : calcul de |X(f)| aux fréquences 10, 18, 20, 22, 25 Hz pour (1 + 0.5 cos(2 pi 2 t)) cos(2 pi 20 t).
- `spectre_am.png` : signal AM avec son enveloppe, et spectre.
- `spectre_defauts.png` : spectre d'un signal avec ripple, brouilleurs et bruit.

## Résultat
|X(20)| = 0.5, |X(18)| = |X(22)| = 0.125 (m = 0.5), conformes à la dérivation. Avec m = 1, les raies latérales valent 0.25.
