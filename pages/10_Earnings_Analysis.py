import requests
import streamlit
import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as gemini

load_dotenv()  

ninja_api_key = os.getenv('NINJA_API_KEY') 
google_api_key = os.getenv('GOOGLE_API_KEY') 

transcript_url = f"https://api.api-ninjas.com/v1/earningstranscript"

ticker = streamlit.session_state.get('ticker', '')

def generate_summary(transcript):
    model = gemini.GenerativeModel('gemini-pro')
    prompt = f"""As a financial analyst, summarize the following earnings call transcript in 3-4 key points:
        {transcript}"""
    response = model.generate_content(prompt)
    return response.text

def analyze_sentiment(transcript):
    model = gemini.GenerativeModel('gemini-pro')
    prompt = f"""As a financial analyst, analyze the sentiment of this earnings call transcript and predict the likely stock direction. 
    Consider factors like:
    - Management's tone and confidence
    - Financial performance vs expectations
    - Forward guidance and outlook
    - Key challenges or opportunities mentioned
    
    Provide a clear directional view (bullish/bearish/neutral) with supporting points from the transcript:
    {transcript}"""
    response = model.generate_content(prompt)
    return response.text

if not ticker:
    streamlit.warning("Please enter a ticker on the home page first.")
else:
    streamlit.title("Earnings Call Transcript")
    streamlit.write(f"Analyzing earnings for: {ticker}")

    year = streamlit.number_input("Enter year:", min_value=2000, max_value=datetime.now().year, value=2024)
    quarter = streamlit.selectbox("Select quarter:", [1, 2, 3, 4])

    if 'transcript_data' not in streamlit.session_state:
        streamlit.session_state.transcript_data = None

    if streamlit.button("Get Transcript"):
        params = {
            'ticker': ticker,
            'year': year,
            'quarter': quarter
        }
        
        response = requests.get(transcript_url, params=params, headers={'X-Api-Key': ninja_api_key})
        streamlit.session_state.transcript_data = response.json()
    
    if streamlit.session_state.transcript_data and 'transcript' in streamlit.session_state.transcript_data:
        transcript = streamlit.session_state.transcript_data['transcript']
        if transcript:
            streamlit.text_area("Transcript:", transcript, height=300)
            
            streamlit.download_button(
                label="Download Transcript",
                data=transcript,
                file_name=f"{ticker}_Q{quarter}_{year}_transcript.txt",
            )
            
            with streamlit.spinner("Creating summary..."):
                summary = generate_summary(transcript)
                streamlit.text_area("Summary:", summary, height=500)
                
            with streamlit.spinner("Analyzing sentiment..."):
                sentiment = analyze_sentiment(transcript)
                streamlit.text_area("Sentiment Analysis:", sentiment, height=300)
        else:
            streamlit.error(f"No transcript available for {ticker} in Q{quarter} {year}")
    