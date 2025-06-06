DataVibes

📝 Description
Datavibes est une application Django minimaliste qui combine deux fonctionnalités : 
l’affichage d’une citation inspirante liée à la data science chaque jour, et la 
récupération automatique des dernières actualités du domaine via web scraping. 
Le site s’appuie sur une base de données, une interface web simple, et un pipeline 
CI/CD complet avec GitHub, Jenkins et Docker. Un projet idéal pour illustrer une 
application backend fonctionnelle avec automatisation du déploiement.

Datavibes - Data Science Daily est une application Django minimaliste qui combine :

- 📌 Une citation inspirante quotidienne sur la data science
- 📰 Un scraper automatique des dernières actualités du domaine

🏗 Structure du Projet

<pre> ```
Exam_con_vir/
├── datavibes/               # Configuration du projet
│   ├── __init__.py
│   ├── settings.py          # Paramètres
│   ├── urls.py              # URLs globaux
│   ├── asgi.py    
│   └── wsgi.py
├── main/          # Application principale
│   ├── migrations/          # Migrations de la base de données
│   ├── templates/           # Templates HTML
│   │   └── datavibes/
│   │       ├── base.html    # Template de base
│   │       ├── home.html    # Page d'accueil
│   │       ├── daily_quote.html  # Citations
│   │       └── news_list.html    # Actualités
│   ├── __init__.py
│   ├── admin.py             # Configuration admin
│   ├── apps.py
│   ├── models.py            # Modèles de données
│   ├── tests.py
│   ├── urls.py              # URLs de l'application
│   ├── views.py             # Vues
│   └── utils.py             # Fonctions de scraping
├── manage.py
├── requirements.txt         
├── Dockerfile   
├── Jenkinsfile
└── README.md
``` </pre>


🎯 Fonctionnalités
1. Citations Quotidiennes (Inspire)
    - 💬 Affiche une citation inspirante différente chaque jour

    - ✍️ Stockée en base de données avec auteur et date

    - 📅 Met à jour automatiquement la citation du jour

2. Scraper d'Actualités 

🤖 Récupère automatiquement les articles depuis :
    - Towards Data Science
    - KDnuggets
    - Data Science Central
    - Reddit Data Science

📆 Conserve l'historique des articles

🔍 Filtre les doublons

🛠 Configuration Technique

Modèles de Données

<pre>```
class DailyQuote(models.Model):
    quote = models.TextField()  # La citation
    author = models.CharField(max_length=200)  # L'auteur
    date = models.DateField(default=timezone.now, unique=True)  # Date

class DataScienceNews(models.Model):
    title = models.CharField(max_length=300)  # Titre de l'article
    url = models.URLField()  # Lien vers l'article
    source = models.CharField(max_length=100)  # Source
    summary = models.TextField(blank=True)  # Résumé
    publish_date = models.DateField()  # Date de publication

```</pre>

Fonctionnement du Scraper
Le scraper utilise :

📡 Les flux RSS des sites pour une récupération fiable

⏱ Un système de cache pour éviter les doublons

📊 Une journalisation détaillée des opérations

🐳 Déploiement avec Docker
Construire l'image :

<pre> ``` 
docker build -t datavibes . ```
</pre>

Lancer le conteneur :

<pre> ```
docker run -p 8000:8000 datavibes  ```
</pre>


🔄 Pipeline CI/CD
Le projet inclut :

- 🔗 Intégration avec GitHub

- 🚀 Déploiement automatique via Jenkins

- 📦 Containerisation avec Docker

- 💡 Idées d'Amélioration

- 🔍 Ajouter plus de sources d'actualités

- 📊 Tableau de bord des citations populaires

- 🔔 Notifications par email des nouvelles actualités

- 🔄 Planification automatique du scraping


Ce projet illustre parfaitement une application Django fonctionnelle avec :

- ✅ Une base de données

- 🌐 Une interface web simple

- 🤖 Un système automatisé de collecte de données

- 🛠 Un pipeline CI/CD complet