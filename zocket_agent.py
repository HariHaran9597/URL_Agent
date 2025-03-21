# zocket_agent.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
import plotly.express as px
import pandas as pd

# Download NLTK data
nltk.download('punkt')


# Custom CSS with Zocket-inspired colors
st.markdown("""
<style>
    .reportview-container { background: #f8f9fa }
    h1 { color: white }
    .stTextInput input { border: 2px solid #4a90e2; border-radius: 5px }
    .stButton button { 
        background-color: #4a90e2; 
        color: white; 
        border-radius: 5px; 
        font-weight: bold;
    }
    .stSuccess { background-color: #d4edda; color: #155724 }
    .stMetric { color: #2b3d4f }
    .stExpander { border: 1px solid #4a90e2; border-radius: 5px }
</style>
""", unsafe_allow_html=True)

# Core Functions
def get_web_content(url):
    """Retrieve and clean webpage content."""
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        for element in soup(['script', 'style', 'nav', 'footer']):
            element.decompose()
        return soup.get_text(separator=" ").strip()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def summarize_text(text):
    """Generate a concise summary."""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    return " ".join([str(sentence) for sentence in summarizer(parser.document, 5)])

def detect_ctas(text):
    """Detect marketing CTAs."""
    ctas = ["Buy Now", "Sign Up", "Learn More", "Get Started", "Subscribe"]
    return [cta for cta in ctas if cta in text]

def find_competitors(text):
    """Identify competitor mentions."""
    competitors = ["Hootsuite", "HubSpot", "Mailchimp", "Canva", "Google Ads"]
    return [comp for comp in competitors if comp.lower() in text.lower()]

def analyze_content(text):
    """Perform marketing-focused analysis."""
    keywords = ["ROAS", "CTR", "conversion", "campaign", "audience", 
               "targeting", "ad spend", "CPC", "impressions", "engagement"]
    found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
    
    positive_words = ["increase", "growth", "success", "improve", "boost"]
    negative_words = ["decline", "issue", "problem", "challenge", "drop"]
    
    pos_count = sum(text.lower().count(word) for word in positive_words)
    neg_count = sum(text.lower().count(word) for word in negative_words)
    
    return {
        "keywords": found_keywords,
        "sentiment": "Positive" if pos_count > neg_count else "Negative" if neg_count > pos_count else "Neutral",
        "word_count": len(text.split()),
        "key_metrics": {
            "Positive Signals": pos_count,
            "Negative Signals": neg_count
        },
        "ctas": detect_ctas(text),
        "competitors": find_competitors(text)
    }

def estimate_ad_potential(analysis):
    """Predict ad performance potential."""
    score = 0
    score += len(analysis["keywords"]) * 2
    score += analysis["key_metrics"]["Positive Signals"] * 3
    score -= analysis["key_metrics"]["Negative Signals"] * 2
    return min(max(score, 0), 100)

def generate_recommendations(analysis):
    """Generate actionable marketing recommendations."""
    recs = []
    if analysis["sentiment"] == "Positive":
        recs.append("✅ Boost ad spend on this content")
    if "CTR" in analysis["keywords"]:
        recs.append("✅ A/B test headlines for better CTR")
    if analysis["competitors"]:
        recs.append(f"🚨 Monitor competitors: {', '.join(analysis['competitors'])}")
    return recs

# Streamlit UI
st.title("Zocket Content Analyzer")
url = st.text_input("Enter Marketing Content URL:", "https://zocket.com")

if st.button("Analyze"):
    with st.spinner("Analyzing content..."):
        text = get_web_content(url)
        
        if text:
            analysis = analyze_content(text)
            
            # Display Results
            st.subheader("Analysis Results")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Key Insights")
                st.metric("Sentiment", analysis["sentiment"])
                st.metric("Ad Potential Score", f"{estimate_ad_potential(analysis)}%")
                st.write("**Detected Keywords:**", ", ".join(analysis["keywords"]))
                st.write("**Detected CTAs:**", ", ".join(analysis["ctas"]))
                
            with col2:
                st.markdown("### Content Metrics")
                st.metric("Total Words", analysis["word_count"])
                st.write("Positive Signals:", analysis["key_metrics"]["Positive Signals"])
                st.write("Negative Signals:", analysis["key_metrics"]["Negative Signals"])
            
            # Visualizations
            with st.expander("Advanced Marketing Insights"):
                st.plotly_chart(px.bar(
                    x=["Positive", "Negative"],
                    y=[analysis["key_metrics"]["Positive Signals"], 
                    analysis["key_metrics"]["Negative Signals"]],
                    title="Sentiment Analysis",
                    labels={"x": "Sentiment", "y": "Count"}
                ))
                
                st.write("**Competitor Mentions:**", ", ".join(analysis["competitors"]))
            
            # Recommendations
            st.subheader("Zocket Recommendations")
            for rec in generate_recommendations(analysis):
                st.success(rec)
            
            # Content Display
            st.subheader("Content Summary")
            st.write(summarize_text(text))
            
            st.subheader("Content Preview")
            st.text(text[:500] + "...")