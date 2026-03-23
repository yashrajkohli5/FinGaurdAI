from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Load artifacts
model = joblib.load('artifacts/credit_model.pkl')
encoders = joblib.load('artifacts/encoders.pkl')
features = joblib.load('artifacts/features.pkl')

class Applicant(BaseModel):
    person_age: int
    person_income: float
    person_home_ownership: str
    person_emp_length: float
    loan_intent: str
    loan_grade: str
    loan_amnt: float
    loan_int_rate: float            # <--- ADDED
    loan_percent_income: float
    cb_person_default_on_file: str
    cb_person_cred_hist_length: int  # <--- ADDED
@app.get('/')
def home():
    print("FinGaurd AI Prediction Home Page")

@app.post("/predict")
def predict(data: Applicant):
    try:
        df = pd.DataFrame([data.model_dump()])
        
        # Encoding
        for col, le in encoders.items():
            if col in df.columns:
                df[col] = le.transform(df[col])
        
        # Ensure all 'features' from training are present and in order
        df = df[features]
        
        prob = float(model.predict_proba(df)[0][1])
        return {
            "prediction": "High Risk" if prob > 0.3 else "Safe",
            "risk_probability": prob
        }
    except Exception as e:
        # This will now tell us exactly which column is still missing if any
        raise HTTPException(status_code=500, detail=str(e))