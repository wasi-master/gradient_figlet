import unicodedata
import re

import rich
from rich.console import Console
from rich.terminal_theme import TerminalTheme
from colour import Color

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

rgb = lambda r, g, b: (r, g, b)

__all__ = ("print_with_gradient", "make_gradient")
__author__ = "Wasi Master"
__version__ = "0.4.3"

console = Console(record=True)
DRACULA_TERMINAL_THEME = TerminalTheme(
    rgb(40, 42, 54),
    rgb(248, 248, 242),
    [
        rgb(40, 42, 54),
        rgb(255, 85, 85),
        rgb(80, 250, 123),
        rgb(241, 250, 140),
        rgb(189, 147, 249),
        rgb(255, 121, 198),
        rgb(139, 233, 253),
        rgb(255, 255, 255),
    ],
    [
        rgb(40, 42, 54),
        rgb(255, 85, 85),
        rgb(80, 250, 123),
        rgb(241, 250, 140),
        rgb(189, 147, 249),
        rgb(255, 121, 198),
        rgb(139, 233, 253),
        rgb(255, 255, 255),
    ],
)

def print_with_gradient(text: str, color1: Color, color2: Color, also_to_html=False, original_text=None) -> None:
    lines = text.splitlines()
    for c, l in zip(color1.range_to(color2, len(lines)), lines):
        console.print(f"[{c.hex_l}]{l}[/]")
    if also_to_html:
        console.save_html(slugify(original_text if original_text else "output") + ".html", theme=DRACULA_TERMINAL_THEME)
