import pytz
from datetime import datetime


def now():
    return datetime.utcnow().replace(tzinfo=pytz.utc)
