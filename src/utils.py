import json
import logging
import os
import re
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(current_dir)
file_path = os.path.join(project_root, "logs", "application.log")

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_greeting():
    """Приветствует пользователя"""

    logger.info("Функция get_greeting начала работу")
    hour = datetime.now().hour
    if 0 <= hour <= 5:
        logger.info("Функция get_greeting отработала успешно")
        return "Доброй ночи"
    elif 6 <= hour <= 11:
        logger.info("Функция get_greeting отработала успешно")
        return "Доброе утро"
    elif 12 <= hour <= 17:
        logger.info("Функция get_greeting отработала успешно")
        return "Добрый день"
    elif 18 <= hour <= 23:
        logger.info("Функция get_greeting отработала успешно")
        return "Добрый вечер"


def read_excel(file_name):
    """Функция читает excel-файл из папки data, и возвращает данные.
    Принимает на вход имя файла из папки data"""

    logger.info("Функция read_excel начала работу")
    current_dir = os.path.dirname(__file__)
    project_root = os.path.dirname(current_dir)
    path_to_file = os.path.join(project_root, "data", file_name)
    try:
        excel_data = pd.read_excel(path_to_file, engine="openpyxl")
    except Exception as ex:
        logger.error(f"Ошибка в функции read_excel {ex}")
        return f"Ошибка чтения файла {ex}"
    logger.info("Функция read_excel отработала успешно")
    return excel_data


def get_date_interval(date_time, date_format="%Y-%m-%d %H:%M:%S"):
    """Функция принимает дату в формате YYYY-MM-DD HH:MM:SS
    возвращает список с двумя датами:
    дата от начала месяца, на который выпадает входящая дата, по входящую дату."""
    logger.info("Функция get_date_interval начала работу")
    pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
    result = re.findall(pattern, date_time, flags=0)
    if not result:
        logger.error("Ошибка. Неверная дата")
        print("Ошибка. Неверная дата")
        return result
    dt = datetime.strptime(date_time, date_format)
    start_of_month = dt.replace(day=1, hour=0, minute=0, second=0)
    logger.info("Функция get_date_interval отработала успешно")
    return [start_of_month.strftime("%d.%m.%Y %H:%M:%S"), dt.strftime("%d.%m.%Y %H:%M:%S")]


def selection_by_date(dataframe, list_of_date):
    """Функция принимает dataframe и временной диапазон от начала месяца
    до какого-то дня и возвращает список транзакций из данного диапазона"""
    logger.info("Функция selection_by_date начала работу")
    start, end = list_of_date

    start_dt = pd.to_datetime(start, format="%d.%m.%Y %H:%M:%S")
    end_dt = pd.to_datetime(end, format="%d.%m.%Y %H:%M:%S")

    dataframe["Дата операции"] = pd.to_datetime(dataframe["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    filtered_df = dataframe[(dataframe["Дата операции"] >= start_dt) & (dataframe["Дата операции"] <= end_dt)]
    logger.info("Функция selection_by_date отработала успешно")
    return filtered_df


def executed_operations(data_frame):
    """Функция принимает dataframe в указанном диапазоне,
    возвращает только операции со статусом OK"""

    logger.info("Функция executed_operations начала работу")
    logger.info("Функция executed_operations отработала успешно")
    return data_frame.loc[data_frame["Статус"].isin(["OK"])]


def get_amount_by_card(data_frame):
    """Функция принимает dataframe в указанном диапазоне, со статусом OK.
    Возвращает сумму расходов по каждой карте в формате series"""

    logger.info("Функция get_amount_by_card начала работу")
    negative_amount = data_frame[data_frame["Сумма операции"] < 0]
    group_data = negative_amount.groupby("Номер карты")
    result = group_data["Сумма операции"].sum()
    logger.info("Функция get_amount_by_card отработала успешно")
    return result


def get_dict_with_cards(series):
    """Функция принимает series с номерами карт и суммой расходов по ним.
    Возвращает список словарей: [{
      "last_digits": number,
      "total_spent": sum,
      "cashback": cashback
    }]"""
    logger.info("Функция get_dict_with_cards начала работу")
    list_of_dict = [
        {"last_digits": card.replace("*", ""), "total_spent": abs(sum_), "cashback": round(abs(sum_) / 100, 2)}
        for card, sum_ in series.items()
    ]
    logger.info("Функция get_dict_with_cards отработала успешно")
    return list_of_dict


def get_top_transaction(data_frame):
    """Функция принимает отсортированный по статусу dataframe
    и возвращает топ 5 транзакций по сумме платежа"""
    logger.info("Функция get_top_transaction начала работу")
    dt_top_sorted = data_frame.sort_values(by=["Сумма платежа"]).head()
    result = [
        {
            "date": row["Дата платежа"],
            "amount": row["Сумма платежа"],
            "category": row["Категория"],
            "description": row["Описание"],
        }
        for index, row in dt_top_sorted.iterrows()
    ]
    logger.info("Функция get_top_transaction отработала успешно")
    return result


def reading_file_user_settings(file_name):
    """Функция принимает имя json файла из корня проекта, файл содержит валюты для получения обменного курса.
    Читает файл с пользовательскими настройками и возвращает словарь"""
    logger.info("Функция reading_file_user_settings начала работу")
    current_dir = os.path.dirname(__file__)
    project_root = os.path.dirname(current_dir)
    path_to_file = os.path.join(project_root, file_name)

    with open(path_to_file, "r", encoding="utf-8") as file:
        parsed_data = json.load(file)
        logger.info("Функция reading_file_user_settings отработала успешно")
    return parsed_data


def get_exchange_rate(data_json):
    """Функция принимает словарь с валютами и возвращает обменный курс по валютам."""
    logger.info("Функция get_exchange_rate начала работу")
    load_dotenv()
    api_key = os.getenv("API_KEY_EXCHANGE_RATE")

    number_of_iterations = len(data_json["user_currencies"])

    list_of_rates = []
    i = 0
    while i < number_of_iterations:

        from_ = data_json["user_currencies"][i]
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={from_}&amount=1"

        payload = {}
        headers = {"apikey": api_key}
        response = requests.request("GET", url, headers=headers, data=payload)
        status_code = response.status_code
        if status_code != 200:
            logger.error(
                f"Ошибка в функции get_exchange_rate при обращении к api сервису. Статус код: {response.status_code}"
            )
            return f"API Error: {status_code}"

        result = response.json()
        dicts = {"currency": result["query"]["from"], "rate": result["result"]}
        list_of_rates.append(dicts)
        print(status_code)
        i += 1
        logger.info("Функция get_exchange_rate отработала успешно")
    return list_of_rates


def get_stocks(data_json):
    """Функция принимает имя json файла из корня проекта,
    файл содержит тикеры акций для получения актуальных цен на бирже.
    Функция возвращает обменный курс по валютам содержащимся в файле."""
    logger.info("Функция get_stocks начала работу")
    load_dotenv()
    api_key = os.getenv("API_KEY_STOCKS")

    number_of_iterations = len(data_json["user_stocks"])

    list_of_stocks = []
    i = 0
    while i < number_of_iterations:

        stock = data_json["user_stocks"][i]
        url = f"https://api.twelvedata.com/price?symbol={stock}&apikey={api_key}"
        payload = {}
        headers = {"apikey": api_key}
        response = requests.request("GET", url, headers=headers, data=payload)
        status_code = response.status_code
        if status_code != 200:
            logger.error(
                f"Ошибка в функции get_stocks при обращении к api сервису. Статус код: {response.status_code}"
            )
            return f"API Error: {status_code}"

        result = response.json()
        dicts = {"stock": stock, "price": result["price"]}
        list_of_stocks.append(dicts)
        i += 1
        logger.info("Функция get_stocks отработала успешно")
    return list_of_stocks
