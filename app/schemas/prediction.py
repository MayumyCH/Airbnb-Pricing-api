from pydantic import BaseModel
from typing import List

class PredictionRequest(BaseModel):
    latitude: float
    longitude: float
    accommodates: float
    bedrooms: float
    beds: float
    minimum_nights: float

class PredictionResponse(BaseModel):
    suggested_price: float
    currency: str = "EUR"
