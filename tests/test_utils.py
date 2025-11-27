import json
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
from freezegun import freeze_time

from src.utils import (executed_operations, get_amount_by_card, get_date_interval, get_dict_with_cards,
                       get_exchange_rate, get_greeting, get_stocks, get_top_transaction, read_excel,
                       reading_file_user_settings, selection_by_date)


@freeze_time("2025-11-17 11:59:10")
def test_get_greeting_morning():
    result = get_greeting()
    assert result == "Доброе утро"


@freeze_time("2025-11-17 17:59:10")
def test_get_greeting_day():
    result = get_greeting()
    assert result == "Добрый день"


@freeze_time("2025-11-17 23:50:00")
def test_get_greeting_evening():
    result = get_greeting()
    assert result == "Добрый вечер"


@freeze_time("2025-11-17 00:00:00")
def test_get_greeting_night():
    result = get_greeting()
    assert result == "Доброй ночи"


def test_read_excel():
    test_data = pd.DataFrame({"Номер карты": ["*1234"], "Сумма": [100]})
    with patch("src.utils.pd.read_excel") as mock_read_excel:
        mock_read_excel.return_value = test_data
        result = read_excel("user_settings.xlsx")
        pd.testing.assert_frame_equal(result, test_data)


def test_read_excel_error():
    with patch("src.utils.pd.read_excel") as mock_read_excel:
        mock_read_excel.side_effect = FileNotFoundError("File not found")
        result = read_excel("example.xlsx")
        assert "Ошибка чтения файла" in result
        assert "File not found" in result


def test_get_date_interval():
    result = get_date_interval("2025-11-17 23:15:32")
    assert result == ["01.11.2025 00:00:00", "17.11.2025 23:15:32"]


def test_get_date_interval_error():
    result = get_date_interval("adwd-ss-dh iu:po:bb")
    assert result == []


def test_selection_by_date():
    test_data = pd.DataFrame(
        {
            "Номер карты": ["*1234", "*1235", "*1236"],
            "Сумма": [100, 150, 1200],
            "Дата операции": ["12.05.2024 12:33:14", "21.05.2024 15:24:10", "26.05.2024 09:05:50"],
        }
    )
    interval = ["01.05.2024 00:00:00", "22.05.2024 12:00:00"]
    result = selection_by_date(test_data, interval)

    expected = pd.DataFrame(
        {
            "Номер карты": ["*1234", "*1235"],
            "Сумма": [100, 150],
            "Дата операции": ["12.05.2024 12:33:14", "21.05.2024 15:24:10"],
        }
    )
    expected["Дата операции"] = pd.to_datetime(expected["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))


def test_executed_operations():
    test_data = pd.DataFrame({"Номер карты": ["*1234", "*1235", "*1236"], "Статус": ["OK", "OK", "FAILED"]})
    expected = pd.DataFrame({"Номер карты": ["*1234", "*1235"], "Статус": ["OK", "OK"]})
    result = executed_operations(test_data)
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))


def test_get_amount_by_card():
    test_data = pd.DataFrame(
        {"Номер карты": ["*1234", "*1235", "*1234", "*1235"], "Сумма операции": [-1200, -234, -950, -500]}
    )

    expected = pd.Series([-2150, -734], index=["*1234", "*1235"], name="Сумма операции")
    result = get_amount_by_card(test_data)
    pd.testing.assert_series_equal(result.reset_index(drop=True), expected.reset_index(drop=True))


def test_get_dict_with_cards():
    test_data = pd.Series([-2150, -734], index=["*1234", "*1235"], name="Сумма операции")
    expected = [
        {"last_digits": "1234", "total_spent": 2150, "cashback": 21.5},
        {"last_digits": "1235", "total_spent": 734, "cashback": 7.34},
    ]
    result = get_dict_with_cards(test_data)
    assert result == expected


def test_get_top_transaction():
    test_data = pd.DataFrame(
        {
            "Дата платежа": [
                "12.05.2024 12:33:14",
                "14.05.2024 15:24:10",
                "17.05.2024 09:05:50",
                "18.05.2024 14:313:42",
                "21.05.2024 11:04:10",
                "26.05.2024 08:35:05",
                "28.05.2024 19:09:43",
            ],
            "Сумма платежа": [-1200.00, -234.40, -950.00, -500.00, -12000.00, -3440.50, -700.00],
            "Категория": [
                "Супермаркеты",
                "Супермаркеты",
                "Каршеринг",
                "Дом и ремонт",
                "Каршеринг",
                "Супермаркеты",
                "Каршеринг",
            ],
            "Описание": ["Магнит", "Колхоз", "Ситидрайв", "Галамарт", "Ситидрайв", "Магнит", "Яндекс Такси"],
        }
    )

    expected = [
        {"date": "21.05.2024 11:04:10", "amount": -12000.0, "category": "Каршеринг", "description": "Ситидрайв"},
        {"date": "26.05.2024 08:35:05", "amount": -3440.5, "category": "Супермаркеты", "description": "Магнит"},
        {"date": "12.05.2024 12:33:14", "amount": -1200.0, "category": "Супермаркеты", "description": "Магнит"},
        {"date": "17.05.2024 09:05:50", "amount": -950.0, "category": "Каршеринг", "description": "Ситидрайв"},
        {"date": "28.05.2024 19:09:43", "amount": -700.0, "category": "Каршеринг", "description": "Яндекс Такси"},
    ]
    result = get_top_transaction(test_data)
    assert result == expected


def test_reading_file_user_settings_success():
    test_data = {"user_currencies": ["USD", "EUR"]}

    with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
        with patch("json.load") as mock_json:
            mock_json.return_value = test_data
            result = reading_file_user_settings("user_settings.json")
            assert result == test_data


def test_get_exchange_rate():
    user_settings = {"user_currencies": ["USD", "EUR"]}

    with patch.dict("os.environ", {"API_KEY_EXCHANGE_RATE": "test_key"}):
        with patch("requests.request") as mock_request:
            mock_request.side_effect = [
                type(
                    "Response",
                    (),
                    {"status_code": 200, "json": lambda self: {"query": {"from": "USD"}, "result": 75.5}},
                )(),
                type(
                    "Response",
                    (),
                    {"status_code": 200, "json": lambda self: {"query": {"from": "EUR"}, "result": 85.2}},
                )(),
            ]

            result = get_exchange_rate(user_settings)

            expected = [{"currency": "USD", "rate": 75.5}, {"currency": "EUR", "rate": 85.2}]
            assert result == expected
            assert mock_request.call_count == 2


def test_get_exchange_rate_error():
    user_settings = {"user_currencies": ["USD"]}

    with patch.dict("os.environ", {"API_KEY_EXCHANGE_RATE": "test_key"}):
        with patch("requests.request") as mock_request:
            mock_request.side_effect = [
                type(
                    "Response",
                    (),
                    {"status_code": 200, "json": lambda self: {"query": {"from": "USD"}, "result": 75.5}},
                )()
            ]

            result = get_exchange_rate(user_settings)

            expected = [{"currency": "USD", "rate": 75.5}]
            assert result == expected
            assert mock_request.call_count == 1


def test_get_stock():
    user_settings = {"user_stocks": ["AAPL", "GOOGL"]}

    with patch.dict("os.environ", {"API_KEY_STOCKS": "test_key"}):
        with patch("requests.request") as mock_request:

            response_aapl = MagicMock()
            response_aapl.status_code = 200
            response_aapl.json.return_value = {"price": "115.23"}

            response_googl = MagicMock()
            response_googl.status_code = 200
            response_googl.json.return_value = {"price": "423.37"}

            mock_request.side_effect = [response_aapl, response_googl]

            result = get_stocks(user_settings)

            expected = [{"stock": "AAPL", "price": "115.23"}, {"stock": "GOOGL", "price": "423.37"}]
            assert result == expected
