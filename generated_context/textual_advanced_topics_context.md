# Context for: textual

## Directory Structure

```textual/
└── docs
    ├── blog
    │   └── posts
    │       ├── rich-inspect.md
    │       ├── steal-this-code.md
    │       ├── textual-serve-files.md
    │       ├── textual-web.md
    │       └── toolong-retrospective.md
    ├── examples
    │   └── guide
    │       ├── command_palette
    │       │   └── command02.py
    │       ├── compound
    │       │   └── byte03.py
    │       ├── testing
    │       │   └── test_rgb.py
    │       ├── widgets
    │       │   └── checker04.py
    │       └── workers
    │           ├── weather03.py
    │           └── weather05.py
    └── how-to
        ├── package-with-hatch.md
        ├── render-and-compose.md
        └── style-inline-apps.md
```
---

## File Contents

--- START OF FILE docs/how-to/package-with-hatch.md ---
# Package a Textual app with Hatch

Python apps may be distributed via [PyPI](https://pypi.org/) so they can be installed via `pip`.
This is known as *packaging*.
The packaging process for Textual apps is much the same as any Python library, with the additional requirement that we can launch our app from the command line.

!!! tip

    An alternative to packaging your app is to turn it into a web application with [textual-serve](https://github.com/Textualize/textual-serve).

In this How To we will cover how to use [Hatch](https://github.com/pypa/hatch) to package an example application.

Hatch is a *build tool* (a command line app to assist with packaging).
You could use any build tool to package a Textual app (such as [Poetry](https://python-poetry.org/) for example), but Hatch is a good choice given its large feature set and ease of use.


!!! info inline end "Calculator example"

    ```{.textual path="examples/calculator.py" columns=100 lines=41 press="3,.,1,4,5,9,2,wait:400"}
    ```

    This example is [`calculator.py`](https://github.com/Textualize/textual/blob/main/examples/calculator.py) taken from the examples directory in the Textual repository.


## Foreword

Packaging with Python can be a little intimidating if you haven't tackled it before.
But it's not all that complicated. 
When you have been through it once or twice, you should find it fairly straightforward.

## Example repository

See the [textual-calculator-hatch](https://github.com/Textualize/textual-calculator-hatch) repository for the project created in this How To.

## The example app

To demonstrate packaging we are going to take the calculator example from the examples directory, and publish it to PyPI.
The end goal is to allow a user to install it with pip:


```bash
pip install textual-calculator
```

Then launch the app from the command line:

```bash
calculator
```

## Installing Hatch

There are a few ways to install Hatch.
See the [official docs on installation](https://hatch.pypa.io/latest/install/) for the best method for your operating system.

Once installed, you should have the `hatch` command available on the command line.
Run the following to check Hatch was installed correctly:

```bash
hatch
```

## Hatch new

Hatch can create an initial directory structure and files with the `new` *subcommand*.
Enter `hatch new` followed by the name of your project.
For the calculator example, the name will be "textual calculator":

```batch
hatch new "textual calculator"
```

This will create the following directory structure:

```
textual-calculator
├── LICENSE.txt
├── README.md
├── pyproject.toml
├── src
│   └── textual_calculator
│       ├── __about__.py
│       └── __init__.py
└── tests
    └── __init__.py
```

This follows a well established convention when packaging Python code, and will create the following files:

- `LICENSE.txt` contains the license you want to distribute your code under.
- `README.md` is a markdown file containing information about your project, which will be displayed in PyPI and Github (if you use it). You can edit this with information about your app and how to use it.
- `pyproject.toml` is a [TOML](https://en.wikipedia.org/wiki/TOML) file which contains *metadata* (additional information) about your project and how to package it. This is a Python standard. This file may be edited manually or by a build tool (such as Hatch).
- `src/textual_calculator/__about__.py` contains the version number of your app. You should update this when you release new versions.
- `src/textual_calculator/__init__.py`  and `tests/__init__py` indicate the directory they are within contains Python code (these files are often empty).
 
In the top level is a directory called `src`.
This should contain a directory named after your project, and will be the name your code can be imported from.
In our example, this directory is `textual_calculator` so we can do `import textual_calculator` in Python code.

Additionally, there is a `tests` directory where you can add any [test](../guide/testing.md) code.

### More on naming

Note how Hatch replaced the space in the project name with a hyphen (i.e. `textual-calculator`), but the directory in `src` with an underscore (i.e. `textual_calculator`). This is because the directory in `src` contains the Python module, and a hyphen is not legal in a Python import. The top-level directory doesn't have this restriction and uses a hyphen, which is more typical for a directory name.

Bear this in mind if your project name contains spaces.


### Got existing code?

The `hatch new` command assumes you are starting from scratch.
If you have existing code you would like to package, navigate to your directory and run the following command (replace `<YOUR ROJECT NAME>` with the name of your project):

```
hatch new --init <YOUR PROJECT NAME>
```

This will generate a `pyproject.toml` in the current directory.

!!! note
    
    It will simplify things if your code follows the directory structure convention above. This may require that you move your files -- you only need to do this once!

## Adding code

Your code should reside inside `src/<PROJECT NAME>`.
For the calculator example we will copy `calculator.py` and `calculator.tcss` into the `src/textual_calculator` directory, so our directory will look like the following:

```
textual-calculator
├── LICENSE.txt
├── README.md
├── pyproject.toml
├── src
│   └── textual_calculator
│       ├── __about__.py
│       ├── __init__.py
│       ├── calculator.py
│       └── calculator.tcss
└── tests
    └── __init__.py
```

## Adding dependencies

Your Textual app will likely depend on other Python libraries (at the very least Textual itself).
We need to list these in `pyproject.toml` to ensure that these *dependencies* are installed alongside your app.

In `pyproject.toml` there should be a section beginning with `[project]`, which will look something like the following:

```toml
[project]
name = "textual-calculator"
dynamic = ["version"]
description = 'A example app'
readme = "README.md"
requires-python = ">=3.8"
license = "MIT"
keywords = []
authors = [
  { name = "Will McGugan", email = "redacted@textualize.io" },
]
classifiers = [
  "Development Status :: 4 - Beta",
  "Programming Language :: Python",
  "Programming Language :: Python :: 3.8",
  "Programming Language :: Python :: 3.9",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "Programming Language :: Python :: Implementation :: CPython",
  "Programming Language :: Python :: Implementation :: PyPy",
]
dependencies = []
```

We are interested in the `dependencies` value, which should list the app's dependencies.
If you want a particular version of a project you can add `==` followed by the version.

For the calculator, the only dependency is Textual.
We can add Textual by modifying the following line:

```toml
dependencies = ["textual==0.47.1"]
```

At the time of writing, the latest Textual is `0.47.1`.
The entry in `dependencies` will ensure we get that particular version, even when newer versions are released.

See the Hatch docs for more information on specifying [dependencies](https://hatch.pypa.io/latest/config/dependency/).

## Environments

A common problem when working with Python code is managing multiple projects with different dependencies.
For instance, if we had another app that used version `0.40.0` of Textual, it *may* break if we installed version `0.47.1`.

The standard way of solving this is with *virtual environments* (or *venvs*), which allow each project to have its own set of dependencies.
Hatch can create virtual environments for us, and makes working with them very easy.

To create a new virtual environment, navigate to the directory with the `pyproject.toml` file and run the following command (this is only require once, as the virtual environment will persist):

```bash
hatch env create
```

Then run the following command to activate the virtual environment:

```bash
hatch shell
```

If you run `python` now, it will have our app and its dependencies available for import:

```
$ python
Python 3.11.1 (main, Jan  1 2023, 10:28:48) [Clang 14.0.0 (clang-1400.0.29.202)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from textual_calculator import calculator
```

### Running the app

You can launch the calculator from the command line with the following command:

```bash
python -m textual_calculator.calculator
```

The `-m` switch tells Python to import the module and run it.

Although you can run your app this way (and it is fine for development), it's not ideal for sharing.
It would be preferable to have a dedicated command to launch the app, so the user can easily run it from the command line.
To do that, we will need to add an *entry point* to pyproject.toml

## Entry points

An entry point is a function in your project that can be run from the command line.
For our calculator example, we first need to create a function that will run the app.
Add the following file to the `src/textual_calculator` folder, and name it `entry_points.py`:

```python
from textual_calculator.calculator import CalculatorApp


def calculator():
    app = CalculatorApp()
    app.run()
```

!!! tip

    If you already have a function that runs your app, you may not need an `entry_points.py` file.

Then edit `pyproject.toml` to add the following section:

```toml
[project.scripts]
calculator = "textual_calculator.entry_points:calculator"
```

Each entry in the `[project.scripts]` section (there can be more than one) maps a command on to an import and function name.
In the second line above, before the `=` character, `calculator` is the name of the command.
The string after the `=` character contains the name of the import (`textual_calculator.entry_points`), followed by a colon (`:`), and then the name of the function (also called `calculator`).

Specifying an entry point like this is equivalent to doing the following from the Python REPL:

```
>>> import textual_calculator.entry_points
>>> textual_calculator.entry_points.calculator()
```

To add the `calculator` command once you have edited `pyproject.toml`, run the following from the command line:

```bash
pip install -e .
```

!!! info

    You will have no doubt used `pip` before, but perhaps not with `-e .`.
    The addition of `-e` installs the project in *editable* mode which means pip won't copy the `.py` files code anywhere, the dot (`.`) indicates were installing the project in the current directory. 

Now you can launch the calculator from the command line as follows:

```bash
calculator
```

## Building 

Building produces archive files that contain your code.
When you install a package via pip or other tool, it will download one of these archives.

To build your project with Hatch, change to the directory containing your `pyproject.toml` and run the `hatch build` subcommand:

```
cd textual-calculator
hatch build
```

After a moment, you should find that Hatch has created a `dist` (distribution) folder, which contains the project archive files.
You don't typically need to use these files directly, but feel free to have a look at the directory contents.

!!! note "Packaging TCSS and other files"

    Hatch will typically include all the files needed by your project, i.e. the `.py` files.
    It will also include any Textual CSS (`.tcss`) files in the project directory.
    Not all build tools will include files other than `.py`; if you are using another build tool, you may have to consult the documentation for how to add the Textual CSS files.


## Publishing

After your project has been successfully built you are ready to publish it to PyPI.

If you don't have a PyPI account, you can [create one now](https://pypi.org/account/register/).
Be sure to follow the instructions to validate your email and set up 2FA (Two Factor Authentication).

Once you have an account, login to PyPI and go to the Account Settings tab.
Scroll down and click the "Add API token" button.
In the "Create API Token" form, create a token with name "Uploads" and select the "Entire project" scope, then click the "Create token" button.

Copy this API token (long string of random looking characters) somewhere safe.
This API token is how PyPI authenticates uploads are for your account, so you should never share your API token or upload it to the internet.

Run the following command (replacing `<YOUR API TOKEN>` with the text generated in the previous step):

```bash
hatch publish -u __token__ -a <YOUR API TOKEN>
```

Hatch will upload the distribution files, and you should see a PyPI URL in the terminal.

### Managing API Tokens

Creating an API token with the "all projects" permission is required for the first upload.
You may want to generate a new API token with permissions to upload a single project when you upload a new version of your app (and delete the old one).
This way if your token is leaked, it will only impact the one project.

### Publishing new versions

If you have made changes to your app, and you want to publish the updates, you will need to update the `version` value in the `__about__.py` file, then repeat the build and publish steps.

!!! tip "Managing version numbers"

    See [Semver](https://semver.org/) for a popular versioning system (used by Textual itself).

## Installing the calculator

From the user's point of view, they only need run the following command to install the calculator:

```bash
pip install textual_calculator
```

They will then be able to launch the calculator with the following command:

```bash
calculator
```

### Pipx

A downside of installing apps this way is that unless the user has created a [virtual environment](https://docs.python.org/3/library/venv.html), they may find it breaks other packages with conflicting dependencies.

A good solution to this issue is [pipx](https://github.com/pypa/pipx) which automatically creates virtual environments that won't conflict with any other Python commands.
Once PipX is installed, you can advise users to install your app with the following command:

```bash
pipx install textual_calculator
```

This will install the calculator and the `textual` dependency as before, but without the potential of dependency conflicts.

## Summary

1. Use a build system, such as [Hatch](https://hatch.pypa.io/latest/).
2. Initialize your project with `hatch new` (or equivalent).
3. Write a function to run your app, if there isn't one already.
4. Add your dependencies and entry points to `pyproject.toml`.
5. Build your app with `hatch build`.
6. Publish your app with `hatch publish`.

---

If you have any problems packaging Textual apps, we are here to [help](../help.md)!
--- END OF FILE docs/how-to/package-with-hatch.md ---


--- START OF FILE docs/how-to/render-and-compose.md ---
# Render and compose

A common question that comes up on the [Textual Discord server](https://discord.gg/Enf6Z3qhVr) is what is the difference between [`render`][textual.widget.Widget.render] and [`compose`][textual.widget.Widget.compose] methods on a widget?
In this article we will clarify the differences, and use both these methods to build something fun.

<div class="video-wrapper">
<iframe width="1280" height="922" src="https://www.youtube.com/embed/dYU7jHyabX8" title="" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

## Which method to use?

Render and compose are easy to confuse because they both ultimately define what a widget will look like, but they have quite different uses. 

The `render` method on a widget returns a [Rich](https://rich.readthedocs.io/en/latest/) renderable, which is anything you could print with Rich.
The simplest renderable is just text; so `render()` methods often return a string, but could equally return a [`Text`](https://rich.readthedocs.io/en/latest/text.html) instance, a [`Table`](https://rich.readthedocs.io/en/latest/tables.html), or anything else from Rich (or third party library).
Whatever is returned from `render()` will be combined with any styles from CSS and displayed within the widget's borders.

The `compose` method is used to build [*compound* widgets](../guide/widgets.md#compound-widgets) (widgets composed of other widgets).

A general rule of thumb, is that if you implement a `compose` method, there is no need for a `render` method because it is the widgets yielded from `compose` which define how the custom widget will look.
However, you *can* mix these two methods.
If you implement both, the `render` method will set the custom widget's *background* and `compose` will add widgets on top of that background.

## Combining render and compose

Let's look at an example that combines both these methods.
We will create a custom widget with a [linear gradient][textual.renderables.gradient.LinearGradient] as a background.
The background will be animated (I did promise *fun*)!

=== "render_compose.py"

    ```python
    --8<-- "docs/examples/how-to/render_compose.py"
    ```

    1. Refresh the widget 30 times a second.
    2. Compose our compound widget, which contains a single Static.
    3. Render a linear gradient in the background.

=== "Output"

    ```{.textual path="docs/examples/how-to/render_compose.py" columns="100" lines="40"}
    ```

The `Splash` custom widget has a `compose` method which adds a simple `Static` widget to display a message.
Additionally there is a `render` method which returns a renderable to fill the background with a gradient.

!!! tip

    As fun as this is, spinning animated gradients may be too distracting for most apps!

## Summary

Keep the following in mind when building [custom widgets](../guide/widgets.md).

1. Use `render` to return simple text, or a Rich renderable.
2. Use `compose` to create a widget out of other widgets.
3. If you define both, then `render` will be used as a *background*.


---

We are here to [help](../help.md)!
--- END OF FILE docs/how-to/render-and-compose.md ---


--- START OF FILE docs/how-to/style-inline-apps.md ---
# Style Inline Apps

Version 0.55.0 of Textual added support for running apps *inline* (below the prompt).
Running an inline app is as simple as adding `inline=True` to [`run()`][textual.app.App.run].

<iframe width="100%" style="aspect-ratio:757/804;" src="https://www.youtube.com/embed/dxAf3vDr4aQ" title="Textual Inline mode" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

Your apps will typically run inline without modification, but you may want to make some tweaks for inline mode, which you can do with a little CSS.
This How-To will explain how.

Let's look at an inline app.
The following app displays the the current time (and keeps it up to date).

```python hl_lines="31"
--8<-- "docs/examples/how-to/inline01.py"
```

1. The `inline=True` runs the app inline.

With Textual's default settings, this clock will be displayed in 5 lines; 3 for the digits and 2 for a top and bottom border.

You can change the height or the border with CSS and the `:inline` pseudo-selector, which only matches rules in inline mode.
Let's update this app to remove the default border, and increase the height:

```python hl_lines="11-17"
--8<-- "docs/examples/how-to/inline02.py"
```

The highlighted CSS targets online inline mode.
By setting the `height` rule on Screen we can define how many lines the app should consume when it runs.
Setting `border: none` removes the default border when running in inline mode.

We've also added a rule to change the color of the clock when running inline.

## Summary

Most apps will not require modification to run inline, but if you want to tweak the height and border you can write CSS that targets inline mode with the `:inline` pseudo-selector.
--- END OF FILE docs/how-to/style-inline-apps.md ---


--- START OF FILE docs/examples/guide/command_palette/command02.py ---
from __future__ import annotations

from functools import partial
from pathlib import Path

from textual.app import App, ComposeResult
from textual.command import Hit, Hits, Provider
from textual.containers import VerticalScroll
from textual.widgets import Static


class PythonFileCommands(Provider):
    """A command provider to open a Python file in the current working directory."""

    def read_files(self) -> list[Path]:
        """Get a list of Python files in the current working directory."""
        return list(Path("./").glob("*.py"))

    async def startup(self) -> None:  # (1)!
        """Called once when the command palette is opened, prior to searching."""
        worker = self.app.run_worker(self.read_files, thread=True)
        self.python_paths = await worker.wait()

    async def search(self, query: str) -> Hits:  # (2)!
        """Search for Python files."""
        matcher = self.matcher(query)  # (3)!

        app = self.app
        assert isinstance(app, ViewerApp)

        for path in self.python_paths:
            command = f"open {str(path)}"
            score = matcher.match(command)  # (4)!
            if score > 0:
                yield Hit(
                    score,
                    matcher.highlight(command),  # (5)!
                    partial(app.open_file, path),
                    help="Open this file in the viewer",
                )


class ViewerApp(App):
    """Demonstrate a command source."""

    COMMANDS = App.COMMANDS | {PythonFileCommands}  # (6)!

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield Static(id="code", expand=True)

    def open_file(self, path: Path) -> None:
        """Open and display a file with syntax highlighting."""
        from rich.syntax import Syntax

        syntax = Syntax.from_path(
            str(path),
            line_numbers=True,
            word_wrap=False,
            indent_guides=True,
            theme="github-dark",
        )
        self.query_one("#code", Static).update(syntax)


if __name__ == "__main__":
    app = ViewerApp()
    app.run()
--- END OF FILE docs/examples/guide/command_palette/command02.py ---


--- START OF FILE docs/examples/guide/compound/byte03.py ---
from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.geometry import clamp
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input, Label, Switch


class BitSwitch(Widget):
    """A Switch with a numeric label above it."""

    DEFAULT_CSS = """
    BitSwitch {
        layout: vertical;
        width: auto;
        height: auto;
    }
    BitSwitch > Label {
        text-align: center;
        width: 100%;
    }
    """

    class BitChanged(Message):
        """Sent when the 'bit' changes."""

        def __init__(self, bit: int, value: bool) -> None:
            super().__init__()
            self.bit = bit
            self.value = value

    value = reactive(0)

    def __init__(self, bit: int) -> None:
        self.bit = bit
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label(str(self.bit))
        yield Switch()

    def watch_value(self, value: bool) -> None:  # (1)!
        """When the value changes we want to set the switch accordingly."""
        self.query_one(Switch).value = value

    def on_switch_changed(self, event: Switch.Changed) -> None:
        """When the switch changes, notify the parent via a message."""
        event.stop()
        self.value = event.value
        self.post_message(self.BitChanged(self.bit, event.value))


class ByteInput(Widget):
    """A compound widget with 8 switches."""

    DEFAULT_CSS = """
    ByteInput {
        width: auto;
        height: auto;
        border: blank;
        layout: horizontal;
    }
    ByteInput:focus-within {
        border: heavy $secondary;
    }
    """

    def compose(self) -> ComposeResult:
        for bit in reversed(range(8)):
            yield BitSwitch(bit)


class ByteEditor(Widget):
    DEFAULT_CSS = """
    ByteEditor > Container {
        height: 1fr;
        align: center middle;
    }
    ByteEditor > Container.top {
        background: $boost;
    }
    ByteEditor Input {
        width: 16;
    }
    """

    value = reactive(0)

    def validate_value(self, value: int) -> int:  # (2)!
        """Ensure value is between 0 and 255."""
        return clamp(value, 0, 255)

    def compose(self) -> ComposeResult:
        with Container(classes="top"):
            yield Input(placeholder="byte")
        with Container():
            yield ByteInput()

    def on_bit_switch_bit_changed(self, event: BitSwitch.BitChanged) -> None:
        """When a switch changes, update the value."""
        value = 0
        for switch in self.query(BitSwitch):
            value |= switch.value << switch.bit
        self.query_one(Input).value = str(value)

    def on_input_changed(self, event: Input.Changed) -> None:  # (3)!
        """When the text changes, set the value of the byte."""
        try:
            self.value = int(event.value or "0")
        except ValueError:
            pass

    def watch_value(self, value: int) -> None:  # (4)!
        """When self.value changes, update switches."""
        for switch in self.query(BitSwitch):
            with switch.prevent(BitSwitch.BitChanged):  # (5)!
                switch.value = bool(value & (1 << switch.bit))  # (6)!


class ByteInputApp(App):
    def compose(self) -> ComposeResult:
        yield ByteEditor()


if __name__ == "__main__":
    app = ByteInputApp()
    app.run()
--- END OF FILE docs/examples/guide/compound/byte03.py ---


--- START OF FILE docs/examples/guide/testing/test_rgb.py ---
from rgb import RGBApp

from textual.color import Color


async def test_keys():  # (1)!
    """Test pressing keys has the desired result."""
    app = RGBApp()
    async with app.run_test() as pilot:  # (2)!
        # Test pressing the R key
        await pilot.press("r")  # (3)!
        assert app.screen.styles.background == Color.parse("red")  # (4)!

        # Test pressing the G key
        await pilot.press("g")
        assert app.screen.styles.background == Color.parse("green")

        # Test pressing the B key
        await pilot.press("b")
        assert app.screen.styles.background == Color.parse("blue")

        # Test pressing the X key
        await pilot.press("x")
        # No binding (so no change to the color)
        assert app.screen.styles.background == Color.parse("blue")


async def test_buttons():
    """Test pressing keys has the desired result."""
    app = RGBApp()
    async with app.run_test() as pilot:
        # Test clicking the "red" button
        await pilot.click("#red")  # (5)!
        assert app.screen.styles.background == Color.parse("red")

        # Test clicking the "green" button
        await pilot.click("#green")
        assert app.screen.styles.background == Color.parse("green")

        # Test clicking the "blue" button
        await pilot.click("#blue")
        assert app.screen.styles.background == Color.parse("blue")
--- END OF FILE docs/examples/guide/testing/test_rgb.py ---


--- START OF FILE docs/examples/guide/widgets/checker04.py ---
from __future__ import annotations

from textual import events
from textual.app import App, ComposeResult
from textual.geometry import Offset, Region, Size
from textual.reactive import var
from textual.strip import Strip
from textual.scroll_view import ScrollView

from rich.segment import Segment
from rich.style import Style


class CheckerBoard(ScrollView):
    COMPONENT_CLASSES = {
        "checkerboard--white-square",
        "checkerboard--black-square",
        "checkerboard--cursor-square",
    }

    DEFAULT_CSS = """
    CheckerBoard > .checkerboard--white-square {
        background: #A5BAC9;
    }
    CheckerBoard > .checkerboard--black-square {
        background: #004578;
    }
    CheckerBoard > .checkerboard--cursor-square {
        background: darkred;
    }
    """

    cursor_square = var(Offset(0, 0))

    def __init__(self, board_size: int) -> None:
        super().__init__()
        self.board_size = board_size
        # Each square is 4 rows and 8 columns
        self.virtual_size = Size(board_size * 8, board_size * 4)

    def on_mouse_move(self, event: events.MouseMove) -> None:
        """Called when the user moves the mouse over the widget."""
        mouse_position = event.offset + self.scroll_offset
        self.cursor_square = Offset(mouse_position.x // 8, mouse_position.y // 4)

    def watch_cursor_square(
        self, previous_square: Offset, cursor_square: Offset
    ) -> None:
        """Called when the cursor square changes."""

        def get_square_region(square_offset: Offset) -> Region:
            """Get region relative to widget from square coordinate."""
            x, y = square_offset
            region = Region(x * 8, y * 4, 8, 4)
            # Move the region into the widgets frame of reference
            region = region.translate(-self.scroll_offset)
            return region

        # Refresh the previous cursor square
        self.refresh(get_square_region(previous_square))

        # Refresh the new cursor square
        self.refresh(get_square_region(cursor_square))

    def render_line(self, y: int) -> Strip:
        """Render a line of the widget. y is relative to the top of the widget."""

        scroll_x, scroll_y = self.scroll_offset  # The current scroll position
        y += scroll_y  # The line at the top of the widget is now `scroll_y`, not zero!
        row_index = y // 4  # four lines per row

        white = self.get_component_rich_style("checkerboard--white-square")
        black = self.get_component_rich_style("checkerboard--black-square")
        cursor = self.get_component_rich_style("checkerboard--cursor-square")

        if row_index >= self.board_size:
            return Strip.blank(self.size.width)

        is_odd = row_index % 2

        def get_square_style(column: int, row: int) -> Style:
            """Get the cursor style at the given position on the checkerboard."""
            if self.cursor_square == Offset(column, row):
                square_style = cursor
            else:
                square_style = black if (column + is_odd) % 2 else white
            return square_style

        segments = [
            Segment(" " * 8, get_square_style(column, row_index))
            for column in range(self.board_size)
        ]
        strip = Strip(segments, self.board_size * 8)
        # Crop the strip so that is covers the visible area
        strip = strip.crop(scroll_x, scroll_x + self.size.width)
        return strip


class BoardApp(App):
    def compose(self) -> ComposeResult:
        yield CheckerBoard(100)


if __name__ == "__main__":
    app = BoardApp()
    app.run()
--- END OF FILE docs/examples/guide/widgets/checker04.py ---


--- START OF FILE docs/examples/guide/workers/weather03.py ---
import httpx
from rich.text import Text

from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Static


class WeatherApp(App):
    """App to display the current weather."""

    CSS_PATH = "weather.tcss"

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter a City")
        with VerticalScroll(id="weather-container"):
            yield Static(id="weather")

    async def on_input_changed(self, message: Input.Changed) -> None:
        """Called when the input changes"""
        self.update_weather(message.value)

    @work(exclusive=True)
    async def update_weather(self, city: str) -> None:
        """Update the weather for the given city."""
        weather_widget = self.query_one("#weather", Static)
        if city:
            # Query the network API
            url = f"https://wttr.in/{city}"
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                weather = Text.from_ansi(response.text)
                weather_widget.update(weather)
        else:
            # No city, so just blank out the weather
            weather_widget.update("")


if __name__ == "__main__":
    app = WeatherApp()
    app.run()
--- END OF FILE docs/examples/guide/workers/weather03.py ---


--- START OF FILE docs/examples/guide/workers/weather05.py ---
from urllib.parse import quote
from urllib.request import Request, urlopen

from rich.text import Text

from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Static
from textual.worker import Worker, get_current_worker


class WeatherApp(App):
    """App to display the current weather."""

    CSS_PATH = "weather.tcss"

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter a City")
        with VerticalScroll(id="weather-container"):
            yield Static(id="weather")

    async def on_input_changed(self, message: Input.Changed) -> None:
        """Called when the input changes"""
        self.update_weather(message.value)

    @work(exclusive=True, thread=True)
    def update_weather(self, city: str) -> None:
        """Update the weather for the given city."""
        weather_widget = self.query_one("#weather", Static)
        worker = get_current_worker()
        if city:
            # Query the network API
            url = f"https://wttr.in/{quote(city)}"
            request = Request(url)
            request.add_header("User-agent", "CURL")
            response_text = urlopen(request).read().decode("utf-8")
            weather = Text.from_ansi(response_text)
            if not worker.is_cancelled:
                self.call_from_thread(weather_widget.update, weather)
        else:
            # No city, so just blank out the weather
            if not worker.is_cancelled:
                self.call_from_thread(weather_widget.update, "")

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        self.log(event)


if __name__ == "__main__":
    app = WeatherApp()
    app.run()
--- END OF FILE docs/examples/guide/workers/weather05.py ---


--- START OF FILE docs/blog/posts/rich-inspect.md ---
---
draft: false
date: 2023-07-27
categories:
  - DevLog
title: Using Rich Inspect to interrogate Python objects
authors:
  - willmcgugan
---

# Using Rich Inspect to interrogate Python objects

The [Rich](https://github.com/Textualize/rich) library has a few functions that are admittedly a little out of scope for a terminal color library. One such function is `inspect` which is so useful you may want to `pip install rich` just for this feature.

<!-- more -->

The easiest way to describe `inspect` is that it is Python's builtin `help()` but easier on the eye (and with a few more features).
If you invoke it with any object, `inspect` will display a nicely formatted report on that object &mdash; which makes it great for interrogating objects from the REPL. Here's an example:

```python
>>> from rich import inspect
>>> text_file = open("foo.txt", "w")
>>> inspect(text_file)
```

Here we're inspecting a file object, but it could be literally anything.
You will see the following output in the terminal:

<div>
--8<-- "docs/blog/images/inspect1.svg"
</div>

By default, `inspect` will generate a data-oriented summary with a text representation of the object and its data attributes.
You can also add `methods=True` to show all the methods in the public API.
Here's an example:

```python
>>> inspect(text_file, methods=True)
```

<div>
--8<-- "docs/blog/images/inspect2.svg"
</div>

The documentation is summarized by default to avoid generating verbose reports.
If you want to see the full unabbreviated help you can add `help=True`:

```python
>>> inspect(text_file, methods=True, help=True)
```

<div>
--8<-- "docs/blog/images/inspect3.svg"
</div>

There are a few more arguments to refine the level of detail you need (private methods, dunder attributes etc).
You can see the full range of options with this delightful little incantation:

```python
>>> inspect(inspect)
```

If you are interested in Rich or Textual, join our [Discord server](https://discord.gg/Enf6Z3qhVr)!


## Addendum

Here's how to have `inspect` always available without an explicit import:

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Put this in your pythonrc file: <a href="https://t.co/pXTi69ykZL">pic.twitter.com/pXTi69ykZL</a></p>&mdash; Tushar Sadhwani (@sadhlife) <a href="https://twitter.com/sadhlife/status/1684446413785280517?ref_src=twsrc%5Etfw">July 27, 2023</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
--- END OF FILE docs/blog/posts/rich-inspect.md ---


--- START OF FILE docs/blog/posts/steal-this-code.md ---
---
draft: false
date: 2022-11-20
categories:
  - DevLog
authors:
  - willmcgugan
---

# Stealing Open Source code from Textual

I would like to talk about a serious issue in the Free and Open Source software world. Stealing code. You wouldn't steal a car would you?

<div class="video-wrapper">
<iframe width="auto" src="https://www.youtube.com/embed/HmZm8vNHBSU" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

But you *should* steal code from Open Source projects. Respect the license (you may need to give attribution) but stealing code is not like stealing a car. If I steal your car, I have deprived you of a car. If you steal my open source code, I haven't lost anything.

!!! warning

    I'm not advocating for *piracy*. Open source code gives you explicit permission to use it.


From my point of view, I feel like code has greater value when it has been copied / modified in another project.

There are a number of files and modules in [Textual](https://github.com/Textualize/textual) that could either be lifted as is, or wouldn't require much work to extract. I'd like to cover a few here. You might find them useful in your next project.

<!-- more -->

## Loop first / last

How often do you find yourself looping over an iterable and needing to know if an element is the first and/or last in the sequence? It's a simple thing, but I find myself needing this a *lot*, so I wrote some helpers in [_loop.py](https://github.com/Textualize/textual/blob/main/src/textual/_loop.py).

I'm sure there is an equivalent implementation on PyPI, but steal this if you need it.

Here's an example of use:

```python
for last, (y, line) in loop_last(enumerate(self.lines, self.region.y)):
    yield move_to(x, y)
    yield from line
    if not last:
        yield new_line
```

## LRU Cache

Python's [lru_cache](https://docs.python.org/3/library/functools.html#functools.lru_cache) can be the one-liner that makes your code orders of magnitude faster. But it has a few gotchas.

The main issue is managing the lifetime of these caches. The decorator keeps a single global cache, which will keep a reference to every object in the function call. On an instance method that means you keep references to `self` for the lifetime of your app.

For a more flexibility you can use the [LRUCache](https://github.com/Textualize/textual/blob/main/src/textual/_cache.py) implementation from Textual. This uses essentially the same algorithm as the stdlib decorator, but it is implemented as a container.

Here's a quick example of its use. It works like a dictionary until you reach a maximum size. After that, new elements will kick out the element that was used least recently.

```python
>>> from textual._cache import LRUCache
>>> cache = LRUCache(maxsize=3)
>>> cache["foo"] = 1
>>> cache["bar"] = 2
>>> cache["baz"] = 3
>>> dict(cache)
{'foo': 1, 'bar': 2, 'baz': 3}
>>> cache["egg"] = 4
>>> dict(cache)
{'bar': 2, 'baz': 3, 'egg': 4}
```

In Textual, we use a [LRUCache](https://github.com/Textualize/textual/search?q=LRUCache) to store the results of rendering content to the terminal. For example, in a [datatable](https://twitter.com/search?q=%23textualdatatable&src=typed_query&f=live) it is too costly to render everything up front. So Textual renders only the lines that are currently visible on the "screen". The cache ensures that scrolling only needs to render the newly exposed lines, and lines that haven't been displayed in a while are discarded to save memory.


## Color

Textual has a [Color](https://github.com/Textualize/textual/blob/main/src/textual/color.py) class which could be extracted in to a module of its own.

The Color class can parse colors encoded in a variety of HTML and CSS formats. Color object support a variety of methods and operators you can use to manipulate colors, in a fairly natural way.

Here's some examples in the REPL.


```python
>>> from textual.color import Color
>>> color = Color.parse("lime")
>>> color
Color(0, 255, 0, a=1.0)
>>> color.darken(0.8)
Color(0, 45, 0, a=1.0)
>>> color + Color.parse("red").with_alpha(0.1)
Color(25, 229, 0, a=1.0)
>>> color = Color.parse("#12a30a")
>>> color
Color(18, 163, 10, a=1.0)
>>> color.css
'rgb(18,163,10)'
>>> color.hex
'#12A30A'
>>> color.monochrome
Color(121, 121, 121, a=1.0)
>>> color.monochrome.hex
'#797979'
>>> color.hsl
HSL(h=0.3246187363834423, s=0.8843930635838151, l=0.33921568627450976)
>>>
```

There are some very good color libraries in PyPI, which you should also consider using. But Textual's Color class is lean and performant, with no C dependencies.

## Geometry

This may be my favorite module in Textual: [geometry.py](https://github.com/Textualize/textual/blob/main/src/textual/geometry.py).

The geometry module contains a number of classes responsible for storing and manipulating 2D geometry. There is an `Offset` class which is a two dimensional point. A `Region` class which is a rectangular region defined by a coordinate and dimensions. There is a `Spacing` class which defines additional space around a region. And there is a `Size` class which defines the dimensions of an area by its width and height.

These objects are used by Textual's layout engine and compositor, which makes them the oldest and most thoroughly tested part of the project.

There's a lot going on in this module, but the docstrings are quite detailed and have unicode art like this to help explain things.

```
              cut_x ↓
          ┌────────┐ ┌───┐
          │        │ │   │
          │    0   │ │ 1 │
          │        │ │   │
  cut_y → └────────┘ └───┘
          ┌────────┐ ┌───┐
          │    2   │ │ 3 │
          └────────┘ └───┘
```

## You should steal our code

There is a lot going on in the [Textual Repository](https://github.com/Textualize/textual). Including a CSS parser, renderer, layout and compositing engine. All written in pure Python. Steal it with my blessing.
--- END OF FILE docs/blog/posts/steal-this-code.md ---


--- START OF FILE docs/blog/posts/textual-serve-files.md ---
---
draft: false 
date: 2024-09-08
categories:
  - DevLog
authors:
  - darrenburns
title: "Towards Textual Web Applications"
---

In this post we'll look at some new functionality available in Textual apps accessed via a browser and how it helps provide a more equal experience across platforms.

<!-- more -->

## What is `textual-serve`?

[`textual-serve`](https://github.com/Textualize/textual-serve) is an open source project which allows you to serve and access your Textual app via a browser. The Textual app runs on a machine/server under your control, and communicates with the browser via a protocol which runs over websocket. End-users interacting with the app via their browser do not have access to the machine the application is running on via their browser, only the running Textual app.

For example, you could install [`harlequin`](https://github.com/tconbeer/harlequin) (a terminal-based SQL IDE)  on a machine on your network, run it using `textual-serve`, and then share the URL with others. Anyone with the URL would then be able to use `harlequin` to query databases accessible from that server. Or, you could deploy [`posting`](https://github.com/darrenburns/posting) (a terminal-based API client) on a server, and provide your colleagues with the URL, allowing them to quickly send HTTP requests *from that server*, right from within their browser.

<figure markdown>
![posting running in a browser](../images/textual-serve-files/posting-textual-serve.png)
  <figcaption>Accessing an instance of Posting via a web browser.</figcaption>
</figure>

## Providing an equal experience

While you're interacting with the Textual app using your web browser, it's not *running* in your browser. It's running on the machine you've installed it on, similar to typical server driven web app. This creates some interesting challenges for us if we want to provide an equal experience across browser and terminal.

A Textual app running in the browser is inherently more accessible to non-technical users, and we don't want to limit access to important functionality for those users. We also don't want Textual app developers to have to repeatedly check "is the the end-user using a browser or a terminal?".

To solve this, we've created APIs which allow developers to add web links to their apps and deliver files to end-users in a platform agnostic way. The goal of these APIs is to allow developers to write applications knowing that they'll provide a sensible user experience in both terminals and web browsers without any extra effort.

## Opening web links

The ability to click on and open links is a pretty fundamental expectation when interacting with an app running in your browser.

Python offers a [`webbrowser`](https://docs.python.org/3/library/webbrowser.html) module which allows you to open a URL in a web browser. When a Textual app is running in a terminal, a simple call to this module does exactly what we'd expect.

If the app is being used via a browser however, the `webbrowser` module would attempt to open the browser on the machine the app is being served from. This is clearly not very useful to the end-user!

To solve this, we've added a new method to Textual: [`App.open_url`](https://textual.textualize.io/api/app/#textual.app.App.open_url). When running in the terminal, this will use `webbrowser` to open the URL as you would expect. 

When the Textual app is being served and used via the browser however, the running app will inform `textual-serve`, which will in turn tell the browser via websocket that the end-user is requesting to open a link, which will then be opened in their browser - just like a normal web link.

The developer doesn't need to think about *where* their application might be running. By using `open_url`, Textual will ensure that end-users get the experience they expect.

## Saving files to disk

When running a Textual app in the terminal, getting a file into the hands of the end user is relatively simple - you could just write it to disk and notify them of the location, or perhaps open their `$EDITOR` with the content loaded into it. Given they're using a terminal, we can also make an assumption that the end-user is at least some technical knowledge.

Run that same app in the browser however, and we have a problem. If you simply write the file to disk, the end-user would need to be able to access the machine the app is running on and navigate the file system in order to retrieve it. This may not be possible: they may not be permitted to access the machine, or they simply may not know how!

The new [`App.deliver_text`][textual.app.App.deliver_text] and [`App.deliver_binary`][textual.app.App.deliver_binary] methods are designed to let developers get files into the hands of end users, regardless of whether the app is being accessed via the browser or a terminal.

When accessing a Textual app using a terminal, these methods will write a file to disk, and notify the `App` when the write is complete.

In the browser, however, a download will be initiated and the file will be streamed via an ephemeral (one-time) download URL from the server that the Textual app is running on to the end-user's browser. If the app developer wishes, they can specify a custom file name, MIME type, and even whether the browser should attempt to open the file in a new tab or be downloaded.

## How it works

Input in Textual apps is handled, at the lowest level, by "driver" classes. We have different drivers for Linux and Windows, and also one for handling apps being served via web. 

When running in a terminal, the Windows/Linux drivers will read `stdin`, and parse incoming ANSI escape sequences sent by the terminal emulator as a result of mouse movement or keyboard interaction. The driver translates these escape sequences into Textual "Events", which are sent on to your application's message queue for asynchronous handling.

For apps being served over the web, things are again a bit more complex. Interaction between the application and the end-user happens inside the browser - with a terminal rendered using [`xterm.js`](https://xtermjs.org/) - the same front-end terminal engine used in VS Code. `xterm.js` fills the roll of a terminal emulator here, translating user interactions into ANSI escape codes on `stdin`.

These escape codes are sent through websocket to `textual-serve` and then piped to the `stdin` stream of the Textual app which is running as a subprocess. Inside the Textual app, these can be processed and converted into events as normal by Textual's web driver.

A Textual app also writes to the `stdout` stream, which is then read by your emulator and translated into visual output. When running on the web, this stdout is also sent over websocket to the end-user's browser, and `xterm.js` takes care of rendering.

Although most of the data flowing back and forth from browser to Textual app is going to be ANSI escape sequences, we can in reality send anything we wish.

To support file delivery we updated our protocol to allow applications to signal that a file is "ready" for delivery when one of the new "deliver file" APIs is called. An ephemeral, single-use, download link is then generated and sent to the browser via websocket. The front-end of `textual-serve` opens this URL and the file is streamed to the browser.

This streaming process involves continuous delivery of encoded chunks of the file (using a variation of [Bencode](https://en.wikipedia.org/wiki/Bencode) - the encoding used by [BitTorrent](https://en.wikipedia.org/wiki/BitTorrent)) from the Textual app process to `textual-serve`, and then through to the end-user via the download URL.

![textual-serve-overview](../images/textual-serve-files/textual-serve-overview.png)

## The result

These new APIs close an important feature gap and give developers the option to build apps that can accessed via terminals or browsers without worrying that those on the web might miss out on important functionality!

## Found this interesting?

Join our [Discord server](https://discord.gg/Enf6Z3qhVr) to chat to myself and other Textual developers.
--- END OF FILE docs/blog/posts/textual-serve-files.md ---


--- START OF FILE docs/blog/posts/textual-web.md ---
---
draft: false
date: 2023-09-06
categories:
  - News
title: "What is Textual Web?"
authors:
  - willmcgugan
---

# What is Textual Web?

If you know us, you will know that we are the team behind [Rich](https://github.com/Textualize/rich) and [Textual](https://github.com/Textualize/textual) &mdash; two popular Python libraries that work magic in the terminal.

!!! note

    Not to mention [Rich-CLI](https://github.com/Textualize/rich-cli), [Trogon](https://github.com/Textualize/trogon), and [Frogmouth](https://github.com/Textualize/frogmouth)

Today we are adding one project more to that lineup: [textual-web](https://github.com/Textualize/textual-web).


<!-- more -->

Textual Web takes a Textual-powered TUI and turns it in to a web application.
Here's a video of that in action:

<div class="video-wrapper">
<iframe width="auto" src="https://www.youtube.com/embed/A8k8TD7_wg0" title="Textual Web in action" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

With the `textual-web` command you can publish any Textual app on the web, making it available to anyone you send the URL to.
This works without creating a socket server on your machine, so you won't have to configure firewalls and ports to share your applications.

We're excited about the possibilities here.
Textual web apps are fast to spin up and tear down, and they can run just about anywhere that has an outgoing internet connection.
They can be built by a single developer without any experience with a traditional web stack.
All you need is proficiency in Python and a little time to read our [lovely docs](https://textual.textualize.io/).

Future releases will expose more of the Web platform APIs to Textual apps, such as notifications and file system access.
We plan to do this in a way that allows the same (Python) code to drive those features.
For instance, a Textual app might save a file to disk in a terminal, but offer to download it in the browser.

Also in the pipeline is [PWA](https://en.wikipedia.org/wiki/Progressive_web_app) support, so you can build terminal apps, web apps, and desktop apps with a single codebase.

Textual Web is currently in a public beta. Join our [Discord server](https://discord.gg/Enf6Z3qhVr) if you would like to help us test, or if you have any questions.
--- END OF FILE docs/blog/posts/textual-web.md ---


--- START OF FILE docs/blog/posts/toolong-retrospective.md ---
---
draft: false
date: 2024-02-11
categories:
  - DevLog
authors:
  - willmcgugan
---

# File magic with the Python standard library

I recently published [Toolong](https://github.com/textualize/toolong), an app for viewing log files.
There were some interesting technical challenges in building Toolong that I'd like to cover in this post.

<!-- more -->

!!! note "Python is awesome"

    This isn't specifically [Textual](https://github.com/textualize/textual/) related. These techniques could be employed in any Python project.

These techniques aren't difficult, and shouldn't be beyond anyone with an intermediate understanding of Python.
They are the kind of "if you know it you know it" knowledge that you may not need often, but can make a massive difference when you do!

## Opening large files

If you were to open a very large text file (multiple gigabyte in size) in an editor, you will almost certainly find that it takes a while. You may also find that it doesn't load at all because you don't have enough memory, or it disables features like syntax highlighting.

This is because most app will do something analogous to this:

```python
with open("access.log", "rb") as log_file:
    log_data = log_file.read()
```

All the data is read in to memory, where it can be easily processed.
This is fine for most files of a reasonable size, but when you get in to the gigabyte territory the read and any additional processing will start to use a significant amount of time and memory.

Yet Toolong can open a file of *any* size in a second or so, with syntax highlighting.
It can do this because it doesn't need to read the entire log file in to memory.
Toolong opens a file and reads only the portion of it required to display whatever is on screen at that moment.
When you scroll around the log file, Toolong reads the data off disk as required -- fast enough that you may never even notice it.

### Scanning lines

There is an additional bit of work that Toolong has to do up front in order to show the file.
If you open a large file you may see a progress bar and a message about "scanning".

Toolong needs to know where every line starts and ends in a log file, so it can display a scrollbar bar and allow the user to navigate lines in the file.
In other words it needs to know the offset of every new line (`\n`) character within the file.

This isn't a hard problem in itself.
You might have imagined a loop that reads a chunk at a time and searches for new lines characters.
And that would likely have worked just fine, but there is a bit of magic in the Python standard library that can speed that up.

The [mmap](https://docs.python.org/3/library/mmap.html) module is a real gem for this kind of thing.
A *memory mapped file* is an OS-level construct that *appears* to load a file instantaneously.
In Python you get an object which behaves like a `bytearray`, but loads data from disk when it is accessed.
The beauty of this module is that you can work with files in much the same way as if you had read the entire file in to memory, while leaving the actual reading of the file to the OS.

Here's the method that Toolong uses to scan for line breaks.
Forgive the micro-optimizations, I was going for raw execution speed here.

```python
    def scan_line_breaks(
        self, batch_time: float = 0.25
    ) -> Iterable[tuple[int, list[int]]]:
        """Scan the file for line breaks.

        Args:
            batch_time: Time to group the batches.

        Returns:
            An iterable of tuples, containing the scan position and a list of offsets of new lines.
        """
        fileno = self.fileno
        size = self.size
        if not size:
            return
        log_mmap = mmap.mmap(fileno, size, prot=mmap.PROT_READ)
        rfind = log_mmap.rfind
        position = size
        batch: list[int] = []
        append = batch.append
        get_length = batch.__len__
        monotonic = time.monotonic
        break_time = monotonic()

        while (position := rfind(b"\n", 0, position)) != -1:
            append(position)
            if get_length() % 1000 == 0 and monotonic() - break_time > batch_time:
                break_time = monotonic()
                yield (position, batch)
                batch = []
                append = batch.append
        yield (0, batch)
        log_mmap.close()
```

This code runs in a thread (actually a [worker](https://textual.textualize.io/guide/workers/)), and will generate line breaks in batches. Without batching, it risks slowing down the UI with millions of rapid events.

It's fast because most of the work is done in `rfind`, which runs at C speed, while the OS reads from the disk.

## Watching a file for changes

Toolong can tail files in realtime.
When something appends to the file, it will be read and displayed virtually instantly.
How is this done?

You can easily *poll* a file for changes, by periodically querying the size or timestamp of a file until it changes.
The downside of this is that you don't get notified immediately if a file changes between polls.
You could poll at a very fast rate, but if you were to do that you would end up burning a lot of CPU for no good reason.

There is a very good solution for this in the standard library.
The [selectors](https://docs.python.org/3/library/selectors.html) module is typically used for working with sockets (network data), but can also work with files (at least on macOS and Linux).

!!! info "Software developers are an unimaginative bunch when it comes to naming things"

    Not to be confused with CSS [selectors](https://textual.textualize.io/guide/CSS/#selectors)!    

The selectors module can tell you precisely when a file can be read.
It can do this very efficiently, because it relies on the OS to tell us when a file can be read, and doesn't need to poll.

You register a file with a `Selector` object, then call `select()` which returns as soon as there is new data available for reading.

See [watcher.py](https://github.com/Textualize/toolong/blob/main/src/toolong/watcher.py) in Toolong, which runs a thread to monitors files for changes with a selector.

!!! warning "Addendum"

    So it turns out that watching regular files for changes with selectors only works with `KqueueSelector` which is the default on macOS.
    Disappointingly, the Python docs aren't clear on this.
    Toolong will use a polling approach where this selector is unavailable.

## Textual learnings

This project was a chance for me to "dogfood" Textual.
Other Textual devs have build some cool projects ([Trogon](https://github.com/Textualize/trogon) and [Frogmouth](https://github.com/Textualize/frogmouth)), but before Toolong I had only ever written example apps for docs.

I paid particular attention to Textual error messages when working on Toolong, and improved many of them in Textual.
Much of what I improved were general programming errors, and not Textual errors per se.
For instance, if you forget to call `super()` on a widget constructor, Textual used to give a fairly cryptic error.
It's a fairly common gotcha, even for experience devs, but now Textual will detect that and tell you how to fix it.

There's a lot of other improvements which I thought about when working on this app.
Mostly quality of life features that will make implementing some features more intuitive.
Keep an eye out for those in the next few weeks.

## Found this interesting?

If you would like to talk about this post or anything Textual related, join us on the [Discord server](https://discord.gg/Enf6Z3qhVr).
--- END OF FILE docs/blog/posts/toolong-retrospective.md ---


