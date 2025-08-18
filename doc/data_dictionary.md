# 📖 Data Dictionary

## Dataset Overview
**Dataset Name**: Global Cybersecurity Threats (2015-2024)  
**Source**: Kaggle Dataset  
**Total Records**: ~50,000+ incidents  
**Time Period**: 2015-2024  
**Update Frequency**: Annual  

## 📊 Column Specifications

| Column Name | Data Type | Description | Example Values | Constraints |
|-------------|-----------|-------------|----------------|-------------|
| **Country** | String | Country where the cyberattack occurred | USA, UK, Germany, China | Non-null, ISO country codes preferred |
| **Year** | Integer | Year when the incident took place | 2015, 2016, ..., 2024 | Range: 2015-2024 |
| **Threat Type** | String | Classification of the cybersecurity threat | Malware, Phishing, DDoS, Ransomware | Predefined categories |
| **Attack Vector** | String | Method or pathway used to conduct the attack | Email, Web, Network, USB, Social Engineering | Non-null |
| **Affected Industry** | String | Industry sector that was targeted | Finance, Healthcare, Education, Retail | Standard industry classifications |
| **Data Breached (GB)** | Float | Volume of data compromised in gigabytes | 0.5, 100.25, 1500.0 | Non-negative, can be 0 |
| **Financial Impact ($M)** | Float | Estimated financial loss in millions USD | 1.5, 25.7, 100.0 | Non-negative, can be 0 |
| **Severity Level** | String | Assessment of incident severity | Low, Medium, High, Critical | Ordered categorical |
| **Response Time (Hours)** | Float | Time taken to detect and mitigate the attack | 2.5, 24.0, 168.0 | Positive values only |
| **Mitigation Strategy** | String | Primary countermeasure implemented | Patching, Training, Isolation, Blocking | Multiple strategies possible |

## 🏷️ Categorical Value Definitions

### Threat Types
- **Malware**: Malicious software including viruses, trojans, spyware
- **Phishing**: Deceptive emails or websites to steal credentials
- **DDoS**: Distributed Denial of Service attacks
- **Ransomware**: Encryption-based extortion attacks
- **SQL Injection**: Database manipulation attacks
- **Man-in-the-Middle**: Interception of communications
- **Zero-Day**: Exploitation of unknown vulnerabilities
- **Insider Threat**: Attacks from within the organization

### Attack Vectors
- **Email**: Email-based attacks (phishing, malware attachments)
- **Web**: Web application vulnerabilities and browser exploits
- **Network**: Network-level attacks and intrusions
- **USB**: Removable media-based malware delivery
- **Social Engineering**: Human manipulation techniques
- **Mobile**: Mobile device and application attacks
- **Cloud**: Cloud service and infrastructure attacks
- **IoT**: Internet of Things device compromises

### Industries
- **Finance**: Banking, insurance, investment services
- **Healthcare**: Hospitals, clinics, pharmaceutical companies
- **Education**: Schools, universities, educational institutions
- **Retail**: E-commerce, brick-and-mortar stores
- **Government**: Public sector and government agencies
- **Technology**: Software, hardware, IT services companies
- **Manufacturing**: Industrial and production companies
- **Energy**: Utilities, oil & gas, renewable energy
- **Transportation**: Airlines, shipping, logistics
- **Telecommunications**: Telecom operators and services

### Severity Levels
- **Low**: Minimal impact, easily contained, low recovery cost
- **Medium**: Moderate impact, some business disruption, manageable cost
- **High**: Significant impact, major business disruption, substantial cost
- **Critical**: Severe impact, business-critical systems affected, major financial loss

### Mitigation Strategies
- **Patching**: Software updates and security patches
- **Training**: Employee cybersecurity awareness programs
- **Isolation**: Network segmentation and system quarantine
- **Blocking**: Firewall rules and access restrictions
- **Backup Restoration**: Data recovery from backups
- **Incident Response**: Formal incident management procedures
- **Forensic Analysis**: Digital evidence collection and analysis
- **Legal Action**: Law enforcement involvement and prosecution

## 📐 Data Quality Metrics

### Completeness
- **Country**: 100% (Required field)
- **Year**: 100% (Required field)
- **Threat Type**: 100% (Required field)
- **Attack Vector**: 98.5% (Some missing values)
- **Affected Industry**: 99.2% (Rare missing values)
- **Data Breached (GB)**: 95.8% (Some incidents with unknown data loss)
- **Financial Impact ($M)**: 92.3% (Difficult to quantify in some cases)
- **Severity Level**: 100% (Required assessment)
- **Response Time (Hours)**: 97.1% (Some ongoing incidents)
- **Mitigation Strategy**: 94.7% (Some incidents without clear mitigation)

### Accuracy Indicators
- **Geographic Validation**: Country names validated against ISO 3166
- **Temporal Consistency**: Dates within expected ranges
- **Financial Validation**: Impact amounts cross-referenced with public reports
- **Industry Classification**: Mapped to standard NAICS codes where possible

### Data Sources
- **Primary Sources**: 
  - Government cybersecurity agencies (CISA, NCSC, etc.)
  - Industry security reports (Verizon DBIR, IBM X-Force, etc.)
  - Company breach notifications and SEC filings
  
- **Secondary Sources**:
  - Cybersecurity research organizations
  - Academic institutions
  - News outlets and journalism investigations

## 🔍 Known Limitations

### Data Collection Bias
- **Reporting Bias**: Not all incidents are publicly reported
- **Geographic Bias**: Higher reporting rates in developed countries
- **Industry Bias**: Financial and healthcare sectors have mandatory reporting
- **Severity Bias**: Major incidents more likely to be documented

### Temporal Considerations
- **Lag Time**: Some incidents reported months after occurrence
- **Evolving Definitions**: Threat categories have changed over time
- **Attribution Challenges**: Difficulty in determining actual attack origin

### Measurement Challenges
- **Financial Impact**: Difficult to quantify all costs (reputation, opportunity cost)
- **Data Quantification**: Not all breached data can be measured in GB
- **Response Time**: Varies based on detection vs. full remediation

## 🔧 Preprocessing Notes

### Data Cleaning Applied
- **Standardization**: Country names normalized to consistent format
- **Outlier Treatment**: Financial impacts >$1B flagged for review
- **Missing Value Handling**: 
  - Categorical: "Unknown" category
  - Numerical: Median imputation for non-critical fields
- **Duplicate Detection**: Cross-field matching for incident deduplication

### Feature Engineering Opportunities
- **Temporal Features**: Quarter, month, day-of-year extraction
- **Geographic Features**: Region, continent, GDP correlation
- **Industry Features**: Sector size, digitization level
- **Derived Metrics**: Impact per GB, response efficiency ratios

This data dictionary serves as the foundation for all analysis and should be referenced when interpreting results or extending the analysis framework.