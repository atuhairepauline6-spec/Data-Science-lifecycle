# Self-Assessment - Data Science Lifecycle Exam

**Student**: Atuhaire  
**Access Number**: B35093  
**Course**: DSC8201 - Data Science Lifecycle  
**Date**: December 2025

---

## Self-Assessment (Maximum 150 words)

[**Instructions**: Write a concise 150-word reflection covering what you accomplished, challenges faced, key learnings, and your personal contribution. Below is a template you can customize.]

---

### TEMPLATE (Customize this):

Throughout this project, I successfully implemented a complete data science lifecycle for credit scoring, demonstrating proficiency in CRISP-DM methodology, privacy compliance, and MLOps deployment. I created a comprehensive dataset of 40,000 loan applications, performed extensive EDA, and engineered 35+ domain-specific features to enhance model performance.

The main challenges included addressing class imbalance through SMOTE and ensuring algorithmic fairness across demographic groups without sacrificing predictive accuracy. I overcame these by implementing balanced sampling techniques and integrating fairness metrics into model evaluation.

I trained and evaluated [X] models, with [MODEL NAME] achieving [XX]% accuracy and [0.XX] ROC-AUC. Using SHAP analysis, I identified credit score and debt-to-income ratio as the most influential predictors. Successfully deployed a FastAPI application with Docker containerization and implemented MLflow for comprehensive experiment tracking.

Key learnings include the critical importance of fairness-aware machine learning in financial applications, the value of robust privacy compliance frameworks (GDPR, Uganda DPA), and practical deployment considerations for production ML systems. This project significantly enhanced my skills in end-to-end ML system development, from problem formulation through deployment and monitoring.

---

### Alternative Template (More Technical):

This project covered the entire data science lifecycle for credit risk assessment. I began with problem formulation and hypothesis testing, created a simulated 40,000-record dataset reflecting Ugandan microfinance context, and applied comprehensive data preparation including outlier treatment, feature engineering, and SMOTE resampling for class imbalance.

Key challenges included optimizing the trade-off between model performance and fairness. I addressed this through careful feature selection (excluding protected attributes), implementing fairness constraints, and using SHAP for transparent decision-making. Technical hurdles in deployment were resolved through FastAPI async capabilities and Docker containerization.

The [MODEL NAME] achieved [XX]% accuracy ([0.XX] AUC-ROC), meeting all success criteria while maintaining demographic parity (Disparate Impact Ratio: [0.XX]). Top predictors were credit score (SHAP: [X.XX]) and DTI ratio (SHAP: [X.XX]).

Critical learnings: (1) Feature engineering drives performance more than algorithm choice, (2) Fairness must be embedded from design, not retrofitted, (3) MLflow streamlines experiment tracking, (4) Privacy compliance requires proactive governance. This experience bridged theoretical ML knowledge with practical production deployment skills.

---

### Alternative Template (Business-Focused):

I delivered an end-to-end credit scoring solution addressing real-world challenges in financial risk assessment. Starting from business understanding, I identified the need for accurate yet fair automated credit decisions compliant with Uganda Data Protection Act and GDPR.

Major accomplishment was balancing competing objectives: maximizing predictive accuracy while ensuring demographic fairness. I achieved this through data-driven feature engineering (35+ new features), sophisticated modeling([MODEL NAME]: [XX]% accuracy), and comprehensive bias testing. The solution demonstrates [0.XX] Disparate Impact Ratio, exceeding the 0.80 threshold.

Significant challenges included limited domain expertise in Ugandan microfinance—addressed through literature review and consultation with financial sector reports. Technical challenges in MLflow AWS integration were overcome by implementing local tracking with plans for cloud migration.

The deployed API achieves sub-100ms predictions with automatic SHAP explanations, enabling both rapid decisions and regulatory transparency. Estimated business impact: 2.4B UGX annual loss prevention through 4-percentage-point default reduction.

Key learnings: data quality foundations precede model sophistication; fairness requires explicit metrics and monitoring; production deployment demands robust error handling, monitoring, and governance frameworks. This project demonstrated that responsible AI in financial services requires equal emphasis on performance, fairness, and explainability.

---

## Word Count Check

**Instructions**: Keep your final self-assessment to exactly 150 words or fewer. Use this space to count:

Current word count: [COUNT YOUR WORDS]

If over 150, remove:
- Extra adjectives
- Redundant phrases
- Less critical details

If under 150, you can add:
- Specific metric values
- Additional learnings
- More technical details

---

## Final Checklist Before Submission

- [ ] Self-assessment is 150 words or less
- [ ] Mentions specific accomplishments
- [ ] Discusses challenges faced
- [ ] Highlights key learnings
- [ ] Professional tone
- [ ] No grammatical errors
- [ ] Includes actual metric values (if available)
- [ ] Saved as .txt file for submission

---

## Tips for Strong Self-Assessment

**DO**:
✅ Be specific (use numbers, model names, metrics)
✅ Show reflection (what you learned)
✅ Acknowledge challenges (shows honesty)
✅ Demonstrate technical depth
✅ Connect to course objectives

**DON'T**:
❌ Just list what you did
❌ Be vague or generic
❌ Exaggerate or make unsupported claims
❌ Include unnecessary details
❌ Forget to proofread

---

## Example Strong Statements

**Weak**: "I trained several models and got good results."

**Strong**: "I trained 4 models (Logistic Regression, Random Forest, XGBoost, LightGBM), with XGBoost achieving 82% accuracy and 0.85 AUC-ROC."

---

**Weak**: "The project was challenging."

**Strong**: "The main challenge was balancing 82% accuracy with demographic parity (DI Ratio: 0.87), achieved through careful feature selection and SMOTE resampling."

---

**Weak**: "I learned about machine learning."

**Strong**: "Key learning: Feature engineering (35+ domain features) improved model AUC by 12 percentage points more than hyperparameter tuning alone."

---

**Remember**: This is your chance to demonstrate deep understanding and reflection. Make every word count!

---

**Word Count**: Must be ≤ 150 words
