from pydantic import BaseModel
from typing import List

class PredictionRequest(BaseModel):
    latitude: float
    longitude: float
    accommodates: int
    bedrooms: int
    beds: int
    minimum_nights: int

class PredictionResponse(BaseModel):
    suggested_price: float
