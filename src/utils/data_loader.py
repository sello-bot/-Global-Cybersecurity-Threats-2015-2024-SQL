"""
Data loading utilities
"""

import pandas as pd
import os
from pathlib import Path
import logging
from typing import Optional, List

class DataLoader:
    """Handles data loading operations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def load_csv(self, file_path: str, **kwargs) -> pd.DataFrame:
        """Load CSV file with error handling"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
                
            df = pd.read_csv(file_path, **kwargs)
            self.logger.info(f"Successfully loaded {len(df)} rows from {file_path}")
            return df
            
        except Exception as e:
            self.logger.error(f"Error loading CSV: {e}")
            raise
            
    def detect_files_in_directory(self, directory_path: str, 
                                 extensions: List[str] = ['.csv']) -> List[str]:
        """Detect files with specified extensions in directory"""
        try:
            files = []
            for ext in extensions:
                files.extend(Path(directory_path).glob(f'*{ext}'))
            return [str(f) for f in files]
        except Exception as e:
            self.logger.error(f"Error detecting files: {e}")
            return []
            
    def validate_dataset(self, df: pd.DataFrame, required_columns: List[str]) -> bool:
        """Validate if dataset has required columns"""
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            self.logger.warning(f"Missing columns: {missing_columns}")
            return False
        return True
        
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Basic data cleaning operations"""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        numeric_columns = df.select_dtypes(include=['number']).columns
        df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
        
        # Handle categorical missing values
        categorical_columns = df.select_dtypes(include=['object']).columns
        df[categorical_columns] = df[categorical_columns].fillna('Unknown')
        
        self.logger.info("Data cleaning completed")
        return df