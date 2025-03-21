# Zocket Content Analyzer

An AI-powered tool to analyze marketing content and provide actionable insights for Zocket's marketing teams.

## Features

### Web Content Analysis
- Extracts key information from URLs
- Identifies marketing-specific keywords (e.g., ROAS, CTR, conversion)

### Sentiment Analysis
- Determines if content is Positive, Negative, or Neutral
- Provides a confidence score for sentiment

### Call-to-Action (CTA) Detection
- Detects actionable CTAs like "Buy Now", "Sign Up", etc.

### Competitor Tracking
- Flags mentions of competitors like HubSpot, Hootsuite, etc.

### Ad Potential Score
- Quantifies content's potential for ad campaigns (0-100%)

### Actionable Recommendations
- Suggests next steps like boosting ad spend or A/B testing

## Tech Stack

- **Web Scraping**: BeautifulSoup, requests
- **Text Processing**: sumy, nltk
- **UI Framework**: Streamlit
- **Visualization**: Plotly

## How to Run

### 1. Install Dependencies
```bash
pip install streamlit requests beautifulsoup4 sumy nltk plotly
```

### 2. Run the App
```bash
streamlit run zocket_agent.py
```

### 3. Use the App
1. Enter a URL (e.g., https://zocket.com)
2. Click Analyze
3. View results:
   - Key Insights (Sentiment, Ad Potential, Keywords)
   - Content Metrics (Word Count, Positive/Negative Signals)
   - Recommendations (e.g., "Boost ad spend")

## Screenshots

![image](https://github.com/user-attachments/assets/46ec3f53-3093-4415-8712-cc4bd3dbf44c)

![image](https://github.com/user-attachments/assets/f4caf1e5-3ad5-42ca-8574-4aeac5f7d558)
