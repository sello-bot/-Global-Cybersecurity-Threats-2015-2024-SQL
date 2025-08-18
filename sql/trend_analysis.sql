-- Trend Analysis Queries for Cybersecurity Threats Dataset

-- Query 1: Yearly Trend Analysis
SELECT 
    Year,
    COUNT(*) as total_attacks,
    ROUND(SUM("Financial Impact ($M)"), 2) as total_financial_impact,
    ROUND(SUM("Data Breached (GB)"), 2) as total_data_breached,
    ROUND(AVG("Response Time (Hours)"), 2) as avg_response_time,
    COUNT(CASE WHEN "Severity Level" = 'Critical' THEN 1 END) as critical_attacks
FROM cybersecurity_threats
GROUP BY Year
ORDER BY Year;

-- Query 2: Year-over-Year Growth Analysis
WITH yearly_stats AS (
    SELECT 
        Year,
        COUNT(*) as attack_count,
        ROUND(SUM("Financial Impact ($M)"), 2) as total_impact,
        ROUND(SUM("Data Breached (GB)"), 2) as total_data_breached
    FROM cybersecurity_threats
    GROUP BY Year
)
SELECT 
    Year,
    attack_count,
    total_impact,
    total_data_breached,
    LAG(attack_count) OVER (ORDER BY Year) as prev_year_attacks,
    ROUND((attack_count - LAG(attack_count) OVER (ORDER BY Year)) * 100.0 / 
          LAG(attack_count) OVER (ORDER BY Year), 2) as attack_growth_rate,
    ROUND((total_impact - LAG(total_impact) OVER (ORDER BY Year)) * 100.0 / 
          LAG(total_impact) OVER (ORDER BY Year), 2) as impact_growth_rate
FROM yearly_stats
ORDER BY Year;

-- Query 3: Threat Type Evolution by Year
SELECT 
    Year,
    "Threat Type",
    COUNT(*) as attack_count,
    ROUND(AVG("Financial Impact ($M)"), 2) as avg_impact,
    ROUND(COUNT(*) * 100.0 / 
          SUM(COUNT(*)) OVER (PARTITION BY Year), 2) as year_percentage
FROM cybersecurity_threats
GROUP BY Year, "Threat Type"
ORDER BY Year, attack_count DESC;

-- Query 4: Seasonal Analysis (by quarters)
SELECT 
    Year,
    CASE 
        WHEN CAST(substr(Year, -2) AS INTEGER) % 4 = 1 THEN 'Q1'
        WHEN CAST(substr(Year, -2) AS INTEGER) % 4 = 2 THEN 'Q2'
        WHEN CAST(substr(Year, -2) AS INTEGER) % 4 = 3 THEN 'Q3'
        ELSE 'Q4'
    END as Quarter,
    COUNT(*) as attack_count,
    ROUND(AVG("Financial Impact ($M)"), 2) as avg_financial_impact
FROM cybersecurity_threats
GROUP BY Year, Quarter
ORDER BY Year, Quarter;

-- Query 5: Industry Trends Over Time
SELECT 
    Year,
    "Affected Industry",
    COUNT(*) as attack_count,
    ROUND(AVG("Financial Impact ($M)"), 2) as avg_impact,
    RANK() OVER (PARTITION BY Year ORDER BY COUNT(*) DESC) as industry_rank
FROM cybersecurity_threats
GROUP BY Year, "Affected Industry"
ORDER BY Year, attack_count DESC;