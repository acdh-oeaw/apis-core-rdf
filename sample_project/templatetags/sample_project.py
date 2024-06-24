from datetime import datetime, time, date, timedelta, UTC
import pathlib
from django import template

register = template.Library()


@register.simple_tag
def password():
    return pathlib.Path("/tmp/password.txt").read_text()


@register.simple_tag
def teardown():
    init_date = datetime.combine(date.today(), time(0, 30, 0), tzinfo=UTC)
    # create timetsamps for today
    timestamps = [
        init_date,
        init_date.replace(hour=6),
        init_date.replace(hour=12),
        init_date.replace(hour=18),
    ]
    # create timestamps for tomorrow
    timestamps += list(map(lambda x: x + timedelta(hours=24), timestamps))
    # filter timestamps that are after now
    timestamps = list(filter(lambda x: x > datetime.now(UTC), timestamps))
    return timestamps[0]
