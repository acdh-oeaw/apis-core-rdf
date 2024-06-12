import pathlib
from django import template

register = template.Library()


@register.simple_tag
def password():
    return pathlib.Path("/tmp/password.txt").read_text()


@register.simple_tag
def startup():
    return pathlib.Path("/tmp/startup.txt").read_text()
