
import logging
import os
import re

from src.reports import spending_by_category
from src.services import investment_bank, read_json
from src.utils import read_excel
from src.views import get_greeting, main_func

current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(current_dir)
file_path = os.path.join(project_root, "logs", "application.log")

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(file_path, mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def main():
    """Главная функция объединяет логику проекта"""
    logger.info("Функция main начала работу")
    greeting = get_greeting()
    print(greeting)

    print('Получить json-ответ по переданному дата фрейму введите 1')
    print('Получить отчет по тратам за три месяца введите 2')
    print('Рассчитать сколько можно экономить с инвесткопилкой введите 3')
    print('Чтобы закончить работу введите 4')
    while True:
        user_answer = input('Ввод: ')
        if user_answer.strip() == '1':
            data = call_views()
            print(data)
        if user_answer.strip() == '2':
            report = get_report()
            print(report)
        if user_answer.strip() == '3':
            services = call_services()
            print(services)
        if user_answer.strip() == '4':
            break


def call_views():
    """Функция обращается к модулю views и получает json-ответ"""
    logger.info("Функция call_views начала работу")
    print('Чтобы получить данные по транзакциям введите дату.')
    print('Ответ включает транзакции за месяц вплоть до введенной даты')
    print('Формат даты YYYY-MM-DD HH:MM:SS')
    try:
        while True:
            user_input = input('Ввод: ')
            pattern = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
            result = re.findall(pattern, user_input.strip(), flags=0)
            if not result:
                print('Дата введена неверно.')
                print()
                print('Проверьте правильность ввода и соответствие формату')
            else:
                data = main_func(user_input)
                logger.info("Функция call_views отработала успешно")
                return data
    except Exception as ex:
        logger.error(f'Ошибка {ex} в функции call_views')
        return 'Ошибка {ex} в функции call_views'


def get_report():
    """Функция обращается к модулю reports для получения отчета"""
    logger.info("Функция get_report начала работу")
    print()
    print('Введите категорию')
    user_category = input('Ввод: ')
    print()
    print('Введите дату или pass, чтобы пропустить этот этап')
    user_date = input('Ввод: ')
    print()
    print('Введите имя excel-файла из папки data')
    user_answer = input('Ввод: ').strip()
    print()
    try:
        user_data = read_excel(user_answer)
        if not user_date:
            report = spending_by_category(user_data, user_category)
        else:
            report = spending_by_category(user_data, user_category, user_date)
            logger.info("Функция get_report отработала успешно")
        return report
    except Exception as ex:
        logger.error(f'Ошибка {ex} в функции get_report')
        print(f'Ошибка {ex} в функции get_report')
        return 0.0


def call_services():
    """Функция обращается к модулю services для расчета сэкономленных
    денег с инвесткопилкой"""
    logger.info("Функция call_services начала работу")
    print()
    print('Введите месяц, функция рассчитает сумму, которую можно сэкономить')
    print('Формат ввода YYYY-MM')
    print()
    user_month = input('Ввод: ').strip()
    print()
    print('Введите имя json-файла из папки data')
    user_answer = input('Ввод: ').strip()
    print()
    print('Введите лимит, любое удобное для округления число: 10, 50 или 100')
    user_limit = int(input('Ввод: ').strip())
    print()
    try:
        user_data = read_json(user_answer)
        if user_data == 0.0:
            logger.error('Ошибка чтения файла')
            print("Ошибка загрузки данных из JSON файла")
            return 0.0
        data = investment_bank(user_month, user_data, user_limit)
        logger.info("Функция call_services отработала успешно")
        return data
    except Exception as ex:
        logger.error(f'Ошибка {ex} в функции call_services')
        print(f'Ошибка {ex} в функции call_services')
        return 0.0
