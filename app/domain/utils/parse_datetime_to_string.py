from datetime import datetime


def parse_datetime_to_payclub_date_format(date: datetime):
    wished_format = "%Y%m%d %H:%M:%S"
    date_to_string = str(date.strftime(wished_format))
    return date_to_string


def parse_datetime_to_string(date: datetime):
    wished_format = "%d/%m/%Y"
    date_to_string = str(date.strftime(wished_format))
    return date_to_string
