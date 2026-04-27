# ── Étape 1 : image de base ──────────────────────────────────────────
FROM python:3.11-slim

# ── Étape 2 : dossier de travail dans le conteneur ──────────────────
WORKDIR /app

# ── Étape 3 : dépendances en premier (optimisation cache Docker) ─────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Étape 4 : copie du code source ──────────────────────────────────
COPY app/ ./app/

# ── Étape 5 : port exposé (documentation, pas une règle firewall) ────
EXPOSE 8000

# ── Étape 6 : commande de démarrage ─────────────────────────────────
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]