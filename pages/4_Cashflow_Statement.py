import streamlit
import requests
import pandas
import io
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('FMP_API_KEY')
ticker = streamlit.session_state.get('ticker', '') 
cashflow_statement_url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?apikey={api_key}&limit=3" 

cashflow_statement_api_response = requests.get(cashflow_statement_url) 
cashflow_statement_data = cashflow_statement_api_response.json()

if not ticker: 
    streamlit.warning("Please enter a ticker on the home page first.") 
else:
    streamlit.title(f"Cashflow Statement for {ticker}") 
    cashflow_statement_mapping = {
        "Net Income": "netIncome",
        "Depreciation & Amortization": "depreciationAndAmortization",
        "Stock-based Compensation": "stockBasedCompensation",
        "Changes in Working Capital": [
            "-accountsReceivables",  
            "-inventory",            
            "-otherWorkingCapital", 
            "accountsPayables"       
        ],
        "Other Operating Activities": "otherNonCashItems",
        "Net Cash from Operations": "netCashProvidedByOperatingActivities",
        "Capital Expenditures": "-capitalExpenditure",  
        "Net Cash from Investing": "netCashUsedForInvestingActivites",
        "Debt Repayment": "-debtRepayment",
        "Share Repurchases": "-commonStockRepurchased",
        "Dividends Paid": "-dividendsPaid",
        "Net Cash from Financing": "netCashUsedProvidedByFinancingActivities",
        "Net Change in Cash": "netChangeInCash"
    }

    cashflow_statement_values = {}
 
    for year_data in cashflow_statement_data:
        year = year_data['date']
        
        year_values = {}

        for item_name, api_field in cashflow_statement_mapping.items():
            if isinstance(api_field, list):
                value = 0
                for field in api_field:
                    if field.startswith('-'):
                        actual_field = field[1:]
                        value -= year_data.get(actual_field, 0)
                    else:
                        value += year_data.get(field, 0)
            else:
                if api_field.startswith('-'):
                    actual_field = api_field[1:]
                    value = -year_data.get(actual_field, 0)
                else:
                    value = year_data.get(api_field, 0)
            
            year_values[item_name] = value
        
        cashflow_statement_values[year] = year_values

    cashflow_statement_dataframe = pandas.DataFrame(cashflow_statement_values)
    cashflow_statement_dataframe = cashflow_statement_dataframe.rename_axis('Line Items')
    streamlit.dataframe(
        cashflow_statement_dataframe,
        width=1000,
        height=600,
        use_container_width=True
    )

    excel_output_file = io.BytesIO()
    cashflow_statement_dataframe.to_excel(
        excel_output_file,                          
        sheet_name='Cashflow Statement',  
        engine='xlsxwriter'            
    )
    
    streamlit.download_button(
        label="Download Cashflow Statement as Excel", 
        data=excel_output_file.getvalue(),                     
        file_name=f'{ticker}_cashflow_statement.xlsx',           
    )












