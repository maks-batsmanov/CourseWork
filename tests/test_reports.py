from unittest.mock import patch

import pandas as pd

from src.reports import filtered_by_category, get_time_period, spending_by_category


def test_filtered_by_category(call_dataframe):
    result = filtered_by_category(call_dataframe, 'Каршеринг')
    expected = 1323.35
    assert result == expected


def test_filtered_by_category_error_category(call_dataframe):
    result = filtered_by_category(call_dataframe, 'Колхоз')
    expected = 0.0
    assert result == expected


def test_filtered_by_category_error_columns(capsys):
    test_data = pd.DataFrame({'Сумма платежа': [112.00, 480.90], 'Дата операции': ['2024-06-19', '2024-06-29']})
    result = filtered_by_category(test_data, 'Каршеринг')
    captured = capsys.readouterr()
    assert captured.out == 'В переданном датафрейме нет колонки "Категория"\n'
    assert result == 0.0


def test_get_time_period(call_dataframe):
    result = get_time_period(call_dataframe, '2024-08-15')
    expected = pd.DataFrame({'Категория': ['Супермаркеты', 'Супермаркеты', 'Супермаркеты', 'Супермаркеты'],
                             'Дата операции': pd.to_datetime(['2024-07-16', '2024-06-29', '2024-06-26', '2024-05-19']),
                             'Сумма платежа': [112.00, 324.50, 1120.20, 2050.75]})
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))


def test_get_time_period_error(call_dataframe, capsys):
    result = get_time_period(call_dataframe, '2024-08')
    captured = capsys.readouterr()
    assert captured.out == "Ошибка в функции get_time_period time data '2024-08' does not match format '%Y-%m-%d'\n"
    assert result.empty


def test_get_time_period_exception(capsys):
    df = pd.DataFrame({'Категория': ['test'], 'Дата операции': ['2024-07-16']})

    result = get_time_period(df, 'неправильная-дата')

    captured = capsys.readouterr()
    assert 'Ошибка в функции get_time_period' in captured.out
    assert result.empty


def test_spending_by_category(call_dataframe):
    result = spending_by_category(call_dataframe, 'Супермаркеты', '2024-09-16')
    # expected = pd.DataFrame({'Категория': ['Супермаркеты', 'Супермаркеты', 'Супермаркеты'],
    #                          'Дата операции': ['2024-07-16', '2024-06-29', '2024-06-26'],
    #                          'Сумма платежа': [112.00, 324.50, 1120.20]})
    assert result == 1556.70


def test_spending_by_category_error_category(call_dataframe):
    result = spending_by_category(call_dataframe, 'Колхоз', '2024-09-16')
    assert result == 0.0


def test_spending_by_category_error_transaction():
    test_data = pd.DataFrame({})
    result = spending_by_category(test_data, 'Колхоз', '2024-09-16')
    assert result == 0.0


@patch('src.reports.get_time_period')
def test_spending_by_category_error(mock_filtered, call_dataframe):
    mock_filtered.return_value = pd.DataFrame()
    result = spending_by_category(call_dataframe, 'Супермаркеты', '2024-09-16')
    assert result == 0.0
    mock_filtered.assert_called_once_with(call_dataframe, '2024-09-16')


# def test_spending_by_category_error_except(call_dataframe):
#     with pytest.raises(ValueError) as ex:
#         spending_by_category(call_dataframe, '1234', '2024-09-16')
