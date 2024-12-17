import streamlit
import requests
import pandas
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('FMP_API_KEY')
ticker = streamlit.session_state.get('ticker', '')

company_profile_url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={api_key}"
company_multiples_url = f"https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker}?apikey={api_key}"

company_info = requests.get(company_profile_url).json()

if not ticker:
    streamlit.warning("Please enter a ticker on the home page first.")
else:
    streamlit.title(f"Competitor Analysis for {ticker}")
    
    if not company_info:
        streamlit.error(f"No company information available for {ticker}")
    else:
        company_info = company_info[0]
        streamlit.write(f"Sector: {company_info['sector']}")
        streamlit.write(f"Industry: {company_info['industry']}")

        competitors_url = f"https://financialmodelingprep.com/api/v3/stock-screener?sector={company_info['sector']}&industry={company_info['industry']}&apikey={api_key}"
        competitors_data = requests.get(competitors_url).json()
        
        if not competitors_data:
            streamlit.warning(f"No competitors found in the {company_info['industry']} industry")
        else:
            competitors_dataframe = pandas.DataFrame(competitors_data)
            competitors_dataframe = competitors_dataframe[['symbol', 'companyName']].head(5)
            
            company_multiples = []

            main_company_url = f"https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker}?apikey={api_key}"
            main_company_response = requests.get(main_company_url).json()
            
            if main_company_response:
                main_company_ratios = main_company_response[0]
                
                company_multiples.append({
                    'Company': ticker,
                    'EV/EBITDA': main_company_ratios.get('enterpriseValueMultipleTTM', None),
                    'P/E Ratio': main_company_ratios.get('peRatioTTM', None),
                    'P/B Ratio': main_company_ratios.get('priceToBookRatioTTM', None)
                })
            else:
                streamlit.error(f"No financial ratios available for {ticker}")
                streamlit.stop()

            for competitor_symbol in competitors_dataframe['symbol']:
                if competitor_symbol != ticker:
                    competitor_url = f"https://financialmodelingprep.com/api/v3/ratios-ttm/{competitor_symbol}?apikey={api_key}"
                    competitor_response = requests.get(competitor_url).json()
                    
                    if competitor_response and isinstance(competitor_response, list) and len(competitor_response) > 0:
                        competitor_ratios = competitor_response[0]
                        
                        company_multiples.append({
                            'Company': competitor_symbol,
                            'EV/EBITDA': competitor_ratios.get('enterpriseValueMultipleTTM', None),
                            'P/E Ratio': competitor_ratios.get('peRatioTTM', None),
                            'P/B Ratio': competitor_ratios.get('priceToBookRatioTTM', None)
                        })
                    else:
                        continue  
            
            multiples_dataframe = pandas.DataFrame(company_multiples).set_index('Company').round(2)
            streamlit.subheader("Competitor Comparison")
            streamlit.dataframe(multiples_dataframe)

            competitors_only = multiples_dataframe.loc[multiples_dataframe.index != ticker]
            industry_averages = competitors_only.mean()
            
            comparison_table = pandas.DataFrame({
                'Company Value': multiples_dataframe.loc[ticker],
                'Industry Average': industry_averages,
                'Difference %': ((multiples_dataframe.loc[ticker] - industry_averages) / industry_averages * 100)
            })
            
            streamlit.subheader(f"{ticker} vs Industry Average")
            streamlit.dataframe(comparison_table)



    
