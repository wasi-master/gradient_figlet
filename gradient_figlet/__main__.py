"""
Generate cool looking gradient figlets and print them to the terminal
"""
import random
import shutil
from argparse import ArgumentParser

from colour import Color, rgb2hex
from gradient_figlet import rich, print_with_gradient
from pyfiglet import Figlet, FigletFont, figlet_format

from .pleasing_items import good_gradients, good_fonts

terminal_size = shutil.get_terminal_size((80, 20))

parser = ArgumentParser(prog="gradient_figlet",description=__doc__)
parser.add_argument("text", help="The text to print")
parser.add_argument("-c", "--color", help="The colors for the gradient (comma seperated hex codes)", default=",".join(random.choice(list(good_gradients.values()))))
parser.add_argument("-f", "--font", help="The font for the figlet (font supported by pyfiglet)", default=random.choice(good_fonts))
parser.add_argument("-F", "--all-fonts", help="Shows all the available fonts", action="store_true")
parser.add_argument("-p", "--pager", help="Whether to use a pager or not", action="store_true")
parser.add_argument("-d", "--direction", help="`left-to-right` makes the output flush-left.  `right-to-left` makes it flush-right. Left-to-right text will be flush-left, while right-to-left text will be flush-right. `auto` (default) sets it according to whether left-to-right or right-to-left font is selected.")
parser.add_argument("-j", "--justify", help="These option handles the justification  of FIGlet output. `center` centers the output horizontally. `auto` (default) sets the justification according to whether left-to-right or right-to-left text is selected.  (Left-to-right versus right-to-left text is controlled by -d)", action="store_true")
parser.add_argument("-w", "--width", help="How long is the terminal in width", action="store_true", default=terminal_size[0])
args = parser.parse_args()

if args.all_fonts:
    from rich.console import Console
    from rich.columns import Columns
    from rich.panel import Panel
    from rich.text import Text
    from rich.box import ASCII, ROUNDED
    from rich.progress import track
    from rich.markdown import Markdown

    console = Console()
    all_fonts = FigletFont.getFonts()
    num_of_fonts = len(all_fonts)
    colors1 = map(Color, random.choices(list(map(lambda i: i[0], good_gradients.values())), k=num_of_fonts))
    colors2 = map(Color, random.choices(list(map(lambda i: i[1], good_gradients.values())), k=num_of_fonts))

    items = []
    for font, color1, color2 in track(
        zip(all_fonts, colors1, colors2), total=num_of_fonts, description="Formatting fonts", transient=True
    ):
        figlet_text = figlet_format(args.text or "Test", font)
        text = Text()
        lines = figlet_text.splitlines()
        try:
            gradient_colors = list(color1.range_to(color2, len(lines)))
        except ValueError:
            continue
        for c, l in zip(gradient_colors, lines):
            text.append(l + "\n", style=c.hex_l)
        items.append(
            Panel(
                text,
                box=ASCII if args.pager else ROUNDED,
                title=font,
                subtitle=f"[white on {color1.hex_l}]{color1.hex_l}[/] -> [white on {color2.hex_l}]{color2.hex_l}[/]",
            )
        )
    print("\n")
    if args.pager:
        with console.pager():
            console.print(Columns(items))
    else:
        console.print(Columns(items))
    print("\n")
    if console.is_terminal and not args.pager:
        console.print(
            Markdown(
                "**Note:** Consider piping the output to a file or using a pager (`--pager`) for a better viewing experience "
            )
        )
    exit(0)

colors = [Color(h) for h in args.color.split(",")]
f = Figlet(font=args.font, direction=args.direction, justify=args.justify, width=args.width)

get_contrasting_color = lambda x: f"{Color(f'{rgb2hex(tuple(0 if c > 0.5 else 1 for c in x.rgb))}').hex_l}"

print_with_gradient(f.renderText(args.text), *colors)
rich.print(f"Font Used: [green]{args.font}[/]")
rich.print(f"Gradient Used: {' -> '.join(map(lambda x: f'[{get_contrasting_color(x)} on {x.hex_l}]{x.hex_l}[/]', colors))}")
