import os
import requests
import pandas as pd
import json

os.makedirs('data/raw/structured', exist_ok=True)

def fetch_worldbank():
    try:
        wb_url = 'http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json&per_page=20000'
        wb_resp = requests.get(wb_url)
        wb_data = wb_resp.json()
        with open('data/raw/structured/worldbank_gdp.json', 'w', encoding='utf-8') as f:
            json.dump(wb_data, f)
        if len(wb_data) > 1:
            df = pd.DataFrame(wb_data[1])
            df.to_csv('data/raw/structured/worldbank_gdp.csv', index=False)
            print('Saved World Bank GDP data.')
    except Exception as e:
        print(f'World Bank API fetch failed: {e}')

def fetch_covid():
    try:
        covid_url = 'https://api.covid19api.com/summary'
        covid_resp = requests.get(covid_url)
        covid_data = covid_resp.json()
        with open('data/raw/structured/covid19_summary.json', 'w', encoding='utf-8') as f:
            json.dump(covid_data, f)
        if 'Countries' in covid_data:
            df = pd.DataFrame(covid_data['Countries'])
            df.to_csv('data/raw/structured/covid19_summary.csv', index=False)
            print('Saved COVID-19 summary data.')
    except Exception as e:
        print(f'COVID-19 API fetch failed: {e}')

def fetch_comtrade():
    try:
        comtrade_url = 'https://comtrade.un.org/api/get?max=500&type=C&freq=A&px=HS&ps=2022&r=all&p=0&rg=all&cc=01&fmt=json'
        comtrade_resp = requests.get(comtrade_url)
        comtrade_data = comtrade_resp.json()
        with open('data/raw/structured/un_comtrade.json', 'w', encoding='utf-8') as f:
            json.dump(comtrade_data, f)
        if 'dataset' in comtrade_data:
            df = pd.DataFrame(comtrade_data['dataset'])
            df.to_csv('data/raw/structured/un_comtrade.csv', index=False)
            print('Saved UN Comtrade data.')
    except Exception as e:
        print(f'UN Comtrade API fetch failed: {e}')

if __name__ == '__main__':
    fetch_worldbank()
    fetch_covid()
    fetch_comtrade() 