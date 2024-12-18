import streamlit 
import requests 
import pandas 
import io 
from dotenv import load_dotenv 
import os 

load_dotenv()
api_key = os.getenv('FMP_API_KEY') 
ticker = streamlit.session_state.get('ticker', '') 
income_statement_url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?apikey={api_key}" 

income_statement_api_response = requests.get(income_statement_url) 
income_statement_data = income_statement_api_response.json() 

if not ticker: 
    streamlit.warning("Please enter a ticker on the home page first.") 
else: 
    streamlit.title(f"Income Statement for {ticker}") 
    income_statement_mapping = { 
        "Revenue": "revenue",
        "Cost of sales": "-costOfRevenue",
        "Gross Profit": "grossProfit",
        "Research & development": "-researchAndDevelopmentExpenses",
        "Selling, general & administrative": "-sellingGeneralAndAdministrativeExpenses",
        "Operating expenses": "operatingExpenses",
        "Cost and expenses": "costAndExpenses",
        "Operating profit (EBIT)": "operatingIncome",
        "Interest income": "interestIncome",
        "Interest expense": "-interestExpense",
        "Depreciation & amortization": "depreciationAndAmortization",
        "EBITDA": "ebitda",
        "Other income/expenses net": "totalOtherIncomeExpensesNet",
        "Pretax profit": "incomeBeforeTax",
        "Taxes": "-incomeTaxExpense",
        "Net income": "netIncome"
    }

    income_statement_values = {} 
 
    for year_data in income_statement_data: 
        year = year_data['date'] 
        
        year_values = {} 

        for item_name, api_field in income_statement_mapping.items():
            if api_field.startswith('-'): 
                actual_field = api_field[1:] 
                value = -year_data.get(actual_field, 0) 
            else:
                value = year_data.get(api_field, 0)
            
            year_values[item_name] = value
        
        income_statement_values[year] = year_values

    income_statement_dataframe = pandas.DataFrame(income_statement_values) 
    income_statement_dataframe = income_statement_dataframe.rename_axis('Line Items') 
    streamlit.dataframe(
        income_statement_dataframe,
        width=1000, 
        height=600, 
        use_container_width=True 
    )
    
    def format_numbers(number): 
        return '{:,.0f}'.format(number)
    income_statement_dataframe = income_statement_dataframe.applymap(format_numbers) 

    excel_output_file = io.BytesIO() 
    income_statement_dataframe.to_excel(
        excel_output_file,                          
        sheet_name='Income Statement', 
        engine='xlsxwriter'             
    )
    
    streamlit.download_button( 
        label="Download Income Statement as Excel", 
        data=excel_output_file.getvalue(),                   
        file_name=f'{ticker}_income_statement.xlsx', 
    )











