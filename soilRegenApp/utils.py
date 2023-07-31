import requests
import pandas as pd
import json
from datetime import date, datetime
from django.conf import settings

#  API access management

class MarketStack:
    api_key = settings.API_KEY

    @staticmethod
    def get_price_history(symbol, date_from, limit=365):
        date_to = date.today()
        endpoint_url = f"https://api.marketstack.com/v1/eod?access_key={MarketStack.api_key}&symbols={symbol}&date_from={date_from}&date_to={date_to}&limit={1000}"
        print(f"url={endpoint_url}")
        response = requests.get(endpoint_url)
        if response.status_code == 200:
            print("Success! (200) - Data returned")
            print(response.json())
            if response.json()['data'] == []:
                return None
            data = response.json()['data']
            # print(data)
            df = pd.DataFrame.from_records(data)
            df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
            return df
        else:
            print("Error! (Not 200) - None returned")
        return None

    @staticmethod
    def get_List_history(symbol_lst, date_lst, limit=365):
        date_to = date.today()
        date_from = ""
        for i in range (0, len(date_lst)-1):
            # Find earliest date among the symbols
            date_from_i = datetime.strptime(str(date_lst[i]), "%Y-%m-%d").date()
            if date_lst[i] < date_from_i:
                date_from = date_from_i
        endpoint_url = f"https://api.marketstack.com/v1/eod?access_key={MarketStack.api_key}&symbols={symbol_lst}&date_from={date_from}&date_to={date_to}&limit={1000}"
        print(f"url={endpoint_url}")
        response = requests.get(endpoint_url)
        if response.status_code == 200:
            print("Success! (200) - Data returned")
            data = response.json()['data']
            # print(data)
            df = pd.DataFrame.from_records(data)
            df['date'] = pd.to_datetime(df['date'])
            return df
        else:
            print("Error! (Not 200) - None returned")
        return None