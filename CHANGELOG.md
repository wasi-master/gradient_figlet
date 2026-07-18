# Changelog

## Version 0.1.0

- Initial Release

## Version 0.2.0

- Bug fixes and stability improvements

## Version 0.2.1

- Fix screenshot links

## Version 0.3.0

- Add new `direction` parameter
- Add new `justify` parameter
- Add new `width` parameter
- Make the figlet text be printed according to the terminal width instead of a constant width

## version 0.4.0

- Fix bugs with the 3 parameters added in 0.3.0
- Add a `html` parameter

## Version 0.4.1

- Fix the html parameter being true by default

## Version 0.4.2

- Add a banner

## Version 0.4.3

- Switch to click and use rich-click

## Version 0.4.4

- Use custom formatting with rich-click
- Fix the all-fonts parameter not working
- Make all-fonts show contrasting colors for hex codes

## Version 0.5.0

- Make it easier to use the library directly in a script

## Version 0.6.0

- Fix the `--all-fonts` flag crashing due to missing imports
- Fix passing a single color crashing, it now auto-generates a matching second shade
- Fix `--direction` and `--justify` defaulting to `None` instead of `auto`
- Add the missing `pyfiglet` dependency to the package metadata
- Add a `gradient-figlet` console command (no more need for `python -m`)
- Add `make_gradient`, `make_gradient_figlet` and `interpolate_colors` to the library API
- Support gradients with more than two colors (multi-stop gradients)
- Add a `--gradient`/`-g` option to use a built-in named gradient
- Add `--list-gradients` and `--list-fonts` options
- Add tests and a demo script
- Document all CLI options and the library API in the README
