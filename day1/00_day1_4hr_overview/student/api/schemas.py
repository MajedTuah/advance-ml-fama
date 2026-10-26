# Used to define the data structures
from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    age: int = Field(..., ge=18, le=120, description="Customer age")
    income: float = Field(..., gt=0, description="Annual income in USD")
    credit_score: int = Field(..., ge=300, le=850)

class PredictResponse(BaseModel):
    prediction: str
    probability: float
