# fastapi-devops-aws 🚀

![CI/CD](https://github.com/Wisdomuzochi/fastapi-devops-aws/actions/workflows/deploy.yml/badge.svg)
![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)
![AWS ECR](https://img.shields.io/badge/AWS-ECR-orange?logo=amazon-aws)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)

Une **API REST prête pour la production**, construite avec FastAPI, conteneurisée avec Docker, et livrée automatiquement sur **AWS Elastic Container Registry (ECR)** via un pipeline **GitHub Actions** entièrement automatisé.

> Ce projet illustre un cycle DevOps complet : du développement local jusqu'à la livraison d'un artefact cloud — sans aucune intervention manuelle à chaque push sur `main`.

---

## Architecture

```
Développeur (git push)
       │
       ▼
┌──────────────────────┐
│   GitHub Actions     │  ← Pipeline CI/CD déclenché sur push vers main
│                      │
│  1. Checkout code    │
│  2. Configure AWS    │
│  3. Login vers ECR   │
│  4. Docker build     │
│  5. Docker push      │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│      AWS ECR         │  ← Registre privé d'images Docker
│  (eu-west-3 / Paris) │
│                      │
│  Image taguée avec   │
│  le SHA du commit    │  ← Traçabilité complète : image ↔ commit
└──────────────────────┘
```

---

## Fonctionnalités

- `GET /` — Point d'entrée racine avec un message de bienvenue
- `GET /health` — Health check renvoyant le statut du serveur, l'uptime et la version Python
- `GET /docs` — Documentation interactive auto-générée (Swagger UI)

L'endpoint `/health` suit les standards de production — il est conçu pour être interrogé par les load balancers et les orchestrateurs (AWS ECS, Kubernetes) afin de vérifier la disponibilité du service.

---

## Stack technique

| Couche | Technologie |
|---|---|
| Framework API | FastAPI 0.111.0 |
| Serveur ASGI | Uvicorn 0.29.0 |
| Conteneurisation | Docker (python:3.11-slim) |
| CI/CD | GitHub Actions |
| Registre d'images | AWS Elastic Container Registry (ECR) |
| Cloud | AWS (eu-west-3 — Paris) |

---

## Structure du projet

```
fastapi-devops-aws/
├── .github/
│   └── workflows/
│       └── deploy.yml      # Pipeline CI/CD GitHub Actions
├── app/
│   ├── __init__.py
│   └── main.py             # Application FastAPI
├── Dockerfile              # Image Docker optimisée multi-couches
├── .dockerignore
├── requirements.txt        # Dépendances versionnées (pinned)
└── .gitignore
```

---

## Démarrage rapide

### Prérequis

- Python 3.11+
- Docker

### Lancer en local (sans Docker)

```bash
# Cloner le repo
git clone git@github.com:Wisdomuzochi/fastapi-devops-aws.git
cd fastapi-devops-aws

# Créer et activer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
uvicorn app.main:app --reload --port 8000
```

API disponible sur : `http://localhost:8000`
Documentation interactive : `http://localhost:8000/docs`

### Lancer avec Docker

```bash
# Construire l'image
docker build -t fastapi-devops-aws .

# Lancer le conteneur
docker run -p 8000:8000 fastapi-devops-aws
```

---

## Pipeline CI/CD

Le pipeline est défini dans `.github/workflows/deploy.yml` et se déclenche automatiquement à chaque push sur `main`.

```
push sur main
     │
     ├── Checkout du code
     ├── Configuration des credentials AWS (via GitHub Secrets)
     ├── Authentification Docker vers AWS ECR
     ├── Build de l'image Docker
     └── Push de l'image vers ECR (taguée avec le SHA du commit Git)
```

### Secrets GitHub requis

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | Clé d'accès de l'utilisateur IAM |
| `AWS_SECRET_ACCESS_KEY` | Clé secrète de l'utilisateur IAM |

L'utilisateur IAM (`github-actions-ecr`) applique le **principe du moindre privilège** — il ne dispose que de la permission `AmazonEC2ContainerRegistryFullAccess`.

### Image sur AWS ECR

```
884404665409.dkr.ecr.eu-west-3.amazonaws.com/fastapi-devops-aws:<git-sha>
```

Chaque image est taguée avec le SHA exact du commit Git, garantissant une traçabilité complète entre l'artefact déployé et son code source.

---

## Concepts DevOps illustrés

- **Dependency pinning** — versions exactes dans `requirements.txt` pour des builds reproductibles
- **Docker layer caching** — `requirements.txt` copié avant le code source pour optimiser le temps de build
- **IAM least-privilege** — credentials du pipeline limités à ECR uniquement
- **GitHub Secrets** — aucune clé stockée dans le code
- **Traçabilité des artefacts** — chaque image taguée avec son SHA de commit
- **Health check endpoint** — route `/health` conforme aux standards des orchestrateurs

---

## Auteur

**Wisdom MUONAKA**
[GitHub](https://github.com/Wisdomuzochi) · [LinkedIn](https://linkedin.com/in/wisdom-muonaka-45781b321)