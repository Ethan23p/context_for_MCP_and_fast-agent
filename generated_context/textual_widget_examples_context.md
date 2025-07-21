# Context for: textual

## Directory Structure

```textual/
└── docs
    └── examples
        └── widgets
            ├── button.py
            ├── checkbox.py
            ├── collapsible.py
            ├── data_table.py
            ├── data_table_sort.py
            ├── digits.py
            ├── directory_tree.py
            ├── input.py
            ├── link.py
            ├── list_view.py
            ├── loading_indicator.py
            ├── log.py
            ├── markdown.py
            ├── markdown_viewer.py
            ├── option_list_options.py
            ├── placeholder.py
            ├── pretty.py
            ├── progress_bar.py
            ├── rich_log.py
            ├── select_widget.py
            ├── selection_list_selections.py
            ├── sparkline.py
            ├── switch.py
            ├── tabbed_content.py
            ├── tabs.py
            ├── text_area_custom_language.py
            ├── text_area_example.py
            ├── toast.py
            └── tree.py
```
---

## File Contents

--- START OF FILE docs/examples/widgets/button.py ---
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, Static


class ButtonsApp(App[str]):
    CSS_PATH = "button.tcss"

    def compose(self) -> ComposeResult:
        yield Horizontal(
            VerticalScroll(
                Static("Standard Buttons", classes="header"),
                Button("Default"),
                Button("Primary!", variant="primary"),
                Button.success("Success!"),
                Button.warning("Warning!"),
                Button.error("Error!"),
            ),
            VerticalScroll(
                Static("Disabled Buttons", classes="header"),
                Button("Default", disabled=True),
                Button("Primary!", variant="primary", disabled=True),
                Button.success("Success!", disabled=True),
                Button.warning("Warning!", disabled=True),
                Button.error("Error!", disabled=True),
            ),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(str(event.button))


if __name__ == "__main__":
    app = ButtonsApp()
    print(app.run())
--- END OF FILE docs/examples/widgets/button.py ---


--- START OF FILE docs/examples/widgets/checkbox.py ---
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Checkbox


class CheckboxApp(App[None]):
    CSS_PATH = "checkbox.tcss"

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Checkbox("Arrakis :sweat:")
            yield Checkbox("Caladan")
            yield Checkbox("Chusuk")
            yield Checkbox("[b]Giedi Prime[/b]")
            yield Checkbox("[magenta]Ginaz[/]")
            yield Checkbox("Grumman", True)
            yield Checkbox("Kaitain", id="initial_focus")
            yield Checkbox("Novebruns", True)

    def on_mount(self):
        self.query_one("#initial_focus", Checkbox).focus()


if __name__ == "__main__":
    CheckboxApp().run()
--- END OF FILE docs/examples/widgets/checkbox.py ---


--- START OF FILE docs/examples/widgets/collapsible.py ---
from textual.app import App, ComposeResult
from textual.widgets import Collapsible, Footer, Label, Markdown

LETO = """\
# Duke Leto I Atreides

Head of House Atreides."""

JESSICA = """
# Lady Jessica

Bene Gesserit and concubine of Leto, and mother of Paul and Alia.
"""

PAUL = """
# Paul Atreides

Son of Leto and Jessica.
"""


class CollapsibleApp(App[None]):
    """An example of collapsible container."""

    BINDINGS = [
        ("c", "collapse_or_expand(True)", "Collapse All"),
        ("e", "collapse_or_expand(False)", "Expand All"),
    ]

    def compose(self) -> ComposeResult:
        """Compose app with collapsible containers."""
        yield Footer()
        with Collapsible(collapsed=False, title="Leto"):
            yield Label(LETO)
        yield Collapsible(Markdown(JESSICA), collapsed=False, title="Jessica")
        with Collapsible(collapsed=True, title="Paul"):
            yield Markdown(PAUL)

    def action_collapse_or_expand(self, collapse: bool) -> None:
        for child in self.walk_children(Collapsible):
            child.collapsed = collapse


if __name__ == "__main__":
    app = CollapsibleApp()
    app.run()
--- END OF FILE docs/examples/widgets/collapsible.py ---


--- START OF FILE docs/examples/widgets/data_table.py ---
from textual.app import App, ComposeResult
from textual.widgets import DataTable

ROWS = [
    ("lane", "swimmer", "country", "time"),
    (4, "Joseph Schooling", "Singapore", 50.39),
    (2, "Michael Phelps", "United States", 51.14),
    (5, "Chad le Clos", "South Africa", 51.14),
    (6, "László Cseh", "Hungary", 51.14),
    (3, "Li Zhuhao", "China", 51.26),
    (8, "Mehdy Metella", "France", 51.58),
    (7, "Tom Shields", "United States", 51.73),
    (1, "Aleksandr Sadovnikov", "Russia", 51.84),
    (10, "Darren Burns", "Scotland", 51.84),
]


class TableApp(App):
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])


app = TableApp()
if __name__ == "__main__":
    app.run()
--- END OF FILE docs/examples/widgets/data_table.py ---


--- START OF FILE docs/examples/widgets/data_table_sort.py ---
from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer

ROWS = [
    ("lane", "swimmer", "country", "time 1", "time 2"),
    (4, "Joseph Schooling", Text("Singapore", style="italic"), 50.39, 51.84),
    (2, "Michael Phelps", Text("United States", style="italic"), 50.39, 51.84),
    (5, "Chad le Clos", Text("South Africa", style="italic"), 51.14, 51.73),
    (6, "László Cseh", Text("Hungary", style="italic"), 51.14, 51.58),
    (3, "Li Zhuhao", Text("China", style="italic"), 51.26, 51.26),
    (8, "Mehdy Metella", Text("France", style="italic"), 51.58, 52.15),
    (7, "Tom Shields", Text("United States", style="italic"), 51.73, 51.12),
    (1, "Aleksandr Sadovnikov", Text("Russia", style="italic"), 51.84, 50.85),
    (10, "Darren Burns", Text("Scotland", style="italic"), 51.84, 51.55),
]


class TableApp(App):
    BINDINGS = [
        ("a", "sort_by_average_time", "Sort By Average Time"),
        ("n", "sort_by_last_name", "Sort By Last Name"),
        ("c", "sort_by_country", "Sort By Country"),
        ("d", "sort_by_columns", "Sort By Columns (Only)"),
    ]

    current_sorts: set = set()

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        for col in ROWS[0]:
            table.add_column(col, key=col)
        table.add_rows(ROWS[1:])

    def sort_reverse(self, sort_type: str):
        """Determine if `sort_type` is ascending or descending."""
        reverse = sort_type in self.current_sorts
        if reverse:
            self.current_sorts.remove(sort_type)
        else:
            self.current_sorts.add(sort_type)
        return reverse

    def action_sort_by_average_time(self) -> None:
        """Sort DataTable by average of times (via a function) and
        passing of column data through positional arguments."""

        def sort_by_average_time_then_last_name(row_data):
            name, *scores = row_data
            return (sum(scores) / len(scores), name.split()[-1])

        table = self.query_one(DataTable)
        table.sort(
            "swimmer",
            "time 1",
            "time 2",
            key=sort_by_average_time_then_last_name,
            reverse=self.sort_reverse("time"),
        )

    def action_sort_by_last_name(self) -> None:
        """Sort DataTable by last name of swimmer (via a lambda)."""
        table = self.query_one(DataTable)
        table.sort(
            "swimmer",
            key=lambda swimmer: swimmer.split()[-1],
            reverse=self.sort_reverse("swimmer"),
        )

    def action_sort_by_country(self) -> None:
        """Sort DataTable by country which is a `Rich.Text` object."""
        table = self.query_one(DataTable)
        table.sort(
            "country",
            key=lambda country: country.plain,
            reverse=self.sort_reverse("country"),
        )

    def action_sort_by_columns(self) -> None:
        """Sort DataTable without a key."""
        table = self.query_one(DataTable)
        table.sort("swimmer", "lane", reverse=self.sort_reverse("columns"))


app = TableApp()
if __name__ == "__main__":
    app.run()
--- END OF FILE docs/examples/widgets/data_table_sort.py ---


--- START OF FILE docs/examples/widgets/digits.py ---
from textual.app import App, ComposeResult
from textual.widgets import Digits


class DigitApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    #pi {
        border: double green;
        width: auto;
    }
    """

    def compose(self) -> ComposeResult:
        yield Digits("3.141,592,653,5897", id="pi")


if __name__ == "__main__":
    app = DigitApp()
    app.run()
--- END OF FILE docs/examples/widgets/digits.py ---


--- START OF FILE docs/examples/widgets/directory_tree.py ---
from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree


class DirectoryTreeApp(App):
    def compose(self) -> ComposeResult:
        yield DirectoryTree("./")


if __name__ == "__main__":
    app = DirectoryTreeApp()
    app.run()
--- END OF FILE docs/examples/widgets/directory_tree.py ---


--- START OF FILE docs/examples/widgets/input.py ---
from textual.app import App, ComposeResult
from textual.widgets import Input


class InputApp(App):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="First Name")
        yield Input(placeholder="Last Name")


if __name__ == "__main__":
    app = InputApp()
    app.run()
--- END OF FILE docs/examples/widgets/input.py ---


--- START OF FILE docs/examples/widgets/link.py ---
from textual.app import App, ComposeResult
from textual.widgets import Link


class LabelApp(App):
    AUTO_FOCUS = None
    CSS = """
    Screen {
        align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        yield Link(
            "Go to textualize.io",
            url="https://textualize.io",
            tooltip="Click me",
        )


if __name__ == "__main__":
    app = LabelApp()
    app.run()
--- END OF FILE docs/examples/widgets/link.py ---


--- START OF FILE docs/examples/widgets/list_view.py ---
from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, ListItem, ListView


class ListViewExample(App):
    CSS_PATH = "list_view.tcss"

    def compose(self) -> ComposeResult:
        yield ListView(
            ListItem(Label("One")),
            ListItem(Label("Two")),
            ListItem(Label("Three")),
        )
        yield Footer()


if __name__ == "__main__":
    app = ListViewExample()
    app.run()
--- END OF FILE docs/examples/widgets/list_view.py ---


--- START OF FILE docs/examples/widgets/loading_indicator.py ---
from textual.app import App, ComposeResult
from textual.widgets import LoadingIndicator


class LoadingApp(App):
    def compose(self) -> ComposeResult:
        yield LoadingIndicator()


if __name__ == "__main__":
    app = LoadingApp()
    app.run()
--- END OF FILE docs/examples/widgets/loading_indicator.py ---


--- START OF FILE docs/examples/widgets/log.py ---
from textual.app import App, ComposeResult
from textual.widgets import Log

TEXT = """I must not fear.
Fear is the mind-killer.
Fear is the little-death that brings total obliteration.
I will face my fear.
I will permit it to pass over me and through me.
And when it has gone past, I will turn the inner eye to see its path.
Where the fear has gone there will be nothing. Only I will remain."""


class LogApp(App):
    """An app with a simple log."""

    def compose(self) -> ComposeResult:
        yield Log()

    def on_ready(self) -> None:
        log = self.query_one(Log)
        log.write_line("Hello, World!")
        for _ in range(10):
            log.write_line(TEXT)


if __name__ == "__main__":
    app = LogApp()
    app.run()
--- END OF FILE docs/examples/widgets/log.py ---


--- START OF FILE docs/examples/widgets/markdown.py ---
from textual.app import App, ComposeResult
from textual.widgets import Markdown

EXAMPLE_MARKDOWN = """\
## Markdown

- Typography *emphasis*, **strong**, `inline code` etc.    
- Headers    
- Lists    
- Syntax highlighted code blocks
- Tables and more

## Quotes

> I must not fear.
> > Fear is the mind-killer.
> > Fear is the little-death that brings total obliteration.
> > I will face my fear.
> > > I will permit it to pass over me and through me.
> > > And when it has gone past, I will turn the inner eye to see its path.
> > > Where the fear has gone there will be nothing. Only I will remain.

## Tables

| Name            | Type   | Default | Description                        |
| --------------- | ------ | ------- | ---------------------------------- |
| `show_header`   | `bool` | `True`  | Show the table header              |
| `fixed_rows`    | `int`  | `0`     | Number of fixed rows               |
| `fixed_columns` | `int`  | `0`     | Number of fixed columns            |

## Code blocks

```python
def loop_last(values: Iterable[T]) -> Iterable[Tuple[bool, T]]:
    \"\"\"Iterate and generate a tuple with a flag for last value.\"\"\"
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    for value in iter_values:
        yield False, previous_value
        previous_value = value
    yield True, previous_value
```
    

"""


class MarkdownExampleApp(App):

    def compose(self) -> ComposeResult:
        markdown = Markdown(EXAMPLE_MARKDOWN)
        markdown.code_indent_guides = False
        yield markdown


if __name__ == "__main__":
    app = MarkdownExampleApp()
    app.run()
--- END OF FILE docs/examples/widgets/markdown.py ---


--- START OF FILE docs/examples/widgets/markdown_viewer.py ---
from textual.app import App, ComposeResult
from textual.widgets import MarkdownViewer

EXAMPLE_MARKDOWN = """\
# Markdown Viewer

This is an example of Textual's `MarkdownViewer` widget.


## Features

Markdown syntax and extensions are supported.

- Typography *emphasis*, **strong**, `inline code` etc.
- Headers
- Lists (bullet and ordered)
- Syntax highlighted code blocks
- Tables!

## Tables

Tables are displayed in a DataTable widget.

| Name            | Type   | Default | Description                        |
| --------------- | ------ | ------- | ---------------------------------- |
| `show_header`   | `bool` | `True`  | Show the table header              |
| `fixed_rows`    | `int`  | `0`     | Number of fixed rows               |
| `fixed_columns` | `int`  | `0`     | Number of fixed columns            |
| `zebra_stripes` | `bool` | `False` | Display alternating colors on rows |
| `header_height` | `int`  | `1`     | Height of header row               |
| `show_cursor`   | `bool` | `True`  | Show a cell cursor                 |


## Code Blocks

Code blocks are syntax highlighted.

```python
class ListViewExample(App):
    def compose(self) -> ComposeResult:
        yield ListView(
            ListItem(Label("One")),
            ListItem(Label("Two")),
            ListItem(Label("Three")),
        )
        yield Footer()
```

## Litany Against Fear

I must not fear.
Fear is the mind-killer.
Fear is the little-death that brings total obliteration.
I will face my fear.
I will permit it to pass over me and through me.
And when it has gone past, I will turn the inner eye to see its path.
Where the fear has gone there will be nothing. Only I will remain.
"""


class MarkdownExampleApp(App):
    def compose(self) -> ComposeResult:
        markdown_viewer = MarkdownViewer(EXAMPLE_MARKDOWN, show_table_of_contents=True)
        markdown_viewer.code_indent_guides = False
        yield markdown_viewer


if __name__ == "__main__":
    app = MarkdownExampleApp()
    app.run()
--- END OF FILE docs/examples/widgets/markdown_viewer.py ---


--- START OF FILE docs/examples/widgets/option_list_options.py ---
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, OptionList
from textual.widgets.option_list import Option


class OptionListApp(App[None]):
    CSS_PATH = "option_list.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield OptionList(
            Option("Aerilon", id="aer"),
            Option("Aquaria", id="aqu"),
            None,
            Option("Canceron", id="can"),
            Option("Caprica", id="cap", disabled=True),
            None,
            Option("Gemenon", id="gem"),
            None,
            Option("Leonis", id="leo"),
            Option("Libran", id="lib"),
            None,
            Option("Picon", id="pic"),
            None,
            Option("Sagittaron", id="sag"),
            Option("Scorpia", id="sco"),
            None,
            Option("Tauron", id="tau"),
            None,
            Option("Virgon", id="vir"),
        )
        yield Footer()


if __name__ == "__main__":
    OptionListApp().run()
--- END OF FILE docs/examples/widgets/option_list_options.py ---


--- START OF FILE docs/examples/widgets/placeholder.py ---
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Placeholder


class PlaceholderApp(App):
    CSS_PATH = "placeholder.tcss"

    def compose(self) -> ComposeResult:
        yield VerticalScroll(
            Container(
                Placeholder("This is a custom label for p1.", id="p1"),
                Placeholder("Placeholder p2 here!", id="p2"),
                Placeholder(id="p3"),
                Placeholder(id="p4"),
                Placeholder(id="p5"),
                Placeholder(),
                Horizontal(
                    Placeholder(variant="size", id="col1"),
                    Placeholder(variant="text", id="col2"),
                    Placeholder(variant="size", id="col3"),
                    id="c1",
                ),
                id="bot",
            ),
            Container(
                Placeholder(variant="text", id="left"),
                Placeholder(variant="size", id="topright"),
                Placeholder(variant="text", id="botright"),
                id="top",
            ),
            id="content",
        )


if __name__ == "__main__":
    app = PlaceholderApp()
    app.run()
--- END OF FILE docs/examples/widgets/placeholder.py ---


--- START OF FILE docs/examples/widgets/pretty.py ---
from textual.app import App, ComposeResult
from textual.widgets import Pretty

DATA = {
    "title": "Back to the Future",
    "releaseYear": 1985,
    "director": "Robert Zemeckis",
    "genre": "Adventure, Comedy, Sci-Fi",
    "cast": [
        {"actor": "Michael J. Fox", "character": "Marty McFly"},
        {"actor": "Christopher Lloyd", "character": "Dr. Emmett Brown"},
    ],
}


class PrettyExample(App):
    def compose(self) -> ComposeResult:
        yield Pretty(DATA)


app = PrettyExample()

if __name__ == "__main__":
    app.run()
--- END OF FILE docs/examples/widgets/pretty.py ---


--- START OF FILE docs/examples/widgets/progress_bar.py ---
from textual.app import App, ComposeResult
from textual.containers import Center, VerticalScroll
from textual.widgets import Button, Header, Input, Label, ProgressBar


class FundingProgressApp(App[None]):
    CSS_PATH = "progress_bar.tcss"

    TITLE = "Funding tracking"

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Label("Funding: ")
            yield ProgressBar(total=100, show_eta=False)  # (1)!
        with Center():
            yield Input(placeholder="$$$")
            yield Button("Donate")

        yield VerticalScroll(id="history")

    def on_button_pressed(self) -> None:
        self.add_donation()

    def on_input_submitted(self) -> None:
        self.add_donation()

    def add_donation(self) -> None:
        text_value = self.query_one(Input).value
        try:
            value = int(text_value)
        except ValueError:
            return
        self.query_one(ProgressBar).advance(value)
        self.query_one(VerticalScroll).mount(Label(f"Donation for ${value} received!"))
        self.query_one(Input).value = ""


if __name__ == "__main__":
    FundingProgressApp().run()
--- END OF FILE docs/examples/widgets/progress_bar.py ---


--- START OF FILE docs/examples/widgets/rich_log.py ---
import csv
import io

from rich.syntax import Syntax
from rich.table import Table

from textual import events
from textual.app import App, ComposeResult
from textual.widgets import RichLog

CSV = """lane,swimmer,country,time
4,Joseph Schooling,Singapore,50.39
2,Michael Phelps,United States,51.14
5,Chad le Clos,South Africa,51.14
6,László Cseh,Hungary,51.14
3,Li Zhuhao,China,51.26
8,Mehdy Metella,France,51.58
7,Tom Shields,United States,51.73
1,Aleksandr Sadovnikov,Russia,51.84"""


CODE = '''\
def loop_first_last(values: Iterable[T]) -> Iterable[tuple[bool, bool, T]]:
    """Iterate and generate a tuple with a flag for first and last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    first = True
    for value in iter_values:
        yield first, False, previous_value
        first = False
        previous_value = value
    yield first, True, previous_value\
'''


class RichLogApp(App):
    def compose(self) -> ComposeResult:
        yield RichLog(highlight=True, markup=True)

    def on_ready(self) -> None:
        """Called  when the DOM is ready."""
        text_log = self.query_one(RichLog)

        text_log.write(Syntax(CODE, "python", indent_guides=True))

        rows = iter(csv.reader(io.StringIO(CSV)))
        table = Table(*next(rows))
        for row in rows:
            table.add_row(*row)

        text_log.write(table)
        text_log.write("[bold magenta]Write text or any Rich renderable!")

    def on_key(self, event: events.Key) -> None:
        """Write Key events to log."""
        text_log = self.query_one(RichLog)
        text_log.write(event)


if __name__ == "__main__":
    app = RichLogApp()
    app.run()
--- END OF FILE docs/examples/widgets/rich_log.py ---


--- START OF FILE docs/examples/widgets/selection_list_selections.py ---
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, SelectionList
from textual.widgets.selection_list import Selection


class SelectionListApp(App[None]):
    CSS_PATH = "selection_list.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield SelectionList[int](  # (1)!
            Selection("Falken's Maze", 0, True),
            Selection("Black Jack", 1),
            Selection("Gin Rummy", 2),
            Selection("Hearts", 3),
            Selection("Bridge", 4),
            Selection("Checkers", 5),
            Selection("Chess", 6, True),
            Selection("Poker", 7),
            Selection("Fighter Combat", 8, True),
        )
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(SelectionList).border_title = "Shall we play some games?"


if __name__ == "__main__":
    SelectionListApp().run()
--- END OF FILE docs/examples/widgets/selection_list_selections.py ---


--- START OF FILE docs/examples/widgets/select_widget.py ---
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Select

LINES = """I must not fear.
Fear is the mind-killer.
Fear is the little-death that brings total obliteration.
I will face my fear.
I will permit it to pass over me and through me.""".splitlines()


class SelectApp(App):
    CSS_PATH = "select.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Select((line, line) for line in LINES)

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.title = str(event.value)


if __name__ == "__main__":
    app = SelectApp()
    app.run()
--- END OF FILE docs/examples/widgets/select_widget.py ---


--- START OF FILE docs/examples/widgets/sparkline.py ---
import random
from statistics import mean

from textual.app import App, ComposeResult
from textual.widgets import Sparkline

random.seed(73)
data = [random.expovariate(1 / 3) for _ in range(1000)]


class SparklineSummaryFunctionApp(App[None]):
    CSS_PATH = "sparkline.tcss"

    def compose(self) -> ComposeResult:
        yield Sparkline(data, summary_function=max)  # (1)!
        yield Sparkline(data, summary_function=mean)  # (2)!
        yield Sparkline(data, summary_function=min)  # (3)!


app = SparklineSummaryFunctionApp()
if __name__ == "__main__":
    app.run()
--- END OF FILE docs/examples/widgets/sparkline.py ---


--- START OF FILE docs/examples/widgets/switch.py ---
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static, Switch


class SwitchApp(App):
    def compose(self) -> ComposeResult:
        yield Static("[b]Example switches\n", classes="label")
        yield Horizontal(
            Static("off:     ", classes="label"),
            Switch(animate=False),
            classes="container",
        )
        yield Horizontal(
            Static("on:      ", classes="label"),
            Switch(value=True),
            classes="container",
        )

        focused_switch = Switch()
        focused_switch.focus()
        yield Horizontal(
            Static("focused: ", classes="label"), focused_switch, classes="container"
        )

        yield Horizontal(
            Static("custom:  ", classes="label"),
            Switch(id="custom-design"),
            classes="container",
        )


app = SwitchApp(css_path="switch.tcss")
if __name__ == "__main__":
    app.run()
--- END OF FILE docs/examples/widgets/switch.py ---


--- START OF FILE docs/examples/widgets/tabbed_content.py ---
from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, Markdown, TabbedContent, TabPane

LETO = """
# Duke Leto I Atreides

Head of House Atreides.
"""

JESSICA = """
# Lady Jessica

Bene Gesserit and concubine of Leto, and mother of Paul and Alia.
"""

PAUL = """
# Paul Atreides

Son of Leto and Jessica.
"""


class TabbedApp(App):
    """An example of tabbed content."""

    BINDINGS = [
        ("l", "show_tab('leto')", "Leto"),
        ("j", "show_tab('jessica')", "Jessica"),
        ("p", "show_tab('paul')", "Paul"),
    ]

    def compose(self) -> ComposeResult:
        """Compose app with tabbed content."""
        # Footer to show keys
        yield Footer()

        # Add the TabbedContent widget
        with TabbedContent(initial="jessica"):
            with TabPane("Leto", id="leto"):  # First tab
                yield Markdown(LETO)  # Tab content
            with TabPane("Jessica", id="jessica"):
                yield Markdown(JESSICA)
                with TabbedContent("Paul", "Alia"):
                    yield TabPane("Paul", Label("First child"))
                    yield TabPane("Alia", Label("Second child"))

            with TabPane("Paul", id="paul"):
                yield Markdown(PAUL)

    def action_show_tab(self, tab: str) -> None:
        """Switch to a new tab."""
        self.get_child_by_type(TabbedContent).active = tab


if __name__ == "__main__":
    app = TabbedApp()
    app.run()
--- END OF FILE docs/examples/widgets/tabbed_content.py ---


--- START OF FILE docs/examples/widgets/tabs.py ---
from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, Tabs

NAMES = [
    "Paul Atreidies",
    "Duke Leto Atreides",
    "Lady Jessica",
    "Gurney Halleck",
    "Baron Vladimir Harkonnen",
    "Glossu Rabban",
    "Chani",
    "Silgar",
]


class TabsApp(App):
    """Demonstrates the Tabs widget."""

    CSS = """
    Tabs {
        dock: top;
    }
    Screen {
        align: center middle;
    }
    Label {
        margin:1 1;
        width: 100%;
        height: 100%;
        background: $panel;
        border: tall $primary;
        content-align: center middle;
    }
    """

    BINDINGS = [
        ("a", "add", "Add tab"),
        ("r", "remove", "Remove active tab"),
        ("c", "clear", "Clear tabs"),
    ]

    def compose(self) -> ComposeResult:
        yield Tabs(NAMES[0])
        yield Label()
        yield Footer()

    def on_mount(self) -> None:
        """Focus the tabs when the app starts."""
        self.query_one(Tabs).focus()

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        """Handle TabActivated message sent by Tabs."""
        label = self.query_one(Label)
        if event.tab is None:
            # When the tabs are cleared, event.tab will be None
            label.visible = False
        else:
            label.visible = True
            label.update(event.tab.label)

    def action_add(self) -> None:
        """Add a new tab."""
        tabs = self.query_one(Tabs)
        # Cycle the names
        NAMES[:] = [*NAMES[1:], NAMES[0]]
        tabs.add_tab(NAMES[0])

    def action_remove(self) -> None:
        """Remove active tab."""
        tabs = self.query_one(Tabs)
        active_tab = tabs.active_tab
        if active_tab is not None:
            tabs.remove_tab(active_tab.id)

    def action_clear(self) -> None:
        """Clear the tabs."""
        self.query_one(Tabs).clear()


if __name__ == "__main__":
    app = TabsApp()
    app.run()
--- END OF FILE docs/examples/widgets/tabs.py ---


--- START OF FILE docs/examples/widgets/text_area_custom_language.py ---
from pathlib import Path

from tree_sitter_languages import get_language

from textual.app import App, ComposeResult
from textual.widgets import TextArea

java_language = get_language("java")
java_highlight_query = (Path(__file__).parent / "java_highlights.scm").read_text()
java_code = """\
class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
"""


class TextAreaCustomLanguage(App):
    def compose(self) -> ComposeResult:
        text_area = TextArea.code_editor(text=java_code)
        text_area.cursor_blink = False

        # Register the Java language and highlight query
        text_area.register_language("java", java_language, java_highlight_query)

        # Switch to Java
        text_area.language = "java"
        yield text_area


app = TextAreaCustomLanguage()
if __name__ == "__main__":
    app.run()
--- END OF FILE docs/examples/widgets/text_area_custom_language.py ---


--- START OF FILE docs/examples/widgets/text_area_example.py ---
from textual.app import App, ComposeResult
from textual.widgets import TextArea

TEXT = """\
def hello(name):
    print("hello" + name)

def goodbye(name):
    print("goodbye" + name)
"""


class TextAreaExample(App):
    def compose(self) -> ComposeResult:
        yield TextArea.code_editor(TEXT, language="python")


app = TextAreaExample()
if __name__ == "__main__":
    app.run()
--- END OF FILE docs/examples/widgets/text_area_example.py ---


--- START OF FILE docs/examples/widgets/toast.py ---
from textual.app import App


class ToastApp(App[None]):
    def on_mount(self) -> None:
        # Show an information notification.
        self.notify("It's an older code, sir, but it checks out.")

        # Show a warning. Note that Textual's notification system allows
        # for the use of Rich console markup.
        self.notify(
            "Now witness the firepower of this fully "
            "[b]ARMED[/b] and [i][b]OPERATIONAL[/b][/i] battle station!",
            title="Possible trap detected",
            severity="warning",
        )

        # Show an error. Set a longer timeout so it's noticed.
        self.notify("It's a trap!", severity="error", timeout=10)

        # Show an information notification, but without any sort of title.
        self.notify("It's against my programming to impersonate a deity.", title="")


if __name__ == "__main__":
    ToastApp().run()
--- END OF FILE docs/examples/widgets/toast.py ---


--- START OF FILE docs/examples/widgets/tree.py ---
from textual.app import App, ComposeResult
from textual.widgets import Tree


class TreeApp(App):
    def compose(self) -> ComposeResult:
        tree: Tree[str] = Tree("Dune")
        tree.root.expand()
        characters = tree.root.add("Characters", expand=True)
        characters.add_leaf("Paul")
        characters.add_leaf("Jessica")
        characters.add_leaf("Chani")
        yield tree


if __name__ == "__main__":
    app = TreeApp()
    app.run()
--- END OF FILE docs/examples/widgets/tree.py ---


