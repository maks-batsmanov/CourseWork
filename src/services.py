import json
import logging
import os
from typing import Any, Dict, List

current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(current_dir)
file_path = os.path.join(project_root, "logs", "application.log")

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Функция округляет сумму операции по указанному лимиту.
     Функция принимает три аргумента:
        month — месяц, для которого рассчитывается отложенная сумма (строка в формате 'YYYY-MM').
        transactions — список словарей, содержащий информацию о транзакциях,
    в которых содержатся следующие поля: 'Дата операции', 'Сумма операции'.
        limit — предел, до которого нужно округлять суммы операций."""
    logger.info('Начало работы функции investment_bank')
    if not transactions or limit <= 0:
        logger.error('Пустой список или неверно указан лимит')
        return 0.0
    list_transact = [x for x in transactions
                     if x.get('Дата операции', '')[:7] == month
                     and isinstance(x.get('Сумма операции', 0), (int, float))]

    list_round = sum(
        [abs(float(x.get('Сумма операции', 0) % limit - limit))
         for x in list_transact
         if float(x.get('Сумма операции', '')) % limit > 0])
    if not list_round:
        logger.error('Транзакций не нашлось, список пуст')
        return 0.0
    logger.info('Функция investment_bank отработала успешно')
    return round(list_round, 2)


def read_json(file_name):
    """Функция читает json-файл из папки data, и возвращает данные.
        Принимает на вход имя файла из папки data"""
    logger.info("Функция read_excel начала работу")
    current_dir = os.path.dirname(__file__)
    project_root = os.path.dirname(current_dir)
    path_to_file = os.path.join(project_root, "data", file_name)
    try:
        if not os.path.exists(path_to_file):
            logger.error("Ошибка, файл не найден")
            return 0.0
        if os.path.getsize(path_to_file) == 0:
            logger.error("Ошибка, файл пустой")
            return 0.0
        logger.info("Открываем и преобразуем файл в список словарей")
        with open(path_to_file, "r", encoding="utf-8") as file:
            content = json.load(file)
        if not isinstance(content, list):
            logger.error("Ошибка, файл не является списком")
            return 0.0
        logger.info("Работа завершена успешно")
        return content
    except Exception as ex:
        logger.error(f"Ошибка чтения файла {ex}")
        print(f"Ошибка чтения файла {ex}")
        return 0.0
