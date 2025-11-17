import os
from dotenv import load_dotenv
import requests
import pandas as pd
from datetime import datetime
import json


def get_greeting():
    """Приветствует пользователя"""

    hour = datetime.now().hour
    if 0 <= hour <= 5:
        return 'Доброй ночи'
    elif 6 <= hour <= 11:
        return 'Доброе утро'
    elif 12 <= hour <= 17:
        return 'Добрый день'
    elif 18 <= hour <= 23:
        return 'Добрый вечер'


def read_excel(file_name):
    """Функция читает excel-файл из папки data, и возвращает данные.
     Принимает на вход имя файла из папки data"""

    current_dir = os.path.dirname(__file__)
    project_root = os.path.dirname(current_dir)
    path_to_file = os.path.join(project_root, 'data', file_name)
    excel_data = pd.read_excel(path_to_file, engine='openpyxl')
    return excel_data


def get_date_interval(date_time, date_format = '%Y-%m-%d %H:%M:%S'):
    """Функция принимает дату в формате YYYY-MM-DD HH:MM:SS
    и возвращает транзакции с указанной даты по последнюю известную.
    На вход принимает данные из excel-файла"""
    dt = datetime.strptime(date_time, date_format)
    start_of_month = dt.replace(day=1, hour=0, minute=0, second=0)

    return [
        start_of_month.strftime('%d.%m.%Y %H:%M:%S'),
        dt.strftime('%d.%m.%Y %H:%M:%S')
    ]


def selection_by_date(dataframe, list_of_date):
    """Функция принимает временной диапазон от начала месяца
    до какого-то дня и возвращает список транзакций из данного диапазона"""
    start, end = list_of_date

    start_dt = pd.to_datetime(start, format='%d.%m.%Y %H:%M:%S')
    end_dt = pd.to_datetime(end, format='%d.%m.%Y %H:%M:%S')

    dataframe['Дата операции'] = pd.to_datetime(
        dataframe['Дата операции'],
        format='%d.%m.%Y %H:%M:%S')

    filtered_df = dataframe[
            (dataframe['Дата операции'] >= start_dt)&
            (dataframe['Дата операции'] <= end_dt)
        ]
    return filtered_df


def executed_operations(data_frame):
    """Функция принимает dataframe в указанном диапазоне,
    возвращает только операции со статусом OK"""
    return data_frame.loc[data_frame['Статус'].isin(['OK'])]



def get_amount_by_card(data_frame):
    """Функция принимает dataframe в указанном диапазоне, со статусом OK.
    Возвращает сумму расходов"""

    negative_amount = data_frame[data_frame['Сумма операции'] < 0]
    group_data = negative_amount.groupby('Номер карты')
    result = group_data['Сумма операции'].sum()
    return result


def get_dict_with_cards(series):
    """Функция принимает series с номерами карт и суммой расходов по ним.
    Возвращает словарь: {
      "last_digits": number,
      "total_spent": sum,
      "cashback": cashback
    }"""
    list_of_dict = [
        {
        'last_digits': card.replace('*', ''),
        'total_spent': abs(sum_),
        'cashback': round(abs(sum_) / 100, 2)
        }
        for card, sum_ in series.items()
    ]
    return list_of_dict


def get_top_transaction(data_frame):
    """Функция принимает отсортированный по статусу dataframe
    и возвращает топ 5 транзакций по сумме платежа"""
    dt_top_sorted = data_frame.sort_values(by=['Сумма операции']).head()
    result = [
        {
            'date': row['Дата платежа'],
            'amount': row['Сумма платежа'],
            'category': row['Категория'],
            'description': row['Описание']
        }
        for index, row in dt_top_sorted.iterrows()
    ]
    return result


def reading_file_user_settings(file_name):
    """Функция принимает имя json файла из корня проекта, файл содержит валюты для получения обменного курса.
    Читает файл с пользовательскими настройками и возвращает phyton-объект """

    current_dir = os.path.dirname(__file__)
    project_root = os.path.dirname(current_dir)
    path_to_file = os.path.join(project_root, file_name)

    with open(path_to_file, 'r', encoding='utf-8') as file:
        parsed_data = json.load(file)
    return parsed_data


def get_exchange_rate(data_json):
    """.
     Функция возвращает обменный курс по валютам содержащимся в файле."""

    load_dotenv()
    api_key = os.getenv('API_KEY_EXCHANGE_RATE')


    number_of_iterations = len(data_json['user_currencies'])

    list_of_rates = []
    i = 0
    while i < number_of_iterations:

        from_ = data_json['user_currencies'][i]
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={from_}&amount=1"

        payload = {}
        headers = {
            "apikey": api_key
        }
        response = requests.request('GET', url, headers=headers, data = payload)
        status_code = response.status_code
        result = response.json()
        dicts = {
            'currency': result['query']['from'],
            'rate': result['result']
        }
        list_of_rates.append(dicts)

        i += 1
    return list_of_rates


def get_stocks(data_json):
    """Функция принимает имя json файла из корня проекта,
    файл содержит тикеры акций для получения актуальных цен на бирже.
    Функция возвращает обменный курс по валютам содержащимся в файле."""

    load_dotenv()
    api_key = os.getenv('API_KEY_STOCKS')

    number_of_iterations = len(data_json['user_stocks'])

    list_of_stocks = []
    i = 0
    while i < number_of_iterations:

        stock = data_json['user_stocks'][i]
        url = f"https://api.twelvedata.com/price?symbol={stock}&apikey={api_key}"
        payload = {}
        headers = {
            "apikey": api_key
        }
        response = requests.request('GET', url, headers=headers, data = payload)
        status_code = response.status_code
        result = response.json()
        dicts = {
            'stock': stock,
            'price': result['price']
        }
        list_of_stocks.append(dicts)
        i += 1
    return list_of_stocks




# if __name__ == '__main__':
#     # data = read_excel('operations.xlsx')
#     # interval = get_date_interval('2021-12-02 23:50:00')
#     # select = selection_by_date(data, interval)
#     # data_main = executed_operations(select)
#     # data = get_amount_by_card(data)
#     # data = get_dict_with_cards(data)
#     # data_top =get_top_transaction(data_main)
#     data_json_file = reading_file_user_settings('user_settings.json')
#     # exchange_rate = get_exchange_rate(data_json_file)
#     stocks = get_stocks(data_json_file)
#     print(get_exchange_rate(data_json_file))
#
# # , ascending=False