from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

    
def convert_string_to_datetime(date: str) -> datetime:
    return datetime.strptime(date, DATETIME_FORMAT)   