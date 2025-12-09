# Financial Credit Scoring & Fairness Auditing

**Course**: DSC8201 - Data Science Lifecycle  
**Program**: Master of Science in Data Science  
**Institution**: Uganda Christian University  
**Semester**: Advent 2025

## Project Overview

This project implements a comprehensive credit scoring system with fairness auditing, following the CRISP-DM methodology and demonstrating compliance with data protection regulations (Uganda Data Protection Act & GDPR).

## Project Objectives

1. Build a credit-worthiness prediction model
2. Conduct comprehensive fairness analysis (bias detection, disparate impact)
3. Deploy a prototype scoring API with monitoring
4. Ensure ethical AI practices and regulatory compliance

## Project Structure

```
├── notebooks/              # Jupyter notebooks for each milestone
│   ├── 01_data_acquisition_wrangling.ipynb
│   ├── 02_model_development.ipynb
│   └── 03_deployment_evaluation.ipynb
├── data/
│   ├── raw/               # Original datasets
│   └── cleaned/           # Processed datasets (Atuhaire.csv)
├── models/                # Trained model artifacts
├── src/                   # Source code
│   ├── utils.py
│   ├── preprocessing.py
│   └── deployment/        # API and deployment code
├── reports/               # Final documentation
├── mlruns/               # MLflow experiment tracking
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run Notebooks in Order

1. **Data Acquisition & Wrangling**: `notebooks/01_data_acquisition_wrangling.ipynb`
2. **Model Development**: `notebooks/02_model_development.ipynb`
3. **Deployment & Evaluation**: `notebooks/03_deployment_evaluation.ipynb`

### MLflow Tracking

```bash
mlflow ui
# Access at http://localhost:5000
```

### API Deployment

```bash
cd src/deployment
uvicorn api:app --reload
# Access at http://localhost:8000
```

## Key Features

- ✅ CRISP-DM methodology implementation
- ✅ Data privacy & GDPR compliance
- ✅ Comprehensive EDA and feature engineering
- ✅ Multiple ML models (Classical & Deep Learning)
- ✅ Fairness analysis and bias detection
- ✅ Model explainability (SHAP/LIME)
- ✅ Experiment tracking with MLflow
- ✅ REST API deployment
- ✅ Model monitoring and drift detection

## Ethical Considerations

This project addresses:
- Data privacy and de-identification
- Algorithmic fairness across demographic groups
- Model transparency and explainability
- Regulatory compliance (Uganda Data Protection Act, GDPR)

## Author

Student Access Number: B35093  
Last Name: Atuhaire  
Program: MSDS1

## License

Academic project for educational purposes.
