# Context for: textual

## Directory Structure

```textual/
└── docs
    └── examples
        ├── guide
        │   └── input
        │       ├── binding01.py
        │       ├── key01.py
        │       └── mouse01.py
        └── widgets
            ├── input_validation.py
            └── masked_input.py
```
---

## File Contents

--- START OF FILE docs/examples/widgets/input_validation.py ---
from textual import on
from textual.app import App, ComposeResult
from textual.validation import Function, Number, ValidationResult, Validator
from textual.widgets import Input, Label, Pretty


class InputApp(App):
    # (6)!
    CSS = """
    Input.-valid {
        border: tall $success 60%;
    }
    Input.-valid:focus {
        border: tall $success;
    }
    Input {
        margin: 1 1;
    }
    Label {
        margin: 1 2;
    }
    Pretty {
        margin: 1 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("Enter an even number between 1 and 100 that is also a palindrome.")
        yield Input(
            placeholder="Enter a number...",
            validators=[
                Number(minimum=1, maximum=100),  # (1)!
                Function(is_even, "Value is not even."),  # (2)!
                Palindrome(),  # (3)!
            ],
        )
        yield Pretty([])

    @on(Input.Changed)
    def show_invalid_reasons(self, event: Input.Changed) -> None:
        # Updating the UI to show the reasons why validation failed
        if not event.validation_result.is_valid:  # (4)!
            self.query_one(Pretty).update(event.validation_result.failure_descriptions)
        else:
            self.query_one(Pretty).update([])


def is_even(value: str) -> bool:
    try:
        return int(value) % 2 == 0
    except ValueError:
        return False


# A custom validator
class Palindrome(Validator):  # (5)!
    def validate(self, value: str) -> ValidationResult:
        """Check a string is equal to its reverse."""
        if self.is_palindrome(value):
            return self.success()
        else:
            return self.failure("That's not a palindrome :/")

    @staticmethod
    def is_palindrome(value: str) -> bool:
        return value == value[::-1]


app = InputApp()

if __name__ == "__main__":
    app.run()
--- END OF FILE docs/examples/widgets/input_validation.py ---


--- START OF FILE docs/examples/widgets/masked_input.py ---
from textual.app import App, ComposeResult
from textual.widgets import Label, MaskedInput


class MaskedInputApp(App):
    # (1)!
    CSS = """
    MaskedInput.-valid {
        border: tall $success 60%;
    }
    MaskedInput.-valid:focus {
        border: tall $success;
    }
    MaskedInput {
        margin: 1 1;
    }
    Label {
        margin: 1 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("Enter a valid credit card number.")
        yield MaskedInput(
            template="9999-9999-9999-9999;0",  # (2)!
        )


app = MaskedInputApp()

if __name__ == "__main__":
    app.run()
--- END OF FILE docs/examples/widgets/masked_input.py ---


--- START OF FILE docs/examples/guide/input/binding01.py ---
from textual.app import App, ComposeResult
from textual.color import Color
from textual.widgets import Footer, Static


class Bar(Static):
    pass


class BindingApp(App):
    CSS_PATH = "binding01.tcss"
    BINDINGS = [
        ("r", "add_bar('red')", "Add Red"),
        ("g", "add_bar('green')", "Add Green"),
        ("b", "add_bar('blue')", "Add Blue"),
    ]

    def compose(self) -> ComposeResult:
        yield Footer()

    def action_add_bar(self, color: str) -> None:
        bar = Bar(color)
        bar.styles.background = Color.parse(color).with_alpha(0.5)
        self.mount(bar)
        self.call_after_refresh(self.screen.scroll_end, animate=False)


if __name__ == "__main__":
    app = BindingApp()
    app.run()
--- END OF FILE docs/examples/guide/input/binding01.py ---


--- START OF FILE docs/examples/guide/input/key01.py ---
from textual import events
from textual.app import App, ComposeResult
from textual.widgets import RichLog


class InputApp(App):
    """App to display key events."""

    def compose(self) -> ComposeResult:
        yield RichLog()

    def on_key(self, event: events.Key) -> None:
        self.query_one(RichLog).write(event)


if __name__ == "__main__":
    app = InputApp()
    app.run()
--- END OF FILE docs/examples/guide/input/key01.py ---


--- START OF FILE docs/examples/guide/input/mouse01.py ---
from textual import events
from textual.app import App, ComposeResult
from textual.widgets import RichLog, Static


class Ball(Static):
    pass


class MouseApp(App):
    CSS_PATH = "mouse01.tcss"

    def compose(self) -> ComposeResult:
        yield RichLog()
        yield Ball("Textual")

    def on_mouse_move(self, event: events.MouseMove) -> None:
        self.screen.query_one(RichLog).write(event)
        self.query_one(Ball).offset = event.screen_offset - (8, 2)


if __name__ == "__main__":
    app = MouseApp()
    app.run()
--- END OF FILE docs/examples/guide/input/mouse01.py ---


