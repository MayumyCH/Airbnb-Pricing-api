from app.schemas.prediction import PredictionRequest, PredictionResponse
import pandas as pd
import numpy as np
from fastapi import Request

def predict_price(request_body: PredictionRequest, fastapi_request: Request) -> PredictionResponse:
    """
    Realiza una predicción de precio utilizando el modelo de MLflow cargado en app.state.
    """
    model = fastapi_request.app.state.model
    if model is None:
        raise RuntimeError("El modelo de predicción de MLflow no está disponible.")

    # Convertir la solicitud de entrada en un DataFrame de pandas
    feature_names = ['latitude', 'longitude', 'accommodates', 'bedrooms', 'beds', 'minimum_nights']
    input_data = pd.DataFrame([request_body.dict(include=set(feature_names))], columns=feature_names)

    # Realizar la predicción con el modelo de MLflow
    log_prediction = model.predict(input_data)
    
    # Aplicar la transformación inversa para obtener el precio real
    predicted_price = np.expm1(log_prediction)[0]

    return PredictionResponse(suggested_price=round(predicted_price, 2), currency= "EUR")