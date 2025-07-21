# Context for: textual

## Directory Structure

```textual/
├── docs
│   ├── css_types
│   │   └── _template.md
│   └── examples
│       ├── app
│       │   ├── question02.py
│       │   ├── question02.tcss
│       │   └── question03.py
│       ├── guide
│       │   └── css
│       │       ├── nesting02.py
│       │       └── nesting02.tcss
│       ├── styles
│       │   ├── background_transparency.py
│       │   ├── border_all.py
│       │   └── text_style_all.py
│       └── themes
│           └── todo_app.py
└── examples
    ├── calculator.py
    ├── calculator.tcss
    ├── code_browser.py
    ├── code_browser.tcss
    ├── dictionary.py
    ├── dictionary.tcss
    ├── five_by_five.py
    └── five_by_five.tcss
```
---

## File Contents

--- START OF FILE examples/calculator.py ---
"""
An implementation of a classic calculator, with a layout inspired by macOS calculator.

Works like a real calculator. Click the buttons or press the equivalent keys.
"""

from decimal import Decimal

from textual import events, on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.css.query import NoMatches
from textual.reactive import var
from textual.widgets import Button, Digits


class CalculatorApp(App):
    """A working 'desktop' calculator."""

    CSS_PATH = "calculator.tcss"

    numbers = var("0")
    show_ac = var(True)
    left = var(Decimal("0"))
    right = var(Decimal("0"))
    value = var("")
    operator = var("plus")

    # Maps button IDs on to the corresponding key name
    NAME_MAP = {
        "asterisk": "multiply",
        "slash": "divide",
        "underscore": "plus-minus",
        "full_stop": "point",
        "plus_minus_sign": "plus-minus",
        "percent_sign": "percent",
        "equals_sign": "equals",
        "minus": "minus",
        "plus": "plus",
    }

    def watch_numbers(self, value: str) -> None:
        """Called when numbers is updated."""
        self.query_one("#numbers", Digits).update(value)

    def compute_show_ac(self) -> bool:
        """Compute switch to show AC or C button"""
        return self.value in ("", "0") and self.numbers == "0"

    def watch_show_ac(self, show_ac: bool) -> None:
        """Called when show_ac changes."""
        self.query_one("#c").display = not show_ac
        self.query_one("#ac").display = show_ac

    def compose(self) -> ComposeResult:
        """Add our buttons."""
        with Container(id="calculator"):
            yield Digits(id="numbers")
            yield Button("AC", id="ac", variant="primary")
            yield Button("C", id="c", variant="primary")
            yield Button("+/-", id="plus-minus", variant="primary")
            yield Button("%", id="percent", variant="primary")
            yield Button("÷", id="divide", variant="warning")
            yield Button("7", id="number-7", classes="number")
            yield Button("8", id="number-8", classes="number")
            yield Button("9", id="number-9", classes="number")
            yield Button("×", id="multiply", variant="warning")
            yield Button("4", id="number-4", classes="number")
            yield Button("5", id="number-5", classes="number")
            yield Button("6", id="number-6", classes="number")
            yield Button("-", id="minus", variant="warning")
            yield Button("1", id="number-1", classes="number")
            yield Button("2", id="number-2", classes="number")
            yield Button("3", id="number-3", classes="number")
            yield Button("+", id="plus", variant="warning")
            yield Button("0", id="number-0", classes="number")
            yield Button(".", id="point")
            yield Button("=", id="equals", variant="warning")

    def on_key(self, event: events.Key) -> None:
        """Called when the user presses a key."""

        def press(button_id: str) -> None:
            """Press a button, should it exist."""
            try:
                self.query_one(f"#{button_id}", Button).press()
            except NoMatches:
                pass

        key = event.key
        if key.isdecimal():
            press(f"number-{key}")
        elif key == "c":
            press("c")
            press("ac")
        else:
            button_id = self.NAME_MAP.get(key)
            if button_id is not None:
                press(self.NAME_MAP.get(key, key))

    @on(Button.Pressed, ".number")
    def number_pressed(self, event: Button.Pressed) -> None:
        """Pressed a number."""
        assert event.button.id is not None
        number = event.button.id.partition("-")[-1]
        self.numbers = self.value = self.value.lstrip("0") + number

    @on(Button.Pressed, "#plus-minus")
    def plus_minus_pressed(self) -> None:
        """Pressed + / -"""
        self.numbers = self.value = str(Decimal(self.value or "0") * -1)

    @on(Button.Pressed, "#percent")
    def percent_pressed(self) -> None:
        """Pressed %"""
        self.numbers = self.value = str(Decimal(self.value or "0") / Decimal(100))

    @on(Button.Pressed, "#point")
    def pressed_point(self) -> None:
        """Pressed ."""
        if "." not in self.value:
            self.numbers = self.value = (self.value or "0") + "."

    @on(Button.Pressed, "#ac")
    def pressed_ac(self) -> None:
        """Pressed AC"""
        self.value = ""
        self.left = self.right = Decimal(0)
        self.operator = "plus"
        self.numbers = "0"

    @on(Button.Pressed, "#c")
    def pressed_c(self) -> None:
        """Pressed C"""
        self.value = ""
        self.numbers = "0"

    def _do_math(self) -> None:
        """Does the math: LEFT OPERATOR RIGHT"""
        try:
            if self.operator == "plus":
                self.left += self.right
            elif self.operator == "minus":
                self.left -= self.right
            elif self.operator == "divide":
                self.left /= self.right
            elif self.operator == "multiply":
                self.left *= self.right
            self.numbers = str(self.left)
            self.value = ""
        except Exception:
            self.numbers = "Error"

    @on(Button.Pressed, "#plus,#minus,#divide,#multiply")
    def pressed_op(self, event: Button.Pressed) -> None:
        """Pressed one of the arithmetic operations."""
        self.right = Decimal(self.value or "0")
        self._do_math()
        assert event.button.id is not None
        self.operator = event.button.id

    @on(Button.Pressed, "#equals")
    def pressed_equals(self) -> None:
        """Pressed ="""
        if self.value:
            self.right = Decimal(self.value)
        self._do_math()


if __name__ == "__main__":
    CalculatorApp().run(inline=True)
--- END OF FILE examples/calculator.py ---


--- START OF FILE examples/calculator.tcss ---
Screen {
    overflow: auto;
}

#calculator {
    layout: grid;
    grid-size: 4;
    grid-gutter: 1 2;
    grid-columns: 1fr;
    grid-rows: 2fr 1fr 1fr 1fr 1fr 1fr;
    margin: 1 2;
    min-height: 25;
    min-width: 26;
    height: 100%;

    &:inline {
        margin: 0 2;
    }
}

Button {
    width: 100%;
    height: 100%;
}

#numbers {
    column-span: 4;
    padding: 0 1;
    height: 100%;
    background: $panel;
    color: $text;
    content-align: center middle;
    text-align: right;
}

#number-0 {
    column-span: 2;
}
--- END OF FILE examples/calculator.tcss ---


--- START OF FILE examples/code_browser.py ---
"""
Code browser example.

Run with:

    python code_browser.py PATH
"""

from __future__ import annotations

import sys
from pathlib import Path

from rich.traceback import Traceback

from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.highlight import highlight
from textual.reactive import reactive, var
from textual.widgets import DirectoryTree, Footer, Header, Static


class CodeBrowser(App):
    """Textual code browser app."""

    CSS_PATH = "code_browser.tcss"
    BINDINGS = [
        ("f", "toggle_files", "Toggle Files"),
        ("q", "quit", "Quit"),
    ]

    show_tree = var(True)
    path: reactive[str | None] = reactive(None)

    def watch_show_tree(self, show_tree: bool) -> None:
        """Called when show_tree is modified."""
        self.set_class(show_tree, "-show-tree")

    def compose(self) -> ComposeResult:
        """Compose our UI."""
        path = "./" if len(sys.argv) < 2 else sys.argv[1]
        yield Header()
        with Container():
            yield DirectoryTree(path, id="tree-view")
            with VerticalScroll(id="code-view"):
                yield Static(id="code", expand=True)
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(DirectoryTree).focus()

        def theme_change(_signal) -> None:
            """Force the syntax to use a different theme."""
            self.watch_path(self.path)

        self.theme_changed_signal.subscribe(self, theme_change)

    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        """Called when the user click a file in the directory tree."""
        event.stop()
        self.path = str(event.path)

    def watch_path(self, path: str | None) -> None:
        """Called when path changes."""
        code_view = self.query_one("#code", Static)
        if path is None:
            code_view.update("")
            return
        try:
            code = Path(path).read_text(encoding="utf-8")
            syntax = highlight(code, path=path)
        except Exception:
            code_view.update(Traceback(theme="github-dark", width=None))
            self.sub_title = "ERROR"
        else:
            code_view.update(syntax)
            self.query_one("#code-view").scroll_home(animate=False)
            self.sub_title = path

    def action_toggle_files(self) -> None:
        """Called in response to key binding."""
        self.show_tree = not self.show_tree


if __name__ == "__main__":
    CodeBrowser().run()
--- END OF FILE examples/code_browser.py ---


--- START OF FILE examples/code_browser.tcss ---
Screen {
    &:inline {
        height: 50vh;
    }
}

#tree-view {
    display: none;
    scrollbar-gutter: stable;
    overflow: auto;
    width: auto;
    height: 100%;
    dock: left;
}

CodeBrowser.-show-tree #tree-view {
    display: block;
    max-width: 50%;
}


#code-view {
    overflow: auto scroll;
    min-width: 100%;
    hatch: right $panel;
}
#code {
    width: auto;
    padding: 0 1;
    background: $surface;
}
--- END OF FILE examples/code_browser.tcss ---


--- START OF FILE examples/dictionary.py ---
from __future__ import annotations

try:
    import httpx
except ImportError:
    raise ImportError("Please install httpx with 'pip install httpx' ")


from textual import getters, work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Markdown


class DictionaryApp(App):
    """Searches a dictionary API as-you-type."""

    CSS_PATH = "dictionary.tcss"

    results = getters.query_one("#results", Markdown)
    input = getters.query_one(Input)

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search for a word", id="dictionary-search")
        with VerticalScroll(id="results-container"):
            yield Markdown(id="results")

    async def on_input_changed(self, message: Input.Changed) -> None:
        """A coroutine to handle a text changed message."""
        if message.value:
            self.lookup_word(message.value)
        else:
            # Clear the results
            await self.results.update("")

    @work(exclusive=True)
    async def lookup_word(self, word: str) -> None:
        """Looks up a word."""
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            try:
                results = response.json()
            except Exception:
                self.results.update(response.text)
                return

        if word == self.input.value:
            markdown = self.make_word_markdown(results)
            self.results.update(markdown)

    def make_word_markdown(self, results: object) -> str:
        """Convert the results into markdown."""
        lines = []
        if isinstance(results, dict):
            lines.append(f"# {results['title']}")
            lines.append(results["message"])
        elif isinstance(results, list):
            for result in results:
                lines.append(f"# {result['word']}")
                lines.append("")
                for meaning in result.get("meanings", []):
                    lines.append(f"_{meaning['partOfSpeech']}_")
                    lines.append("")
                    for definition in meaning.get("definitions", []):
                        lines.append(f" - {definition['definition']}")
                    lines.append("---")

        return "\n".join(lines)


if __name__ == "__main__":
    app = DictionaryApp()
    app.run()
--- END OF FILE examples/dictionary.py ---


--- START OF FILE examples/dictionary.tcss ---
Screen {
    background: $panel;
}

Input#dictionary-search {
    dock: top;
    margin: 1 0;
}

#results {
    width: 100%;
    height: auto;
}

#results-container {
    background: $surface;
    margin: 0 0 1 0;
    height: 100%;
    overflow: hidden auto;
    border: tall transparent;
}

#results-container:focus {
    border: tall $border;
}
--- END OF FILE examples/dictionary.tcss ---


--- START OF FILE examples/five_by_five.py ---
"""Simple version of 5x5, developed for/with Textual."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, cast

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.css.query import DOMQuery
from textual.reactive import reactive
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Footer, Label, Markdown

if TYPE_CHECKING:
    from typing_extensions import Final


class Help(Screen):
    """The help screen for the application."""

    BINDINGS = [("escape,space,q,question_mark", "app.pop_screen", "Close")]
    """Bindings for the help screen."""

    def compose(self) -> ComposeResult:
        """Compose the game's help.

        Returns:
            ComposeResult: The result of composing the help screen.
        """
        yield Markdown(Path(__file__).with_suffix(".md").read_text())


class WinnerMessage(Label):
    """Widget to tell the user they have won."""

    MIN_MOVES: Final = 14
    """int: The minimum number of moves you can solve the puzzle in."""

    @staticmethod
    def _plural(value: int) -> str:
        return "" if value == 1 else "s"

    def show(self, moves: int) -> None:
        """Show the winner message.

        Args:
            moves (int): The number of moves required to win.
        """
        self.update(
            "W I N N E R !\n\n\n"
            f"You solved the puzzle in {moves} move{self._plural(moves)}."
            + (
                (
                    f" It is possible to solve the puzzle in {self.MIN_MOVES}, "
                    f"you were {moves - self.MIN_MOVES} move{self._plural(moves - self.MIN_MOVES)} over."
                )
                if moves > self.MIN_MOVES
                else " Well done! That's the minimum number of moves to solve the puzzle!"
            )
        )
        self.add_class("visible")

    def hide(self) -> None:
        """Hide the winner message."""
        self.remove_class("visible")


class GameHeader(Widget):
    """Header for the game.

    Comprises of the title (``#app-title``), the number of moves ``#moves``
    and the count of how many cells are turned on (``#progress``).
    """

    moves = reactive(0)
    """int: Keep track of how many moves the player has made."""

    filled = reactive(0)
    """int: Keep track of how many cells are filled."""

    def compose(self) -> ComposeResult:
        """Compose the game header.

        Returns:
            ComposeResult: The result of composing the game header.
        """
        with Horizontal():
            yield Label(self.app.title, id="app-title")
            yield Label(id="moves")
            yield Label(id="progress")

    def watch_moves(self, moves: int):
        """Watch the moves reactive and update when it changes.

        Args:
            moves (int): The number of moves made.
        """
        self.query_one("#moves", Label).update(f"Moves: {moves}")

    def watch_filled(self, filled: int):
        """Watch the on-count reactive and update when it changes.

        Args:
            filled (int): The number of cells that are currently on.
        """
        self.query_one("#progress", Label).update(f"Filled: {filled}")


class GameCell(Button):
    """Individual playable cell in the game."""

    @staticmethod
    def at(row: int, col: int) -> str:
        """Get the ID of the cell at the given location.

        Args:
            row (int): The row of the cell.
            col (int): The column of the cell.

        Returns:
            str: A string ID for the cell.
        """
        return f"cell-{row}-{col}"

    def __init__(self, row: int, col: int) -> None:
        """Initialise the game cell.

        Args:
            row (int): The row of the cell.
            col (int): The column of the cell.
        """
        super().__init__("", id=self.at(row, col))
        self.row = row
        self.col = col


class GameGrid(Widget):
    """The main playable grid of game cells."""

    def compose(self) -> ComposeResult:
        """Compose the game grid.

        Returns:
            ComposeResult: The result of composing the game grid.
        """
        for row in range(Game.SIZE):
            for col in range(Game.SIZE):
                yield GameCell(row, col)


class Game(Screen):
    """Main 5x5 game grid screen."""

    SIZE: Final = 5
    """The size of the game grid. Clue's in the name really."""

    BINDINGS = [
        Binding("n", "new_game", "New Game"),
        Binding("question_mark", "app.push_screen('help')", "Help", key_display="?"),
        Binding("q", "app.quit", "Quit"),
        Binding("up,w,k", "navigate(-1,0)", "Move Up", False),
        Binding("down,s,j", "navigate(1,0)", "Move Down", False),
        Binding("left,a,h", "navigate(0,-1)", "Move Left", False),
        Binding("right,d,l", "navigate(0,1)", "Move Right", False),
        Binding("space", "move", "Toggle", False),
    ]
    """The bindings for the main game grid."""

    @property
    def filled_cells(self) -> DOMQuery[GameCell]:
        """DOMQuery[GameCell]: The collection of cells that are currently turned on."""
        return cast(DOMQuery[GameCell], self.query("GameCell.filled"))

    @property
    def filled_count(self) -> int:
        """int: The number of cells that are currently filled."""
        return len(self.filled_cells)

    @property
    def all_filled(self) -> bool:
        """bool: Are all the cells filled?"""
        return self.filled_count == self.SIZE * self.SIZE

    def game_playable(self, playable: bool) -> None:
        """Mark the game as playable, or not.

        Args:
            playable (bool): Should the game currently be playable?
        """
        self.query_one(GameGrid).disabled = not playable

    def cell(self, row: int, col: int) -> GameCell:
        """Get the cell at a given location.

        Args:
            row (int): The row of the cell to get.
            col (int): The column of the cell to get.

        Returns:
            GameCell: The cell at that location.
        """
        return self.query_one(f"#{GameCell.at(row,col)}", GameCell)

    def compose(self) -> ComposeResult:
        """Compose the game screen.

        Returns:
            ComposeResult: The result of composing the game screen.
        """
        yield GameHeader()
        yield GameGrid()
        yield Footer()
        yield WinnerMessage()

    def toggle_cell(self, row: int, col: int) -> None:
        """Toggle an individual cell, but only if it's in bounds.

        If the row and column would place the cell out of bounds for the
        game grid, this function call is a no-op. That is, it's safe to call
        it with an invalid cell coordinate.

        Args:
            row (int): The row of the cell to toggle.
            col (int): The column of the cell to toggle.
        """
        if 0 <= row <= (self.SIZE - 1) and 0 <= col <= (self.SIZE - 1):
            self.cell(row, col).toggle_class("filled")

    _PATTERN: Final = (-1, 1, 0, 0, 0)

    def toggle_cells(self, cell: GameCell) -> None:
        """Toggle a 5x5 pattern around the given cell.

        Args:
            cell (GameCell): The cell to toggle the cells around.
        """
        for row, col in zip(self._PATTERN, reversed(self._PATTERN)):
            self.toggle_cell(cell.row + row, cell.col + col)
        self.query_one(GameHeader).filled = self.filled_count

    def make_move_on(self, cell: GameCell) -> None:
        """Make a move on the given cell.

        All relevant cells around the given cell are toggled as per the
        game's rules.

        Args:
            cell (GameCell): The cell to make a move on
        """
        self.toggle_cells(cell)
        self.query_one(GameHeader).moves += 1
        if self.all_filled:
            self.query_one(WinnerMessage).show(self.query_one(GameHeader).moves)
            self.game_playable(False)

    def on_button_pressed(self, event: GameCell.Pressed) -> None:
        """React to a press of a button on the game grid.

        Args:
            event (GameCell.Pressed): The event to react to.
        """
        self.make_move_on(cast(GameCell, event.button))

    def action_new_game(self) -> None:
        """Start a new game."""
        self.query_one(GameHeader).moves = 0
        self.filled_cells.remove_class("filled")
        self.query_one(WinnerMessage).hide()
        middle = self.cell(self.SIZE // 2, self.SIZE // 2)
        self.toggle_cells(middle)
        self.set_focus(middle)
        self.game_playable(True)

    def action_navigate(self, row: int, col: int) -> None:
        """Navigate to a new cell by the given offsets.

        Args:
            row (int): The row of the cell to navigate to.
            col (int): The column of the cell to navigate to.
        """
        if isinstance(self.focused, GameCell):
            self.set_focus(
                self.cell(
                    (self.focused.row + row) % self.SIZE,
                    (self.focused.col + col) % self.SIZE,
                )
            )

    def action_move(self) -> None:
        """Make a move on the current cell."""
        if isinstance(self.focused, GameCell):
            self.focused.press()

    def on_mount(self) -> None:
        """Get the game started when we first mount."""
        self.action_new_game()


class FiveByFive(App[None]):
    """Main 5x5 application class."""

    CSS_PATH = "five_by_five.tcss"
    """The name of the stylesheet for the app."""

    SCREENS = {"help": Help}
    """The pre-loaded screens for the application."""

    BINDINGS = [("ctrl+d", "toggle_dark", "Toggle Dark Mode")]
    """App-level bindings."""

    TITLE = "5x5 -- A little annoying puzzle"
    """The title of the application."""

    def on_mount(self) -> None:
        """Set up the application on startup."""
        self.push_screen(Game())


if __name__ == "__main__":
    FiveByFive().run()
--- END OF FILE examples/five_by_five.py ---


--- START OF FILE examples/five_by_five.tcss ---
$animation-type: linear;
$animation-speed: 175ms;

Game {
    align: center middle;
    layers: gameplay messages;
}

GameGrid {
    layout: grid;
    grid-size: 5 5;
    layer: gameplay;
}

GameHeader {
    background: $primary-background;
    color: $text;
    height: 1;
    dock: top;
    layer: gameplay;
}

GameHeader #app-title {
    width: 60%;
}

GameHeader #moves {
    width: 20%;
}

GameHeader #progress {
    width: 20%;
}

Footer {
    height: 1;
    dock: bottom;
    layer: gameplay;
}

GameCell {
    width: 100%;
    height: 100%;
    background: $surface;
    border: round $surface-darken-1;
    transition: background $animation-speed $animation-type, color $animation-speed $animation-type;
}

GameCell:hover {
    background: $panel-lighten-1;
    border: round $panel;
}

GameCell.filled {
    background: $secondary;
    border: round $secondary-darken-1;
}

GameCell.filled:hover {
    background: $secondary-lighten-1;
    border: round $secondary;
}

WinnerMessage {
    width: 50%;
    height: 25%;
    layer: messages;
    visibility: hidden;
    content-align: center middle;
    text-align: center;
    background: $success;
    color: $text;
    border: round;
    padding: 2;
}

.visible {
    visibility: visible;
}

Help {
    border: round $primary-lighten-3;
}

/* five_by_five.tcss ends here */
--- END OF FILE examples/five_by_five.tcss ---


--- START OF FILE docs/css_types/_template.md ---
<!-- Template file for a Textual CSS type reference page. -->

# &lt;type-name&gt;

<!-- Short description of the type. -->

## Syntax


<!--
For a simple type like <integer>:

Describe the type in a short paragraph with an absolute link to the type page.
E.g., “The [`<my-type>`](/css_types/my_type) type is such and such with sprinkles on top.”
-->

<!--
For a type with many different values like <color>:

Introduce the type with a link to [`<my-type>`](/css_types/my_type).
Then, a bullet list with the variants accepted:

 - you can create this type with X Y Z;
 - you can also do A B C; and
 - also use D E F.
-->

<!--
For a type that accepts specific options like <border>:

Add a sentence and a table. Consider ordering values in alphabetical order if there is no other obvious ordering. See below:

The [`<my-type>`](/css_types/my_type) type can take any of the following values:

| Value         | Description                                   |
|---------------|-----------------------------------------------|
| `abc`         | Describe here.                                |
| `other val`   | Describe this one also.                       |
| `value three` | Please use full stops.                        |
| `zyx`         | Describe the value without assuming any rule. |
-->


## Examples

### CSS

<!--
Include a good variety of examples.
If the type has many different syntaxes, cover all of them.
Add comments when needed/if helpful.
-->

```css
.some-class {
    rule: type-value-1;
    rule: type-value-2;
    rule: type-value-3;
}
```

### Python

<!-- Same examples as above. -->

```py
widget.styles.rule = type_value_1
widget.styles.rule = type_value_2
widget.styles.rule = type_value_3
```
--- END OF FILE docs/css_types/_template.md ---


--- START OF FILE docs/examples/app/question02.py ---
from textual.app import App, ComposeResult
from textual.widgets import Button, Label


class QuestionApp(App[str]):
    CSS_PATH = "question02.tcss"

    def compose(self) -> ComposeResult:
        yield Label("Do you love Textual?", id="question")
        yield Button("Yes", id="yes", variant="primary")
        yield Button("No", id="no", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button.id)


if __name__ == "__main__":
    app = QuestionApp()
    reply = app.run()
    print(reply)
--- END OF FILE docs/examples/app/question02.py ---


--- START OF FILE docs/examples/app/question02.tcss ---
Screen {
    layout: grid;
    grid-size: 2;
    grid-gutter: 2;
    padding: 2;
}
#question {
    width: 100%;
    height: 100%;
    column-span: 2;
    content-align: center bottom;
    text-style: bold;
}

Button {
    width: 100%;
}
--- END OF FILE docs/examples/app/question02.tcss ---


--- START OF FILE docs/examples/app/question03.py ---
from textual.app import App, ComposeResult
from textual.widgets import Label, Button


class QuestionApp(App[str]):
    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-gutter: 2;
        padding: 2;
    }
    #question {
        width: 100%;
        height: 100%;
        column-span: 2;
        content-align: center bottom;
        text-style: bold;
    }

    Button {
        width: 100%;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("Do you love Textual?", id="question")
        yield Button("Yes", id="yes", variant="primary")
        yield Button("No", id="no", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button.id)


if __name__ == "__main__":
    app = QuestionApp()
    reply = app.run()
    print(reply)
--- END OF FILE docs/examples/app/question03.py ---


--- START OF FILE docs/examples/styles/background_transparency.py ---
from textual.app import App, ComposeResult
from textual.widgets import Static


class BackgroundTransparencyApp(App):
    """Simple app to exemplify different transparency settings."""

    CSS_PATH = "background_transparency.tcss"

    def compose(self) -> ComposeResult:
        yield Static("10%", id="t10")
        yield Static("20%", id="t20")
        yield Static("30%", id="t30")
        yield Static("40%", id="t40")
        yield Static("50%", id="t50")
        yield Static("60%", id="t60")
        yield Static("70%", id="t70")
        yield Static("80%", id="t80")
        yield Static("90%", id="t90")
        yield Static("100%", id="t100")


if __name__ == "__main__":
    app = BackgroundTransparencyApp()
    app.run()
--- END OF FILE docs/examples/styles/background_transparency.py ---


--- START OF FILE docs/examples/styles/border_all.py ---
from textual.app import App
from textual.containers import Grid
from textual.widgets import Label


class AllBordersApp(App):
    CSS_PATH = "border_all.tcss"

    def compose(self):
        yield Grid(
            Label("ascii", id="ascii"),
            Label("blank", id="blank"),
            Label("dashed", id="dashed"),
            Label("double", id="double"),
            Label("heavy", id="heavy"),
            Label("hidden/none", id="hidden"),
            Label("hkey", id="hkey"),
            Label("inner", id="inner"),
            Label("outer", id="outer"),
            Label("panel", id="panel"),
            Label("round", id="round"),
            Label("solid", id="solid"),
            Label("tall", id="tall"),
            Label("thick", id="thick"),
            Label("vkey", id="vkey"),
            Label("wide", id="wide"),
        )


if __name__ == "__main__":
    app = AllBordersApp()
    app.run()
--- END OF FILE docs/examples/styles/border_all.py ---


--- START OF FILE docs/examples/styles/text_style_all.py ---
from textual.app import App
from textual.containers import Grid
from textual.widgets import Label

TEXT = """I must not fear.
Fear is the mind-killer.
Fear is the little-death that brings total obliteration.
I will face my fear.
I will permit it to pass over me and through me.
And when it has gone past, I will turn the inner eye to see its path.
Where the fear has gone there will be nothing. Only I will remain."""


class AllTextStyleApp(App):
    CSS_PATH = "text_style_all.tcss"

    def compose(self):
        yield Grid(
            Label("none\n" + TEXT, id="lbl1"),
            Label("bold\n" + TEXT, id="lbl2"),
            Label("italic\n" + TEXT, id="lbl3"),
            Label("reverse\n" + TEXT, id="lbl4"),
            Label("strike\n" + TEXT, id="lbl5"),
            Label("underline\n" + TEXT, id="lbl6"),
            Label("bold italic\n" + TEXT, id="lbl7"),
            Label("reverse strike\n" + TEXT, id="lbl8"),
        )


if __name__ == "__main__":
    app = AllTextStyleApp()
    app.run()
--- END OF FILE docs/examples/styles/text_style_all.py ---


--- START OF FILE docs/examples/themes/todo_app.py ---
from itertools import cycle

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Input, Label, SelectionList


class TodoList(App[None]):
    CSS = """
Screen {
    align: center middle;
    hatch: right $foreground 10%;
}
#content {
    height: auto;
    width: 40;
    padding: 1 2;
}
#header {
    height: 1;
    width: auto;
    margin-bottom: 1;
}
.title {
    text-style: bold;
    padding: 0 1;
    width: 1fr;
}
#overdue {
    color: $text-error;
    background: $error-muted;
    padding: 0 1;
    width: auto;
}
#done {
    color: $text-success;
    background: $success-muted;
    padding: 0 1;
    margin: 0 1;
}
#footer {
    height: auto;
    margin-bottom: 2;
}
#history-header {
    height: 1;
    width: auto;
}
#history-done {
    width: auto;
    padding: 0 1;
    margin: 0 1;
    background: $primary-muted;
    color: $text-primary;
}
"""

    BINDINGS = [Binding("ctrl+t", "cycle_theme", "Cycle theme")]
    THEMES = cycle(
        ["nord", "gruvbox", "tokyo-night", "textual-dark", "solarized-light"]
    )

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="content"):
            with Horizontal(id="header"):
                yield Label("Today", classes="title")
                yield Label("1 overdue", id="overdue")
                yield Label("1 done", id="done")
            yield SelectionList(
                ("Buy milk", 0),
                ("Buy bread", 1),
                ("Go and vote", 2, True),
                ("Return package", 3),
                id="todo-list",
            )
            with Horizontal(id="footer"):
                yield Input(placeholder="Add a task")

            with Horizontal(id="history-header"):
                yield Label("History", classes="title")
                yield Label("4 items", id="history-done")

        yield Footer()

    def on_mount(self) -> None:
        self.action_cycle_theme()

    def action_cycle_theme(self) -> None:
        self.theme = next(self.THEMES)


app = TodoList()
if __name__ == "__main__":
    app.run()
--- END OF FILE docs/examples/themes/todo_app.py ---


--- START OF FILE docs/examples/guide/css/nesting02.py ---
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static


class NestingDemo(App):
    """App with nested CSS."""

    CSS_PATH = "nesting02.tcss"

    def compose(self) -> ComposeResult:
        with Horizontal(id="questions"):
            yield Static("Yes", classes="button affirmative")
            yield Static("No", classes="button negative")


if __name__ == "__main__":
    app = NestingDemo()
    app.run()
--- END OF FILE docs/examples/guide/css/nesting02.py ---


--- START OF FILE docs/examples/guide/css/nesting02.tcss ---
/* Style the container */
#questions {
    border: heavy $primary;
    align: center middle;

    /* Style all buttons */
    .button {
        width: 1fr;
        padding: 1 2;
        margin: 1 2;
        text-align: center;
        border: heavy $panel;

        /* Style the Yes button */
        &.affirmative {
            border: heavy $success;
        }

        /* Style the No button */
        &.negative {
            border: heavy $error;
        }
    }
}
--- END OF FILE docs/examples/guide/css/nesting02.tcss ---


