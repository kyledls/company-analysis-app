import streamlit
import requests
import pandas 
import plotly.graph_objects as plotly
from dotenv import load_dotenv
import os

load_dotenv() 
api_key = os.getenv('FMP_API_KEY') 
ticker = streamlit.session_state.get('ticker', '') 
income_statement_url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?apikey={api_key}&limit=3" 

if not ticker: 
    streamlit.warning("Please enter a ticker on the home page first.") 
else:
    streamlit.title(f"Projection Analysis for {ticker}") 
    income_statement_api_response = requests.get(income_statement_url) 
    income_statement_data = income_statement_api_response.json() 

    streamlit.subheader("5 Year Projections") 
    streamlit.write("Adjust the assumptions using the text boxes below:") 
    
    latest_year = income_statement_data[0] 
    latest_revenue = latest_year["revenue"] 
    latest_gross_profit = latest_year["grossProfit"] 
    latest_rd_expenses = latest_year["researchAndDevelopmentExpenses"] 
    latest_sga_expenses = latest_year.get("sellingGeneralAndAdministrativeExpenses", 0) 
    latest_tax_expenses = latest_year.get("incomeTaxExpenses", 0) 

    gross_margin = (latest_gross_profit / latest_revenue) * 100 
    rd_ratio = (abs(latest_rd_expenses) / latest_revenue) * 100 if latest_rd_expenses else 0 
    sga_ratio = (abs(latest_sga_expenses) / latest_revenue) * 100 if latest_sga_expenses else 0 
    tax_rate = (abs(latest_tax_expenses) / latest_year['incomeBeforeTax']) * 100 if latest_year['incomeBeforeTax'] != 0 else 0

    col1, col2 = streamlit.columns(2) 

    with col1: 
        revenue_growth_input = streamlit.number_input( 
            "Revenue Growth (%)", 
            min_value=0.0, 
            max_value=100.0, 
            step=0.1, 
            help="Annual revenue growth rate" 
        )
                
        gross_margin_input = streamlit.number_input( 
            "Gross Profit Margin (%)", 
            min_value=0.0, 
            max_value=100.0, 
            value=gross_margin, 
            step=0.1 
        )

    with col2:
        rd_percent_of_sales_input = streamlit.number_input( 
            "R&D % of Sales", 
            min_value=0.0, 
            max_value=100.0, 
            value=rd_ratio, 
            step=0.1 
        )
            
        sga_percent_of_sales_input = streamlit.number_input( 
            "SG&A % of Sales", 
            min_value=0.0, 
            max_value=100.0, 
            value=sga_ratio, 
            step=0.1 
        )

    tax_rate_input = streamlit.number_input( 
        "Tax Rate (%)", 
        min_value=0.0, 
        max_value=100.0, 
        value=tax_rate, 
        step=0.1 
    )

    number_of_years = 5
    start_year = int(latest_year['date'][:4])  
    future_years = []
    
    for i in range(1, number_of_years + 1):
        future_year = str(start_year + i)
        future_years.append(future_year)

    projections = []

    for year_index in range(number_of_years):
        if year_index == 0:
            revenue = latest_revenue * (1 + revenue_growth_input/100)
        else:
            previous_year_revenue = projections[year_index-1]['Revenue']
            revenue = previous_year_revenue * (1 + revenue_growth_input/100)
        
        revenue = round(revenue)
        
        gross_profit = round(revenue * (gross_margin_input/100))
        rd_expense = round(revenue * (rd_percent_of_sales_input/100))
        sga_expense = round(revenue * (sga_percent_of_sales_input/100))
        
        operating_income = gross_profit - rd_expense - sga_expense
        
        tax_expense = round(operating_income * (tax_rate_input/100))
        net_income = operating_income - tax_expense
        
        yearly_projection = {
            'Year': future_years[year_index],
            'Revenue': revenue,
            'Gross Profit': gross_profit,
            'R&D': -rd_expense,  
            'SG&A': -sga_expense, 
            'Operating Income': operating_income,
            'Taxes': -tax_expense,  
            'Net Income': net_income
        }
        
        projections.append(yearly_projection)

    projections_dataframe = pandas.DataFrame(projections)
    projections_dataframe = projections_dataframe.set_index('Year')
    streamlit.dataframe(projections_dataframe)

    projection_bar_chart = plotly.Figure()
    bar_chart_revenue_values = [p['Revenue'] for p in projections]
    projection_bar_chart.add_trace(plotly.Bar(
        x=future_years,
        y=bar_chart_revenue_values,
        name='Revenue'
    ))
    bar_chart_net_income_values = [p['Net Income'] for p in projections]
    projection_bar_chart.add_trace(plotly.Bar(
        x=future_years,
        y=bar_chart_net_income_values,
        name='Net Income'
    ))

    projection_bar_chart.update_layout(
        title='Projected Revenue and Net Income',
        barmode='group',
        xaxis_title='Year',
        yaxis_title='Amount ($)'
    )

    streamlit.plotly_chart(projection_bar_chart, use_container_width=True)
    












