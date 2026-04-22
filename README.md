# Ba7ath Project — Graphiques de comparaison de l’inflation (Tunisie)

Ce dépôt contient **2 scripts Python** pour charger un dataset CSV (inflation en Tunisie), **nettoyer des valeurs de pourcentage** (ex: `5,30%`, `~6,5%`, `N/A`) et **générer un graphique PNG**.

Les scripts sont **“Créés par: Ba7ath Project Team”**.

## Scripts

- **`convert_compare_csv.py`**
  - **But**: comparer l’inflation entre plusieurs sources: **INS (réel)**, **FMI**, **BM**, **BAD**
  - **Sortie par défaut**: `inflation_comparaison_tunisie.png`

- **`convert_compare_ins_bm.py`**
  - **But**: comparer l’inflation entre **INS (réel)** et **BM** (Banque mondiale)
  - **Sortie par défaut**: `inflation_compare.png`

## Installation

### Prérequis

- **Python 3.9+** (recommandé)

### Dépendances

Le fichier `requirements.txt` contient les dépendances:
- `pandas`
- `numpy`
- `matplotlib`

Installe-les avec:

```bash
python -m pip install -r requirements.txt
```

## Exécution

Les deux scripts acceptent:
- **`--csv`**: chemin du CSV d’entrée
- **`--out`**: chemin du PNG généré

### 1) Comparaison multi-sources (INS/FMI/BM/BAD)

```bash
python convert_compare_csv.py --csv "Inflation-Tunisie.csv" --out "inflation_tunisie.png"
```

### 2) Comparaison INS vs BM

```bash
python convert_compare_ins_bm.py --csv "Inflation-Tunisie.csv" --out "inflation_ins_vs_bm.png"
```

## Format attendu du dataset (CSV)

### Encodage

- Le CSV est lu en **UTF-8** (variante **`utf-8-sig`** supportée, utile si le fichier vient d’Excel sous Windows).

### Colonnes minimales

Pour que les scripts fonctionnent, le CSV doit contenir:

- **`Année`**: entier (ex: `2020`)
- **`INS (réel)`**: pourcentage en texte ou nombre

Ensuite, selon le script:

- **`convert_compare_csv.py`** attend aussi: **`FMI`**, **`BM`**, **`BAD`**
- **`convert_compare_ins_bm.py`** attend aussi: **`BM`**

La colonne **`Notes`** est optionnelle (elle n’est pas utilisée pour le tracé).

### Formats de valeurs acceptés

Les valeurs des colonnes sources peuvent être:

- **Pourcentages au format “FR”**: `5,30%`
- **Avec un tilde**: `~6,5%`
- **Valeur manquante**: `N/A`
- **Ou numérique**: `5` / `5.3`

### Exemple de lignes

```csv
Année,INS (réel),FMI,BM,BAD,Notes
2020,"5,30%","5,50%","5,60%","5,40%",Alignement fort
2026,5%,"6,50%",N/A,N/A,Projection FMI
```

## Fichiers de données (exemples présents)

- `Inflation-Tunisie.csv`: dataset principal (INS/FMI/BM/BAD)
- `Anne-INS-BanquemondialeIPC.csv`: dataset alternatif possible (vérifie juste qu’il contient les colonnes attendues)

