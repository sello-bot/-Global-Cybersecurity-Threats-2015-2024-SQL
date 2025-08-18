"""
Unit tests for SQL queries and analysis functions
"""

import unittest
import pandas as pd
import sqlite3
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from analysis.threat_analyzer import ThreatAnalyzer
from utils.data_loader import DataLoader
from utils.query_executor import QueryExecutor

class TestCybersecurityAnalysis(unittest.TestCase):
    """Test suite for cybersecurity analysis functions"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test data"""
        # Create sample data for testing
        cls.sample_data = pd.DataFrame({
            'Country': ['USA', 'UK', 'Germany', 'USA', 'UK'],
            'Year': [2020, 2020, 2021, 2021, 2022],
            'Threat Type': ['Malware', 'Phishing', 'DDoS', 'Ransomware', 'Malware'],
            'Attack Vector': ['Email', 'Web', 'Network', 'Email', 'USB'],
            'Affected Industry': ['Finance', 'Healthcare', 'Tech', 'Finance', 'Retail'],
            'Data Breached (GB)': [100.5, 25.3, 500.7, 75.2, 200.1],
            'Financial Impact ($M)': [10.5, 2.3, 50.7, 7.5, 20.1],
            'Severity Level': ['High', 'Medium', 'Critical', 'High', 'Low'],
            'Response Time (Hours)': [24, 48, 12, 36, 72],
            'Mitigation Strategy': ['Patching', 'Training', 'Blocking', 'Backup', 'Isolation']
        })
        
        # Create in-memory database
        cls.conn = sqlite3.connect(':memory:')
        cls.sample_data.to_sql('cybersecurity_threats', cls.conn, 
                              index=False, if_exists='replace')
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        cls.conn.close()
    
    def test_data_loader(self):
        """Test DataLoader functionality"""
        loader = DataLoader()
        
        # Test required columns validation
        required_columns = ['Country', 'Year', 'Threat Type']
        self.assertTrue(loader.validate_dataset(self.sample_data, required_columns))
        
        # Test missing columns
        missing_columns = ['NonExistentColumn']
        self.assertFalse(loader.validate_dataset(self.sample_data, missing_columns))
    
    def test_basic_queries(self):
        """Test basic SQL queries"""
        executor = QueryExecutor()
        
        # Test threat type distribution
        query = '''
        SELECT 
            "Threat Type",
            COUNT(*) as count
        FROM cybersecurity_threats
        GROUP BY "Threat Type"
        ORDER BY count DESC
        '''
        
        result = executor.execute_query(query, self.conn)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(len(result) > 0)
        self.assertIn('Threat Type', result.columns)
        self.assertIn('count', result.columns)
    
    def test_country_analysis(self):
        """Test country-based analysis"""
        executor = QueryExecutor()
        
        query = '''
        SELECT 
            Country,
            COUNT(*) as attack_count,
            AVG("Financial Impact ($M)") as avg_impact
        FROM cybersecurity_threats
        GROUP BY Country
        ORDER BY attack_count DESC
        '''
        
        result = executor.execute_query(query, self.conn)
        self.assertTrue(len(result) > 0)
        
        # Check if USA has the highest attack count (based on sample data)
        top_country = result.iloc[0]['Country']
        self.assertEqual(top_country, 'USA')
    
    def test_severity_analysis(self):
        """Test severity level analysis"""
        executor = QueryExecutor()
        
        query = '''
        SELECT 
            "Severity Level",
            COUNT(*) as count,
            AVG("Response Time (Hours)") as avg_response_time
        FROM cybersecurity_threats
        GROUP BY "Severity Level"
        '''
        
        result = executor.execute_query(query, self.conn)
        self.assertTrue(len(result) > 0)
        self.assertIn('Severity Level', result.columns)
    
    def test_yearly_trends(self):
        """Test yearly trend analysis"""
        executor = QueryExecutor()
        
        query = '''
        SELECT 
            Year,
            COUNT(*) as attack_count,
            SUM("Financial Impact ($M)") as total_impact
        FROM cybersecurity_threats
        GROUP BY Year
        ORDER BY Year
        '''
        
        result = executor.execute_query(query, self.conn)
        self.assertTrue(len(result) > 0)
        self.assertTrue(result['Year'].is_monotonic_increasing)

if __name__ == '__main__':
    unittest.main()