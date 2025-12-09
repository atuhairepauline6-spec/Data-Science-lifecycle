# Quick Start Guide - Data Science Lifecycle Exam

**Student**: Atuhaire (B35093)  
**Project**: Financial Credit Scoring & Fairness Auditing

---

## 📋 Prerequisites

```bash
# Python 3.9+
# pip or conda

# Recommended: Create virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

---

## 🚀 Setup & Installation

### 1. Install Dependencies

```bash
cd "d:\Projects\data science exam"
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
python -c "import pandas, numpy, sklearn, matplotlib; print('✅ Core libraries installed')"
```

---

## 📊 Running the Notebooks

### MILESTONE ONE: Data Preparation

```bash
# Navigate to notebooks folder
cd notebooks

# Open Jupyter
jupyter notebook

# Run in order:
# 1. 01_data_acquisition_wrangling.ipynb
# 2. 01_part2_data_preparation.ipynb
```

**Output**: Creates `data/cleaned/Atuhaire.csv`

### MILESTONE TWO: Model Development

```bash
# Run model development notebook
# 02_model_development.ipynb

# This will:
# - Train multiple models
# - Track experiments with MLflow
# - Generate model artifacts in models/
```

**View MLflow Results**:
```bash
mlflow ui
# Open browser: http://localhost:5000
```

---

## 🔧 Running the API (Deployment)

### Local Development

```bash
cd "d:\Projects\data science exam"

# Run API server
python src/deployment/api.py

# Or using uvicorn directly:
uvicorn src.deployment.api:app --reload
```

API will be available at:
- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Test the API

```bash
# Using curl (Windows PowerShell):
Invoke-RestMethod -Uri http://localhost:8000/predict -Method POST -Headers @{"Content-Type"="application/json"} -Body '{
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
}'
```

### Docker Deployment

```bash
# Build Docker image
docker build -t credit-scoring-api:latest .

# Run container
docker run -d -p 8000:8000 --name credit-api credit-scoring-api:latest

# Check logs
docker logs credit-api

# Stop container
docker stop credit-api
```

---

## 📁 Project Structure

```
data-science-exam/
├── notebooks/               # Jupyter notebooks for each milestone
│   ├── 01_data_acquisition_wrangling.ipynb
│   ├── 01_part2_data_preparation.ipynb
│   └── 02_model_development.ipynb
├── data/
│   ├── raw/                # Original/simulated data
│   └── cleaned/            # Atuhaire.csv (clean dataset)
├── models/                 # Trained model artifacts
├── src/
│   ├── utils.py           # Utility functions
│   ├── preprocessing.py   # Data preparation
│   └── deployment/
│       └── api.py         # FastAPI application
├── reports/               # Final documentation
├── mlruns/               # MLflow experiment tracking
├── requirements.txt      # Dependencies
├── Dockerfile           # Container configuration
├── README.md            # Project documentation
└── PROGRESS_REPORT.md   # Current status
```

---

## ✅ Checklist for Completion

### MILESTONE ONE ✓
- [x] CRISP-DM framework documented
- [x] Data acquired and documented
- [x] Privacy compliance demonstrated
- [x] Data cleaned and transformed
- [x] EDA completed with insights
- [x] Feature engineering done
- [x] Atuhaire.csv created

### MILESTONE TWO (In Progress)
- [x] Model selection justified
- [ ] Models trained with MLflow
- [ ] Hyperparameter tuning
- [ ] SHAP/LIME explainability
- [ ] Fairness analysis
- [x] API created
- [x] Dockerfile created
- [ ] Monitoring design

### MILESTONE THREE (To Do)
- [ ] PDF Report (4-5 pages)
- [ ] Presentation slides (15 slides)
- [ ] Self-assessment (150 words)
- [ ] Final submission package

---

## 🔍 Troubleshooting

### Issue: Notebook won't run
```bash
# Ensure you're in the correct directory
cd "d:\Projects\data science exam"

# Reinstall Jupyter
pip install jupyter ipykernel --upgrade

# Register kernel
python -m ipykernel install --user --name=venv
```

### Issue: MLflow UI not starting
```bash
# Navigate to project root
cd "d:\Projects\data science exam"

# Start MLflow
mlflow ui

# Try different port if 5000 is busy
mlflow ui --port 5001
```

### Issue: API won't start
```bash
# Check if port 8000 is available
# Windows:
netstat -ano | findstr :8000

# Try different port
uvicorn src.deployment.api:app --port 8001
```

### Issue: Import errors
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall

# Check Python path
python -c "import sys; print(sys.path)"
```

---

## 📚 Key Files to Review

1. **PROGRESS_REPORT.md** - Current status and next steps
2. **implementation_plan.md** - Detailed plan
3. **task.md** - Task checklist
4. **notebooks/** - All analysis and models
5. **src/deployment/api.py** - Deployment code

---

## 🎯 Next Steps

1. **Complete Model Training**:
   - Open `02_model_development.ipynb`
   - Run all cells
   - Review MLflow experiments

2. **Test API**:
   - Start API server
   - Test with sample data
   - Verify predictions

3. **Create Docker Image**:
   - Build Docker image
   - Test container
   - Screenshot for report

4. **Write Final Report**:
   - Use template in reports/
   - Include all required sections
   - Add screenshots

5. **Create Presentation**:
   - 15 slides max
   - Cover all milestones
   - Include visualizations

6. **Package Submission**:
   - Zip all files
   - Name: B35093_MSDS1_Data Science Lifecycle.zip
   - Submit to Moodle

---

## 📞 Support

If you encounter issues:
1. Check PROGRESS_REPORT.md for current status
2. Review error messages in detail
3. Verify all dependencies installed
4. Check Python version (3.9+ required)

---

**Good luck with your exam! 🎓**
