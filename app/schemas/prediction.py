from pydantic import BaseModel
from typing import List

class PredictionRequest(BaseModel):
    latitude: float
    longitude: float
    guests: int
    rooms: int
    beds: int
    nights: int

class JustificationItem(BaseModel):
    description: str
    impact: float
    type: str  # 'positive' o 'negative'

class CompetitiveAnalysis(BaseModel):
    your_price: float
    neighborhood_average: float
    neighborhood_max: float

class PredictionResponse(BaseModel):
    suggested_price: float
    percentage_vs_average: float
    justification: List[JustificationItem]
    competitive_analysis: CompetitiveAnalysis
