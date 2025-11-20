from src.services import investment_bank
import pytest


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
