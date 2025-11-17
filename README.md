<div align="center">

# 🎧🏃 DataHub – Spotify, Strava & IA

Application web permettant de se connecter à différents services (Spotify, Strava, etc.),
de visualiser ses données et d’échanger dessus avec une intelligence artificielle intégrée.

</div>

---

## ✨ Fonctionnalités

- 🔐 Connexion à plusieurs comptes (Spotify, Strava, …)
- 📊 Visualisation de statistiques personnalisées (musique, activité, etc.)
- 🤖 Chat avec une IA à partir de tes propres données
- 🎛️ Dashboards interactifs et filtrables
- 🌐 Architecture full stack : **Angular 20** (frontend) + **Django** (backend)

---

## 🧱 Stack technique

- **Frontend** : Angular 20
- **Backend** : Django
- **Intégrations** : Spotify, Strava (et autres à venir)
- **API** : REST (Django) consommée par l’app Angular

---

##  Démarrer le projet

### 1. Prérequis

- **Node.js** + **npm**
- **Angular CLI**
- **Python 3**
- **pip**  
- (Optionnel) **venv** pour un environnement virtuel Python

---

### 2. Installation du frontend (Angular)

Depuis le dossier **frontend** :

```bash
cd frontend
npm install
ng serve --open
```
---

### 3. Installation du backend (Django)

Depuis le dossier **backend** :
Créer une environnement :
python -m venv venv

Lancer le serveur : python manage.py runserver
