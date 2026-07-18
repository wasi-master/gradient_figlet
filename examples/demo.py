"""A quick tour of what gradient_figlet can do.

Run it with:

    python examples/demo.py
"""
from rich.console import Console
from rich.rule import Rule

from gradient_figlet import make_gradient, make_gradient_figlet
from gradient_figlet.pleasing_items import good_gradients

console = Console()

# 1. The one-liner: render a figlet with a gradient and print it.
console.print(Rule("A simple two color gradient"))
console.print(make_gradient_figlet("Hello!", "#ff512f", "#dd2476", font="slant"))

# 2. Gradients can have any number of stops.
console.print(Rule("A gradient with three stops"))
console.print(make_gradient_figlet("Rainbow", "red", "yellow", "blue", font="big"))

# 3. Use one of the built-in named gradients.
console.print(Rule("A built-in named gradient"))
color1, color2 = good_gradients["Endless River"]
console.print(make_gradient_figlet("Rivers", color1, color2, font="standard"))

# 4. make_gradient works on any multiline text, not just figlets.
console.print(Rule("Gradients on plain text"))
poem = "\n".join(
    [
        "Gradients are nice,",
        "they fade from one color",
        "into another one,",
        "line by line by line.",
    ]
)
console.print(make_gradient(poem, "#06beb6", "#48b1bf"))
