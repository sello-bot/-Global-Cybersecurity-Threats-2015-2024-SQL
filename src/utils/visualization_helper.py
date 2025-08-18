"""
Visualization utilities for cybersecurity analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
from typing import Optional, List, Tuple

class VisualizationHelper:
    """Helper class for creating visualizations"""
    
    def __init__(self, style: str = 'seaborn-v0_8'):
        plt.style.use(style)
        sns.set_palette('viridis')
        self.logger = logging.getLogger(__name__)
        
    def plot_threat_distribution(self, df: pd.DataFrame, 
                               title: str = "Threat Type Distribution") -> plt.Figure:
        """Create bar plot for threat distribution"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        threat_counts = df['Threat Type'].value_counts()
        bars = ax.bar(range(len(threat_counts)), threat_counts.values)
        
        # Customize plot
        ax.set_xlabel('Threat Type')
        ax.set_ylabel('Count')
        ax.set_title(title)
        ax.set_xticks(range(len(threat_counts)))
        ax.set_xticklabels(threat_counts.index, rotation=45, ha='right')
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        return fig
        
    def plot_geographic_heatmap(self, df: pd.DataFrame, 
                              value_column: str = 'attack_count') -> go.Figure:
        """Create geographic heatmap using Plotly"""
        country_data = df.groupby('Country').agg({
            'Country': 'count',
            'Financial Impact ($M)': 'mean'
        }).rename(columns={'Country': 'attack_count'}).reset_index()
        
        fig = px.choropleth(
            country_data,
            locations='Country',
            color=value_column,
            hover_name='Country',
            hover_data=['attack_count', 'Financial Impact ($M)'],
            color_continuous_scale='Viridis',
            title=f'Global Cybersecurity Threats - {value_column.title()}'
        )
        
        fig.update_layout(
            geo=dict(showframe=False, showcoastlines=True),
            title_x=0.5
        )
        
        return fig
        
    def plot_time_series(self, df: pd.DataFrame, 
                        x_col: str = 'Year', 
                        y_col: str = 'attack_count') -> plt.Figure:
        """Create time series plot"""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        yearly_data = df.groupby(x_col).size().reset_index(name=y_col)
        
        ax.plot(yearly_data[x_col], yearly_data[y_col], 
               marker='o', linewidth=2, markersize=8)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col.replace('_', ' ').title())
        ax.set_title(f'{y_col.replace("_", " ").title()} Over Time')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
        
    def plot_correlation_matrix(self, df: pd.DataFrame, 
                              numeric_cols: Optional[List[str]] = None) -> plt.Figure:
        """Create correlation matrix heatmap"""
        if numeric_cols is None:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
        correlation_matrix = df[numeric_cols].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', 
                   center=0, ax=ax, square=True)
        ax.set_title('Correlation Matrix - Numeric Variables')
        
        plt.tight_layout()
        return fig
        
    def create_dashboard(self, df: pd.DataFrame) -> go.Figure:
        """Create comprehensive dashboard"""
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Threat Types', 'Countries', 'Industries', 'Yearly Trends'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}],
                   [{'type': 'bar'}, {'type': 'scatter'}]]
        )
        
        # Threat types
        threat_counts = df['Threat Type'].value_counts().head(10)
        fig.add_trace(
            go.Bar(x=threat_counts.index, y=threat_counts.values, name='Threats'),
            row=1, col=1
        )
        
        # Countries
        country_counts = df['Country'].value_counts().head(10)
        fig.add_trace(
            go.Bar(x=country_counts.index, y=country_counts.values, name='Countries'),
            row=1, col=2
        )
        
        # Industries
        industry_counts = df['Affected Industry'].value_counts().head(10)
        fig.add_trace(
            go.Bar(x=industry_counts.index, y=industry_counts.values, name='Industries'),
            row=2, col=1
        )
        
        # Yearly trends
        yearly_data = df.groupby('Year').size()
        fig.add_trace(
            go.Scatter(x=yearly_data.index, y=yearly_data.values, 
                      mode='lines+markers', name='Yearly Attacks'),
            row=2, col=2
        )
        
        fig.update_layout(
            height=800,
            title_text="Cybersecurity Threats Dashboard",
            showlegend=False
        )
        
        return fig