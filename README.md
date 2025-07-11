# MBAESG_EVALUATION_MANAGEMENT_OPERATIONNEL 

## Répartition des tâches entre les membres de l’équipe

Ce projet a été réalisé en binôme par **Paola NGOUADJEL** et **Vylaivane PHOMMAHAXAY**.

## Présentation du projet

Dans le cadre de notre formation, nous avons travaillé sur un projet de data visualisation en utilisant Streamlit.  
L’objectif était de créer une application web interactive qui permet de :

- charger un fichier CSV (avec des données Airbnb),
- interroger et analyser les données avec DuckDB,
- afficher des KPIs utiles (comme le nombre de logements ou la disponibilité moyenne),
- visualiser les résultats à travers des graphiques dynamiques.

On a aussi intégré des filtres (quartier, date, etc.) pour rendre l’analyse plus personnalisable.

---

## Fonctionnalités

- Téléversement d’un fichier CSV
- Requêtes SQL exécutées avec DuckDB directement dans l’appli
- Visualisation de 4 indicateurs clés avec Matplotlib/Seaborn
- Filtres dynamiques par quartier, date, nom…
- Interface simple et rapide à prendre en main

---

## Arborescence du projet

stream_application/
├── data/
│   ├── Airbnb_Open_Data.csv
│   └── app.py
├── requirements.txt
└── README.md

## Ce qu'on a appris:
Ce projet nous a permis de :
	•	manipuler DuckDB pour interroger des données localement sans base distante,
	•	créer une interface claire et interactive avec Streamlit,
	•	mieux collaborer via Git/GitHub,
	•	structurer un projet data de A à Z.

⸻

Merci de votre attention ! N’hésitez pas à tester le projet et explorer le code 

## Instructions d’installation
1. Cloner le projet :
```bash
git clone https://github.com/Paolangd/stream_application.git
cd stream_application

python -m venv .venv
source .venv/bin/activate  # Pour Mac/Linux
# ou
.venv\Scripts\activate  # Pour Windows

pip install -r requirements.txt

streamlit run data/app.py

