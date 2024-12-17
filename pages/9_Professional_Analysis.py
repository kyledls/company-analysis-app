import streamlit
import yfinance
import pandas
import finnhub
import plotly.graph_objects as plotly
from dotenv import load_dotenv
import os

load_dotenv()
finnhub_client = finnhub.Client(api_key=os.getenv('FINNHUB_API_KEY'))

ticker = streamlit.session_state.get('ticker', '')

if not ticker:
    streamlit.warning("Please enter a ticker on the home page first.")
else:
    streamlit.title(f"Professional Analysis for {ticker}")
    
    streamlit.header("Price Target Analysis")
    ticker_data = yfinance.Ticker(ticker).info
    col1, col2, col3, col4 = streamlit.columns(4)
    
    current_price = ticker_data.get('currentPrice')
    target_mean = ticker_data.get('targetMeanPrice')
    target_high = ticker_data.get('targetHighPrice')
    target_low = ticker_data.get('targetLowPrice')
    
    current_price = f"${current_price:.2f}" 
    target_mean = f"${target_mean:.2f}" 
    target_high = f"${target_high:.2f}" 
    target_low = f"${target_low:.2f}" 
    
    col1.metric("Current Price", current_price)
    col2.metric("Target Mean", target_mean)
    col3.metric("Target High", target_high)
    col4.metric("Target Low", target_low)
    
    streamlit.header("Analyst Recommendation Trends")
    analyst_recommendations = finnhub_client.recommendation_trends(ticker)
    
    if analyst_recommendations:
        analyst_recommendations_dataframe = pandas.DataFrame(analyst_recommendations)
        analyst_recommendations_dataframe = analyst_recommendations_dataframe[['period', 'strongBuy', 'buy', 'hold', 'sell', 'strongSell']]
        
        analyst_recommendation_chart = plotly.Figure()
        
        analyst_recommendation_chart.add_trace(plotly.Bar(
            x=analyst_recommendations_dataframe.period,
            y=analyst_recommendations_dataframe.strongSell,
            name='Strong Sell',
            marker_color='#8B0000' 
        ))
        analyst_recommendation_chart.add_trace(plotly.Bar(
            x=analyst_recommendations_dataframe.period,
            y=analyst_recommendations_dataframe.sell,
            name='Sell',
            marker_color='#FF4444'  
        ))
        analyst_recommendation_chart.add_trace(plotly.Bar(
            x=analyst_recommendations_dataframe.period,
            y=analyst_recommendations_dataframe.hold,
            name='Hold',
            marker_color='#FFD700'  
        ))
        analyst_recommendation_chart.add_trace(plotly.Bar(
            x=analyst_recommendations_dataframe.period,
            y=analyst_recommendations_dataframe.buy,
            name='Buy',
            marker_color='#90EE90'  
        ))
        analyst_recommendation_chart.add_trace(plotly.Bar(
            x=analyst_recommendations_dataframe.period,
            y=analyst_recommendations_dataframe.strongBuy,
            name='Strong Buy',
            marker_color='#006400'  
        ))
        
        analyst_recommendation_chart.update_layout(
            barmode='stack',
            height=400,
            title_text='Analyst Recommendations',
            showlegend=True,
            xaxis_title='Period',
            yaxis_title='Number of Analysts'
        )
        
        streamlit.plotly_chart(analyst_recommendation_chart, use_container_width=True)
    else:
        streamlit.info("No recommendation trends available for this ticker.")
