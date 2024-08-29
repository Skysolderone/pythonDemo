#Alpha Vantage！您的 API 密钥是：6F5VORYY3C0SK972

import requests
url='https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey=6F5VORYY3C0SK972'
response=requests.get(url)
response_data = response.json()
# print(response_data)



#day
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey=6F5VORYY3C0SK972'
r = requests.get(url)
data = r.json()

# print(data)
#week
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol=BTC&market=USD&apikey=6F5VORYY3C0SK972'
r = requests.get(url)
data = r.json()

# print(data)

#month
url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol=BTC&market=USD&apikey=6F5VORYY3C0SK972'
r = requests.get(url)
data = r.json()

# print(data)


#news
url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=COIN,CRYPTO:BTC,FOREX:USD&time_from=20230410T0130&limit=1000&apikey=6F5VORYY3C0SK972'
r = requests.get(url)
data = r.json()

# print(data)
from datetime import datetime

# 获取当前时间
current_time = datetime.now()

# 将时间格式化为 YYYYMMDDTHHMMSS
formatted_time = current_time.strftime("%Y%m%dT%H%M%S")

print(formatted_time)
#新闻过时  需付费获取高级api