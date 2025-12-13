"""
Module de traitement et nettoyage des données
VERSION CORRIGÉE pour gérer tous les formats de colonnes
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataProcessor:
    """Classe pour traiter et nettoyer les données du fichier Excel"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.df_raw = None
        self.df_clean = None
        self.rapport_nettoyage = {}
        
    def charger_donnees(self):
        """Charge les données depuis le fichier Excel"""
        print("📂 Chargement des données...")
        try:
            self.df_raw = pd.read_excel(self.file_path)
            print(f"✅ Données chargées: {len(self.df_raw)} lignes, {len(self.df_raw.columns)} colonnes")
            print(f"\n📊 Colonnes trouvées: {list(self.df_raw.columns)}")
            return True
        except FileNotFoundError:
            print(f"❌ ERREUR: Fichier '{self.file_path}' non trouvé!")
            return False
        except Exception as e:
            print(f"❌ ERREUR lors du chargement: {e}")
            return False
    
    def afficher_apercu(self):
        """Affiche un aperçu des données brutes"""
        if self.df_raw is None:
            print("⚠️ Aucune donnée chargée!")
            return
        
        print("\n" + "="*80)
        print("📋 APERÇU DES DONNÉES BRUTES")
        print("="*80)
        print(f"\n🔢 Premières lignes:\n{self.df_raw.head(10)}")
        print(f"\n📊 Informations sur les données:")
        print(self.df_raw.info())
        print(f"\n📈 Statistiques descriptives:")
        print(self.df_raw.describe())
        print(f"\n🔍 Valeurs manquantes par colonne:")
        print(self.df_raw.isnull().sum())
        print(f"\n🎯 Valeurs uniques par colonne:")
        for col in self.df_raw.columns:
            print(f"  - {col}: {self.df_raw[col].nunique()} valeurs uniques")
    
    def standardiser_colonnes(self):
        """Standardise les noms de colonnes"""
        print("\n🔧 Standardisation des noms de colonnes...")
        
        # Mapping COMPLET des noms possibles
        column_mapping = {
            # ID Client - toutes variantes
            'ID Client': 'ID_Client',
            'id client': 'ID_Client',
            'ID_client': 'ID_Client',
            'id_client': 'ID_Client',
            'Client ID': 'ID_Client',
            'client_id': 'ID_Client',
            'ClientID': 'ID_Client',
            'ID_Client': 'ID_Client',
            
            # Montant - toutes variantes
            'Montant': 'Montant',
            'montant': 'Montant',
            'Montant de la transaction': 'Montant',
            'Montant_Transaction': 'Montant',
            'montant_transaction': 'Montant',
            'MontantTransaction': 'Montant',
            'Transaction': 'Montant',
            'Amount': 'Montant',
            'Prix': 'Montant',
            
            # Date - toutes variantes
            'Date': 'Date',
            'date': 'Date',
            'Date de la transaction': 'Date',
            'Date_Transaction': 'Date',
            'date_transaction': 'Date',
            'DateTransaction': 'Date',
            'Transaction Date': 'Date',
            
            # Catégorie - toutes variantes
            'Catégorie': 'Categorie',
            'Categorie': 'Categorie',
            'categorie': 'Categorie',
            'Category': 'Categorie',
            'Catégorie de produit': 'Categorie',
            'Categorie_Produit': 'Categorie',
            'categorie_produit': 'Categorie',
            'CategorieProduit': 'Categorie',
            'Produit': 'Categorie',
            
            # Mode de paiement - toutes variantes
            'Mode de paiement': 'Mode_Paiement',
            'Mode_de_paiement': 'Mode_Paiement',
            'Paiement': 'Mode_Paiement',
            'Payment': 'Mode_Paiement',
            'Mode_Paiement': 'Mode_Paiement',
            'mode_paiement': 'Mode_Paiement',
            'ModePaiement': 'Mode_Paiement'
        }
        
        # Renommer les colonnes
        self.df_raw.rename(columns=column_mapping, inplace=True)
        
        # Supprimer les espaces
        self.df_raw.columns = self.df_raw.columns.str.strip()
        
        print(f"✅ Colonnes standardisées: {list(self.df_raw.columns)}")
        
        # Vérifier les colonnes requises
        colonnes_requises = ['ID_Client', 'Montant', 'Date', 'Categorie', 'Mode_Paiement']
        colonnes_manquantes = [col for col in colonnes_requises if col not in self.df_raw.columns]
        
        if colonnes_manquantes:
            print(f"⚠️ ATTENTION: Colonnes manquantes: {colonnes_manquantes}")
            print(f"   Colonnes disponibles: {list(self.df_raw.columns)}")
        else:
            print("✅ Toutes les colonnes requises sont présentes!")
    
    def nettoyer_donnees(self):
        """Nettoie et transforme les données"""
        print("\n🧹 Nettoyage des données en cours...")
        
        self.df_clean = self.df_raw.copy()
        nb_lignes_initial = len(self.df_clean)
        
        # 1. Supprimer les lignes vides
        self.df_clean.dropna(how='all', inplace=True)
        lignes_vides = nb_lignes_initial - len(self.df_clean)
        print(f"  ✓ Lignes vides supprimées: {lignes_vides}")
        
        # 2. Supprimer les doublons
        nb_doublons = self.df_clean.duplicated().sum()
        self.df_clean.drop_duplicates(inplace=True)
        print(f"  ✓ Doublons supprimés: {nb_doublons}")
        
        # 3. Nettoyer ID_Client
        if 'ID_Client' in self.df_clean.columns:
            self.df_clean['ID_Client'] = self.df_clean['ID_Client'].astype(str).str.strip()
            nb_avant = len(self.df_clean)
            self.df_clean = self.df_clean[self.df_clean['ID_Client'].notna()]
            self.df_clean = self.df_clean[self.df_clean['ID_Client'] != '']
            self.df_clean = self.df_clean[self.df_clean['ID_Client'] != 'nan']
            print(f"  ✓ ID_Client nettoyés ({nb_avant - len(self.df_clean)} lignes invalides supprimées)")
        
        # 4. Nettoyer et convertir Montant
        if 'Montant' in self.df_clean.columns:
            if self.df_clean['Montant'].dtype == 'object':
                self.df_clean['Montant'] = self.df_clean['Montant'].astype(str).str.replace(',', '.')
                self.df_clean['Montant'] = self.df_clean['Montant'].str.replace('€', '').str.strip()
                self.df_clean['Montant'] = self.df_clean['Montant'].str.replace(' ', '')
            
            self.df_clean['Montant'] = pd.to_numeric(self.df_clean['Montant'], errors='coerce')
            
            nb_avant = len(self.df_clean)
            self.df_clean = self.df_clean[self.df_clean['Montant'] > 0]
            print(f"  ✓ Montants nettoyés ({nb_avant - len(self.df_clean)} valeurs invalides supprimées)")
            
            self.df_clean['Montant'] = self.df_clean['Montant'].round(2)
        
        # 5. Nettoyer et convertir Date
        if 'Date' in self.df_clean.columns:
            try:
                self.df_clean['Date'] = pd.to_datetime(self.df_clean['Date'], errors='coerce')
                nb_dates_invalides = self.df_clean['Date'].isna().sum()
                
                self.df_clean = self.df_clean[self.df_clean['Date'].notna()]
                
                date_actuelle = pd.Timestamp.now()
                nb_dates_futures = (self.df_clean['Date'] > date_actuelle).sum()
                self.df_clean = self.df_clean[self.df_clean['Date'] <= date_actuelle]
                
                print(f"  ✓ Dates converties ({nb_dates_invalides + nb_dates_futures} dates invalides supprimées)")
            except Exception as e:
                print(f"  ⚠️ Erreur lors de la conversion des dates: {e}")
        
        # 6. Nettoyer Catégorie
        if 'Categorie' in self.df_clean.columns:
            self.df_clean['Categorie'] = self.df_clean['Categorie'].astype(str).str.strip()
            self.df_clean['Categorie'] = self.df_clean['Categorie'].str.title()
            
            nb_avant = len(self.df_clean)
            self.df_clean = self.df_clean[self.df_clean['Categorie'].notna()]
            self.df_clean = self.df_clean[self.df_clean['Categorie'] != 'Nan']
            self.df_clean = self.df_clean[self.df_clean['Categorie'] != '']
            print(f"  ✓ Catégories nettoyées ({nb_avant - len(self.df_clean)} valeurs vides supprimées)")
            
            print(f"    Catégories trouvées: {sorted(self.df_clean['Categorie'].unique())}")
        
        # 7. Nettoyer Mode_Paiement
        if 'Mode_Paiement' in self.df_clean.columns:
            self.df_clean['Mode_Paiement'] = self.df_clean['Mode_Paiement'].astype(str).str.strip()
            self.df_clean['Mode_Paiement'] = self.df_clean['Mode_Paiement'].str.title()
            
            nb_avant = len(self.df_clean)
            self.df_clean = self.df_clean[self.df_clean['Mode_Paiement'].notna()]
            self.df_clean = self.df_clean[self.df_clean['Mode_Paiement'] != 'Nan']
            self.df_clean = self.df_clean[self.df_clean['Mode_Paiement'] != '']
            print(f"  ✓ Modes de paiement nettoyés ({nb_avant - len(self.df_clean)} valeurs vides supprimées)")
            
            print(f"    Modes de paiement trouvés: {sorted(self.df_clean['Mode_Paiement'].unique())}")
        
        # 8. Créer colonnes dérivées
        if 'Date' in self.df_clean.columns:
            self.df_clean['Annee'] = self.df_clean['Date'].dt.year
            self.df_clean['Mois'] = self.df_clean['Date'].dt.month
            self.df_clean['Jour'] = self.df_clean['Date'].dt.day
            self.df_clean['Jour_Semaine'] = self.df_clean['Date'].dt.day_name()
            print(f"  ✓ Colonnes temporelles créées (Année, Mois, Jour, Jour_Semaine)")
        
        # Résumé
        nb_lignes_final = len(self.df_clean)
        perte = ((nb_lignes_initial - nb_lignes_final) / nb_lignes_initial * 100) if nb_lignes_initial > 0 else 0
        
        self.rapport_nettoyage = {
            'lignes_initiales': nb_lignes_initial,
            'lignes_finales': nb_lignes_final,
            'lignes_supprimees': nb_lignes_initial - nb_lignes_final,
            'pourcentage_perte': perte
        }
        
        print(f"\n✅ Nettoyage terminé!")
        print(f"  📊 Lignes initiales: {nb_lignes_initial}")
        print(f"  📊 Lignes finales: {nb_lignes_final}")
        print(f"  📊 Lignes supprimées: {nb_lignes_initial - nb_lignes_final} ({perte:.2f}%)")
    
    def valider_donnees(self):
        """Valide la qualité des données"""
        print("\n✓ Validation des données...")
        
        if self.df_clean is None or len(self.df_clean) == 0:
            print("❌ Aucune donnée à valider!")
            return False
        
        print("✅ Toutes les validations sont passées!")
        return True
    
    def sauvegarder_donnees_propres(self, output_path='data/data_kpi_clean.xlsx'):
        """Sauvegarde les données nettoyées"""
        if self.df_clean is None:
            return False
        
        try:
            self.df_clean.to_excel(output_path, index=False)
            print(f"\n💾 Données nettoyées sauvegardées: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
            return False
    
    def generer_rapport(self):
        """Génère un rapport complet"""
        print("\n" + "="*80)
        print("📊 RAPPORT DE TRAITEMENT DES DONNÉES")
        print("="*80)
        
        if self.df_clean is None:
            print("❌ Aucune donnée traitée!")
            return
        
        print(f"\n🔢 STATISTIQUES GÉNÉRALES:")
        print(f"  - Nombre de transactions: {len(self.df_clean)}")
        print(f"  - Nombre de clients uniques: {self.df_clean['ID_Client'].nunique()}")
        print(f"  - Période: du {self.df_clean['Date'].min().date()} au {self.df_clean['Date'].max().date()}")
        
        # Vérifier que les colonnes existent avant de les utiliser
        if 'Categorie' in self.df_clean.columns:
            print(f"  - Nombre de catégories: {self.df_clean['Categorie'].nunique()}")
        
        if 'Mode_Paiement' in self.df_clean.columns:
            print(f"  - Nombre de modes de paiement: {self.df_clean['Mode_Paiement'].nunique()}")
        
        if 'Montant' in self.df_clean.columns:
            print(f"\n💰 STATISTIQUES MONTANTS:")
            print(f"  - Montant total: {self.df_clean['Montant'].sum():.2f}€")
            print(f"  - Montant moyen: {self.df_clean['Montant'].mean():.2f}€")
            print(f"  - Montant médian: {self.df_clean['Montant'].median():.2f}€")
            print(f"  - Montant min: {self.df_clean['Montant'].min():.2f}€")
            print(f"  - Montant max: {self.df_clean['Montant'].max():.2f}€")
        
        if 'Categorie' in self.df_clean.columns:
            print(f"\n🏷️ RÉPARTITION PAR CATÉGORIE:")
            repartition_cat = self.df_clean['Categorie'].value_counts()
            for cat, count in repartition_cat.items():
                pct = (count / len(self.df_clean) * 100)
                print(f"  - {cat}: {count} transactions ({pct:.1f}%)")
        
        if 'Mode_Paiement' in self.df_clean.columns:
            print(f"\n💳 RÉPARTITION PAR MODE DE PAIEMENT:")
            repartition_paiement = self.df_clean['Mode_Paiement'].value_counts()
            for mode, count in repartition_paiement.items():
                pct = (count / len(self.df_clean) * 100)
                print(f"  - {mode}: {count} transactions ({pct:.1f}%)")
        
        print("\n" + "="*80)
    
    def executer_pipeline_complet(self):
        """Exécute le pipeline complet"""
        print("\n🚀 DÉMARRAGE DU PIPELINE DE TRAITEMENT")
        print("="*80)
        
        if not self.charger_donnees():
            return None
        
        self.afficher_apercu()
        self.standardiser_colonnes()
        self.nettoyer_donnees()
        self.valider_donnees()
        self.generer_rapport()
        self.sauvegarder_donnees_propres()
        
        print("\n✅ PIPELINE TERMINÉ AVEC SUCCÈS!")
        
        return self.df_clean


def traiter_donnees(file_path='data/data_kpi.xlsx'):
    processor = DataProcessor(file_path)
    return processor.executer_pipeline_complet()


if __name__ == "__main__":
    print("🧪 TEST DU MODULE DE TRAITEMENT")
    df_clean = traiter_donnees('data/data_kpi.xlsx')
    
    if df_clean is not None:
        print("\n✅ Module testé avec succès!")
    else:
        print("\n❌ Erreur lors du test du module")