from typing import Any, Dict, List
import logging
import os


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
        logger.error('Пустой датафрейм или неверно указан лимит')
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
