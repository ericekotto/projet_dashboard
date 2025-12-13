# Dashboard KPI - Analyse des Ventes

## 📊 Description
Dashboard interactif pour l'analyse des ventes d'une entreprise de commerce en ligne.

## 🚀 Installation

### 1. Créer l'environnement Anaconda
```bash
conda create -n dashboard_env python=3.10 -y
conda activate dashboard_env
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Générer les données (si nécessaire)
```bash
python generer_donnees.py
```

### 4. Lancer l'application
```bash
python app.py
```

### 5. Ouvrir dans le navigateur
Aller à : http://127.0.0.1:8050

## 📁 Structure du projet
```
projet_dashboard/
├── data/
│   └── data_kpi.xlsx
├── assets/
│   └── style.css
├── app.py
├── data_processing.py
├── generer_donnees.py
├── test_traitement.py
├── requirements.txt
└── README.md
```

## 🎯 Fonctionnalités
- Calcul automatique des KPI
- Filtres interactifs par date et catégorie
- 6 onglets d'analyse détaillée
- Graphiques interactifs Plotly
- Design moderne et responsive

## 👨‍💻 Auteur
Projet de TP - Analyse décisionnelle
