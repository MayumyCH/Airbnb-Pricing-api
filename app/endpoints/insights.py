from fastapi import APIRouter, HTTPException, Request
from app.schemas.prediction import PredictionRequest
from app.schemas.insights import InsightsResponse
from app.services.data_service import get_average_price

router = APIRouter()

@router.post("/average_price", response_model=InsightsResponse, summary="Calcula el precio promedio para propiedades similares")
def calculate_average_price(request_body: PredictionRequest, request: Request):
    """
    Calcula y devuelve el precio promedio para propiedades con características similares
    basándose en un conjunto de datos local.
    """
    if not hasattr(request.app.state, 'data') or request.app.state.data is None:
        raise HTTPException(status_code=503, detail="Los datos para insights no están disponibles. Comprueba los logs del servidor.")

    try:
        insights = get_average_price(request_body, request.app.state.data)
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular el precio promedio: {str(e)}")
