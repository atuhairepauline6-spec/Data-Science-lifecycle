# Data Science Lifecycle Exam - Credit Scoring & Fairness Auditing

**Student**: Atuhaire  
**Access Number**: B35093  
**Course**: DSC8201 - Data Science Lifecycle  
**Project**: Financial Credit Scoring & Fairness Auditing

---

## Project Overview

This project implements a complete data science lifecycle for credit scoring with emphasis on fairness and regulatory compliance, covering all three exam milestones:

- **PART A**: CRISP-DM framework, data acquisition, privacy compliance, and feature engineering
- **PART B**: Model development, deployment, and evaluation
- **PART C**: Final report, presentation, and individual contribution

---

## Repository Structure

```
├── notebooks/                          # Jupyter notebooks for all analysis
│   ├── 01_data_acquisition_wrangling.ipynb
│   ├── 01_part2_data_preparation.ipynb
│   └── 02_model_development.ipynb
│
├── data/cleaned/                       # Clean dataset
│   └── Atuhaire.csv
│
├── src/                                # Source code
│   ├── utils.py
│   ├── preprocessing.py
│   ├── train_models.py
│   └── deployment/
│       └── api.py
│
├── reports/                            
│   ├── data_science_exam_report.pdf
│   ├── data_science_exam_presentation.pptx
│   ├── Self_Assessment_Final.pdf
│   └── git_commit_log.txt
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Key Results

- **Best Model**: XGBoost
- **Accuracy**: 82.34% (target: >75%)
- **ROC-AUC**: 0.8567 (target: >0.80)
- **Fairness**: Disparate Impact Ratio 0.87-0.99 (compliant)
- **Business Impact**: 28.8B UGX annual loss prevention

---

## Setup & Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run notebooks in order
jupyter notebook

# Test API deployment
python src/deployment/api.py

# Build Docker container
docker build -t credit-scoring-api .
```

---

## Technologies Used

- **ML**: Scikit-learn, XGBoost, LightGBM
- **Explainability**: SHAP
- **Fairness**: Fairlearn
- **Deployment**: FastAPI, Docker
- **Tracking**: MLflow
- **Data**: Pandas, NumPy

---

## Compliance

- ✅ Uganda Data Protection Act, 2019
- ✅ GDPR Principles
- ✅ Fairness Metrics (80% rule)
- ✅ Model Explainability (SHAP)

---

**Author**: Atuhaire (B35093)  
**Date**: December 2025  
**Institution**: Uganda Christian University
