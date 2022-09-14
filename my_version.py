import requests
import smtplib

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
access_key = "XXX"
endpoint = 'https://www.alphavantage.co/query'
news_endpoint = "https://newsapi.org/v2/everything"
news_api_key = "XXX"


news_parameters = {
    "q": COMPANY_NAME,
    "apiKey": news_api_key,
    "sortBy": "publishedAt",
}

news_response = requests.get(news_endpoint, params=news_parameters)
news_response.raise_for_status()
data_news = news_response.json()
recent_3_news = data_news["articles"][:3]

first_news_title = recent_3_news[0]["title"]
second_news_title = recent_3_news[1]["title"]
third_news_title = recent_3_news[2]["title"]

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": access_key
}

response = requests.get(endpoint, params=parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]

yesterday_data = dict(list(data.items())[:1])
before_yesterday_data = dict(list(data.items())[1:2])


def lowest_value(day):
    for value in day:
        new_dict = day[value]
        new_dict_sliced = dict(list(new_dict.items())[2:3])
        for price in new_dict_sliced:
            return new_dict_sliced[price]


def highest_value(day):
    for value in day:
        new_dict = day[value]
        new_dict_sliced = dict(list(new_dict.items())[1:2])
        for price in new_dict_sliced:
            return new_dict_sliced[price]


yesterday_low = float(lowest_value(yesterday_data))
before_yesterday_low = float(lowest_value(before_yesterday_data))
yesterday_high = float(highest_value(yesterday_data))
before_yesterday_high = float(highest_value(before_yesterday_data))


def send_mail(text):
    my_email = "XXX"
    password = "XXX"
    with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="XXX",
            msg=text)


if yesterday_high > before_yesterday_low:
    difference = (yesterday_high * 100 / before_yesterday_low) - 100
    if difference > 1:
        print(f"Stocks went UP for more than 5%\n{first_news_title}\n{second_news_title}\n{third_news_title}")
        send_mail(f"Subject: Stock News\n\nStocks went UP for more than 5%.\n{first_news_title}\n{second_news_title}\n{third_news_title}")

if yesterday_low < before_yesterday_high:
    difference = 100 - (yesterday_low * 100 / before_yesterday_high)
    if difference > 1:
        print(f"Stocks went DOWN for more than 5%\n{first_news_title}\n{second_news_title}\n{third_news_title}")
        send_mail(f"Subject: Stock News\n\nStocks went DOWN for more than 5%.\n{first_news_title}\n{second_news_title}\n{third_news_title}")