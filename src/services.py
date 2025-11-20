from typing import Any, Dict, List


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Функция округляет сумму операции по указанному лимиту.
     Функция принимает три аргумента:
        month — месяц, для которого рассчитывается отложенная сумма (строка в формате 'YYYY-MM').
        transactions — список словарей, содержащий информацию о транзакциях,
    в которых содержатся следующие поля: 'Дата операции', 'Сумма операции'.
        limit — предел, до которого нужно округлять суммы операций."""

    if not transactions or limit <= 0:
        return 0.0
    list_transact = [x for x in transactions
                     if x.get('Дата операции', '')[:7] == month
                     and isinstance(x.get('Сумма операции', 0), (int, float))]

    list_round = sum(
        [abs(float(x.get('Сумма операции', 0) % limit - limit))
         for x in list_transact
         if float(x.get('Сумма операции', '')) % limit > 0])
    if not list_round:
        return 0.0
    return round(list_round, 2)
