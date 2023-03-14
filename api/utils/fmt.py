"""String formatting utilities"""


import re
import jinja2
from pydantic import BaseModel

def pascalcase(_str: str):
    """Converts a string to PascalCase"""
    return "".join([word.capitalize() for word in _str.split("_")])


def camelcase(_str: str):
    """Converts a string to camelCase"""
    return (
        "".join([word.capitalize() for word in _str.split("_")])[0].lower()
        + "".join([word.capitalize() for word in _str.split("_")])[1:]
    )


def snakecase(_str: str):
    """Converts a string to snake_case"""
    return re.sub(r"([A-Z])", r"_\1", _str).lower()


def kebabcase(_str: str):
    """Converts a string to kebab-case"""
    return snakecase(_str).replace("_", "-")


def render_template(template: str, instance:BaseModel):
    """Renders a Jinja2 template"""
    _env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'))
    template = _env.get_template(template)
    return template.render(instance.dict())

