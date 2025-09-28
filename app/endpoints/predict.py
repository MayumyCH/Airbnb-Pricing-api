from fastapi import APIRouter, HTTPException
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.model_service import predict_price

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse, summary="Realiza una predicción de precio")
async def create_prediction(request: PredictionRequest):
    """
    Recibe los datos de una propiedad y devuelve una predicción de precio sugerido
    junto con un análisis competitivo.
    """
    try:
        prediction = predict_price(request)
        return prediction
    except Exception as e:
        # En un caso real, aquí se registraría el error
        raise HTTPException(status_code=500, detail=f"Ocurrió un error interno: {str(e)}")
