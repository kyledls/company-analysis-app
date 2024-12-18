import streamlit 
import requests 
import pandas 
import io 
from dotenv import load_dotenv 
import os 

load_dotenv() 
api_key = os.getenv('FMP_API_KEY') 
ticker = streamlit.session_state.get('ticker', '') 
balance_sheet_statement_url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?apikey={api_key}" 

balance_sheet_statement_api_response = requests.get(balance_sheet_statement_url) 
balance_sheet_statement_data = balance_sheet_statement_api_response.json() 

if not ticker: 
    streamlit.warning("Please enter a ticker on the home page first.") 
else:
    streamlit.title(f"Balance Sheet Statement for {ticker}") 
    balance_sheet_mapping = { 
    "Cash & Short-term Investments": ["cashAndCashEquivalents", "shortTermInvestments"],
    "Accounts Receivable": "netReceivables",
    "Inventory": "inventory",
    "Other Current Assets": "otherCurrentAssets",
    "Total Current Assets": "totalCurrentAssets",
    "Property, Plant & Equipment": "propertyPlantEquipmentNet",
    "Goodwill": "goodwill",
    "Intangible Assets": "intangibleAssets",
    "Other Non-Current Assets": "otherNonCurrentAssets",
    "Total Non-Current Assets": "totalNonCurrentAssets",
    "Total Assets": "totalAssets",
    "Accounts Payable": "accountPayables",
    "Short-term Debt": "shortTermDebt",
    "Deferred Revenue": "deferredRevenue",
    "Other Current Liabilities": "otherCurrentLiabilities",
    "Total Current Liabilities": "totalCurrentLiabilities",
    "Long-term Debt": "longTermDebt",
    "Deferred Revenue (Non-Current)": "deferredRevenueNonCurrent",
    "Deferred Tax Liabilities": "deferredTaxLiabilitiesNonCurrent",
    "Other Non-Current Liabilities": "otherNonCurrentLiabilities",
    "Total Non-Current Liabilities": "totalNonCurrentLiabilities",
    "Total Liabilities": "totalLiabilities",
    "Common Stock": "commonStock",
    "Retained Earnings": "retainedEarnings",
    "Other Comprehensive Income": "accumulatedOtherComprehensiveIncomeLoss",
    "Total Stockholders Equity": "totalStockholdersEquity",
    "Total Liabilities & Equity": "totalLiabilitiesAndStockholdersEquity"
}

    balance_sheet_statement_values = {} 
 
    for year_data in balance_sheet_statement_data:
        year = year_data['date']
        
        year_values = {}

        for item_name, api_field in balance_sheet_mapping.items():
            if isinstance(api_field, list):
                value = sum(year_data.get(field, 0) for field in api_field)
            else:
                value = year_data.get(api_field, 0)
            
            year_values[item_name] = value
        
        balance_sheet_statement_values[year] = year_values

    balance_sheet_statement_dataframe = pandas.DataFrame(balance_sheet_statement_values)
    balance_sheet_statement_dataframe = balance_sheet_statement_dataframe.rename_axis('Line Items')
    streamlit.dataframe(
        balance_sheet_statement_dataframe,
        width=1000,
        height=600,
        use_container_width=True
    )

    def format_numbers(number):
        return '{:,.0f}'.format(number)
    balance_sheet_statement_dataframe = balance_sheet_statement_dataframe.applymap(format_numbers)

    excel_output_file = io.BytesIO()
    balance_sheet_statement_dataframe.to_excel(
        excel_output_file,                          
        sheet_name='Balance Sheet Statement',  
        engine='xlsxwriter'            
    )
    
    streamlit.download_button(
        label="Download Balance Sheet Statement as Excel", 
        data=excel_output_file.getvalue(),                     
        file_name=f'{ticker}_balance_sheet_statement.xlsx',          
    )
    
    












