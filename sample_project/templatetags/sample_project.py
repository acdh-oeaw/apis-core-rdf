import datetime
import pathlib
from django import template

register = template.Library()


@register.simple_tag
def password():
    return pathlib.Path("/tmp/password.txt").read_text()


@register.simple_tag
def teardown():
    date = datetime.datetime.fromisoformat(pathlib.Path("/tmp/startup.txt").read_text())
    until = date + datetime.timedelta(hours=6)
    return until
