# Final Execution Checklist

**Student**: Atuhaire (B35093)  
**Deadline**: December 14, 2025  
**Current Date**: Check current date

---

## 🚀 QUICK START - Run This First!

### Step 0: Verify Setup (5 minutes)

```bash
# Navigate to project
cd "d:\Projects\data science exam"

# Check if clean data exists
dir data\cleaned\Atuhaire.csv

# If file exists:  ✅ Ready to proceed
# If file doesn't exist: Run notebooks 01 and 01_part2 first
```

---

## ⚡ FAST TRACK - Model Training (30 minutes)

### Option A: Run Automated Script (RECOMMENDED - Fastest)

```bash
# Install dependencies if needed
pip install -r requirements.txt

# Run automated training
python src/train_models.py

# This will:
# ✅ Load Atuhaire.csv
# ✅ Train 4 models (LogReg, RF, XGBoost, LightGBM)
# ✅ Evaluate each model
# ✅ Log to MLflow (if available)
# ✅ Save best model to models/
# ✅ Generate training_summary.txt

# Expected time: 10-30 minutes depending on your machine
```

**Check Results**:
- models/best_model.pkl (✓ saved)
- models/training_summary.txt (✓ read this for metrics)
- models/model_results.json (✓ all metrics)

### Option B: Run Notebook (Slower, More Detailed)

```bash
# Open Jupyter
jupyter notebook

# Run: notebooks/02_model_development.ipynb
# Execute all cells
# Review MLflow UI: mlflow ui
```

---

## 📊 MILESTONE COMPLETION CHECKLIST

### ✅ MILESTONE ONE (30 marks) - COMPLETE

- [x] CRISP-DM framework documented
- [x] Research hypotheses defined
- [x] Dataset acquired (40,000 records)
- [x] Privacy compliance demonstrated
- [x] Data cleaned (missing values, outliers)
- [x] EDA completed with 10+ insights
- [x] 35+ features engineered
- [x] **Atuhaire.csv created**

**Evidence**: 
- notebooks/01_data_acquisition_wrangling.ipynb
- notebooks/01_part2_data_preparation.ipynb
- data/cleaned/Atuhaire.csv

---

### 🔄 MILESTONE TWO (40 marks) - IN PROGRESS

#### Part 1: Model Selection & Justification (8 marks) - COMPLETE
- [x] 6 models selected with justification
- [x] Hypothesis alignment documented
- [x] Data characteristics analyzed
- [x] Ethical considerations addressed
- [x] Interpretability requirements defined

**Evidence**: 
- notebooks/02_model_development.ipynb (Section 1)
- COMPLETION_ROADMAP.md

#### Part 2: Model Training (10 marks) - TO COMPLETE TODAY

**Action Items**:
```bash
# Run this NOW:
python src/train_models.py
```

**What This Does**:
- [ ] Train Logistic Regression
- [ ] Train Random Forest  
- [ ] Train XGBoost
- [ ] Train LightGBM
- [ ] Save all models to models/
- [ ] Generate performance metrics
- [ ] Log to MLflow (automatically)

**Expected Output**:
```
models/
├── best_model.pkl
├── logistic_regression.pkl
├── random_forest.pkl
├── xgboost.pkl
├── lightgbm.pkl
├── feature_columns.pkl
├── model_results.json
└── training_summary.txt
```

**Time**: 20-40 minutes

#### Part 3: Explainability (SHAP/LIME) - TO COMPLETE

**Quick SHAP Analysis** (if you have time):

```python
# Add this to a new notebook cell or Python script
import shap
import joblib

# Load best model
model = joblib.load('models/best_model.pkl')
X_test = # your test data

# SHAP analysis
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Save plot
shap.summary_plot(shap_values, X_test, show=False)
plt.savefig('reports/shap_summary.png', dpi=300, bbox_inches='tight')
print("✅ SHAP plot saved!")
```

**Time**: 15-20 minutes

#### Part 4: Deployment (12 marks) - CODE READY

- [x] FastAPI code created (src/deployment/api.py)
- [x] Dockerfile created
- [ ] Test API locally
- [ ] Take screenshots
- [ ] (Optional) Build Docker image

**Testing API** (5-10 minutes):

```bash
# Terminal 1: Start API
python src/deployment/api.py

# Terminal 2: Test (PowerShell)
Invoke-RestMethod -Uri http://localhost:8000/health

# Browser: Open http://localhost:8000/docs
# Screenshot the Swagger UI!
```

**Docker** (Optional, 10-15 minutes):

```bash
# Build
docker build -t credit-api .

# Run
docker run -d -p 8000:8000 credit-api

# Screenshot
docker ps
docker images
```

#### Part 5: Evaluation (10 marks) - MOSTLY DONE

- [x] Metrics defined
- [ ] Fill in actual values from training_summary.txt
- [ ] Create comparison table
- [ ] Fairness analysis (if time permits)

**Quick Fairness Check**:
- Calculate approval rates by gender/age from test set
- Check if Disparate Impact Ratio > 0.80
- Document results

---

### ❌ MILESTONE THREE (30 marks) - TO START

#### Report (20 marks) - 3-4 hours

**Use Template**: `reports/REPORT_TEMPLATE.md`

**Steps**:
1. Copy template content
2. Fill in [XX] placeholders with actual metrics from training_summary.txt
3. Insert screenshots (MLflow, API, Docker)
4. Add SHAP plots (if generated)
5. Proofread
6. Convert to PDF

**Tools for PDF**:
- Microsoft Word → Save as PDF
- Google Docs → Download as PDF
- pandoc (if you have it): `pandoc REPORT_TEMPLATE.md -o Final_Report.pdf`

**Time**: 3-4 hours

#### Presentation (10 marks) - 2-3 hours

**Use Outline**: `reports/PRESENTATION_OUTLINE.md`

**Steps**:
1. Open PowerPoint/Google Slides
2. Create 15 slides following outline
3. Add charts from notebooks
4. Add screenshots (API, Docker, MLflow)
5. Practice delivery (10-15 min)

**Time**: 2-3 hours

#### Self-Assessment (150 words) - 15 minutes

**Use Template**: `reports/SELF_ASSESSMENT_TEMPLATE.md`

**Steps**:
1. Choose template version
2. Fill in your actual metrics
3. Customize for your experience
4. Check word count (≤150)
5. Save as .txt file

**Time**: 15 minutes

---

## 📦 SUBMISSION PREPARATION (30 minutes)

### Step 1: Gather Git Logs

```bash
cd "d:\Projects\data science exam"

# Generate commit log
git log --all --graph --decorate --oneline > reports/git_commit_log.txt

# Verify
type reports\git_commit_log.txt
```

### Step 2: Create Submission Folder

```powershell
# Create submission directory
New-Item -ItemType Directory -Force -Path "submission"

# Copy required files
Copy-Item -Recurse "notebooks" "submission\notebooks"
Copy-Item -Recurse "data\cleaned" "submission\data"
Copy-Item -Recurse "reports" "submission\reports"
Copy-Item -Recurse "src" "submission\src"
Copy-Item -Recurse "models" "submission\models"
Copy-Item "README.md" "submission\"
Copy-Item "requirements.txt" "submission\"
```

### Step 3: Verify Contents

**Required Files**:
```
submission/
├── notebooks/
│   ├── 01_data_acquisition_wrangling.ipynb ✓
│   ├── 01_part2_data_preparation.ipynb ✓
│   └── 02_model_development.ipynb ✓
├── data/
│   └── Atuhaire.csv ✓
├── reports/
│   ├── Final_Report.pdf ✓
│   ├── Presentation.pptx ✓
│   ├── Self_Assessment.txt ✓
│   └── git_commit_log.txt ✓
├── src/ ✓
├── models/
│   └── best_model.pkl ✓
├── README.md ✓
└── requirements.txt ✓
```

### Step 4: Create Zip File

```powershell
# Windows PowerShell
Compress-Archive -Path "submission\*" -DestinationPath "B35093_MSDS1_Data Science Lifecycle.zip" -Force

# Verify
Get-Item "B35093_MSDS1_Data Science Lifecycle.zip"
```

### Step 5: Final Checks

- [ ] Zip file name correct: `B35093_MSDS1_Data Science Lifecycle.zip`
- [ ] No personal name in files (only access number)
- [ ] All notebooks run without errors
- [ ] Atuhaire.csv present
- [ ] Final_Report.pdf is 4-5 pages
- [ ] Presentation.pptx is max 15 slides
- [ ] Self_Assessment.txt is ≤150 words
- [ ] Git logs included
- [ ] File size reasonable (<500MB)

---

## ⏰ TIME MANAGEMENT

### Today (Day 1) - 6 hours
- [ ] Run model training script (30 min)
- [ ] Test API and take screenshots (30 min)
- [ ] Generate SHAP plots (20 min)
- [ ] Start writing report (4 hours)

### Day 2 - 4 hours
- [ ] Finish report (2 hours)
- [ ] Create presentation (2 hours)

### Day 3 - 2 hours
- [ ] Write self-assessment (30 min)
- [ ] Prepare submission package (30 min)
- [ ] Final review (1 hour)

### Day 4 - Submit!
- [ ] Upload to Moodle
- [ ] Verify submission
- [ ] Keep backup

---

## 🆘 IF YOU'RE SHORT ON TIME

### Minimum Viable Submission (6-8 hours total):

1. **Run training script** (30 min):
   ```bash
   python src/train_models.py
   ```

2. **Fill report template** (2 hours):
   - Use actual metrics from training_summary.txt
   - Skip SHAP if no time
   - Use simple screenshots

3. **Quick presentation** (1.5 hours):
   - Use PRESENTATION_OUTLINE.md
   - Copy key charts from notebooks
   - Keep slides simple

4. **Self-assessment** (15 min):
   - Use template, customize minimally

5. **Package submission** (30 min):
   - Follow submission prep steps

6. **Submit** (15 min)

---

## 📞 HELP & RESOURCES

### If Training Fails:
- Check data/cleaned/Atuhaire.csv exists
- Verify Python packages installed: `pip install -r requirements.txt`
- Check error messages in terminal
- Try running notebooks manually

### If You Get Stuck:
- Review PROGRESS_REPORT.md for status
- Check QUICKSTART.md for setup help
- Review COMPLETION_ROADMAP.md for detailed steps

### Reference Documents:
- Implementation Plan: `implementation_plan.md`
- Progress Report: `PROGRESS_REPORT.md`
- Quick Start: `QUICKSTART.md`
- Completion Roadmap: `COMPLETION_ROADMAP.md`
- Walkthrough: Artifact walkthrough.md

---

## ✅ SUCCESS CRITERIA

### Minimum to Pass (70%+):
- [ ] All 3 notebooks execute
- [ ] Atuhaire.csv created
- [ ] At least 2 models trained
- [ ] Basic report (4-5 pages)
- [ ] Presentation (15 slides)
- [ ] Self-assessment (≤150 words)

### Excellent Grade (85%+):
- [ ] All above, plus:
- [ ] 4+ models trained with MLflow
- [ ] SHAP explainability
- [ ] Fairness analysis
- [ ] API tested with screenshots
- [ ] Professional report with visualizations
- [ ] Polished presentation

---

## 🎯 YOUR ACTION PLAN FOR TODAY

```bash
# 1. RUN THIS NOW (30 min):
python src/train_models.py

# 2. While training, start report (use waiting time):
# Open reports/REPORT_TEMPLATE.md and start filling in

# 3. After training completes:
# - Check models/training_summary.txt for metrics
# - Fill metrics into report template
# - Take screenshots of MLflow UI (if available)

# 4. Test API (10 min):
python src/deployment/api.py
# Open http://localhost:8000/docs and screenshot

# 5. Continue report writing (3-4 hours)

# 6. Tomorrow: Presentation + Self-assessment
```

---

**YOU'VE GOT THIS! 🚀**

**Current Status**: ~60% complete  
**Remaining**: ~40% (mostly documentation)  
**Time Available**: 5 days  
**Estimated Time Needed**: 10-15 hours  

**You're in great shape! Just follow this checklist step-by-step.**

---

**Last Updated**: December 9, 2025  
**Created by**: Atuhaire Project Assistant
