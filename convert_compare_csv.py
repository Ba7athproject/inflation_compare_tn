import pandas as pd
import numpy as np
import logging
import argparse

# Configuration du logging pour tracer les erreurs (Bonne pratique OSINT/Data)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_data(filepath: str) -> pd.DataFrame:
    """Charge le fichier CSV avec gestion d'erreur."""
    try:
        # utf-8-sig gère le BOM éventuel (fréquent sur Windows/Excel)
        df = pd.read_csv(filepath, encoding="utf-8-sig")
        logging.info(f"Fichier '{filepath}' chargé avec succès.")
        return df
    except FileNotFoundError:
        logging.error(f"Le fichier '{filepath}' est introuvable.")
        raise
    except Exception as e:
        logging.error(f"Erreur inattendue lors de la lecture : {e}")
        raise

def clean_percentage(val) -> float:
    """
    Nettoie les chaînes de caractères représentant des pourcentages.
    Convertit les formats '5,3%', '~5,5%' ou 'N/A' en float (ou NaN).
    """
    if pd.isna(val) or str(val).strip().upper() == 'N/A':
        return np.nan
    
    if isinstance(val, str):
        # Nettoyage des caractères parasites et conversion de la virgule
        val_clean = val.replace('%', '').replace(',', '.').replace('~', '').strip()
        try:
            return float(val_clean)
        except ValueError:
            logging.warning(f"Impossible de convertir la valeur : '{val}' en float.")
            return np.nan
    return float(val)

def generate_inflation_chart(df: pd.DataFrame, output_file: str = "inflation_tunisie.png"):
    """
    Génère et sauvegarde le graphique de comparaison.
    """
    try:
        import matplotlib.pyplot as plt  # pyright: ignore[reportMissingImports]
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            "Dépendance manquante: matplotlib. Installez-la avec "
            "`python -m pip install matplotlib` (ou `pip install -r requirements.txt`) "
            "et assurez-vous que votre IDE utilise le même interpréteur Python."
        ) from e

    # 1. Préparation des données
    sources = ['INS (réel)', 'FMI', 'BM', 'BAD']
    
    # Création d'une copie pour ne pas altérer le DataFrame d'origine
    df_clean = df.copy()
    
    # Application de la fonction de nettoyage sur chaque colonne source
    for col in sources:
        df_clean[col] = df_clean[col].apply(clean_percentage)
        
    # 2. Configuration du graphique
    plt.figure(figsize=(10, 6))
    
    # Palette de couleurs sobre (accessible aux daltoniens et adaptée au web)
    colors = {'INS (réel)': '#e63946', 'FMI': '#1d3557', 'BM': '#457b9d', 'BAD': '#2a9d8f'}
    markers = {'INS (réel)': 'o', 'FMI': 's', 'BM': '^', 'BAD': 'D'}
    
    # 3. Tracé des courbes
    for source in sources:
        # Masquer les valeurs NaN pour éviter de briser les courbes
        mask = df_clean[source].notna()
        plt.plot(df_clean['Année'][mask], df_clean[source][mask], 
                 marker=markers[source], color=colors[source], 
                 linewidth=2, label=source, markersize=8)

    # 4. Habillage du graphique
    plt.title('Comparaison des taux d\'inflation en Tunisie selon différentes sources (2020-2026)', 
              fontsize=14, pad=15, fontweight='bold')
    plt.xlabel('Année', fontsize=12, fontweight='bold')
    plt.ylabel('Taux d\'inflation (%)', fontsize=12, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='Sources', fontsize=10, title_fontsize=11)
    
    # S'assurer que toutes les années s'affichent correctement sur l'axe X
    plt.xticks(df_clean['Année'])

    # Mention (footer)
    plt.figtext(
        0.99,
        0.01,
        "Powered by: Ba7ath Project Team",
        ha="right",
        va="bottom",
        fontsize=9,
        color="#555555",
    )
    
    # 5. Sauvegarde
    plt.tight_layout()
    try:
        plt.savefig(output_file, dpi=300) # Haute résolution pour la publication
        logging.info(f"Graphique sauvegardé sous : {output_file}")
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde du graphique : {e}")

# --- Exécution principale (Point d'entrée) ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Génère un graphique de comparaison des taux d'inflation.")
    parser.add_argument(
        "--csv",
        default="Inflation-Tunisie.csv",
        help="Chemin du fichier CSV (par défaut: Inflation-Tunisie.csv)",
    )
    parser.add_argument(
        "--out",
        default="inflation_comparaison_tunisie.png",
        help="Nom du fichier image de sortie (PNG).",
    )
    args = parser.parse_args()

    fichier_csv = args.csv
    try:
        donnees = load_data(fichier_csv)
        generate_inflation_chart(donnees, args.out)
    except Exception as e:
        print("L'exécution du script a échoué. Vérifiez les logs.")