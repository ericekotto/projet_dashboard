"""
Script de test pour vérifier le traitement des données
"""

from data_processing import DataProcessor
import pandas as pd

def tester_traitement():
    """Teste le processus de traitement des données"""
    
    print("="*80)
    print("🧪 TEST DU TRAITEMENT DES DONNÉES")
    print("="*80)
    
    # Créer une instance du processeur
    processor = DataProcessor('data/data_kpi.xlsx')
    
    # Tester chaque étape individuellement
    print("\n📌 ÉTAPE 1: Chargement des données")
    if processor.charger_donnees():
        print("✅ Chargement réussi")
        print(f"   Nombre de lignes: {len(processor.df_raw)}")
        print(f"   Colonnes: {list(processor.df_raw.columns)}")
    else:
        print("❌ Échec du chargement")
        return
    
    print("\n📌 ÉTAPE 2: Affichage de l'aperçu")
    processor.afficher_apercu()
    
    print("\n📌 ÉTAPE 3: Standardisation des colonnes")
    processor.standardiser_colonnes()
    print(f"✅ Colonnes après standardisation: {list(processor.df_raw.columns)}")
    
    print("\n📌 ÉTAPE 4: Nettoyage des données")
    processor.nettoyer_donnees()
    print(f"✅ Données nettoyées: {len(processor.df_clean)} lignes")
    
    print("\n📌 ÉTAPE 5: Validation")
    if processor.valider_donnees():
        print("✅ Validation réussie")
    else:
        print("⚠️ Validation avec avertissements")
    
    print("\n📌 ÉTAPE 6: Génération du rapport")
    processor.generer_rapport()
    
    print("\n📌 ÉTAPE 7: Sauvegarde")
    if processor.sauvegarder_donnees_propres():
        print("✅ Sauvegarde réussie")
    
    print("\n📌 ÉTAPE 8: Vérification des données nettoyées")
    print("\nAperçu des données finales:")
    print(processor.df_clean.head())
    print("\nTypes de données:")
    print(processor.df_clean.dtypes)
    print("\nStatistiques:")
    print(processor.df_clean.describe())
    
    print("\n" + "="*80)
    print("✅ TEST TERMINÉ AVEC SUCCÈS!")
    print("="*80)
    
    return processor.df_clean


if __name__ == "__main__":
    df_propre = tester_traitement()
    
    if df_propre is not None:
        print("\n💡 CONSEILS:")
        print("  1. Vérifiez le fichier 'data/data_kpi_clean.xlsx' créé")
        print("  2. Les données sont maintenant prêtes pour l'analyse")
        print("  3. Utilisez ce fichier nettoyé dans votre dashboard")