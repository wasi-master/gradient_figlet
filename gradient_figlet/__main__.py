"""
Generate cool looking gradient figlets and print them to the terminal
"""
import random
import shutil

import rich_click as click
from colour import Color, rgb2hex
from gradient_figlet import rich, print_with_gradient, print_with_gradient_figlet

from .pleasing_items import good_gradients, good_fonts

terminal_size = shutil.get_terminal_size((80, 20))
click.rich_click.USE_RICH_MARKUP = True

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument("text")
@click.option("-c", "--color", help="The [red]c[yellow]o[green]l[cyan]o[magenta]r[blue]s[/][default on default] for the [/][#43cea2]g[#00c3aa]r[#00b8b1]a[#00acb7]d[#009fba]i[#0092bb]e[#0077b3]n[#0069a9]t[/][default on default] [b](comma seperated hexadecimal color codes)[/]", default=",".join(random.choice(list(good_gradients.values()))))
@click.option("-f", "--font", help="The [black on #96ff00]f[black on #bffb00]o[black on #e2f600]n[black on #fff000]t[/][default on default] for the [#ff009c]f[#eb009d]i[#d6009e]g[#cb009e]l[#b5009d]e[#9e009b]t[/] [b default on default](has to be a font supported by pyfiglet)[/]", default=random.choice(good_fonts))
@click.option("-F", "--all-fonts", help="Shows [#00eaff][/][#00e5ff]a[/][#00e0ff]l[/][#00daff]l[/][#00d5ff] [/][#00d0ff]t[/][#00cbff]h[/][#00c5ff]e[/][#00c0ff] [/][#00bbff]a[/][#00b6ff]v[/][#00b1ff]a[/][#00abff]i[/][#00a6ff]l[/][#00a1ff]a[/][#009cff]b[/][#0097ff]l[/][#0091ff]e[/][#008cff] [/][#0087ff]f[/][#0082ff]o[/][#007cff]n[/][#0077ff]t[/][#0072ff]s[/]", is_flag=True)
@click.option("-p", "--pager", help="Whether to use a [green]pager[/] or not", is_flag=True)
@click.option("-d", "--direction", help="[yellow on #000000]left-to-right[/] makes the output flush-left.  [yellow on #000000]right-to-left[/] makes it flush-right. Left-to-right text will be flush-left, while right-to-left text will be flush-right. [yellow on #000000]auto[/] (default) sets it according to whether [yellow on #000000]left-to-right[/] or [yellow on #000000]right-to-left[/] font is selected.")
@click.option("-j", "--justify", help="These option handles the justification  of FIGlet output. [yellow on #000000]center[/] centers the output horizontally. [yellow on #000000]auto[/] (default) sets the justification according to whether [yellow on #000000]left-to-right[/] or [yellow on #000000]right-to-left[/] text is selected.  (Left-to-right versus right-to-left text is controlled by -d)")
@click.option("-w", "--width", help="How long is the terminal in width", type=int, default=terminal_size[0])
@click.option("-html/-no-html", "--save-html/--no-save-html", help="Whether to also save the output in HTML format, The [magenta]file name[/] is a slugified version of the text", default=False)
def cli(text, color, font, all_fonts, pager, direction, justify, width, save_html):
    if all_fonts:
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
            figlet_text = figlet_format(str(text), font)
            rich_text = Text()
            lines = figlet_text.splitlines()
            get_contrasting_color = lambda x: f"{Color(f'{rgb2hex(tuple(0 if c > 0.5 else 1 for c in x.rgb))}').hex_l}"
            try:
                gradient_colors = list(color1.range_to(color2, len(lines)))
            except ValueError:
                continue
            for c, l in zip(gradient_colors, lines):
                rich_text.append(l + "\n", style=c.hex_l)
            items.append(
                Panel(
                    rich_text,
                    box=ASCII if pager else ROUNDED,
                    title=font,
                    subtitle=f"[{get_contrasting_color(color1)} on {color1.hex_l}]{color1.hex_l}[/] -> [{get_contrasting_color(color2)}  on {color2.hex_l}]{color2.hex_l}[/]",
                )
            )
        print("\n")
        if pager:
            with console.pager():
                console.print(Columns(items))
        else:
            console.print(Columns(items))
        print("\n")
        if console.is_terminal and not pager:
            console.print(
                Markdown(
                    "**Note:** Consider piping the output to a file or using a pager (`--pager`) for a better viewing experience "
                )
            )
        exit(0)


    get_contrasting_color = lambda x: f"{Color(f'{rgb2hex(tuple(0 if c > 0.5 else 1 for c in x.rgb))}').hex_l}"


    colors = [Color(h) for h in color.split(",")]
    if len(colors) > 2:
        print("You may not use more than two colors")
        raise click.Abort()

    print_with_gradient_figlet(text, font=font, color1=colors[0], color2=colors[1], direction=direction, justify=justify, width=width, save_html=save_html)

    rich.print(f"Font Used: [green]{font}[/]")
    rich.print(f"Gradient Used: {' -> '.join(map(lambda x: f'[{get_contrasting_color(x)} on {x.hex_l}]{x.hex_l}[/]', colors))}")


if __name__ == '__main__':
    cli(obj={})