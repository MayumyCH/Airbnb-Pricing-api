from app.schemas.prediction import PredictionRequest, PredictionResponse
import joblib
import pandas as pd
from pathlib import Path

# Obtener la ruta absoluta al directorio actual del archivo
BASE_DIR = Path(__file__).resolve(strict=True).parent

# Cargar el modelo una sola vez cuando se inicie la aplicación
try:
    model_path = Path(BASE_DIR).parent / "models" / "model.pkl"
    model = joblib.load(model_path)
except FileNotFoundError:
    model = None
except Exception as e:
    # Manejar otros posibles errores de carga
    print(f"Error al cargar el modelo: {e}")
    model = None

def predict_price(request: PredictionRequest) -> PredictionResponse:
    """
    Realiza una predicción de precio utilizando el modelo de machine learning cargado.
    """
    if model is None:
        # Opcional: puedes devolver un error específico si el modelo no se cargó
        raise RuntimeError("El modelo de predicción no está disponible.")

    # Convertir la solicitud de entrada en un DataFrame de pandas
    # Asegúrate de que el orden de las columnas coincida con el que espera el modelo
    feature_names = ['latitude', 'longitude', 'accommodates', 'bedrooms', 'beds', 'minimum_nights']
    
    input_data = pd.DataFrame([request.dict(include=set(feature_names))], columns=feature_names)

    # Realizar la predicción
    prediction = model.predict(input_data)

    # El resultado de la predicción suele ser un array de numpy, tomamos el primer elemento
    suggested_price = prediction[0]

    return PredictionResponse(suggested_price=round(suggested_price, 2))