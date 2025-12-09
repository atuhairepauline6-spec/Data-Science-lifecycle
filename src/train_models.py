"""
Automated Model Training Script
MILESTONE TWO - Quick Execution
Run this to train all models quickly without notebooks

Usage:
    python src/train_models.py
"""

import pandas as pd
import numpy as np
import warnings
import sys
import joblib
from pathlib import Path
from datetime import datetime
import json

# ML Libraries
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    roc_auc_score, confusion_matrix, classification_report
)

from imblearn.over_sampling import SMOTE

try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except:
    XGBOOST_AVAILABLE = False
    print("⚠️ XGBoost not available")

try:
    from lightgbm import LGBMClassifier
    LIGHTGBM_AVAILABLE = True
except:
    LIGHTGBM_AVAILABLE = False
    print("⚠️ LightGBM not available")

try:
    import mlflow
    import mlflow.sklearn
    MLFLOW_AVAILABLE = True
except:
    MLFLOW_AVAILABLE = False
    print("⚠️ MLflow not available - metrics will be saved to JSON")

warnings.filterwarnings('ignore')

class CreditScoringTrainer:
    """Automated trainer for credit scoring models"""
    
    def __init__(self, data_path):
        self.data_path = data_path
        self.models = {}
        self.results = {}
        self.best_model = None
        self.best_score = 0
        
    def load_data(self):
        """Load and prepare data"""
        print("="*80)
        print("LOADING DATA".center(80))
        print("="*80)
        
        df = pd.read_csv(self.data_path)
        print(f"\n✅ Loaded dataset: {df.shape}")
        
        # Identify target and features
        target_col = 'default_status'
        exclude_cols = [target_col, 'applicant_id', 'gender', 'age_group', 'marital_status']
        
        # Handle if columns don't exist
        exclude_cols = [col for col in exclude_cols if col in df.columns]
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        
        print(f"Features: {len(feature_cols)}")
        print(f"Target: {target_col}")
        
        X = df[feature_cols].copy()
        y = df[target_col].copy()
        
        # Handle any remaining missing values
        X = X.fillna(X.median())
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=42, stratify=y
        )
        
        print(f"\nTrain: {X_train.shape[0]:,} | Test: {X_test.shape[0]:,}")
        print(f"Default rate - Train: {y_train.mean():.2%} | Test: {y_test.mean():.2%}")
        
        # Apply SMOTE
        print("\n🔄 Applying SMOTE...")
        smote = SMOTE(random_state=42, sampling_strategy=0.7)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
        
        print(f"After SMOTE: {X_train_balanced.shape[0]:,} samples")
        print(f"New default rate: {y_train_balanced.mean():.2%}")
        
        self.X_train = X_train_balanced
        self.y_train = y_train_balanced
        self.X_test = X_test
        self.y_test = y_test
        self.feature_cols = feature_cols
        
        return self
    
    def train_logistic_regression(self):
        """Train Logistic Regression"""
        print("\n" + "="*80)
        print("1. TRAINING LOGISTIC REGRESSION".center(80))
        print("="*80)
        
        model = LogisticRegression(
            max_iter=1000,
            class_weight='balanced',
            random_state=42,
            solver='liblinear'
        )
        
        model.fit(self.X_train, self.y_train)
        
        metrics = self._evaluate_model(model, "Logistic Regression")
        self.models['logistic_regression'] = model
        self.results['logistic_regression'] = metrics
        
        return self
    
    def train_random_forest(self):
        """Train Random Forest"""
        print("\n" + "="*80)
        print("2. TRAINING RANDOM FOREST".center(80))
        print("="*80)
        
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=10,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(self.X_train, self.y_train)
        
        metrics = self._evaluate_model(model, "Random Forest")
        self.models['random_forest'] = model
        self.results['random_forest'] = metrics
        
        return self
    
    def train_xgboost(self):
        """Train XGBoost"""
        if not XGBOOST_AVAILABLE:
            print("\n⚠️ XGBoost not available, skipping...")
            return self
            
        print("\n" + "="*80)
        print("3. TRAINING XGBOOST".center(80))
        print("="*80)
        
        # Calculate scale_pos_weight
        scale_pos_weight = (self.y_train == 0).sum() / (self.y_train == 1).sum()
        
        model = XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            scale_pos_weight=scale_pos_weight,
            random_state=42,
            use_label_encoder=False,
            eval_metric='logloss'
        )
        
        model.fit(self.X_train, self.y_train)
        
        metrics = self._evaluate_model(model, "XGBoost")
        self.models['xgboost'] = model
        self.results['xgboost'] = metrics
        
        return self
    
    def train_lightgbm(self):
        """Train LightGBM"""
        if not LIGHTGBM_AVAILABLE:
            print("\n⚠️ LightGBM not available, skipping...")
            return self
            
        print("\n" + "="*80)
        print("4. TRAINING LIGHTGBM".center(80))
        print("="*80)
        
        model = LGBMClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            class_weight='balanced',
            random_state=42,
            verbose=-1
        )
        
        model.fit(self.X_train, self.y_train)
        
        metrics = self._evaluate_model(model, "LightGBM")
        self.models['lightgbm'] = model
        self.results['lightgbm'] = metrics
        
        return self
    
    def _evaluate_model(self, model, model_name):
        """Evaluate model performance"""
        # Predictions
        y_pred = model.predict(self.X_test)
        y_prob = model.predict_proba(self.X_test)[:, 1]
        
        # Metrics
        metrics = {
            'model_name': model_name,
            'accuracy': accuracy_score(self.y_test, y_pred),
            'precision': precision_score(self.y_test, y_pred, zero_division=0),
            'recall': recall_score(self.y_test, y_pred, zero_division=0),
            'f1_score': f1_score(self.y_test, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(self.y_test, y_prob)
        }
        
        # Cross-validation on training set
        cv_scores = cross_val_score(
            model, self.X_train, self.y_train, 
            cv=5, scoring='roc_auc', n_jobs=-1
        )
        metrics['cv_auc_mean'] = cv_scores.mean()
        metrics['cv_auc_std'] = cv_scores.std()
        
        # Print results
        print(f"\n✅ {model_name} Results:")
        print(f"   Accuracy:  {metrics['accuracy']:.4f}")
        print(f"   Precision: {metrics['precision']:.4f}")
        print(f"   Recall:    {metrics['recall']:.4f}")
        print(f"   F1-Score:  {metrics['f1_score']:.4f}")
        print(f"   ROC-AUC:   {metrics['roc_auc']:.4f}")
        print(f"   CV AUC:    {metrics['cv_auc_mean']:.4f} (±{metrics['cv_auc_std']:.4f})")
        
        # Track best model
        if metrics['roc_auc'] > self.best_score:
            self.best_score = metrics['roc_auc']
            self.best_model = (model_name, model)
        
        # Log to MLflow if available
        if MLFLOW_AVAILABLE:
            try:
                mlflow.set_experiment("credit_scoring_models")
                with mlflow.start_run(run_name=model_name):
                    mlflow.log_params({
                        'model_type': model_name,
                        'features': len(self.feature_cols)
                    })
                    mlflow.log_metrics({
                        'accuracy': metrics['accuracy'],
                        'precision': metrics['precision'],
                        'recall': metrics['recall'],
                        'f1_score': metrics['f1_score'],
                        'roc_auc': metrics['roc_auc'],
                        'cv_auc': metrics['cv_auc_mean']
                    })
                    mlflow.sklearn.log_model(model, "model")
            except Exception as e:
                print(f"   ⚠️ MLflow logging failed: {e}")
        
        return metrics
    
    def save_results(self):
        """Save models and results"""
        print("\n" + "="*80)
        print("SAVING RESULTS".center(80))
        print("="*80)
        
        # Create models directory
        models_dir = Path("models")
        models_dir.mkdir(exist_ok=True)
        
        # Save best model
        if self.best_model:
            model_name, model = self.best_model
            model_path = models_dir / "best_model.pkl"
            joblib.dump(model, model_path)
            print(f"\n✅ Best model ({model_name}) saved: {model_path}")
            
            # Save feature columns
            features_path = models_dir / "feature_columns.pkl"
            joblib.dump(self.feature_cols, features_path)
            print(f"✅ Feature columns saved: {features_path}")
        
        # Save all models
        for name, model in self.models.items():
            path = models_dir / f"{name}.pkl"
            joblib.dump(model, path)
            print(f"✅ {name} saved: {path}")
        
        # Save metrics to JSON
        results_path = models_dir / "model_results.json"
        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n✅ Results saved: {results_path}")
        
        # Create summary report
        self._create_summary_report()
        
        return self
    
    def _create_summary_report(self):
        """Create summary report"""
        report_path = Path("models") / "training_summary.txt"
        
        with open(report_path, 'w') as f:
            f.write("="*80 + "\n")
            f.write("CREDIT SCORING MODEL TRAINING SUMMARY\n")
            f.write("="*80 + "\n\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Dataset: {self.data_path}\n")
            f.write(f"Training samples: {len(self.X_train):,}\n")
            f.write(f"Test samples: {len(self.X_test):,}\n")
            f.write(f"Features: {len(self.feature_cols)}\n\n")
            
            f.write("="*80 + "\n")
            f.write("MODEL PERFORMANCE COMPARISON\n")
            f.write("="*80 + "\n\n")
            
            # Sort by ROC-AUC
            sorted_results = sorted(
                self.results.items(),
                key=lambda x: x[1]['roc_auc'],
                reverse=True
            )
            
            f.write(f"{'Model':<20} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1':<12} {'ROC-AUC':<12}\n")
            f.write("-"*80 + "\n")
            
            for name, metrics in sorted_results:
                f.write(f"{metrics['model_name']:<20} ")
                f.write(f"{metrics['accuracy']:<12.4f} ")
                f.write(f"{metrics['precision']:<12.4f} ")
                f.write(f"{metrics['recall']:<12.4f} ")
                f.write(f"{metrics['f1_score']:<12.4f} ")
                f.write(f"{metrics['roc_auc']:<12.4f}\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write(f"BEST MODEL: {self.best_model[0] if self.best_model else 'N/A'}\n")
            f.write(f"BEST ROC-AUC: {self.best_score:.4f}\n")
            f.write("="*80 + "\n")
        
        print(f"✅ Summary report: {report_path}")
        
        # Also print to console
        print("\n" + "="*80)
        print("MODEL COMPARISON SUMMARY".center(80))
        print("="*80)
        
        print(f"\n{'Model':<20} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1':<12} {'ROC-AUC':<12}")
        print("-"*80)
        
        for name, metrics in sorted_results:
            print(f"{metrics['model_name']:<20} ", end='')
            print(f"{metrics['accuracy']:<12.4f} ", end='')
            print(f"{metrics['precision']:<12.4f} ", end='')
            print(f"{metrics['recall']:<12.4f} ", end='')
            print(f"{metrics['f1_score']:<12.4f} ", end='')
            print(f"{metrics['roc_auc']:<12.4f}")
        
        print("\n" + "="*80)
        print(f"🏆 BEST MODEL: {self.best_model[0] if self.best_model else 'N/A'}")
        print(f"🏆 BEST ROC-AUC: {self.best_score:.4f}")
        print("="*80)


def main():
    """Main execution"""
    print("\n" + "="*80)
    print("CREDIT SCORING - AUTOMATED MODEL TRAINING".center(80))
    print("Student: Atuhaire (B35093)".center(80))
    print("="*80 + "\n")
    
    # Data path
    data_path = Path("data") / "cleaned" / "Atuhaire.csv"
    
    if not data_path.exists():
        print(f"❌ Error: Dataset not found at {data_path}")
        print("Please run the data preparation notebooks first!")
        return
    
    # Create trainer
    trainer = CreditScoringTrainer(data_path)
    
    try:
        # Execute training pipeline
        trainer.load_data() \
               .train_logistic_regression() \
               .train_random_forest() \
               .train_xgboost() \
               .train_lightgbm() \
               .save_results()
        
        print("\n" + "="*80)
        print("✅ TRAINING COMPLETE!".center(80))
        print("="*80)
        print("\nNext steps:")
        print("1. Check models/ directory for saved models")
        print("2. Review models/training_summary.txt")
        print("3. Run: mlflow ui (to view experiments)")
        print("4. Use best model in deployment API")
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
