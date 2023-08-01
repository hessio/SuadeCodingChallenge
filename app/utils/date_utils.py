from datetime import datetime


def parse_date(date):
    return str(datetime.strptime(date, "%Y-%m-%d")).split(' ')[0]


def date_in_range(date_string):
    return datetime(2019, 8, 1) <= datetime(date_string[0], date_string[1], date_string[2]) <= datetime(2019, 9, 29)


def validate_date_format(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        raise ValueError("Invalid date format. Please use the 'YYYY-MM-DD' format.")


def convert_date_to_int(date_str):

    res = date_str.split('-')
    for i in range(len(res)):
        res[i] = int(res[i])
    return res
