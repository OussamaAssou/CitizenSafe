# CitizenSafe

CitizenSafe est une application web conçue pour améliorer la sécurité des citoyens en facilitant la communication entre les citoyens, les policiers et les facteurs. L'application permet aux utilisateurs de signaler des incidents, de soumettre des observations et d'optimiser les patrouilles de police.

## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Technologies utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Contribuer](#contribuer)
- [License](#license)

## Fonctionnalités

- **Inscription et connexion** : Les utilisateurs peuvent s'inscrire et se connecter à l'application.
- **Signalement d'incidents** : Les policiers peuvent créer des rapports d'incidents.
- **Observations** : Les facteurs peuvent soumettre des observations concernant des activités suspectes.
- **Optimisation des patrouilles** : Les policiers peuvent optimiser leurs patrouilles en fonction des zones à risque.
- **Conseils de sécurité** : Les utilisateurs peuvent consulter des conseils de sécurité.

## Technologies utilisées

- Django
- Django REST Framework
- SQLite (ou tout autre SGBD compatible)
- HTML, CSS, JavaScript (pour le frontend)

## Installation

1. Clonez le dépôt :
   bash
   git clone https://github.com/votre-utilisateur/CitizenSafe.git
   cd CitizenSafe
2. Créez un environnement virtuel :
    bash
    python -m venv env
    source env/bin/activate  # Sur Windows utilisez `env\Scripts\activate`

3. Installez les dépendances :
    bash
    pip install -r requirements.txt

4. Effectuez les migrations :
    bash
    python manage.py migrate
  
5. Créez un super utilisateur pour accéder à l'interface d'administration :
    bash
    python manage.py createsuperuser

6. Démarrez le serveur de développement :
    bash
    python manage.py runserver

## Configuration
1. Assurez-vous que le fichier settings.py est correctement configuré pour votre environnement. Vous pouvez également définir votre modèle d'utilisateur personnalisé si nécessaire.
   
## Utilisation
1. Accédez à l'application via http://127.0.0.1:8000/.
2. Inscrivez-vous ou connectez-vous en tant que citoyen, policier ou facteur.
3. Utilisez les différentes fonctionnalités disponibles dans l'application.
