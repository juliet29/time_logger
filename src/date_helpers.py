from datetime import date, datetime


def format_date(_date: date) -> str:
    return _date.strftime("%Y-%m-%d")


def get_todays_date() -> date:
    return date.today()


def validate_date(date_text: str) -> date:
    try:
        entered_datetime =  datetime.strptime(date_text, "%y%m%d")
    except ValueError:
        raise ValueError("Incorrect data format, should be YYMMDD")
    assert entered_datetime.year >= 2024
    return entered_datetime.date()
