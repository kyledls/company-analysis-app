import streamlit
import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('FMP_API_KEY')

streamlit.set_page_config(
    page_title="Company Analysis App",
    page_icon="📊"
)

streamlit.title("Company Analysis App")

ticker = streamlit.text_input("Enter a stock ticker (e.g., AAPL):").upper() 
test_url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?apikey={api_key}" 

if ticker: 
    response = requests.get(test_url) 
    
    if response.ok and response.json(): 
        streamlit.session_state.ticker = ticker 
        streamlit.success(f"Ticker {ticker} selected! Navigate to Income Statement page to view the analysis.") 
    else:
        streamlit.error(f"Invalid ticker: {ticker}. Please enter a valid stock ticker.") 
        streamlit.session_state.ticker = '' 





