"""
SQL Query execution utilities
"""

import pandas as pd
import sqlite3
import logging
from typing import Optional, Any

class QueryExecutor:
    """Handles SQL query execution"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def execute_query(self, query: str, connection: sqlite3.Connection) -> pd.DataFrame:
        """Execute SQL query and return DataFrame"""
        try:
            result = pd.read_sql_query(query, connection)
            self.logger.info(f"Query executed successfully, returned {len(result)} rows")
            return result
        except Exception as e:
            self.logger.error(f"Error executing query: {e}")
            self.logger.error(f"Query: {query[:100]}...")
            raise
            
    def execute_many_queries(self, queries: list, connection: sqlite3.Connection) -> dict:
        """Execute multiple queries and return results dictionary"""
        results = {}
        for i, query in enumerate(queries):
            try:
                results[f"query_{i+1}"] = self.execute_query(query, connection)
            except Exception as e:
                self.logger.error(f"Error in query {i+1}: {e}")
                results[f"query_{i+1}"] = None
        return results
        
    def create_table_from_df(self, df: pd.DataFrame, table_name: str, 
                           connection: sqlite3.Connection, if_exists: str = 'replace') -> bool:
        """Create table from DataFrame"""
        try:
            df.to_sql(table_name, connection, index=False, if_exists=if_exists)
            self.logger.info(f"Table '{table_name}' created successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error creating table: {e}")
            return False