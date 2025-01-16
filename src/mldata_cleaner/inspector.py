import pandas as pd
import numpy as np

class DataInspector:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        
    def get_basic_stats(self):
        """Get basic dataset statistics"""
        return {
            'rows': len(self.df),
            'columns': len(self.df.columns),
            'total_missing': self.df.isnull().sum().sum(),
            'memory_usage': f"{self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
        }
    
    def analyze_missing_values(self):
        """Analyze missing values in detail"""
        missing_data = {}
        for column in self.df.columns:
            missing_count = self.df[column].isnull().sum()
            missing_percentage = (missing_count / len(self.df)) * 100
            missing_data[column] = {
                'count': missing_count,
                'percentage': missing_percentage
            }
        return missing_data
    
    def get_data_types(self):
        """Get column data types"""
        return self.df.dtypes.to_dict()
    
    def analyze_duplicates(self):
        """Analyze duplicate rows"""
        duplicates = self.df.duplicated()
        return {
            'total_duplicates': duplicates.sum(),
            'percentage': (duplicates.sum() / len(self.df)) * 100
        }
    
    def get_statistics(self):
        """Get numerical column statistics"""
        return self.df.describe()