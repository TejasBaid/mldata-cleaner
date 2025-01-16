import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

class DataCleaner:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.original_df = self.df.copy()
    
    def get_columns_with_missing(self):
        """Get list of columns with missing values"""
        return [col for col in self.df.columns if self.df[col].isnull().any()]
    
    def get_columns(self):
        """Get all column names"""
        return list(self.df.columns)
    
    def get_numerical_columns(self):
        """Get numerical columns"""
        return list(self.df.select_dtypes(include=[np.number]).columns)
    
    def handle_missing_values(self, strategy, columns, fill_value=None):
        """Handle missing values in specified columns"""
        for column in columns:
            if strategy == 'constant':
                self.df[column].fillna(fill_value, inplace=True)
            elif strategy in ['mean', 'median', 'most_frequent']:
                imputer = SimpleImputer(strategy=strategy)
                self.df[column] = imputer.fit_transform(self.df[[column]])
            elif strategy == 'drop':
                self.df.dropna(subset=[column], inplace=True)
    
    def remove_duplicates(self):
        """Remove duplicate rows"""
        self.df.drop_duplicates(inplace=True)

    def count_duplicates(self):
        """Count duplicate rows"""
        return self.df.duplicated().sum()

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
        elif method == 'zscore':
            mean = self.df[column].mean()
            std_dev = self.df[column].std()
            self.df = self.df[(self.df[column] - mean).abs() / std_dev <= threshold]
    
    def get_column_stats(self, column):
        """Get statistics for a single column"""
        return {
            'type': self.df[column].dtype,
            'missing': self.df[column].isnull().sum(),
            'unique': self.df[column].nunique()
        }
    
    def save(self, output_path):
        """Save cleaned dataset"""
        self.df.to_csv(output_path, index=False)

    def print_column_types(cleaner, columns):
        """Print column types and relevant metadata"""
        from rich.table import Table
        from rich.console import Console

        console = Console()
        table = Table(title="Column Data Types")

        table.add_column("Column", style="cyan", justify="left")
        table.add_column("Type", style="magenta", justify="left")
        table.add_column("Sample Value", style="green", justify="left")

        for column in columns:
            col_type = cleaner.get_column_type(column)
            sample_value = cleaner.get_column_sample(column)
            table.add_row(column, str(col_type), str(sample_value))

        console.print(table)
    class DataCleaner:
        def get_column_type(self, column):
            """Get the data type of a specific column"""
            return self.data[column].dtype

        def get_column_sample(self, column):
            """Get a sample value from a specific column"""
            return self.data[column].iloc[0] if not self.data[column].empty else "N/A"

__all__ = ["DataCleaner", "print_column_types"]


