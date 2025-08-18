"""
Risk scoring model for cybersecurity threats
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import logging
from typing import Dict, List, Tuple, Optional

class RiskScoreModel:
    """Machine learning model for calculating threat risk scores"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.feature_columns = []
        self.is_trained = False
        self.logger = logging.getLogger(__name__)
        
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for risk scoring"""
        # Create a copy to avoid modifying original data
        data = df.copy()
        
        # Encode categorical variables
        categorical_cols = ['Country', 'Threat Type', 'Attack Vector', 
                          'Affected Industry', 'Severity Level', 'Mitigation Strategy']
        
        for col in categorical_cols:
            if col in data.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    data[f'{col}_encoded'] = self.label_encoders[col].fit_transform(data[col])
                else:
                    # Handle unseen labels
                    known_labels = set(self.label_encoders[col].classes_)
                    data[col] = data[col].apply(lambda x: x if x in known_labels else 'Unknown')
                    
                    if 'Unknown' not in known_labels:
                        # Add 'Unknown' class
                        classes = list(self.label_encoders[col].classes_) + ['Unknown']
                        self.label_encoders[col].classes_ = np.array(classes)
                    
                    data[f'{col}_encoded'] = self.label_encoders[col].transform(data[col])
        
        # Create risk-related features
        data['impact_per_gb'] = data['Financial Impact ($M)'] / (data['Data Breached (GB)'] + 1)
        data['response_efficiency'] = 1 / (data['Response Time (Hours)'] + 1)
        
        # Severity level numeric mapping
        severity_mapping = {'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}
        data['severity_numeric'] = data['Severity Level'].map(severity_mapping)
        
        return data
        
    def create_risk_score(self, df: pd.DataFrame, weights: Optional[Dict] = None) -> pd.Series:
        """Create composite risk score using weighted formula"""
        if weights is None:
            weights = {
                'financial_impact': 0.3,
                'data_breached': 0.2,
                'severity': 0.3,
                'response_time': 0.2
            }
        
        # Normalize features
        normalized_data = df.copy()
        
        # Normalize financial impact (0-1 scale)
        max_impact = df['Financial Impact ($M)'].max()
        normalized_data['norm_financial'] = df['Financial Impact ($M)'] / max_impact
        
        # Normalize data breached (0-1 scale)
        max_data = df['Data Breached (GB)'].max()
        normalized_data['norm_data'] = df['Data Breached (GB)'] / max_data
        
        # Normalize severity (already 1-4, convert to 0-1)
        severity_mapping = {'Low': 0.25, 'Medium': 0.5, 'High': 0.75, 'Critical': 1.0}
        normalized_data['norm_severity'] = df['Severity Level'].map(severity_mapping)
        
        # Normalize response time (inverse - faster response = higher score)
        max_response = df['Response Time (Hours)'].max()
        normalized_data['norm_response'] = 1 - (df['Response Time (Hours)'] / max_response)
        
        # Calculate composite risk score
        risk_score = (
            weights['financial_impact'] * normalized_data['norm_financial'] +
            weights['data_breached'] * normalized_data['norm_data'] +
            weights['severity'] * normalized_data['norm_severity'] +
            weights['response_time'] * normalized_data['norm_response']
        )
        
        # Scale to 0-100
        return (risk_score * 100).round(2)
        
    def train_ml_model(self, df: pd.DataFrame, target_col: str = 'Financial Impact ($M)') -> Dict:
        """Train ML model for risk prediction"""
        # Prepare features
        data = self.prepare_features(df)
        
        # Select features for training
        feature_cols = [col for col in data.columns if col.endswith('_encoded')] + \
                      ['Data Breached (GB)', 'Response Time (Hours)', 
                       'impact_per_gb', 'response_efficiency', 'severity_numeric']
        
        self.feature_columns = [col for col in feature_cols if col in data.columns]
        
        X = data[self.feature_columns]
        y = data[target_col]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Make predictions
        y_pred = self.model.predict(X_test_scaled)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        self.is_trained = True
        
        metrics = {
            'mse': mse,
            'rmse': np.sqrt(mse),
            'r2': r2,
            'feature_importance': dict(zip(self.feature_columns, 
                                         self.model.feature_importances_))
        }
        
        self.logger.info(f"Model trained successfully. R² Score: {r2:.3f}")
        return metrics
        
    def predict_risk(self, df: pd.DataFrame) -> np.ndarray:
        """Predict risk scores for new data"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
            
        data = self.prepare_features(df)
        X = data[self.feature_columns]
        X_scaled = self.scaler.transform(X)
        
        return self.model.predict(X_scaled)
        
    def get_feature_importance(self) -> pd.DataFrame:
        """Get feature importance from trained model"""
        if not self.is_trained:
            raise ValueError("Model must be trained first")
            
        importance_df = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return importance_df