import os
from time import strptime
from datetime import datetime
import openpyxl
import pandas as pd
from datetime import datetime


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
    # not_null_numbers = data_frame.loc[data_frame['Номер карты'].notnull()]
    # cards = list(set(not_null_numbers['Номер карты']))
    # dict_cards = {}
    # for card, amount in

    cards_df = data_frame.groupby('Номер карты')
    new_dt = cards_df['Сумма операции'].sum()

    print(new_dt)
    return []



if __name__ == '__main__':
    data = read_excel('operations.xlsx')
    interval = get_date_interval('2020-07-31 23:30:00')
    select = selection_by_date(data, interval)
    data = executed_operations(select)
    data = get_amount_by_card(data)
    print(data)


# user_date = input('Ввод: ').strip()
#     pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
# if pattern.fullmatch(user_date) is None:

