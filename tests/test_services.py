from src.services import investment_bank, read_json
import pytest
from unittest.mock import patch

@pytest.mark.parametrize('month, limit, expected', [
        ('2024-02', 100, 129.50),
        ('2024-06', 10, 11.58),
        ('2024-02', 50, 79.50),
        ('2024-06', 100, 211.58)
    ])
def test_investment_bank_(month, limit, data_transactions, expected):
    result = investment_bank(month, data_transactions, limit)
    assert result == expected


def test_investment_bank_limit_is_not(data_transactions):
    result = investment_bank('2024-02', data_transactions, 0)
    assert result == 0.0


def test_investment_bank_transaction_is_not(data_transactions):
    data_is_not = []
    result = investment_bank('2024-02', data_is_not, 100)
    assert result == 0.0


def test_investment_bank_sum_is_not_(data_transactions):
    result = investment_bank('2024-07', data_transactions, 10)
    assert result == 0.0


def test_read_json_1():
    assert read_json(r"C:\Users\Smart PC\PycharmProjects\NewProject\tests\test_transactions.json") == [
        {'id': 441945886,
         'state': 'EXECUTED',
         'date': '2019-08-26T10:50:58.294041',
         'operationAmount': {'amount': '31957.58',
                             'currency': {'name': 'руб.', 'code': 'RUB'}},
         'description': 'Перевод организации',
         'from': 'Maestro 1596837868705199',
         'to': 'Счет 64686473678894779589'},

        {'id': 41428829,
         'state': 'EXECUTED',
         'date': '2019-07-03T18:35:29.512364',
         'operationAmount': {'amount': '8221.37',
                             'currency': {'name': 'USD', 'code': 'USD'}},
         'description': 'Перевод организации',
         'from': 'MasterCard 7158300734726758',
         'to': 'Счет 35383033474447895560'},

        {'id': 939719570,
         'state': 'EXECUTED',
         'date': '2018-06-30T02:08:58.425572',
         'operationAmount': {'amount': '9824.07',
                             'currency': {'name': 'USD', 'code': 'USD'}},
         'description': 'Перевод организации',
         'from': 'Счет 75106830613657916952',
         'to': 'Счет 11776614605963066702'}]


@pytest.mark.parametrize('value, expected', [
    ('123', 0.0),
    ('{}', 0.0),
    ('[]', 0.0),
    ('0', 0.0),
])
def test_read_json(value, expected):
    assert read_json(value) == expected


def test_file_not_exists():
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = False
        result = read_json('fake_path.json')
        assert result == 0.0
        mock_exists.assert_called_once()


def test_file_not_exists_error():
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = KeyError
        result = read_json('fake_path.json')
        assert result == 0.0
        mock_exists.assert_called_once()