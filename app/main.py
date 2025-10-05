from fastapi import FastAPI
from app.endpoints import predict, insights
from app.services.data_service import load_data_from_mlflow
import os
import logging
from dotenv import load_dotenv
import dagshub
import mlflow
import pandas as pd

# --- Environment and Logging Setup ---
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Configuration ---
MODEL_NAME = os.getenv("MLFLOW_MODEL_NAME", "airbnb_pricing_model_simple_sevilla")
MODEL_STAGE = os.getenv("MLFLOW_MODEL_STAGE", "latest")

app = FastAPI(
    title="Airbnb Pricing API con MLflow",
    description="API para la predicción de precios de alquileres de Airbnb y análisis de mercado, utilizando modelos de MLflow.",
    version="3.0.0"
)

@app.on_event("startup")
def startup_event():
    """
    Carga el modelo y los datos como artefactos desde MLflow al iniciar la aplicación.
    """
    logger.info("Iniciando la carga de artefactos desde MLflow...")
    
    # --- DagsHub & MLflow Integration ---
    try:
        dagshub.init(repo_owner=os.getenv("DAGSHUB_REPO_OWNER"), repo_name=os.getenv("DAGSHUB_REPO_NAME"), mlflow=True)
        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
        logger.info("MLflow tracking URI configurado exitosamente.")
    except Exception as e:
        logger.error("Fallo al inicializar DagsHub/MLflow: %s", e)
        raise RuntimeError("No se pudo conectar al servidor de tracking de MLflow.") from e

    # --- Load Model ---
    model_uri = f"models:/{MODEL_NAME}/{MODEL_STAGE}"
    logger.info("Intentando cargar el modelo desde la URI: %s", model_uri)
    try:
        app.state.model = mlflow.pyfunc.load_model(model_uri)
        logger.info("✅ Modelo cargado exitosamente.")
    except mlflow.exceptions.MlflowException as e:
        logger.error("❌ Fallo al cargar el modelo desde el registro de MLflow: %s", e)
        raise RuntimeError(f"No se pudo encontrar o cargar el modelo '{model_uri}'.") from e

    # --- Load Data Artifact ---
    app.state.data, app.state.global_average_price = load_data_from_mlflow(app.state.model)


# Incluir los routers de los endpoints
app.include_router(predict.router, prefix="/api/v1", tags=["Predictions"])
app.include_router(insights.router, prefix="/api/v1", tags=["Insights"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bienvenido a la API de predicción de precios de Airbnb. Visita /docs para la documentación."}
