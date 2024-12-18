import streamlit 
import requests 
import yfinance 
from datetime import datetime 
from dotenv import load_dotenv 
import os 

load_dotenv() 
api_key = os.getenv('FMP_API_KEY') 
ticker = streamlit.session_state.get('ticker', '') 
company_profile_url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={api_key}" 

company_profile_api_response = requests.get(company_profile_url)  
company_profile_data = company_profile_api_response.json() 

if not ticker: 
    streamlit.warning("Please enter a ticker on the home page first.") 
else:
    logo_url = f"https://financialmodelingprep.com/image-stock/{ticker}.png" 
    streamlit.image(logo_url, width=50) 
    streamlit.title(f"Company Profile for {ticker}") 
    most_recent_company_data = company_profile_data[0] 
    streamlit.title(f"{most_recent_company_data['companyName']} ({ticker})") 
    col1, col2 = streamlit.columns(2) 
    
    with col1: 
        streamlit.subheader("Company Information") 
        streamlit.write(f"**CEO:** {most_recent_company_data['ceo']}") 
        streamlit.write(f"**Exchange:** {most_recent_company_data['exchange']}") 
        streamlit.write(f"**Country:** {most_recent_company_data['country']}") 
        streamlit.write(f"**Website:** [{most_recent_company_data['website']}]({most_recent_company_data['website']})") 

    with col2: 
        streamlit.subheader("Financial Overview") 
        streamlit.write(f"**Current Price:** ${most_recent_company_data['price']:,.2f}") 
        streamlit.write(f"**Market Cap:** ${most_recent_company_data['mktCap']:,.2f}") 
        streamlit.write(f"**Volume Average:** {most_recent_company_data['volAvg']:,}") 
        streamlit.write(f"**Range:** {most_recent_company_data['range']}") 

    streamlit.subheader("Description") 
    streamlit.write(most_recent_company_data['description']) 

    current_year = datetime.now().year 
    start_year = current_year - 1 

    streamlit.subheader(f"{ticker} Price Chart ({start_year}-{current_year})") 
    stock_data = yfinance.download(ticker, start=f'{start_year}-01-01') 
    streamlit.line_chart(stock_data['Close'])
