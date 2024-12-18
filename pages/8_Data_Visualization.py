import streamlit
import plotly.graph_objects as plotly
import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('FMP_API_KEY')

ticker = streamlit.session_state.get('ticker', '')

income_statement_url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?apikey={api_key}"
balance_sheet_url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?apikey={api_key}"
cashflow_statement_url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?apikey={api_key}"

income_statement_response = requests.get(income_statement_url).json()
balance_sheet_response = requests.get(balance_sheet_url).json()
cashflow_statement_response = requests.get(cashflow_statement_url).json()

if not ticker:
    streamlit.warning("Please enter a ticker on the home page first.")
else:
    streamlit.title(f"Data Visualizations for {ticker}")
    streamlit.header("Financial Metrics Trends")
    
    dates = [item['date'] for item in income_statement_response]
    revenue = [item['revenue'] for item in income_statement_response]
    net_income = [item['netIncome'] for item in income_statement_response]
    operating_income = [item['operatingIncome'] for item in income_statement_response]
    
    financial_metrics_line_chart = plotly.Figure()
    financial_metrics_line_chart.add_trace(plotly.Scatter(
        x=dates, 
        y=revenue, 
        name="Revenue", 
        mode='lines+markers'
    ))
    financial_metrics_line_chart.add_trace(plotly.Scatter(
        x=dates, 
        y=net_income, 
        name="Net Income", 
        mode='lines+markers'
    ))
    financial_metrics_line_chart.add_trace(plotly.Scatter(
        x=dates, 
        y=operating_income, 
        name="Operating Income", 
        mode='lines+markers'
    ))
    
    financial_metrics_line_chart.update_layout(
        title="Key Financial Metrics Over Time",
        xaxis_title="Date",
        yaxis_title="Amount ($)",
        height=500
    )
    streamlit.plotly_chart(financial_metrics_line_chart, use_container_width=True)
    
    streamlit.header("Cashflow Components")
    operating_cashflow = [item['operatingCashFlow'] for item in cashflow_statement_response]
    investing_cashflow = [item['netCashUsedForInvestingActivites'] for item in cashflow_statement_response]
    financing_cashflow = [item['netCashUsedProvidedByFinancingActivities'] for item in cashflow_statement_response]
    
    cashflow_components_bar_chart = plotly.Figure()
    cashflow_components_bar_chart.add_trace(plotly.Bar(
        x=dates,
        y=operating_cashflow,
        name="Operating Cashflow",
        marker_color='#90EE90'  
    ))
    cashflow_components_bar_chart.add_trace(plotly.Bar(
        x=dates,
        y=investing_cashflow,
        name="Investing Cashflow",
        marker_color='#FFD700'  
    ))
    cashflow_components_bar_chart.add_trace(plotly.Bar(
        x=dates,
        y=financing_cashflow,
        name="Financing Cashflow",
        marker_color='#FF4444'  
    ))
    
    cashflow_components_bar_chart.update_layout(
        barmode='relative',
        title="Cashflow Components Over Time",
        xaxis_title="Date",
        yaxis_title="Amount ($)",
        height=500
    )
    streamlit.plotly_chart(cashflow_components_bar_chart, use_container_width=True)
    
    streamlit.header("Expenses Breakdown")
    latest_data = income_statement_response[0]
    expense_categories = [
        'Cost of Revenue',
        'R&D Expenses',
        'SG&A Expenses',
        'Interest Expense',
        'Other Expenses'
    ]
    
    expense_values = [
        latest_data.get('costOfRevenue', 0),
        latest_data.get('researchAndDevelopmentExpenses', 0),
        latest_data.get('sellingGeneralAndAdministrativeExpenses', 0),
        latest_data.get('interestExpense', 0),
        latest_data.get('otherExpenses', 0)
    ]
    
    expenses_donut_chart = plotly.Figure(data=[plotly.Pie(
        labels=expense_categories,
        values=expense_values,
        hole=.4,
        textinfo='label+percent'
    )])
    
    expenses_donut_chart.update_layout(
        title="Expense Distribution (Latest Period)",
        height=500
    )
    streamlit.plotly_chart(expenses_donut_chart, use_container_width=True)