"""
Configuration settings for Cybersecurity Threats Analysis
"""
import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_DIR = DATA_DIR / "sample"

# Output directories
VISUALIZATIONS_DIR = PROJECT_ROOT / "visualizations"
CHARTS_DIR = VISUALIZATIONS_DIR / "charts"
MAPS_DIR = VISUALIZATIONS_DIR / "maps"
DASHBOARDS_DIR = VISUALIZATIONS_DIR / "dashboards"

# SQL directory
SQL_DIR = PROJECT_ROOT / "sql"

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", ":memory:")
KAGGLE_DATA_PATH = "/kaggle/input/global-cybersecurity-threats-2015-2024"

# Analysis parameters
DEFAULT_LIMIT = 50
RISK_SCORE_WEIGHTS = {
    'frequency': 0.3,
    'financial_impact': 0.3,
    'data_breached': 0.1,
    'severity': 0.3
}

# Visualization settings
PLOT_STYLE = "seaborn-v0_8"
COLOR_PALETTE = "viridis"
FIGURE_SIZE = (12, 8)
DPI = 300

# Column mappings
COLUMN_MAPPING = {
    'country': 'Country',
    'year': 'Year',
    'threat_type': 'Threat Type',
    'attack_vector': 'Attack Vector',
    'affected_industry': 'Affected Industry',
    'data_breached_gb': 'Data Breached (GB)',
    'financial_impact_m': 'Financial Impact ($M)',
    'severity_level': 'Severity Level',
    'response_time_hours': 'Response Time (Hours)',
    'mitigation_strategy': 'Mitigation Strategy'
}

# Create directories if they don't exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, SAMPLE_DATA_DIR,
                 VISUALIZATIONS_DIR, CHARTS_DIR, MAPS_DIR, DASHBOARDS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)