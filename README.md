# 💰 BudgetWise - Application de Gestion de Budget Personnel

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3+-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Une application web moderne et intuitive pour gérer votre budget personnel, suivre vos revenus et dépenses, et visualiser vos statistiques financières.

## ✨ Fonctionnalités

### 🎯 Fonctionnalités Principales
- **Gestion des Revenus** : Ajout, modification et suppression de revenus
- **Gestion des Dépenses** : Suivi détaillé des dépenses par catégorie
- **Budget Mensuel** : Définition et suivi de budgets mensuels
- **Tableau de Bord** : Vue d'ensemble avec statistiques en temps réel
- **Catégorisation** : Organisation des dépenses par catégories personnalisables
- **Tags** : Système de tags pour une meilleure organisation
- **Graphiques** : Visualisation des données avec Chart.js

### 🔐 Sécurité
- **Authentification JWT** : Système d'authentification sécurisé
- **Chiffrement des mots de passe** : Utilisation de bcrypt
- **Validation des données** : Validation côté serveur avec Pydantic

### 📊 Statistiques et Rapports
- **Solde en temps réel** : Calcul automatique du solde actuel
- **Statistiques mensuelles** : Revenus, dépenses et balance par mois
- **Répartition par catégorie** : Graphiques en secteurs des dépenses
- **Transactions récentes** : Historique des dernières opérations

## 🛠️ Technologies Utilisées

### Backend
- **FastAPI** : Framework web moderne et rapide
- **SQLAlchemy** : ORM pour la gestion de base de données
- **Pydantic** : Validation et sérialisation des données
- **JWT** : Authentification par tokens
- **MySQL** : Base de données relationnelle

### Frontend
- **HTML5/CSS3** : Structure et style modernes
- **Bootstrap 5** : Framework CSS responsive
- **JavaScript ES6+** : Interactivité côté client
- **Chart.js** : Graphiques interactifs
- **Font Awesome** : Icônes vectorielles

### DevOps
- **GitHub Actions** : CI/CD automatisé
- **pytest** : Tests unitaires
- **flake8** : Linting du code
- **black** : Formatage automatique du code

## 🚀 Installation et Configuration

### Prérequis
- Python 3.11+
- MySQL 8.0+
- Node.js (optionnel, pour le développement frontend)

### Installation

1. **Cloner le repository**
```bash
git clone https://github.com/votre-username/budgetwise.git
cd budgetwise
```

2. **Configuration de l'environnement backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

3. **Configuration de la base de données**
```bash
# Créer la base de données MySQL
mysql -u root -p
CREATE DATABASE budget_db;
exit

# Configurer les variables d'environnement
cp .env.example .env
# Éditer le fichier .env avec vos paramètres
```

4. **Lancer l'application**
```bash
# Backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# L'application sera accessible sur http://localhost:8000
```

## 📁 Structure du Projet

```
budgetwise/
├── backend/
│   ├── main.py                 # Point d'entrée de l'application
│   ├── config.py              # Configuration de l'application
│   ├── database.py            # Configuration de la base de données
│   ├── models.py              # Modèles SQLAlchemy
│   ├── schemas.py             # Schémas Pydantic
│   ├── crud.py                # Opérations CRUD
│   ├── routes/                # Routes API
│   │   ├── auth.py           # Authentification
│   │   ├── budget.py         # Gestion des budgets
│   │   ├── expenses.py       # Gestion des dépenses
│   │   ├── revenues.py       # Gestion des revenus
│   │   ├── categories.py     # Gestion des catégories
│   │   └── tags.py           # Gestion des tags
│   ├── services/              # Services métier
│   │   ├── auth.py           # Service d'authentification
│   │   └── budget_service.py # Service de calculs budgétaires
│   ├── tests/                 # Tests unitaires
│   └── requirements.txt       # Dépendances Python
├── frontend/
│   ├── index.html            # Page principale
│   ├── assets/
│   │   ├── css/
│   │   │   └── style.css     # Styles personnalisés
│   │   └── js/
│   │       └── script.js     # JavaScript principal
├── .github/
│   └── workflows/
│       └── ci.yml            # Pipeline CI/CD
├── .flake8                   # Configuration du linting
└── README.md                 # Documentation
```

## 🧪 Tests

### Lancer les tests
```bash
cd backend
pytest --cov=. --cov-report=html
```

### Linting et formatage
```bash
# Vérification du style de code
flake8 .

# Formatage automatique
black .
```

## 🚀 Déploiement

### Déploiement sur Render

1. **Préparer l'application**
   - Assurez-vous que tous les tests passent
   - Configurez les variables d'environnement de production

2. **Configuration Render**
   - Créez un nouveau service Web sur Render
   - Connectez votre repository GitHub
   - Configurez les variables d'environnement

3. **Variables d'environnement requises**
```
DB_URL=mysql+pymysql://user:password@host:port/database
SECRET_KEY=your-secret-key
```

### CI/CD avec GitHub Actions

Le pipeline CI/CD automatique :
- ✅ Exécute les tests sur chaque push
- ✅ Vérifie le style de code avec flake8
- ✅ Formate le code avec black
- ✅ Déploie automatiquement sur la branche main

## 📖 API Documentation

Une fois l'application lancée, la documentation interactive de l'API est disponible sur :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

### Endpoints principaux

#### Authentification
- `POST /auth/register` - Créer un compte
- `POST /auth/login` - Se connecter

#### Budget
- `GET /budgets/dashboard` - Statistiques du tableau de bord
- `POST /budgets/` - Créer/modifier un budget
- `GET /budgets/` - Lister les budgets

#### Transactions
- `POST /revenues/` - Ajouter un revenu
- `GET /revenues/` - Lister les revenus
- `POST /expenses/` - Ajouter une dépense
- `GET /expenses/` - Lister les dépenses

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. **Fork** le projet
2. **Créer** une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. **Commit** vos changements (`git commit -m 'Add some AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrir** une Pull Request

### Guidelines de contribution
- Suivez les conventions de code existantes
- Ajoutez des tests pour les nouvelles fonctionnalités
- Mettez à jour la documentation si nécessaire
- Assurez-vous que tous les tests passent

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👥 Auteurs

- **Votre Nom** - *Développeur principal* - [VotreGitHub](https://github.com/votre-username)

## 🙏 Remerciements

- [FastAPI](https://fastapi.tiangolo.com/) pour le framework backend
- [Bootstrap](https://getbootstrap.com/) pour le framework CSS
- [Chart.js](https://www.chartjs.org/) pour les graphiques
- [Font Awesome](https://fontawesome.com/) pour les icônes

## 📞 Support

Si vous avez des questions ou des problèmes :
- 📧 Email : votre.email@example.com
- 🐛 Issues : [GitHub Issues](https://github.com/votre-username/budgetwise/issues)
- 💬 Discussions : [GitHub Discussions](https://github.com/votre-username/budgetwise/discussions)

---

⭐ **N'oubliez pas de donner une étoile au projet si vous l'avez trouvé utile !**