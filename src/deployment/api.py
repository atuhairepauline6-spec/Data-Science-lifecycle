"""
FastAPI deployment for Credit Scoring Model
MILESTONE TWO - Deployment Component
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Credit Scoring API",
    description="AI-powered credit risk assessment with fairness monitoring",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class LoanApplication(BaseModel):
    """Loan application input schema"""
    age: int = Field(..., ge=18, le=100, description="Applicant age")
    annual_income: float = Field(..., gt=0, description="Annual income")
    employment_status: str = Field(..., description="Employment status: Employed, Self-Employed, Unemployed")
    employment_duration_months: int = Field(..., ge=0, description="Employment duration in months")
    credit_score: float = Field(..., ge=300, le=850, description="Credit score")
    existing_debt: float = Field(..., ge=0, description="Existing debt amount")
    loan_amount: float = Field(..., gt= 0, description="Requested loan amount")
    loan_term_months: int = Field(..., description="Loan term in months")
    loan_purpose: str = Field(..., description="Loan purpose")
    num_credit_accounts: int = Field(..., ge=0, description="Number of credit accounts")
    credit_utilization: float = Field(..., ge=0, le=1, description="Credit utilization ratio")
    num_delinquencies: int = Field(..., ge=0, description="Number of delinquencies")
    payment_history_months: int = Field(..., ge=0, description="Payment history in months")
    
    class Config:
        schema_extra = {
            "example": {
                "age": 35,
                "annual_income": 50000,
                "employment_status": "Employed",
                "employment_duration_months": 48,
                "credit_score": 680,
                "existing_debt": 15000,
                "loan_amount": 10000,
                "loan_term_months": 36,
                "loan_purpose": "Home",
                "num_credit_accounts": 3,
                "credit_utilization": 0.45,
                "num_delinquencies": 0,
                "payment_history_months": 60
            }
        }


class PredictionResponse(BaseModel):
    """Prediction output schema"""
    application_id: str
    default_probability: float
    risk_category: str
    decision: str
    confidence: float
    explanation: Optional[Dict] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    version: str


# Global variables for model
MODEL_PATH = Path(__file__).parent.parent.parent / "models"
model = None
feature_columns = []


def load_model():
    """Load the trained model"""
    global model, feature_columns
    try:
        model_file = MODEL_PATH / "best_model.pkl"
        if model_file.exists():
            model = joblib.load(model_file)
            logger.info(f"Model loaded successfully from {model_file}")
            
            # Load feature columns
            features_file = MODEL_PATH / "feature_columns.pkl"
            if features_file.exists():
                feature_columns = joblib.load(features_file)
                logger.info(f"Loaded {len(feature_columns)} feature columns")
        else:
            logger.warning(f"Model file not found at {model_file}")
            # For demo purposes, model will be None
    except Exception as e:
        logger.error(f"Error loading model: {e}")


def preprocess_input(application: LoanApplication) -> pd.DataFrame:
    """Preprocess input data to match training format"""
    # Create DataFrame from input
    data = {
        'age': [application.age],
        'annual_income': [application.annual_income],
        'employment_duration_months': [application.employment_duration_months],
        'credit_score': [application.credit_score],
        'existing_debt': [application.existing_debt],
        'loan_amount': [application.loan_amount],
        'loan_term_months': [application.loan_term_months],
        'num_credit_accounts': [application.num_credit_accounts],
        'credit_utilization': [application.credit_utilization],
        'num_delinquencies': [application.num_delinquencies],
        'payment_history_months': [application.payment_history_months],
    }
    
    df = pd.DataFrame(data)
    
    # Calculate derived features
    df['debt_to_income_ratio'] = df['existing_debt'] / (df['annual_income'] + 1)
    df['loan_to_income_ratio'] = df['loan_amount'] / (df['annual_income'] + 1)
    
    # Interest rate estimate (simplified)
    interest_rate = 12.0  # Default rate
    df['interest_rate'] = interest_rate
    
    # Monthly payment calculation
    monthly_rate = interest_rate / 100 / 12
    df['monthly_payment'] = df['loan_amount'] * monthly_rate / (1 - (1 + monthly_rate) ** (-df['loan_term_months']))
    df['payment_to_income_ratio'] = (df['monthly_payment'] * 12) / (df['annual_income'] + 1)
    
    # Encode categorical features (simplified for demo)
    employment_mapping = {'Employed': 0, 'Self-Employed': 1, 'Unemployed': 2}
    df['employment_status_encoded'] = employment_mapping.get(application.employment_status, 0)
    
    return df


def calculate_risk_category(probability: float) -> str:
    """Categorize risk based on probability"""
    if probability < 0.20:
        return "LOW_RISK"
    elif probability < 0.40:
        return "MODERATE_RISK"
    elif probability < 0.60:
        return "HIGH_RISK"
    else:
        return "VERY_HIGH_RISK"


def make_decision(probability: float, confidence: float) -> str:
    """Make lending decision based on probability and confidence"""
    if confidence < 0.7:
        return "MANUAL_REVIEW"
    elif probability < 0.30:
        return "APPROVED"
    elif probability < 0.50:
        return "CONDITIONAL_APPROVAL"
    else:
        return "REJECTED"


# API Endpoints
@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    load_model()


@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "version": "1.0.0"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy" if model is not None else "degraded",
        "model_loaded": model is not None,
        "version": "1.0.0"
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict_credit_risk(application: LoanApplication):
    """
    Predict credit default risk for a loan application
    
    Returns:
    - default_probability: Probability of default (0-1)
    - risk_category: LOW_RISK, MODERATE_RISK, HIGH_RISK, VERY_HIGH_RISK
    - decision: APPROVED, CONDITIONAL_APPROVAL, REJECTED, MANUAL_REVIEW
    - confidence: Model confidence in prediction
    """
    try:
        # Generate application ID
        import uuid
        app_id = f"APP_{uuid.uuid4().hex[:8].upper()}"
        
        # Preprocess input
        df = preprocess_input(application)
        
        # Make prediction
        if model is not None:
            # Use actual model
            try:
                probability = model.predict_proba(df)[0][1]
                confidence = max(model.predict_proba(df)[0])
            except Exception as e:
                logger.error(f"Model prediction error: {e}")
                # Fallback to rule-based prediction
                probability = calculate_rule_based_probability(application)
                confidence = 0.6
        else:
            # Rule-based prediction for demo
            probability = calculate_rule_based_probability(application)
            confidence = 0.6
        
        # Calculate risk category and decision
        risk_category = calculate_risk_category(probability)
        decision = make_decision(probability, confidence)
        
        # Generate simple explanation
        explanation = {
            "credit_score_impact": "high" if application.credit_score < 600 else "low",
            "debt_ratio_impact": "high" if (application.existing_debt / application.annual_income) > 0.5 else "low",
            "employment_impact": "high" if application.employment_status == "Unemployed" else "low",
            "delinquency_impact": "high" if application.num_delinquencies > 2 else "low"
        }
        
        return {
            "application_id": app_id,
            "default_probability": round(probability, 4),
            "risk_category": risk_category,
            "decision": decision,
            "confidence": round(confidence, 4),
            "explanation": explanation
        }
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/batch_predict")
async def batch_predict(applications: List[LoanApplication]):
    """Batch prediction endpoint"""
    results = []
    for app in applications:
        try:
            result = await predict_credit_risk(app)
            results.append(result)
        except Exception as e:
            logger.error(f"Batch prediction error: {e}")
            results.append({"error": str(e)})
    
    return {"predictions": results, "total": len(applications), "successful": len([r for r in results if "error" not in r])}


def calculate_rule_based_probability(application: LoanApplication) -> float:
    """
    Calculate default probability using rules (for demo when model not available)
    """
    probability = 0.10  # Base rate
    
    # Credit score factor
    if application.credit_score < 600:
        probability += 0.25
    elif application.credit_score < 650:
        probability += 0.15
    elif application.credit_score < 700:
        probability += 0.05
    
    # Debt-to-income ratio
    dti = application.existing_debt / (application.annual_income + 1)
    if dti > 0.5:
        probability += 0.20
    elif dti > 0.4:
        probability += 0.10
    
    # Employment status
    if application.employment_status == "Unemployed":
        probability += 0.15
    elif application.employment_status == "Self-Employed":
        probability += 0.05
    
    # Delinquencies
    if application.num_delinquencies > 2:
        probability += 0.20
    elif application.num_delinquencies > 0:
        probability += 0.10
    
    # Credit utilization
    if application.credit_utilization > 0.8:
        probability += 0.10
    elif application.credit_utilization > 0.6:
        probability += 0.05
    
    return min(probability, 0.95)  # Cap at 95%


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
