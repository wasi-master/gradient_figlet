"""Print beautiful gradient figlets to the terminal.

The functions you most likely want are :func:`print_with_gradient_figlet`
(render text as a figlet and print it with a gradient) and
:func:`make_gradient` (get the gradient as a :class:`rich.text.Text` object
to compose into your own rich output).

Example:
    >>> from gradient_figlet import print_with_gradient_figlet
    >>> print_with_gradient_figlet("Hello", font="slant", color1="#ff512f", color2="#dd2476")
"""
from typing import List, Optional, Sequence, Union
import unicodedata
import re
import shutil

import rich
from rich.console import Console
from rich.terminal_theme import TerminalTheme
from rich.text import Text
from colour import Color
from pyfiglet import Figlet, FigletFont, figlet_format

__all__ = (
    "interpolate_colors",
    "make_gradient",
    "make_gradient_figlet",
    "print_with_gradient",
    "print_with_gradient_figlet",
)
__author__ = "Wasi Master"
__version__ = "0.6.0"

ColorInput = Union[Color, str]


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
terminal_size = shutil.get_terminal_size((80, 20))

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


def _as_color(color: ColorInput) -> Color:
    """Convert a color name/hex string to a :class:`colour.Color`, pass Color through."""
    return color if isinstance(color, Color) else Color(color)


def _blend(color1: Color, color2: Color, position: float) -> Color:
    """Linearly interpolate between two colors in HSL space.

    ``position`` is between 0 (entirely ``color1``) and 1 (entirely ``color2``).
    """
    h1, s1, l1 = color1.hsl
    h2, s2, l2 = color2.hsl
    return Color(
        hsl=(
            h1 + (h2 - h1) * position,
            s1 + (s2 - s1) * position,
            l1 + (l2 - l1) * position,
        )
    )


def interpolate_colors(colors: Sequence[ColorInput], steps: int) -> List[Color]:
    """Interpolate any number of colors into a gradient of ``steps`` colors.

    Unlike :meth:`colour.Color.range_to`, this supports gradients with more
    than two stops: the steps are distributed evenly across each pair of
    neighbouring colors.

    Args:
        colors: The gradient stops, as :class:`colour.Color` objects or
            anything the ``colour`` library can parse (names, hex codes).
        steps: How many colors the resulting gradient should have.

    Returns:
        A list of exactly ``steps`` colors. Empty if ``steps`` is 0 or less.
    """
    stops = [_as_color(color) for color in colors]
    if steps <= 0 or not stops:
        return []
    if len(stops) == 1:
        return [Color(stops[0]) for _ in range(steps)]
    if steps == 1:
        return [Color(stops[0])]
    segments = len(stops) - 1
    gradient = []
    for step in range(steps):
        position = step / (steps - 1) * segments
        segment = min(int(position), segments - 1)
        gradient.append(_blend(stops[segment], stops[segment + 1], position - segment))
    return gradient


def make_gradient(text: str, *colors: ColorInput) -> Text:
    """Apply a vertical gradient to multiline text.

    Each line gets a single color, interpolated between the given gradient
    stops from the first line to the last.

    Args:
        text: The (usually multiline) text to colorize.
        *colors: Two or more gradient stops. A single color produces solid
            colored text.

    Returns:
        A :class:`rich.text.Text` you can print with any rich console.
    """
    lines = text.splitlines()
    gradient = interpolate_colors(colors, len(lines))
    result = Text()
    for color, line in zip(gradient, lines):
        result.append(line + "\n", style=color.hex_l)
    return result


def make_gradient_figlet(
    text: str,
    *colors: ColorInput,
    font: str = "standard",
    direction: str = "auto",
    justify: str = "auto",
    width: int = terminal_size[0],
) -> Text:
    """Render ``text`` as a figlet and apply a vertical gradient to it.

    Args:
        text: The text to render.
        *colors: Two or more gradient stops (color names or hex codes).
        font: Any font supported by pyfiglet.
        direction: ``auto``, ``left-to-right`` or ``right-to-left``.
        justify: ``auto``, ``left``, ``center`` or ``right``.
        width: The width to render the figlet in, defaults to the terminal width.

    Returns:
        A :class:`rich.text.Text` you can print with any rich console.
    """
    figlet = Figlet(font=font, direction=direction, justify=justify, width=width)
    return make_gradient(figlet.renderText(text), *colors)


def print_with_gradient(
    text: str,
    color1: ColorInput,
    color2: ColorInput,
    *extra_colors: ColorInput,
    also_to_html: bool = False,
    original_text: Optional[str] = None,
) -> None:
    """Print multiline text with a vertical gradient.

    Args:
        text: The (usually multiline) text to print.
        color1: The color of the first line.
        color2: The color of the last line (or an intermediate stop when
            ``extra_colors`` are given).
        *extra_colors: Optional additional gradient stops.
        also_to_html: Whether to also save the output as an HTML file. The
            file name is a slugified version of ``original_text`` (or
            ``output.html`` when that is not given).
        original_text: The original, pre-figlet text, used for the HTML file name.
    """
    console.print(make_gradient(text, color1, color2, *extra_colors), end="")
    if also_to_html:
        console.save_html(slugify(original_text if original_text else "output") + ".html", theme=DRACULA_TERMINAL_THEME)


def print_with_gradient_figlet(
    text: str,
    font: str,
    color1: ColorInput,
    color2: ColorInput,
    *extra_colors: ColorInput,
    direction: str = "auto",
    justify: str = "auto",
    width: int = terminal_size[0],
    save_html: bool = False,
) -> None:
    """Render ``text`` as a figlet and print it with a vertical gradient.

    Args:
        text: The text to render.
        font: Any font supported by pyfiglet.
        color1: The color of the first line.
        color2: The color of the last line (or an intermediate stop when
            ``extra_colors`` are given).
        *extra_colors: Optional additional gradient stops.
        direction: ``auto``, ``left-to-right`` or ``right-to-left``.
        justify: ``auto``, ``left``, ``center`` or ``right``.
        width: The width to render the figlet in, defaults to the terminal width.
        save_html: Whether to also save the output as an HTML file named
            after a slugified version of ``text``.
    """
    figlet = Figlet(font=font, direction=direction, justify=justify, width=width)
    print_with_gradient(
        figlet.renderText(text),
        color1,
        color2,
        *extra_colors,
        also_to_html=save_html,
        original_text=text,
    )
