from fastapi import FastAPI
import platform
import time

# L'heure de démarrage du serveur, enregistrée une seule fois
START_TIME = time.time()

app = FastAPI(
    title="DevOps Demo API",
    description="A simple API built to practice Docker, CI/CD and AWS deployment.",
    version="1.0.0",
)


@app.get("/")
def root():
    """Point d'entrée racine."""
    return {"message": "API is running. Go to /health for status."}


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    Utilisé par les load balancers et orchestrateurs (ECS, Kubernetes)
    pour vérifier que le service est vivant.
    """
    uptime_seconds = round(time.time() - START_TIME, 2)

    return {
        "status": "healthy",
        "uptime_seconds": uptime_seconds,
        "python_version": platform.python_version(),
        "system": platform.system(),
    }