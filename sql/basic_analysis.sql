-- Basic Analysis Queries for Cybersecurity Threats Dataset

-- Query 1: Dataset Overview
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT Country) as unique_countries,
    COUNT(DISTINCT Year) as unique_years,
    COUNT(DISTINCT "Threat Type") as unique_threat_types,
    MIN(Year) as earliest_year,
    MAX(Year) as latest_year
FROM cybersecurity_threats;

-- Query 2: Threat Type Distribution
SELECT 
    "Threat Type",
    COUNT(*) as threat_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM cybersecurity_threats), 2) as percentage,
    ROUND(AVG("Financial Impact ($M)"), 2) as avg_financial_impact
FROM cybersecurity_threats
GROUP BY "Threat Type"
ORDER BY threat_count DESC;

-- Query 3: Top 15 Countries by Attack Count
SELECT 
    Country,
    COUNT(*) as attack_count,
    ROUND(AVG("Financial Impact ($M)"), 2) as avg_financial_impact,
    ROUND(AVG("Data Breached (GB)"), 2) as avg_data_breached,
    ROUND(AVG("Response Time (Hours)"), 2) as avg_response_time
FROM cybersecurity_threats
GROUP BY Country
ORDER BY attack_count DESC
LIMIT 15;

-- Query 4: Attack Vector Analysis
SELECT 
    "Attack Vector",
    COUNT(*) as frequency,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM cybersecurity_threats), 2) as percentage,
    ROUND(AVG("Financial Impact ($M)"), 2) as avg_financial_impact,
    ROUND(AVG("Data Breached (GB)"), 2) as avg_data_breached
FROM cybersecurity_threats
GROUP BY "Attack Vector"
ORDER BY frequency DESC;

-- Query 5: Industry Analysis
SELECT 
    "Affected Industry",
    COUNT(*) as attack_count,
    ROUND(AVG("Financial Impact ($M)"), 2) as avg_financial_impact,
    ROUND(AVG("Data Breached (GB)"), 2) as avg_data_breached,
    ROUND(AVG("Response Time (Hours)"), 2) as avg_response_time,
    SUM(CASE WHEN "Severity Level" = 'Critical' THEN 1 ELSE 0 END) as critical_attacks
FROM cybersecurity_threats
GROUP BY "Affected Industry"
ORDER BY attack_count DESC;

-- Query 6: Severity Level Analysis
SELECT 
    "Severity Level",
    COUNT(*) as attack_count,
    ROUND(AVG("Financial Impact ($M)"), 2) as avg_financial_impact,
    ROUND(AVG("Data Breached (GB)"), 2) as avg_data_breached,
    ROUND(AVG("Response Time (Hours)"), 2) as avg_response_time,
    ROUND(MIN("Response Time (Hours)"), 2) as min_response_time,
    ROUND(MAX("Response Time (Hours)"), 2) as max_response_time
FROM cybersecurity_threats
GROUP BY "Severity Level"
ORDER BY 
    CASE "Severity Level"
        WHEN 'Critical' THEN 1
        WHEN 'High' THEN 2
        WHEN 'Medium' THEN 3
        WHEN 'Low' THEN 4
    END;