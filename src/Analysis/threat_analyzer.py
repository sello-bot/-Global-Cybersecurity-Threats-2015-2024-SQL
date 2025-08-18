"""
Core threat analysis functionality
"""

import pandas as pd
import sqlite3
from typing import Dict, List, Optional
import logging

from ..utils.data_loader import DataLoader
from ..utils.query_executor import QueryExecutor

class ThreatAnalyzer:
    """Main class for cybersecurity threat analysis"""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.loader = DataLoader()
        self.executor = QueryExecutor()
        self.df = None
        self.conn = None
        self.logger = logging.getLogger(__name__)
        
    def load_data(self) -> pd.DataFrame:
        """Load and prepare the dataset"""
        try:
            self.df = self.loader.load_csv(self.data_path)
            self.conn = sqlite3.connect(':memory:')
            self.df.to_sql('cybersecurity_threats', self.conn, 
                          index=False, if_exists='replace')
            self.logger.info(f"Data loaded successfully: {self.df.shape}")
            return self.df
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            raise
            
    def get_threat_distribution(self) -> pd.DataFrame:
        """Get distribution of threat types"""
        query = """
        SELECT 
            "Threat Type",
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM cybersecurity_threats), 2) as percentage
        FROM cybersecurity_threats
        GROUP BY "Threat Type"
        ORDER BY count DESC
        """
        return self.executor.execute_query(query, self.conn)
        
    def get_top_countries(self, limit: int = 10) -> pd.DataFrame:
        """Get top countries by attack count"""
        query = f"""
        SELECT 
            Country,
            COUNT(*) as attack_count,
            ROUND(AVG("Financial Impact ($M)"), 2) as avg_financial_impact,
            ROUND(AVG("Data Breached (GB)"), 2) as avg_data_breached
        FROM cybersecurity_threats
        GROUP BY Country
        ORDER BY attack_count DESC
        LIMIT {limit}
        """
        return self.executor.execute_query(query, self.conn)
        
    def get_industry_analysis(self) -> pd.DataFrame:
        """Analyze attacks by industry"""
        query = """
        SELECT 
            "Affected Industry",
            COUNT(*) as attack_count,
            ROUND(AVG("Financial Impact ($M)"), 2) as avg_financial_impact,
            ROUND(AVG("Response Time (Hours)"), 2) as avg_response_time,
            SUM(CASE WHEN "Severity Level" IN ('Critical', 'High') THEN 1 ELSE 0 END) as high_severity_count
        FROM cybersecurity_threats
        GROUP BY "Affected Industry"
        ORDER BY attack_count DESC
        """
        return self.executor.execute_query(query, self.conn)
        
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()