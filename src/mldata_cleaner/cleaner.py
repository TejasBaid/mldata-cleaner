import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

class DataCleaner:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.original_df = self.df.copy()
        self.cleaning_log = []
    
    def get_columns_with_missing(self):
        """Get list of columns with missing values"""
        return [col for col in self.df.columns if self.df[col].isnull().any()]
    
    def handle_missing_values(self, strategy, columns, fill_value=None):
        """Handle missing values in specified columns"""
        for column in columns:
            if strategy == 'constant':
                self.df[column].fillna(fill_value, inplace=True)
            elif strategy in ['mean', 'median', 'mode']:
                if pd.api.types.is_numeric_dtype(self.df[column]):
                    imputer = SimpleImputer(strategy=strategy)
                    self.df[column] = imputer.fit_transform(self.df[[column]])
                else:
                    self.df[column].fillna(self.df[column].mode()[0], inplace=True)
            elif strategy == 'drop':
                self.df.dropna(subset=[column], inplace=True)
    
    def remove_duplicates(self):
        """Remove duplicate rows"""
        self.df.drop_duplicates(inplace=True)
    
    def convert_dtype(self, column, dtype):
        """Convert column data type"""
        try:
            self.df[column] = self.df[column].astype(dtype)
        except Exception as e:
            raise ValueError(f"Could not convert {column} to {dtype}: {str(e)}")
    
    def handle_outliers(self, column, method='iqr', threshold=1.5):
        """Handle outliers in specified column"""
        if method == 'iqr':
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            self.df = self.df[(self.df[column] >= lower_bound) & 
                             (self.df[column] <= upper_bound)]
    
    def save(self, output_path):
        """Save cleaned dataset"""
        self.df.to_csv(output_path, index=False)