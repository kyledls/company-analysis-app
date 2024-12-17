import streamlit
import requests
import pandas
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('FMP_API_KEY')
ticker = streamlit.session_state.get('ticker', '') 
discounted_cash_flow_url = f"https://financialmodelingprep.com/api/v3/discounted-cash-flow/{ticker}?apikey={api_key}"
discounted_cash_flow_response = requests.get(discounted_cash_flow_url)

if not ticker: 
    streamlit.warning("Please enter a ticker on the home page first.") 
else:
    streamlit.title(f"Sensitivity Analysis for {ticker}")
    
    discounted_cash_flow_data = discounted_cash_flow_response.json()
    
    if not discounted_cash_flow_data:
        streamlit.error(f"No DCF data available for {ticker}")
    else:
        base_dcf = discounted_cash_flow_data[0]['dcf']
        
        col1, col2 = streamlit.columns(2)
        with col1:
            base_wacc = streamlit.number_input(
                "Base WACC (%)",
                min_value=0.0,
                max_value=30.0,
                value=9.0,
                step=0.1,
                help="Weighted Average Cost of Capital"
            ) / 100

        with col2:
            base_growth = streamlit.number_input(
                "Base Terminal Growth (%)",
                min_value=-10.0,
                max_value=20.0,
                value=2.0,
                step=0.1,
                help="Long-term growth rate"
            ) / 100
        
        wacc_range = [
            base_wacc - 0.01,
            base_wacc - 0.005,
            base_wacc,
            base_wacc + 0.005,
            base_wacc + 0.01
        ]
        
        growth_range = [
            base_growth - 0.01,
            base_growth - 0.005,
            base_growth,
            base_growth + 0.005,
            base_growth + 0.01
        ]
        
        matrix_values = []
        
        for growth_rate in growth_range:
            single_row = []
            
            for discount_rate in wacc_range:
                gordon_growth_factor = (1 + growth_rate) / (discount_rate - growth_rate)
                base_factor = (base_wacc - base_growth) / (1 + base_growth)
                
                new_dcf_value = base_dcf * gordon_growth_factor * base_factor
                new_dcf_value = round(new_dcf_value, 2)
                
                single_row.append(new_dcf_value)
                
            matrix_values.append(single_row)
        
        sensitivity_table = pandas.DataFrame(
            data=matrix_values,
            columns=[f'WACC: {rate:.2%}' for rate in wacc_range],
            index=[f'Growth: {rate:.2%}' for rate in growth_range]
        )
        
        streamlit.subheader("DCF Sensitivity Analysis (WACC vs Terminal Growth)")
        streamlit.dataframe(sensitivity_table)
    
    
    












