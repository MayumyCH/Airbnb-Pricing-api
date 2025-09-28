from fastapi import FastAPI
from app.endpoints import predict

app = FastAPI(
    title="Airbnb Pricing API",
    description="API para la predicción de precios de alquileres de Airbnb.",
    version="1.0.0"
)

# Incluir el router de predicciones
app.include_router(predict.router, prefix="/api/v1", tags=["Predictions"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bienvenido a la API de predicción de precios de Airbnb. Visita /docs para la documentación."}
