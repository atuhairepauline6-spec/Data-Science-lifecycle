"""
Utility functions for the Credit Scoring project
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# Set visualization defaults
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def print_section_header(title: str, char: str = "=") -> None:
    """Print a formatted section header."""
    print(f"\n{char * 80}")
    print(f"{title.center(80)}")
    print(f"{char * 80}\n")


def dataset_overview(df: pd.DataFrame, name: str = "Dataset") -> None:
    """
    Print comprehensive dataset overview.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset to analyze
    name : str
        Name of the dataset for display
    """
    print_section_header(f"{name} Overview")
    
    print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]:,} columns")
    print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"\nColumn Types:")
    print(df.dtypes.value_counts())
    
    print(f"\nMissing Values:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing Count': missing[missing > 0],
        'Percentage': missing_pct[missing > 0]
    }).sort_values('Percentage', ascending=False)
    
    if len(missing_df) > 0:
        print(missing_df)
    else:
        print("No missing values found!")
    
    print(f"\nDuplicate Rows: {df.duplicated().sum():,}")
    
    print(f"\nNumerical Columns Summary:")
    print(df.describe().T)


def plot_missing_values(df: pd.DataFrame, figsize: Tuple[int, int] = (12, 6)) -> None:
    """
    Visualize missing values in the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset to analyze
    figsize : Tuple[int, int]
        Figure size
    """
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Column': missing.index,
        'Missing Count': missing.values,
        'Percentage': missing_pct.values
    })
    missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Percentage', ascending=False)
    
    if len(missing_df) == 0:
        print("No missing values to visualize!")
        return
    
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Bar plot
    axes[0].barh(missing_df['Column'], missing_df['Percentage'], color='coral')
    axes[0].set_xlabel('Percentage Missing (%)')
    axes[0].set_title('Missing Values by Column')
    axes[0].grid(axis='x', alpha=0.3)
    
    # Heatmap
    sns.heatmap(df.isnull().T, cmap='YlOrRd', cbar=True, ax=axes[1])
    axes[1].set_title('Missing Values Heatmap')
    
    plt.tight_layout()
    plt.show()


def plot_distribution(df: pd.DataFrame, columns: List[str], ncols: int = 3, figsize: Tuple[int, int] = (15, 10)) -> None:
    """
    Plot distributions of numerical columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset
    columns : List[str]
        List of columns to plot
    ncols : int
        Number of columns in subplot grid
    figsize : Tuple[int, int]
        Figure size
    """
    nrows = (len(columns) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    axes = axes.flatten() if len(columns) > 1 else [axes]
    
    for idx, col in enumerate(columns):
        if idx < len(axes):
            df[col].hist(bins=30, ax=axes[idx], edgecolor='black', alpha=0.7)
            axes[idx].set_title(f'Distribution of {col}')
            axes[idx].set_xlabel(col)
            axes[idx].set_ylabel('Frequency')
            axes[idx].grid(axis='y', alpha=0.3)
    
    # Hide unused subplots
    for idx in range(len(columns), len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.show()


def plot_correlation_matrix(df: pd.DataFrame, figsize: Tuple[int, int] = (12, 10), method: str = 'pearson') -> None:
    """
    Plot correlation matrix heatmap.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset
    figsize : Tuple[int, int]
        Figure size
    method : str
        Correlation method ('pearson', 'spearman', 'kendall')
    """
    # Select only numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numerical_cols) < 2:
        print("Not enough numerical columns for correlation analysis!")
        return
    
    corr_matrix = df[numerical_cols].corr(method=method)
    
    plt.figure(figsize=figsize)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title(f'{method.capitalize()} Correlation Matrix', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()


def detect_outliers_iqr(df: pd.DataFrame, column: str, multiplier: float = 1.5) -> pd.Series:
    """
    Detect outliers using IQR method.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset
    column : str
        Column name to check for outliers
    multiplier : float
        IQR multiplier (default 1.5)
    
    Returns:
    --------
    pd.Series : Boolean series indicating outliers
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    
    return (df[column] < lower_bound) | (df[column] > upper_bound)


def plot_outliers_boxplot(df: pd.DataFrame, columns: List[str], ncols: int = 3, figsize: Tuple[int, int] = (15, 10)) -> None:
    """
    Plot boxplots to visualize outliers.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset
    columns : List[str]
        List of columns to plot
    ncols : int
        Number of columns in subplot grid
    figsize : Tuple[int, int]
        Figure size
    """
    nrows = (len(columns) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    axes = axes.flatten() if len(columns) > 1 else [axes]
    
    for idx, col in enumerate(columns):
        if idx < len(axes):
            df.boxplot(column=col, ax=axes[idx])
            axes[idx].set_title(f'Boxplot of {col}')
            axes[idx].set_ylabel(col)
            axes[idx].grid(axis='y', alpha=0.3)
    
    # Hide unused subplots
    for idx in range(len(columns), len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.show()


def save_dataset(df: pd.DataFrame, filepath: str, index: bool = False) -> None:
    """
    Save dataset to CSV file.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset to save
    filepath : str
        Output file path
    index : bool
        Whether to include index
    """
    df.to_csv(filepath, index=index)
    print(f"✅ Dataset saved to: {filepath}")
    print(f"   Shape: {df.shape[0]:,} rows × {df.shape[1]:,} columns")
    print(f"   File size: {pd.io.common.file_exists(filepath) and 'Success' or 'Failed'}")


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray = None) -> Dict[str, float]:
    """
    Calculate comprehensive classification metrics.
    
    Parameters:
    -----------
    y_true : np.ndarray
        True labels
    y_pred : np.ndarray
        Predicted labels
    y_prob : np.ndarray, optional
        Predicted probabilities for positive class
    
    Returns:
    --------
    Dict[str, float] : Dictionary of metrics
    """
    from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                                   f1_score, roc_auc_score, confusion_matrix)
    
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average='binary', zero_division=0),
        'recall': recall_score(y_true, y_pred, average='binary', zero_division=0),
        'f1_score': f1_score(y_true, y_pred, average='binary', zero_division=0)
    }
    
    if y_prob is not None:
        metrics['roc_auc'] = roc_auc_score(y_true, y_prob)
    
    return metrics


def print_metrics(metrics: Dict[str, float]) -> None:
    """
    Print metrics in a formatted table.
    
    Parameters:
    -----------
    metrics : Dict[str, float]
        Dictionary of metrics
    """
    print("\n" + "="*50)
    print("MODEL PERFORMANCE METRICS".center(50))
    print("="*50)
    
    for metric_name, value in metrics.items():
        print(f"{metric_name.replace('_', ' ').title():<30}: {value:.4f}")
    
    print("="*50 + "\n")
