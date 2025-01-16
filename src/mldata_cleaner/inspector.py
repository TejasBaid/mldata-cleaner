import pandas as pd
import numpy as np

class DataInspector:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
    
    def generate_report(self, detailed=False):
        """Generate a comprehensive data quality report"""
        report = {
            'missing_values': self._analyze_missing_values(),
            'data_types': self.df.dtypes.to_dict()
        }
        return report
    
    def _analyze_missing_values(self):
        """Analyze missing values in each column"""
        missing_data = {}
        for column in self.df.columns:
            missing_count = self.df[column].isnull().sum()
            missing_percentage = (missing_count / len(self.df)) * 100
            missing_data[column] = {
                'count': missing_count,
                'percentage': missing_percentage
            }
        return missing_data