# Context for: textual

## Directory Structure

```textual/
└── docs
    └── examples
        ├── events
        │   ├── custom01.py
        │   ├── dictionary.py
        │   ├── on_decorator02.py
        │   └── prevent.py
        └── guide
            └── reactivity
                ├── computed01.py
                ├── refresh01.py
                ├── refresh02.py
                ├── validate01.py
                └── watch01.py
```
---

## File Contents

--- START OF FILE docs/examples/events/custom01.py ---
from textual.app import App, ComposeResult
from textual.color import Color
from textual.message import Message
from textual.widgets import Static


class ColorButton(Static):
    """A color button."""

    class Selected(Message):
        """Color selected message."""

        def __init__(self, color: Color) -> None:
            self.color = color
            super().__init__()

    def __init__(self, color: Color) -> None:
        self.color = color
        super().__init__()

    def on_mount(self) -> None:
        self.styles.margin = (1, 2)
        self.styles.content_align = ("center", "middle")
        self.styles.background = Color.parse("#ffffff33")
        self.styles.border = ("tall", self.color)

    def on_click(self) -> None:
        # The post_message method sends an event to be handled in the DOM
        self.post_message(self.Selected(self.color))

    def render(self) -> str:
        return str(self.color)


class ColorApp(App):
    def compose(self) -> ComposeResult:
        yield ColorButton(Color.parse("#008080"))
        yield ColorButton(Color.parse("#808000"))
        yield ColorButton(Color.parse("#E9967A"))
        yield ColorButton(Color.parse("#121212"))

    def on_color_button_selected(self, message: ColorButton.Selected) -> None:
        self.screen.styles.animate("background", message.color, duration=0.5)


if __name__ == "__main__":
    app = ColorApp()
    app.run()
--- END OF FILE docs/examples/events/custom01.py ---


--- START OF FILE docs/examples/events/dictionary.py ---
import asyncio

try:
    import httpx
except ImportError:
    raise ImportError("Please install httpx with 'pip install httpx' ")

from rich.json import JSON

from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Static


class DictionaryApp(App):
    """Searches a dictionary API as-you-type."""

    CSS_PATH = "dictionary.tcss"

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search for a word")
        yield VerticalScroll(Static(id="results"), id="results-container")

    async def on_input_changed(self, message: Input.Changed) -> None:
        """A coroutine to handle a text changed message."""
        if message.value:
            # Look up the word in the background
            asyncio.create_task(self.lookup_word(message.value))
        else:
            # Clear the results
            self.query_one("#results", Static).update()

    async def lookup_word(self, word: str) -> None:
        """Looks up a word."""
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        async with httpx.AsyncClient() as client:
            results = (await client.get(url)).text

        if word == self.query_one(Input).value:
            self.query_one("#results", Static).update(JSON(results))


if __name__ == "__main__":
    app = DictionaryApp()
    app.run()
--- END OF FILE docs/examples/events/dictionary.py ---


--- START OF FILE docs/examples/events/on_decorator02.py ---
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button


class OnDecoratorApp(App):
    CSS_PATH = "on_decorator.tcss"

    def compose(self) -> ComposeResult:
        """Three buttons."""
        yield Button("Bell", id="bell")
        yield Button("Toggle dark", classes="toggle dark")
        yield Button("Quit", id="quit")

    @on(Button.Pressed, "#bell")  # (1)!
    def play_bell(self):
        """Called when the bell button is pressed."""
        self.bell()

    @on(Button.Pressed, ".toggle.dark")  # (2)!
    def toggle_dark(self):
        """Called when the 'toggle dark' button is pressed."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    @on(Button.Pressed, "#quit")  # (3)!
    def quit(self):
        """Called when the quit button is pressed."""
        self.exit()


if __name__ == "__main__":
    app = OnDecoratorApp()
    app.run()
--- END OF FILE docs/examples/events/on_decorator02.py ---


--- START OF FILE docs/examples/events/prevent.py ---
from textual.app import App, ComposeResult
from textual.widgets import Button, Input


class PreventApp(App):
    """Demonstrates `prevent` context manager."""

    def compose(self) -> ComposeResult:
        yield Input()
        yield Button("Clear", id="clear")

    def on_button_pressed(self) -> None:
        """Clear the text input."""
        input = self.query_one(Input)
        with input.prevent(Input.Changed):  # (1)!
            input.value = ""

    def on_input_changed(self) -> None:
        """Called as the user types."""
        self.bell()  # (2)!


if __name__ == "__main__":
    app = PreventApp()
    app.run()
--- END OF FILE docs/examples/events/prevent.py ---


--- START OF FILE docs/examples/guide/reactivity/computed01.py ---
from textual.app import App, ComposeResult
from textual.color import Color
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import Input, Static


class ComputedApp(App):
    CSS_PATH = "computed01.tcss"

    red = reactive(0)
    green = reactive(0)
    blue = reactive(0)
    color = reactive(Color.parse("transparent"))

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Input("0", placeholder="Enter red 0-255", id="red"),
            Input("0", placeholder="Enter green 0-255", id="green"),
            Input("0", placeholder="Enter blue 0-255", id="blue"),
            id="color-inputs",
        )
        yield Static(id="color")

    def compute_color(self) -> Color:  # (1)!
        return Color(self.red, self.green, self.blue).clamped

    def watch_color(self, color: Color) -> None:  # (2)
        self.query_one("#color").styles.background = color

    def on_input_changed(self, event: Input.Changed) -> None:
        try:
            component = int(event.value)
        except ValueError:
            self.bell()
        else:
            if event.input.id == "red":
                self.red = component
            elif event.input.id == "green":
                self.green = component
            else:
                self.blue = component


if __name__ == "__main__":
    app = ComputedApp()
    app.run()
--- END OF FILE docs/examples/guide/reactivity/computed01.py ---


--- START OF FILE docs/examples/guide/reactivity/refresh01.py ---
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input


class Name(Widget):
    """Generates a greeting."""

    who = reactive("name")

    def render(self) -> str:
        return f"Hello, {self.who}!"


class WatchApp(App):
    CSS_PATH = "refresh01.tcss"

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter your name")
        yield Name()

    def on_input_changed(self, event: Input.Changed) -> None:
        self.query_one(Name).who = event.value


if __name__ == "__main__":
    app = WatchApp()
    app.run()
--- END OF FILE docs/examples/guide/reactivity/refresh01.py ---


--- START OF FILE docs/examples/guide/reactivity/refresh02.py ---
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input


class Name(Widget):
    """Generates a greeting."""

    who = reactive("name", layout=True)  # (1)!

    def render(self) -> str:
        return f"Hello, {self.who}!"


class WatchApp(App):
    CSS_PATH = "refresh02.tcss"

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter your name")
        yield Name()

    def on_input_changed(self, event: Input.Changed) -> None:
        self.query_one(Name).who = event.value


if __name__ == "__main__":
    app = WatchApp()
    app.run()
--- END OF FILE docs/examples/guide/reactivity/refresh02.py ---


--- START OF FILE docs/examples/guide/reactivity/validate01.py ---
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import Button, RichLog


class ValidateApp(App):
    CSS_PATH = "validate01.tcss"

    count = reactive(0)

    def validate_count(self, count: int) -> int:
        """Validate value."""
        if count < 0:
            count = 0
        elif count > 10:
            count = 10
        return count

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Button("+1", id="plus", variant="success"),
            Button("-1", id="minus", variant="error"),
            id="buttons",
        )
        yield RichLog(highlight=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "plus":
            self.count += 1
        else:
            self.count -= 1
        self.query_one(RichLog).write(f"count = {self.count}")


if __name__ == "__main__":
    app = ValidateApp()
    app.run()
--- END OF FILE docs/examples/guide/reactivity/validate01.py ---


--- START OF FILE docs/examples/guide/reactivity/watch01.py ---
from textual.app import App, ComposeResult
from textual.color import Color, ColorParseError
from textual.containers import Grid
from textual.reactive import reactive
from textual.widgets import Input, Static


class WatchApp(App):
    CSS_PATH = "watch01.tcss"

    color = reactive(Color.parse("transparent"))  # (1)!

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter a color")
        yield Grid(Static(id="old"), Static(id="new"), id="colors")

    def watch_color(self, old_color: Color, new_color: Color) -> None:  # (2)!
        self.query_one("#old").styles.background = old_color
        self.query_one("#new").styles.background = new_color

    def on_input_submitted(self, event: Input.Submitted) -> None:
        try:
            input_color = Color.parse(event.value)
        except ColorParseError:
            pass
        else:
            self.query_one(Input).value = ""
            self.color = input_color  # (3)!


if __name__ == "__main__":
    app = WatchApp()
    app.run()
--- END OF FILE docs/examples/guide/reactivity/watch01.py ---


