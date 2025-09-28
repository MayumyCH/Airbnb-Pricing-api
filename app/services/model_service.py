from app.schemas.prediction import PredictionRequest, PredictionResponse, JustificationItem, CompetitiveAnalysis
import random

def predict_price(request: PredictionRequest) -> PredictionResponse:
    """
    Simula la lógica de un modelo de IA para predecir el precio.
    Genera datos falsos pero realistas basados en la entrada.
    """
    # Fórmula de simulación simple para el precio base
    base_price_per_night = 50 + (request.guests * 15) + (request.rooms * 25) + (request.beds * 5)
    total_price = base_price_per_night * request.nights

    # Simulación de análisis competitivo
    neighborhood_avg_nightly = base_price_per_night * random.uniform(0.8, 1.1)
    neighborhood_max_nightly = neighborhood_avg_nightly * random.uniform(1.5, 2.0)

    print("Data App", request)

    # Simulación de justificación
    justification = []
    if request.guests > 4:
        justification.append(JustificationItem(
            description="El alto número de huéspedes justifica un precio mayor.",
            impact=request.guests * 5.0,
            type="positive"
        ))
    if request.rooms > 2:
        justification.append(JustificationItem(
            description="Más habitaciones que el promedio en la zona.",
            impact=request.rooms * 10.0,
            type="positive"
        ))
    if request.nights < 2:
        justification.append(JustificationItem(
            description="Las estancias cortas suelen tener una tarifa por noche más alta.",
            impact=15.0,
            type="positive"
        ))
    else:
        justification.append(JustificationItem(
            description="Precio ajustado para una estancia de varias noches.",
            impact=-10.0,
            type="negative"
        ))

    # Calcular el precio sugerido final
    suggested_price = total_price + sum(item.impact for item in justification)
    
    # Asegurarse de que el precio no sea negativo
    suggested_price = max(suggested_price, 50.0)

    # Calcular el porcentaje sobre el promedio del vecindario
    percentage_vs_average = ((suggested_price / (neighborhood_avg_nightly * request.nights)) - 1) * 100 if neighborhood_avg_nightly > 0 else 0

    return PredictionResponse(
        suggested_price=round(suggested_price, 2),
        percentage_vs_average=round(percentage_vs_average, 2),
        justification=justification,
        competitive_analysis=CompetitiveAnalysis(
            your_price=round(suggested_price, 2),
            neighborhood_average=round(neighborhood_avg_nightly * request.nights, 2),
            neighborhood_max=round(neighborhood_max_nightly * request.nights, 2)
        )
    )
