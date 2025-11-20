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
    return list_round


input_data = [
    {'Дата операции': '2024-02-13', 'Сумма операции': 765.00},
    {'Дата операции': '2024-02-02', 'Сумма операции': 1105.50},
    {'Дата операции': '2024-06-07', 'Сумма операции': 220.30},
    {'Дата операции': '2024-06-19', 'Сумма операции': 118.12},
    {'Дата операции': '2024-06-29', 'Сумма операции': 350.00}
]

if __name__ == '__main__':
    print(investment_bank('2024-02', input_data, 50))