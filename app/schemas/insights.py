from pydantic import BaseModel

class InsightsResponse(BaseModel):
    global_average_price: float
    filtered_average_price: float
    filtered_properties_count: int
    currency: str = "EUR"
