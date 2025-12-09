"""
Data preprocessing functions for Credit Scoring project
"""

import pandas as pd
import numpy as np
from typing import List, Tuple, Dict, Any
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')


class DataPreprocessor:
    """
    Comprehensive data preprocessing pipeline for credit scoring.
    """
    
    def __init__(self):
        self.label_encoders = {}
        self.scaler = None
        self.imputers = {}
        self.feature_names = []
        
    def handle_missing_values(self, df: pd.DataFrame, strategy: Dict[str, str] = None) -> pd.DataFrame:
        """
        Handle missing values with specified strategies.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        strategy : Dict[str, str]
            Dictionary mapping column names to imputation strategies
            ('mean', 'median', 'mode', 'ffill', 'bfill', or specific value)
        
        Returns:
        --------
        pd.DataFrame : DataFrame with imputed values
        """
        df_clean = df.copy()
        
        if strategy is None:
            # Default strategy: mean for numerical, mode for categorical
            numerical_cols = df_clean.select_dtypes(include=[np.number]).columns
            categorical_cols = df_clean.select_dtypes(include=['object', 'category']).columns
            
            for col in numerical_cols:
                if df_clean[col].isnull().any():
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
            
            for col in categorical_cols:
                if df_clean[col].isnull().any():
                    df_clean[col].fillna(df_clean[col].mode()[0] if not df_clean[col].mode().empty else 'Unknown', inplace=True)
        else:
            for col, strat in strategy.items():
                if col in df_clean.columns and df_clean[col].isnull().any():
                    if strat == 'mean':
                        df_clean[col].fillna(df_clean[col].mean(), inplace=True)
                    elif strat == 'median':
                        df_clean[col].fillna(df_clean[col].median(), inplace=True)
                    elif strat == 'mode':
                        df_clean[col].fillna(df_clean[col].mode()[0] if not df_clean[col].mode().empty else 'Unknown', inplace=True)
                    elif strat == 'ffill':
                        df_clean[col].fillna(method='ffill', inplace=True)
                    elif strat == 'bfill':
                        df_clean[col].fillna(method='bfill', inplace=True)
                    else:
                        df_clean[col].fillna(strat, inplace=True)
        
        return df_clean
    
    def handle_outliers(self, df: pd.DataFrame, columns: List[str], method: str = 'iqr', 
                       action: str = 'cap', multiplier: float = 1.5) -> pd.DataFrame:
        """
        Handle outliers in specified columns.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        columns : List[str]
            Columns to check for outliers
        method : str
            Outlier detection method ('iqr' or 'zscore')
        action : str
            Action to take ('cap', 'remove', or 'flag')
        multiplier : float
            Multiplier for IQR method
        
        Returns:
        --------
        pd.DataFrame : DataFrame with handled outliers
        """
        df_clean = df.copy()
        
        for col in columns:
            if col not in df_clean.columns or df_clean[col].dtype not in [np.int64, np.float64]:
                continue
            
            if method == 'iqr':
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - multiplier * IQR
                upper_bound = Q3 + multiplier * IQR
            elif method == 'zscore':
                mean = df_clean[col].mean()
                std = df_clean[col].std()
                lower_bound = mean - 3 * std
                upper_bound = mean + 3 * std
            else:
                continue
            
            if action == 'cap':
                df_clean[col] = df_clean[col].clip(lower=lower_bound, upper=upper_bound)
            elif action == 'remove':
                df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
            elif action == 'flag':
                df_clean[f'{col}_is_outlier'] = ((df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)).astype(int)
        
        return df_clean
    
    def encode_categorical(self, df: pd.DataFrame, columns: List[str], method: str = 'label') -> pd.DataFrame:
        """
        Encode categorical variables.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        columns : List[str]
            Columns to encode
        method : str
            Encoding method ('label' or 'onehot')
        
        Returns:
        --------
        pd.DataFrame : DataFrame with encoded variables
        """
        df_encoded = df.copy()
        
        for col in columns:
            if col not in df_encoded.columns:
                continue
            
            if method == 'label':
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    df_encoded[col] = self.label_encoders[col].fit_transform(df_encoded[col].astype(str))
                else:
                    df_encoded[col] = self.label_encoders[col].transform(df_encoded[col].astype(str))
            
            elif method == 'onehot':
                dummies = pd.get_dummies(df_encoded[col], prefix=col, drop_first=True)
                df_encoded = pd.concat([df_encoded, dummies], axis=1)
                df_encoded.drop(col, axis=1, inplace=True)
        
        return df_encoded
    
    def scale_features(self, df: pd.DataFrame, columns: List[str], method: str = 'standard') -> pd.DataFrame:
        """
        Scale numerical features.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        columns : List[str]
            Columns to scale
        method : str
            Scaling method ('standard' or 'minmax')
        
        Returns:
        --------
        pd.DataFrame : DataFrame with scaled features
        """
        df_scaled = df.copy()
        
        if method == 'standard':
            if self.scaler is None:
                self.scaler = StandardScaler()
                df_scaled[columns] = self.scaler.fit_transform(df_scaled[columns])
            else:
                df_scaled[columns] = self.scaler.transform(df_scaled[columns])
        
        elif method == 'minmax':
            if self.scaler is None:
                self.scaler = MinMaxScaler()
                df_scaled[columns] = self.scaler.fit_transform(df_scaled[columns])
            else:
                df_scaled[columns] = self.scaler.transform(df_scaled[columns])
        
        return df_scaled
    
    def create_interaction_features(self, df: pd.DataFrame, feature_pairs: List[Tuple[str, str]]) -> pd.DataFrame:
        """
        Create interaction features from pairs of columns.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        feature_pairs : List[Tuple[str, str]]
            List of feature pairs to create interactions
        
        Returns:
        --------
        pd.DataFrame : DataFrame with interaction features
        """
        df_features = df.copy()
        
        for col1, col2 in feature_pairs:
            if col1 in df_features.columns and col2 in df_features.columns:
                if df_features[col1].dtype in [np.int64, np.float64] and df_features[col2].dtype in [np.int64, np.float64]:
                    df_features[f'{col1}_x_{col2}'] = df_features[col1] * df_features[col2]
                    df_features[f'{col1}_div_{col2}'] = df_features[col1] / (df_features[col2] + 1e-8)
        
        return df_features
    
    def create_polynomial_features(self, df: pd.DataFrame, columns: List[str], degree: int = 2) -> pd.DataFrame:
        """
        Create polynomial features.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        columns : List[str]
            Columns to create polynomial features
        degree : int
            Polynomial degree
        
        Returns:
        --------
        pd.DataFrame : DataFrame with polynomial features
        """
        df_poly = df.copy()
        
        for col in columns:
            if col in df_poly.columns and df_poly[col].dtype in [np.int64, np.float64]:
                for d in range(2, degree + 1):
                    df_poly[f'{col}_pow_{d}'] = df_poly[col] ** d
        
        return df_poly
    
    def create_binned_features(self, df: pd.DataFrame, column: str, bins: int = 5, labels: List[str] = None) -> pd.DataFrame:
        """
        Create binned categorical features from continuous variables.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        column : str
            Column to bin
        bins : int
            Number of bins
        labels : List[str]
            Custom labels for bins
        
        Returns:
        --------
        pd.DataFrame : DataFrame with binned feature
        """
        df_binned = df.copy()
        
        if column in df_binned.columns and df_binned[column].dtype in [np.int64, np.float64]:
            if labels is None:
                labels = [f'{column}_bin_{i}' for i in range(bins)]
            
            df_binned[f'{column}_binned'] = pd.cut(df_binned[column], bins=bins, labels=labels)
        
        return df_binned


def anonymize_data(df: pd.DataFrame, sensitive_columns: List[str]) -> pd.DataFrame:
    """
    Anonymize sensitive data for privacy compliance.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    sensitive_columns : List[str]
        Columns containing sensitive information
    
    Returns:
    --------
    pd.DataFrame : Anonymized dataframe
    """
    df_anon = df.copy()
    
    for col in sensitive_columns:
        if col in df_anon.columns:
            # Hash sensitive data
            df_anon[col] = df_anon[col].apply(lambda x: hash(str(x)) % 1000000)
    
    return df_anon


def create_privacy_report(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Create data privacy compliance report.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    
    Returns:
    --------
    Dict : Privacy analysis report
    """
    report = {
        'total_records': len(df),
        'total_features': len(df.columns),
        'potential_pii_columns': [],
        'data_minimization_check': True,
        'anonymization_required': []
    }
    
    # Identify potential PII columns
    pii_keywords = ['name', 'email', 'phone', 'address', 'ssn', 'id', 'passport']
    for col in df.columns:
        if any(keyword in col.lower() for keyword in pii_keywords):
            report['potential_pii_columns'].append(col)
            report['anonymization_required'].append(col)
    
    return report
