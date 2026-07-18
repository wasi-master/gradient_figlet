"""Tests for the gradient_figlet library and CLI."""
import pytest
from click.testing import CliRunner
from colour import Color

from gradient_figlet import (
    interpolate_colors,
    make_gradient,
    make_gradient_figlet,
    slugify,
)
from gradient_figlet.__main__ import cli, complementary_shade
from gradient_figlet.pleasing_items import good_gradients, good_fonts


class TestInterpolateColors:
    def test_two_stops(self):
        gradient = interpolate_colors(["red", "blue"], 3)
        assert [c.hex_l for c in gradient] == ["#ff0000", "#00ff00", "#0000ff"]

    def test_endpoints_are_exact(self):
        gradient = interpolate_colors(["#ff512f", "#dd2476"], 10)
        assert gradient[0].hex_l == "#ff512f"
        assert gradient[-1].hex_l == "#dd2476"

    def test_multiple_stops(self):
        gradient = interpolate_colors(["red", "lime", "blue"], 5)
        assert gradient[0].hex_l == "#ff0000"
        assert gradient[2].hex_l == "#00ff00"
        assert gradient[-1].hex_l == "#0000ff"

    def test_single_color(self):
        gradient = interpolate_colors(["red"], 4)
        assert len(gradient) == 4
        assert all(c.hex_l == "#ff0000" for c in gradient)

    def test_zero_steps(self):
        assert interpolate_colors(["red", "blue"], 0) == []

    def test_one_step(self):
        gradient = interpolate_colors(["red", "blue"], 1)
        assert [c.hex_l for c in gradient] == ["#ff0000"]

    def test_no_colors(self):
        assert interpolate_colors([], 5) == []

    def test_accepts_color_objects(self):
        gradient = interpolate_colors([Color("red"), Color("blue")], 2)
        assert [c.hex_l for c in gradient] == ["#ff0000", "#0000ff"]

    def test_correct_number_of_steps(self):
        for steps in (1, 2, 3, 7, 100):
            assert len(interpolate_colors(["red", "blue"], steps)) == steps


class TestMakeGradient:
    def test_preserves_text(self):
        text = make_gradient("hello\nworld", "red", "blue")
        assert text.plain == "hello\nworld\n"

    def test_empty_text(self):
        assert make_gradient("", "red", "blue").plain == ""

    def test_single_line(self):
        assert make_gradient("hello", "red", "blue").plain == "hello\n"


class TestMakeGradientFiglet:
    def test_renders_figlet(self):
        text = make_gradient_figlet("Hi", "red", "blue", font="standard", width=80)
        assert text.plain.strip() != ""
        assert "\n" in text.plain

    def test_unknown_font_raises(self):
        with pytest.raises(Exception):
            make_gradient_figlet("Hi", "red", "blue", font="not-a-real-font")


class TestComplementaryShade:
    def test_dark_color_gets_lighter(self):
        shade = complementary_shade(Color("#200000"))
        assert shade.get_luminance() > Color("#200000").get_luminance()

    def test_light_color_gets_darker(self):
        shade = complementary_shade(Color("#ffeeee"))
        assert shade.get_luminance() < Color("#ffeeee").get_luminance()


class TestSlugify:
    def test_basic(self):
        assert slugify("Hello World") == "hello-world"

    def test_special_characters(self):
        assert slugify("Hello, World!") == "hello-world"


class TestCli:
    def setup_method(self):
        self.runner = CliRunner()

    def test_basic(self):
        result = self.runner.invoke(cli, ["Hi"])
        assert result.exit_code == 0
        assert "Font Used" in result.output

    def test_single_color(self):
        result = self.runner.invoke(cli, ["Hi", "-c", "red"])
        assert result.exit_code == 0

    def test_three_colors(self):
        result = self.runner.invoke(cli, ["Hi", "-c", "red,yellow,blue"])
        assert result.exit_code == 0

    def test_named_gradient(self):
        result = self.runner.invoke(cli, ["Hi", "-g", "Cherry"])
        assert result.exit_code == 0
        assert "Cherry" in result.output

    def test_named_gradient_is_case_insensitive(self):
        result = self.runner.invoke(cli, ["Hi", "-g", "cherry"])
        assert result.exit_code == 0

    def test_unknown_gradient(self):
        result = self.runner.invoke(cli, ["Hi", "-g", "does-not-exist"])
        assert result.exit_code != 0
        assert "Unknown gradient" in result.output

    def test_invalid_color(self):
        result = self.runner.invoke(cli, ["Hi", "-c", "not-a-color"])
        assert result.exit_code != 0

    def test_color_and_gradient_conflict(self):
        result = self.runner.invoke(cli, ["Hi", "-c", "red", "-g", "Cherry"])
        assert result.exit_code != 0

    def test_list_gradients(self):
        result = self.runner.invoke(cli, ["x", "--list-gradients"])
        assert result.exit_code == 0
        for name in good_gradients:
            assert name in result.output

    def test_list_fonts(self):
        result = self.runner.invoke(cli, ["x", "--list-fonts"])
        assert result.exit_code == 0
        for font in good_fonts:
            assert font in result.output

    def test_justify_and_direction(self):
        result = self.runner.invoke(cli, ["Hi", "-j", "center", "-d", "left-to-right"])
        assert result.exit_code == 0

    def test_save_html(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        result = self.runner.invoke(cli, ["Hello World", "-html"])
        assert result.exit_code == 0
        assert (tmp_path / "hello-world.html").exists()
