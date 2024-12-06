from datetime import date

def format_date(_date:date):
    return _date.strftime("%m-%d-%y")

def get_todays_date():
    return date.today()

def date_validator(data):
    return True