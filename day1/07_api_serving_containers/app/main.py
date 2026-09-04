from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# In a real app, you would load your trained model here
# using joblib or pickle. For this lesson, we use a fake model!

class PredictRequest(BaseModel):
    age: int = Field(..., ge=18, le=120, description="Customer age")
    income: float = Field(..., gt=0, description="Annual income in USD")
    credit_score: int = Field(..., ge=300, le=850)

class PredictResponse(BaseModel):
    prediction: str
    probability: float

app = FastAPI(title="Bank Risk ML API")

@app.get("/health")
async def health_check():
    """Load balancers use this to check if the API is alive."""
    return {"status": "healthy"}

@app.post("/v1/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """Takes in customer data and returns a default prediction."""
    try:
        # FAKE MODEL LOGIC:
        # If income is high and credit score is good, no default!
        if request.income > 60000 and request.credit_score > 650:
            return PredictResponse(prediction="No Default", probability=0.1)
        else:
            return PredictResponse(prediction="Default", probability=0.85)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
