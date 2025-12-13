"""
Script d'installation automatique du projet Dashboard KPI
Exécutez ce script pour créer TOUS les fichiers nécessaires
"""

import os

print("="*70)
print("🚀 INSTALLATION DU PROJET DASHBOARD KPI")
print("="*70)

# Créer la structure des dossiers
print("\n📁 Création de la structure des dossiers...")
folders = ['data', 'assets']
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"  ✅ Dossier '{folder}' créé")
    else:
        print(f"  ✓ Dossier '{folder}' existe déjà")

# Créer requirements.txt
print("\n📝 Création de requirements.txt...")
requirements_content = """dash==2.14.2
plotly==5.18.0
pandas==2.1.4
openpyxl==3.1.2
gunicorn==21.2.0"""

with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write(requirements_content)
print("  ✅ requirements.txt créé")

# Créer .gitignore
print("\n📝 Création de .gitignore...")
gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Anaconda
.conda/
.ipynb_checkpoints/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Données temporaires
*.tmp
*.bak
data_kpi_clean.xlsx"""

with open('.gitignore', 'w', encoding='utf-8') as f:
    f.write(gitignore_content)
print("  ✅ .gitignore créé")

# Créer Procfile
print("\n📝 Création de Procfile...")
procfile_content = "web: gunicorn app:server"

with open('Procfile', 'w', encoding='utf-8') as f:
    f.write(procfile_content)
print("  ✅ Procfile créé")

# Créer README.md
print("\n📝 Création de README.md...")
readme_content = """# Dashboard KPI - Analyse des Ventes

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
"""

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)
print("  ✅ README.md créé")

# Afficher le résumé
print("\n" + "="*70)
print("✅ INSTALLATION TERMINÉE !")
print("="*70)
print("\n📁 Structure créée:")
print("""
projet_dashboard/
├── data/
├── assets/
├── requirements.txt
├── .gitignore
├── Procfile
└── README.md
""")

print("\n🎯 PROCHAINES ÉTAPES:")
print("="*70)
print("""
1. Si vous n'avez PAS de fichier data_kpi.xlsx:
   → Exécutez: python generer_donnees.py
   
2. Copiez les fichiers Python depuis les artifacts:
   → data_processing.py
   → app.py
   → test_traitement.py
   
3. Copiez le fichier CSS:
   → assets/style.css
   
4. Installez les dépendances:
   → pip install -r requirements.txt
   
5. Lancez l'application:
   → python app.py
""")
print("="*70)