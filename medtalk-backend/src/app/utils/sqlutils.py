from datetime import datetime, date, timedelta
from typing import Any
from sqlmodel import cast
from sqlalchemy import DATE

time_now = datetime.now


def yesterday():
    return date.today() - timedelta(days=1)


def is_today(field: Any):
    return cast(field, DATE) == date.today()


def is_yesterday(field: Any):
    return cast(field, DATE) == yesterday()
