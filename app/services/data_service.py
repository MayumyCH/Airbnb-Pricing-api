import pandas as pd
import mlflow
import logging
from app.schemas.prediction import PredictionRequest

logger = logging.getLogger(__name__)

def load_data_from_mlflow(model):
    """
    Descarga el artefacto de datos (processed.csv) desde MLflow usando el run_id del modelo.
    """
    try:
        run_id = model.metadata.run_id
        logger.info("Run_id inferido desde los metadatos del modelo: %s", run_id)

        artifact_path = "data/processed.csv"
        logger.info("Descargando artefacto '%s' desde el run_id '%s'", artifact_path, run_id)
        
        local_path = mlflow.artifacts.download_artifacts(run_id=run_id, artifact_path=artifact_path)
        
        data = pd.read_csv(local_path)
        global_average_price = round(data['price'].mean(), 2)
        logger.info("✅ Artefacto de datos cargado. Precio promedio global: %s EUR", global_average_price)
        return data, global_average_price
    except Exception as e:
        logger.error("Fallo al cargar el artefacto de datos: %s", e)
        return None, -1.0

def get_average_price(request: PredictionRequest, data: pd.DataFrame):
    """
    Calcula el precio promedio para propiedades con características similares.
    """
    if data is None:
        raise RuntimeError("Los datos para los insights no están disponibles.")

    df = data
    mask = pd.Series([True] * len(df))
    
    features = request.dict()
    
    if features.get('bedrooms') is not None:
        mask &= (df['bedrooms'] == features['bedrooms'])
    if features.get('accommodates') is not None:
        mask &= (df['accommodates'] == features['accommodates'])
    if features.get('beds') is not None:
        mask &= (df['beds'] == features['beds'])
    if features.get('minimum_nights') is not None:
        mask &= (df['minimum_nights'] <= features['minimum_nights'])

    filtered_df = df[mask]
    filtered_count = len(filtered_df)
    filtered_average = round(filtered_df['price'].mean(), 2) if filtered_count > 0 else 0
    global_average_price = round(df['price'].mean(), 2)

    return {
        "global_average_price": global_average_price,
        "filtered_average_price": filtered_average,
        "filtered_properties_count": filtered_count,
        "currency": "EUR",
    }
