# Context for: textual

## Directory Structure

```textual/
└── docs
    ├── examples
    │   └── guide
    │       └── layout
    │           ├── combining_layouts.py
    │           ├── dock_layout1_sidebar.py
    │           ├── grid_layout1.py
    │           ├── horizontal_layout.py
    │           ├── layers.py
    │           └── vertical_layout.py
    └── how-to
        ├── center-things.md
        ├── design-a-layout.md
        └── work-with-containers.md
```
---

## File Contents

--- START OF FILE docs/how-to/center-things.md ---
# Center things

If you have ever needed to center something in a web page, you will be glad to know it is **much** easier in Textual.

This article discusses a few different ways in which things can be centered, and the differences between them.

## Aligning widgets

The [align](../styles/align.md) rule will center a widget relative to one or both edges.
This rule is applied to a *container*, and will impact how the container's children are arranged.
Let's see this in practice with a trivial app containing a [Static](../widgets/static.md) widget:

```python
--8<-- "docs/examples/how-to/center01.py"
```

Here's the output:

```{.textual path="docs/examples/how-to/center01.py"}
```

The container of the widget is the screen, which has the `align: center middle;` rule applied. The
`center` part tells Textual to align in the horizontal direction, and `middle` tells Textual to align in the vertical direction.

The output *may* surprise you.
The text appears to be aligned in the middle (i.e. vertical edge), but *left* aligned on the horizontal.
This isn't a bug &mdash; I promise.
Let's make a small change to reveal what is happening here.
In the next example, we will add a background and a border to our text:

!!! tip

    Adding a border is a very good way of visualizing layout issues, if something isn't behaving as you would expect.

```python hl_lines="13-16 20"
--8<-- "docs/examples/how-to/center02.py"
```

The static widget will now have a blue background and white border:

```{.textual path="docs/examples/how-to/center02.py"}
```

Note the static widget is as wide as the screen.
Since the widget is as wide as its container, there is no room for it to move in the horizontal direction.

!!! info

    The `align` rule applies to *widgets*, not the text.

In order to see the `center` alignment, we will have to make the widget smaller than the width of the screen.
Let's set the width of the Static widget to `auto`, which will make the widget just wide enough to fit the content:

```python hl_lines="16"
--8<-- "docs/examples/how-to/center03.py"
```

If you run this now, you should see the widget is aligned on both axis:

```{.textual path="docs/examples/how-to/center03.py"}
```

## Aligning text

In addition to aligning widgets, you may also want to align *text*.
In order to demonstrate the difference, lets update the example with some longer text.
We will also set the width of the widget to something smaller, to force the text to wrap.

```python hl_lines="4 18 23"
--8<-- "docs/examples/how-to/center04.py"
```

Here's what it looks like with longer text:

```{.textual path="docs/examples/how-to/center04.py"}
```

Note how the widget is centered, but the text within it is flushed to the left edge.
Left aligned text is the default, but you can also center the text with the [text-align](../styles/text_align.md) rule.
Let's center align the longer text by setting this rule:

```python hl_lines="19"
--8<-- "docs/examples/how-to/center05.py"
```

If you run this, you will see that each line of text is individually centered:

```{.textual path="docs/examples/how-to/center05.py"}
```

You can also use `text-align` to right align text or justify the text (align to both edges).

## Aligning content

There is one last rule that can help us center things.
The [content-align](../styles/content_align.md) rule aligns content *within* a widget.
It treats the text as a rectangular region and positions it relative to the space inside a widget's border.

In order to see why we might need this rule, we need to make the Static widget larger than required to fit the text.
Let's set the height of the Static widget to 9 to give the content room to move:

```python hl_lines="19"
--8<-- "docs/examples/how-to/center06.py"
```

Here's what it looks like with the larger widget:

```{.textual path="docs/examples/how-to/center06.py"}
```

Textual aligns a widget's content to the top border by default, which is why the space is below the text.
We can tell Textual to align the content to the center by setting `content-align: center middle`;

!!! note

    Strictly speaking, we only need to align the content vertically here (there is no room to move the content left or right)
    So we could have done `content-align-vertical: middle;`

```python hl_lines="21"
--8<-- "docs/examples/how-to/center07.py"
```

If you run this now, the content will be centered within the widget:

```{.textual path="docs/examples/how-to/center07.py"}
```

## Aligning multiple widgets

It's just as easy to align multiple widgets as it is a single widget.
Applying `align: center middle;` to the parent widget (screen or other container) will align all its children.

Let's create an example with two widgets.
The following code adds two widgets with auto dimensions:

```python
--8<-- "docs/examples/how-to/center08.py"
```

This produces the following output:

```{.textual path="docs/examples/how-to/center08.py"}
```

We can center both those widgets by applying the `align` rule as before:

```python hl_lines="9-11"
--8<-- "docs/examples/how-to/center09.py"
```

Here's the output:

```{.textual path="docs/examples/how-to/center09.py"}
```

Note how the widgets are aligned as if they are a single group.
In other words, their position relative to each other didn't change, just their position relative to the screen.

If you do want to center each widget independently, you can place each widget inside its own container, and set `align` for those containers.
Textual has a builtin [`Center`][textual.containers.Center] container for just this purpose.

Let's wrap our two widgets in a `Center` container:

```python hl_lines="2 22 24"
--8<-- "docs/examples/how-to/center10.py"
```

If you run this, you will see that the widgets are centered relative to each other, not just the screen:

```{.textual path="docs/examples/how-to/center10.py"}
```

## Summary

Keep the following in mind when you want to center content in Textual:

- In order to center a widget, it needs to be smaller than its container.
- The `align` rule is applied to the *parent* of the widget you want to center (i.e. the widget's container).
- The `text-align` rule aligns text on a line by line basis.
- The `content-align` rule aligns content *within* a widget.
- Use the [`Center`][textual.containers.Center] container if you want to align multiple widgets relative to each other.
- Add a border if the alignment isn't working as you would expect.

---

If you need further help, we are here to [help](../help.md).
--- END OF FILE docs/how-to/center-things.md ---


--- START OF FILE docs/how-to/design-a-layout.md ---
# Design a Layout

This article discusses an approach you can take when designing the layout for your applications.

Textual's layout system is flexible enough to accommodate just about any application design you could conceive of, but it may be hard to know where to start. We will go through a few tips which will help you get over the initial hurdle of designing an application layout.


## Tip 1. Make a sketch

The initial design of your application is best done with a sketch.
You could use a drawing package such as [Excalidraw](https://excalidraw.com/) for your sketch, but pen and paper is equally as good.

Start by drawing a rectangle to represent a blank terminal, then draw a rectangle for each element in your application. Annotate each of the rectangles with the content they will contain, and note wether they will scroll (and in what direction).

For the purposes of this article we are going to design a layout for a Twitter or Mastodon client, which will have a header / footer and a number of columns.

!!! note

    The approach we are discussing here is applicable even if the app you want to build looks nothing like our sketch!

Here's our sketch:

<div class="excalidraw">
--8<-- "docs/images/how-to/layout.excalidraw.svg"
</div>

It's rough, but it's all we need.

## Tip 2. Work outside in

Like a sculpture with a block of marble, it is best to work from the outside towards the center.
If your design has fixed elements (like a header, footer, or sidebar), start with those first.

In our sketch we have a header and footer.
Since these are the outermost widgets, we will begin by adding them.

!!! tip

    Textual has builtin [Header](../widgets/header.md) and [Footer](../widgets/footer.md) widgets which you could use in a real application.

The following example defines an [app](../guide/app.md), a [screen](../guide/screens.md), and our header and footer widgets.
Since we're starting from scratch and don't have any functionality for our widgets, we are going to use the [Placeholder][textual.widgets.Placeholder] widget to help us visualize our design.

In a real app, we would replace these placeholders with more useful content.

=== "layout01.py"

    ```python
    --8<-- "docs/examples/how-to/layout01.py"
    ```

    1. The Header widget extends Placeholder.
    2. The footer widget extends Placeholder.
    3. Creates the header widget (the id will be displayed within the placeholder widget).
    4. Creates the footer widget.

=== "Output"

    ```{.textual path="docs/examples/how-to/layout01.py"}
    ```

## Tip 3. Apply docks

This app works, but the header and footer don't behave as expected.
We want both of these widgets to be fixed to an edge of the screen and limited in height.
In Textual this is known as *docking* which you can apply with the [dock](../styles/dock.md) rule.

We will dock the header and footer to the top and bottom edges of the screen respectively, by adding a little [CSS](../guide/CSS.md) to the widget classes:

=== "layout02.py"

    ```python hl_lines="7-12 16-21"
    --8<-- "docs/examples/how-to/layout02.py"
    ```

=== "Output"

    ```{.textual path="docs/examples/how-to/layout02.py"}
    ```

The `DEFAULT_CSS` class variable is used to set CSS directly in Python code.
We could define these in an external CSS file, but writing the CSS inline like this can be convenient if it isn't too complex.

When you dock a widget, it reduces the available area for other widgets.
This means that Textual will automatically compensate for the 6 additional lines reserved for the header and footer.

## Tip 4. Use FR Units for flexible things

After we've added the header and footer, we want the remaining space to be used for the main interface, which will contain the columns in the sketch.
This area is flexible (will change according to the size of the terminal), so how do we ensure that it takes up precisely the space needed?

The simplest way is to use [fr](../css_types/scalar.md#fraction) units.
By setting both the width and height to `1fr`, we are telling Textual to divide the space equally amongst the remaining widgets.
There is only a single widget, so that widget will fill all of the remaining space.

Let's make that change.

=== "layout03.py"

    ```python hl_lines="24-31 38"
    --8<-- "docs/examples/how-to/layout03.py"
    ```

    1. Here's where we set the width and height to `1fr`. We also add a border just to illustrate the dimensions better.

=== "Output"

    ```{.textual path="docs/examples/how-to/layout03.py"}
    ```

As you can see, the central Columns area will resize with the terminal window.

## Tip 5. Use containers

Before we add content to the Columns area, we have an opportunity to simplify.
Rather than extend `Placeholder` for our `ColumnsContainer` widget, we can use one of the builtin *containers*.
A container is simply a widget designed to *contain* other widgets.
Containers are styled with `fr` units to fill the remaining space so we won't need to add any more CSS.

Let's replace the `ColumnsContainer` class in the previous example with a `HorizontalScroll` container, which also adds an automatic horizontal scrollbar.

=== "layout04.py"

    ```python hl_lines="2 29"
    --8<-- "docs/examples/how-to/layout04.py"
    ```

    1. The builtin container widget.


=== "Output"

    ```{.textual path="docs/examples/how-to/layout04.py"}
    ```

The container will appear as blank space until we add some widgets to it.

Let's add the columns to the `HorizontalScroll`.
A column is itself a container which will have a vertical scrollbar, so we will define our `Column` by subclassing `VerticalScroll`.
In a real app, these columns will likely be added dynamically from some kind of configuration, but let's add 4 to visualize the layout.

We will also define a `Tweet` placeholder and add a few to each column.

=== "layout05.py"

    ```python hl_lines="2 25-26 29-32 39-43"
    --8<-- "docs/examples/how-to/layout05.py"
    ```

=== "Output"

    ```{.textual path="docs/examples/how-to/layout05.py"}
    ```

Note from the output that each `Column` takes a quarter of the screen width.
This happens because `Column` extends a container which has a width of `1fr`.

It makes more sense for a column in a Twitter / Mastodon client to use a fixed width.
Let's set the width of the columns to 32.

We also want to reduce the height of each "tweet".
In the real app, you might set the height to "auto" so it fits the content, but lets set it to 5 lines for now.

Here's the final example and a reminder of the sketch.

=== "layout06.py"

    ```python hl_lines="25-32 36-46"
    --8<-- "docs/examples/how-to/layout06.py"
    ```

=== "Output"

    ```{.textual path="docs/examples/how-to/layout06.py" columns="100" lines="32"}
    ```

=== "Sketch"

    <div class="excalidraw">
    --8<-- "docs/images/how-to/layout.excalidraw.svg"
    </div>


A layout like this is a great starting point.
In a real app, you would start replacing each of the placeholders with [builtin](../widget_gallery.md) or [custom](../guide/widgets.md) widgets.


## Summary

Layout is the first thing you will tackle when building a Textual app.
The following tips will help you get started.

1. Make a sketch (pen and paper is fine).
2. Work outside in. Start with the entire space of the terminal, add the outermost content first.
3. Dock fixed widgets. If the content doesn't move or scroll, you probably want to *dock* it.
4. Make use of `fr` for flexible space within layouts.
5. Use containers to contain other widgets, particularly if they scroll!

---

If you need further help, we are here to [help](../help.md).
--- END OF FILE docs/how-to/design-a-layout.md ---


--- START OF FILE docs/how-to/work-with-containers.md ---
# Save time with Textual containers

Textual's [containers][textual.containers] provide a convenient way of arranging your widgets. Let's look at them in a little detail.

!!! info "Are you in the right place?"

    We are talking about Textual container widgets here. Not to be confused with [containerization](https://en.wikipedia.org/wiki/Containerization_(computing))&mdash;which is something else entirely!


## What are containers?

Containers are reusable [compound widgets](../guide/widgets.md#compound-widgets) with preset styles to arrange their children.
For instance, there is a [Horizontal][textual.containers.Horizontal] container which arranges all of its children in a horizontal row.
Let's look at a quick example of that:

```python hl_lines="2 21"
--8<-- "docs/examples/how-to/containers01.py"
```

1. Use the with statement to add the Horizontal container.
2. Any widgets yielded within the Horizontal block will be arranged in a horizontal row.

Here's the output:

```{.textual path="docs/examples/how-to/containers01.py"}
```

Note that inside the `Horizontal` block new widgets will be placed to the right of previous widgets, forming a row.
This will still be the case if you later add or remove widgets.
Without the container, the widgets would be stacked vertically.

### How are containers implemented?

Before I describe some of the other containers, I would like to show how containers are implemented.
The following is the actual source of the `Horizontal` widget:

```python
class Horizontal(Widget):
    """An expanding container with horizontal layout and no scrollbars."""

    DEFAULT_CSS = """
    Horizontal {
        width: 1fr;
        height: 1fr;
        layout: horizontal;
        overflow: hidden hidden;
    }
    """
```

That's it!
A simple widget with a few preset styles.
The other containers are just as simple.

## Horizontal and Vertical

We've seen the `Horizontal` container in action.
The [Vertical][textual.containers.Vertical] container, as you may have guessed, work the same but arranges its children vertically, i.e. from top to bottom.

You can probably imagine what this looks like, but for sake of completeness, here is an example with a Vertical container:

```python hl_lines="2 21"
--8<-- "docs/examples/how-to/containers02.py"
```

1. Stack the widgets vertically.

And here's the output:

```{.textual path="docs/examples/how-to/containers02.py"}
```

Three boxes, vertically stacked.

!!! tip "Styling layout"

    You can set the layout of a compound widget with the [layout](../styles/layout.md) rule.

### Size behavior

Something to keep in mind when using `Horizontal` or `Vertical` is that they will consume the remaining space in the screen. Let's look at an example to illustrate that.

The following code adds a `with-border` style which draws a green border around the container.
This will help us visualize the dimensions of the container.

```python
--8<-- "docs/examples/how-to/containers03.py"
```

1. Add the `with-border` class to draw a border around the container.

Here's the output:

```{.textual path="docs/examples/how-to/containers03.py"}
```

Notice how the container is as large as the screen.
Let's look at what happens if we add another container:

```python hl_lines="31-34"
--8<-- "docs/examples/how-to/containers04.py"
```

And here's the result:

```{.textual path="docs/examples/how-to/containers04.py"}
```

Two horizontal containers divide the remaining screen space in two.
If you were to add another horizontal it would divide the screen space in to thirds&mdash;and so on.

This makes `Horizontal` and `Vertical` excellent for designing the macro layout of your app's interface, but not for making tightly packed rows or columns. For that you need the *group* containers which I'll cover next.

!!! tip "FR Units"

    You can implement this behavior of dividing the screen in your own widgets with [FR units](../guide/styles.md#fr-units)


## Group containers

The [HorizontalGroup][textual.containers.HorizontalGroup] and [VerticalGroup][textual.containers.VerticalGroup] containers are very similar to their non-group counterparts, but don't expand to fill the screen space.

Let's look at an example.
In the following code, we have two HorizontalGroups with a border so we can visualize their size.

```python hl_lines="2 27 31"
--8<-- "docs/examples/how-to/containers05.py"
```

Here's the output:

```{.textual path="docs/examples/how-to/containers05.py"}
```

We can see that the widgets are arranged horizontally as before, but they only use as much vertical space as required to fit.

## Scrolling containers

Something to watch out for regarding the previous containers we have discussed, is that they don't scroll by default.
Let's see what happens if we add more boxes than could fit on the screen.

In the following example, we will add 10 boxes:

```python hl_lines="28 29"
--8<-- "docs/examples/how-to/containers06.py"
```

Here's the output:

```{.textual path="docs/examples/how-to/containers06.py"}
```

We have add 10 `Box` widgets, but there is not enough room for them to fit.
The remaining boxes are off-screen and can't be viewed unless the user resizes their screen.

If we expect more content that fits, we can replacing the containers with [HorizontalScroll][textual.containers.HorizontalScroll] or [VerticalScroll][textual.containers.VerticalScroll], which will automatically add scrollbars if required.

Let's make that change:

```python hl_lines="2 27"
--8<-- "docs/examples/how-to/containers07.py"
```

Here's the output:

```{.textual path="docs/examples/how-to/containers07.py"}
```

We now have a scrollbar we can click and drag to see all the boxes.

!!! tip "Automatic scrollbars"  

    You can also implement automatic scrollbars with the [overflow](../styles/overflow.md) style.


## Center, Right, and Middle

The [Center][textual.containers.Center], [Right][textual.containers.Right], and [Middle][textual.containers.Middle] containers are handy for setting the alignment of select widgets.

First lets look at `Center` and `Right` which align their children on the horizontal axis (there is no `Left` container, as this is the default).

Here's an example:

```python hl_lines="2 28 30"
--8<-- "docs/examples/how-to/containers08.py"
```

1. The default is to align widgets to the left.
2. Align the child to the center.
3. Align the child to the right edge.

Here's the output:

```{.textual path="docs/examples/how-to/containers08.py"}
```

Note how `Center` and `Right` expand to fill the horizontal dimension, but are only as tall as they need to be.

!!! tip "Alignment in TCSS"

    You can set alignment in TCSS with the [align](../styles/align.md) rule.

The [Middle][textual.containers.Middle] container aligns its children to the center of the *vertical* axis.
Let's look at an example.
The following code aligns three boxes on the vertical axis:

```python hl_lines="2 27"
--8<-- "docs/examples/how-to/containers09.py"
```

1. Align children to the center of the vertical axis.

Here's the output:

```{.textual path="docs/examples/how-to/containers09.py"}
```

Note how the container expands on the vertical axis, but fits on the horizontal axis.

## Other containers

This how-to covers the most common widgets, but isn't exhausted.
Be sure to visit the [container reference][textual.containers] for the full list.
There may be new containers added in future versions of Textual.

## Custom containers

The builtin [containers][textual.containers] cover a number of common layout patterns, but are unlikely to cover every possible requirement.
Fortunately, creating your own is easy.
Just like the builtin containers, you can create a container by extending Widget and adding little TCSS.

Here's a template for a custom container:

```python
class MyContainer(Widget):
    """My custom container."""    
    DEFAULT_CSS = """
    MyContainer {
        # Your rules here
    }
    """    
```

## Summary

- Containers are compound widgets with preset styles for arranging their children.
- [`Horizontal`][textual.containers.Horizontal] and [`Vertical`][textual.containers.Vertical] containers stretch to fill available space.
- [`HorizontalGroup`][textual.containers.HorizontalGroup] and [`VerticalGroup`][textual.containers.VerticalGroup] fit to the height of their contents.
- [`HorizontalScroll`][textual.containers.HorizontalScroll] and [`VerticalScroll`][textual.containers.VerticalScroll] add automatic scrollbars.
- [`Center`][textual.containers.Center], [`Right`][textual.containers.Right], and [`Middle`][textual.containers.Middle] set alignment.
- Custom containers are trivial to create.
--- END OF FILE docs/how-to/work-with-containers.md ---


--- START OF FILE docs/examples/guide/layout/combining_layouts.py ---
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Header, Static


class CombiningLayoutsExample(App):
    CSS_PATH = "combining_layouts.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="app-grid"):
            with VerticalScroll(id="left-pane"):
                for number in range(15):
                    yield Static(f"Vertical layout, child {number}")
            with Horizontal(id="top-right"):
                yield Static("Horizontally")
                yield Static("Positioned")
                yield Static("Children")
                yield Static("Here")
            with Container(id="bottom-right"):
                yield Static("This")
                yield Static("panel")
                yield Static("is")
                yield Static("using")
                yield Static("grid layout!", id="bottom-right-final")


if __name__ == "__main__":
    app = CombiningLayoutsExample()
    app.run()
--- END OF FILE docs/examples/guide/layout/combining_layouts.py ---


--- START OF FILE docs/examples/guide/layout/dock_layout1_sidebar.py ---
from textual.app import App, ComposeResult
from textual.widgets import Static

TEXT = """\
Docking a widget removes it from the layout and fixes its position, aligned to either the top, right, bottom, or left edges of a container.

Docked widgets will not scroll out of view, making them ideal for sticky headers, footers, and sidebars.

"""


class DockLayoutExample(App):
    CSS_PATH = "dock_layout1_sidebar.tcss"

    def compose(self) -> ComposeResult:
        yield Static("Sidebar", id="sidebar")
        yield Static(TEXT * 10, id="body")


if __name__ == "__main__":
    app = DockLayoutExample()
    app.run()
--- END OF FILE docs/examples/guide/layout/dock_layout1_sidebar.py ---


--- START OF FILE docs/examples/guide/layout/grid_layout1.py ---
from textual.app import App, ComposeResult
from textual.widgets import Static


class GridLayoutExample(App):
    CSS_PATH = "grid_layout1.tcss"

    def compose(self) -> ComposeResult:
        yield Static("One", classes="box")
        yield Static("Two", classes="box")
        yield Static("Three", classes="box")
        yield Static("Four", classes="box")
        yield Static("Five", classes="box")
        yield Static("Six", classes="box")


if __name__ == "__main__":
    app = GridLayoutExample()
    app.run()
--- END OF FILE docs/examples/guide/layout/grid_layout1.py ---


--- START OF FILE docs/examples/guide/layout/horizontal_layout.py ---
from textual.app import App, ComposeResult
from textual.widgets import Static


class HorizontalLayoutExample(App):
    CSS_PATH = "horizontal_layout.tcss"

    def compose(self) -> ComposeResult:
        yield Static("One", classes="box")
        yield Static("Two", classes="box")
        yield Static("Three", classes="box")


if __name__ == "__main__":
    app = HorizontalLayoutExample()
    app.run()
--- END OF FILE docs/examples/guide/layout/horizontal_layout.py ---


--- START OF FILE docs/examples/guide/layout/layers.py ---
from textual.app import App, ComposeResult
from textual.widgets import Static


class LayersExample(App):
    CSS_PATH = "layers.tcss"

    def compose(self) -> ComposeResult:
        yield Static("box1 (layer = above)", id="box1")
        yield Static("box2 (layer = below)", id="box2")


if __name__ == "__main__":
    app = LayersExample()
    app.run()
--- END OF FILE docs/examples/guide/layout/layers.py ---


--- START OF FILE docs/examples/guide/layout/vertical_layout.py ---
from textual.app import App, ComposeResult
from textual.widgets import Static


class VerticalLayoutExample(App):
    CSS_PATH = "vertical_layout.tcss"

    def compose(self) -> ComposeResult:
        yield Static("One", classes="box")
        yield Static("Two", classes="box")
        yield Static("Three", classes="box")


if __name__ == "__main__":
    app = VerticalLayoutExample()
    app.run()
--- END OF FILE docs/examples/guide/layout/vertical_layout.py ---


