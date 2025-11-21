import json
import os
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta


def writing_reports(func):
    def wrapper(*args, **kwargs):
        """Декоратор записывает результаты вызова функции в файл 'reports_info.txt'"""
        current_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(current_dir)
        file_path = os.path.join(project_root, "logs", "reports_info.txt")
        result = func(*args, **kwargs)
        log_data = {"function": func.__name__, "timestamp": datetime.now().isoformat(), "result": result}
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"{json.dumps(log_data, indent=4, ensure_ascii=False)}\n")
        return result

    return wrapper


@writing_reports
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> float:
    """Функция возвращает траты по заданной категории за последние три месяца от переданной даты."""

    if transactions.empty or not category:
        print(transactions)
        return 0.0
    try:
        filtered_df = get_time_period(transactions, date)
        if filtered_df.empty:
            return 0.0

        result = filtered_by_category(filtered_df, category)

        return abs(round(result, 2))
    except Exception as ex:
        print(f"Ошибка в функции spending_by_category {ex}")
        return 0.0


def get_time_period(transactions, date):
    """Функция принимает DataFrame и дату, возвращает транзакции за три месяца от указанной даты."""

    try:
        if not date:
            dt = datetime.now()
        else:
            dt = datetime.strptime(date, "%Y-%m-%d")

        start_period = dt - relativedelta(months=3)

        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="mixed")

        filtered_df = transactions[
            (transactions["Дата операции"] >= start_period) & (transactions["Дата операции"] <= dt)
        ]

        return filtered_df
    except Exception as ex:
        print(f"Ошибка в функции get_time_period {ex}")
        return pd.DataFrame()


def filtered_by_category(transactions, category):
    """Функция принимает Dataframe и категорию, возвращает сумму трат по категории."""

    try:
        if "Категория" not in transactions.columns:
            print('В переданном датафрейме нет колонки "Категория"')
            return 0.0

        if category not in transactions["Категория"].values:
            return 0.0
        else:
            df = transactions[transactions["Категория"] == category]
            df_sum = df["Сумма платежа"].sum()

            return df_sum
    except Exception as ex:
        print(f"Ошибка в функции filtered_by_category{ex}")
        return 0.0
