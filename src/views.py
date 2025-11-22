import json
import logging
import os

from src.utils import (executed_operations, get_amount_by_card, get_date_interval, get_dict_with_cards,
                       get_exchange_rate, get_greeting, get_stocks, get_top_transaction, read_excel,
                       reading_file_user_settings, selection_by_date)

current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(current_dir)
file_path = os.path.join(project_root, "logs", "application.log")

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def main_func(date_user):
    """Функцию принимает на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращает JSON-ответ"""
    logger.info("Функция main_func начала работу")
    if not date_user or not isinstance(date_user, str):
        logger.error("Функция main_func, некорректный формат даты")
        raise ValueError("Некорректный формат даты")

    greeting = get_greeting()
    data_frame = read_excel("operations.xlsx")
    interval = get_date_interval(date_user)
    selection = selection_by_date(data_frame, interval)
    status = executed_operations(selection)
    get_amount = get_amount_by_card(status)
    get_dict = get_dict_with_cards(get_amount)
    top_transaction = get_top_transaction(status)
    data_json = reading_file_user_settings("user_settings.json")
    exchange_rate = get_exchange_rate(data_json)
    stocks = get_stocks(data_json)

    data_json = {
        "greeting": greeting,
        "cards": get_dict,
        "top transaction": top_transaction,
        "currency_rates": exchange_rate,
        "stock_prices": stocks,
    }
    logger.info("Функция main_func отработала успешно")
    return json.dumps(data_json, indent=4, ensure_ascii=False)
