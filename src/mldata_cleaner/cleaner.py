import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

class DataCleaner:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.original_df = self.df.copy()
        self.cleaning_log = []
    
    def clean(self, strategy='mean', fill_value=None, columns=None):
        """Clean the dataset using specified strategy"""
        if columns is None:
            columns = self.df.columns
        
        for column in columns:
            if self.df[column].isnull().any():
                self._handle_missing_values(column, strategy, fill_value)
    
    def _handle_missing_values(self, column, strategy, fill_value):
        """Handle missing values in a column"""
        if strategy == 'constant' and fill_value is not None:
            self.df[column].fillna(fill_value, inplace=True)
        elif strategy in ['mean', 'median', 'mode']:
            imputer = SimpleImputer(strategy=strategy)
            self.df[column] = imputer.fit_transform(self.df[[column]])
        elif strategy == 'drop':
            self.df.dropna(subset=[column], inplace=True)
        
        self.cleaning_log.append(f"Applied {strategy} strategy to column {column}")
    
    def save(self, output_path):
        """Save the cleaned dataset"""
        self.df.to_csv(output_path, index=False)