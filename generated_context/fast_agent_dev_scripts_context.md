# Project: scripts

## Directory Structure

```
📁 scripts
├── 📄 event_replay.py
├── 📄 event_summary.py
├── 📄 event_viewer.py
├── 📄 example.py
├── 📄 format.py
├── 📄 gen_schema.py
├── 📄 lint.py
├── 📄 promptify.py
├── 📄 rich_progress_test.py
└── 📄 test_package_install.sh
```

------------------------------------------------------------

## File Contents

--- START OF FILE event_replay.py ---
#!/usr/bin/env python3
"""Event Replay Script

Replays events from a JSONL log file using rich_progress display.
"""

import json
import time
from datetime import datetime
from pathlib import Path

import typer

from mcp_agent.event_progress import convert_log_event
from mcp_agent.logging.events import Event
from mcp_agent.logging.rich_progress import RichProgressDisplay


def load_events(path: Path) -> list[Event]:
    """Load events from JSONL file."""
    events = []
    with open(path) as f:
        for line in f:
            if line.strip():
                raw_event = json.loads(line)
                # Convert from log format to event format
                event = Event(
                    type=raw_event.get("level", "info").lower(),
                    namespace=raw_event.get("namespace", ""),
                    message=raw_event.get("message", ""),
                    timestamp=datetime.fromisoformat(raw_event["timestamp"]),
                    data=raw_event.get("data", {}),  # Get data directly
                )
                events.append(event)
    return events


def main(log_file: str) -> None:
    """Replay MCP Agent events from a log file with progress display."""
    # Load events from file
    events = load_events(Path(log_file))

    # Initialize progress display
    progress = RichProgressDisplay()
    progress.start()

    try:
        # Process each event in sequence
        for event in events:
            progress_event = convert_log_event(event)
            if progress_event:
                # Add agent info to the progress event target from data
                progress.update(progress_event)
                # Add a small delay to make the replay visible
                time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        progress.stop()


if __name__ == "__main__":
    typer.run(main)

--- END OF FILE event_replay.py ---


--- START OF FILE event_summary.py ---
#!/usr/bin/env python3
"""MCP Event Summary"""

import json
from datetime import datetime
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from mcp_agent.event_progress import ProgressAction, convert_log_event
from mcp_agent.logging.events import Event


def load_events(path: Path) -> list[Event]:
    """Load events from JSONL file."""
    events = []
    with open(path) as f:
        for line in f:
            if line.strip():
                raw_event = json.loads(line)
                # Convert from log format to event format
                event = Event(
                    type=raw_event.get("level", "info").lower(),
                    namespace=raw_event.get("namespace", ""),
                    message=raw_event.get("message", ""),
                    timestamp=datetime.fromisoformat(raw_event["timestamp"]),
                    data=raw_event.get("data", {}),  # Get data directly
                )
                events.append(event)
    return events


def create_event_table(events: list[Event]) -> Table:
    """Create a rich table for displaying events."""

    # Convert events to progress events
    progress_events = []
    for event in events:
        progress_event = convert_log_event(event)
        if progress_event:
            if not progress_events or str(progress_event) != str(progress_events[-1]):
                # Store tuple of (progress_event, original_event)
                progress_events.append((progress_event, event))

    # Create table
    table = Table(show_header=True, header_style="bold", show_lines=True)
    table.add_column("Agent", style="yellow", width=20)
    table.add_column("Action", style="cyan", width=12)
    table.add_column("Target", style="green", width=30)
    table.add_column("Details", style="magenta", width=30)

    # Add events
    for progress_event, orig_event in progress_events:
        # Extract agent name from data or fallback to namespace
        try:
            agent = orig_event.data.get("data", {}).get("agent_name", "")
            if not agent:  # Fallback to namespace if agent_name not found
                agent = orig_event.namespace.split(".")[-1] if orig_event.namespace else ""
        except (AttributeError, KeyError):
            # Fallback to namespace if there's any error accessing data
            agent = orig_event.namespace.split(".")[-1] if orig_event.namespace else ""
        table.add_row(
            agent,
            progress_event.action.value,
            progress_event.target,
            progress_event.details or "",
        )

    return table


def create_summary_panel(events: list[Event]) -> Panel:
    """Create a summary panel with stats."""

    text = Text()

    # Count various event types
    chatting = 0
    tool_calls = 0
    mcps = set()

    for event in events:
        if event.type == "info":
            if "mcp_connection_manager" in event.namespace:
                message = event.message
                if ": " in message:
                    mcp_name = message.split(": ")[0]
                    mcps.add(mcp_name)

        progress_event = convert_log_event(event)
        if progress_event:
            if progress_event.action == ProgressAction.CHATTING:
                chatting += 1
            elif progress_event.action == ProgressAction.CALLING_TOOL:
                tool_calls += 1

    text.append("Summary:\n\n", style="bold")
    text.append("MCPs: ", style="bold")
    text.append(f"{', '.join(sorted(mcps))}\n", style="green")
    text.append("Chat Turns: ", style="bold")
    text.append(f"{chatting}\n", style="blue")
    text.append("Tool Calls: ", style="bold")
    text.append(f"{tool_calls}\n", style="magenta")

    return Panel(text, title="Event Statistics")


def main(log_file: str) -> None:
    """View MCP Agent events from a log file."""
    events = load_events(Path(log_file))
    console = Console()

    # Create layout
    console.print("\n")
    console.print(create_summary_panel(events))
    console.print("\n")
    console.print(Panel(create_event_table(events), title="Progress Events"))
    console.print("\n")


if __name__ == "__main__":
    typer.run(main)

--- END OF FILE event_summary.py ---


--- START OF FILE event_viewer.py ---
#!/usr/bin/env python3
"""MCP Event Viewer"""

import json
import sys
import termios
import tty
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text

from mcp_agent.event_progress import ProgressEvent, convert_log_event
from mcp_agent.logging.events import Event


def get_key() -> str:
    """Get a single keypress."""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


class EventDisplay:
    """Display MCP events from a log file."""

    def __init__(self, events: List[Event]) -> None:
        self.events = events
        self.total = len(events)
        self.current = 0
        self.current_iteration: Optional[int] = None
        self.tool_calls = 0
        self.progress_events: List[ProgressEvent] = []
        self._process_current()

    def next(self, steps: int = 1) -> None:
        """Move forward n steps."""
        for _ in range(steps):
            if self.current < self.total - 1:
                self.current += 1
                self._process_current()

    def prev(self, steps: int = 1) -> None:
        """Move backward n steps."""
        if self.current > 0:
            self.current = max(0, self.current - steps)
            # Need to rebuild progress events up to this point
            self._rebuild_progress_events()

    def _rebuild_progress_events(self) -> None:
        """Rebuild progress events up to current position."""
        self.progress_events = []
        for i in range(self.current + 1):
            progress_event = convert_log_event(self.events[i])
            if progress_event:
                if not self.progress_events or str(progress_event) != str(self.progress_events[-1]):
                    self.progress_events.append(progress_event)

    def _process_current(self) -> None:
        """Process the current event."""
        event = self.events[self.current]
        message = event.message

        # Track iterations
        if "Iteration" in message:
            try:
                self.current_iteration = int(message.split("Iteration")[1].split(":")[0])
            except (ValueError, IndexError):
                pass

        # Track tool calls
        if "Tool call" in message or "Calling tool" in message:
            self.tool_calls += 1

        # Update progress events
        progress_event = convert_log_event(event)
        if progress_event:
            if not self.progress_events or str(progress_event) != str(self.progress_events[-1]):
                self.progress_events.append(progress_event)

    def render(self) -> Panel:
        """Render current event state."""
        # Create the main layout
        main_layout = Layout()

        # State section
        state_text = Text()
        state_text.append("Current Status:\n", style="bold")
        state_text.append("Iteration: ", style="bold")
        state_text.append(f"{self.current_iteration or 'None'}\n", style="blue")
        state_text.append(f"Event: {self.current + 1}/{self.total}\n", style="cyan")
        state_text.append(f"Tool Calls: {self.tool_calls}\n", style="magenta")

        # Current event details
        if self.events:
            event = self.events[self.current]
            event_str = f"[{event.type}] {event.namespace}: {event.message}"
            # Get console width and account for panel borders/padding
            max_width = Console().width - 4
            if len(event_str) > max_width:
                event_str = event_str[: max_width - 3] + "..."
            state_text.append(event_str + "\n", style="yellow")

        # Progress event section
        if self.progress_events:
            latest_event = self.progress_events[-1]
            progress_text = Text("\nLatest Progress Event:\n", style="bold")
            progress_text.append("Action: ", style="bold")
            progress_text.append(f"{latest_event.action}\n", style="cyan")
            progress_text.append("Target: ", style="bold")
            progress_text.append(f"{latest_event.target}\n", style="green")
            # Add agent name from event data
            try:
                current_event = self.events[self.current]
                agent = current_event.data.get("data", {}).get("agent_name", "")
                if not agent:  # Fallback to namespace if agent_name not found
                    agent = current_event.namespace.split(".")[-1] if current_event.namespace else ""
                if agent:
                    progress_text.append("Agent: ", style="bold")
                    progress_text.append(f"{agent}\n", style="yellow")
            except (AttributeError, KeyError):
                pass  # Skip agent display if data is malformed

            if latest_event.details:
                progress_text.append("Details: ", style="bold")
                progress_text.append(f"{latest_event.details}\n", style="magenta")
        else:
            progress_text = Text("\nNo progress events yet\n", style="dim")

        # Controls
        controls_text = Text(
            "\n[h] prev • [l] next • [H] prev x10 • [L] next x10 • [q] quit",
            style="dim",
        )

        # Combine sections into layout
        main_layout.split(
            Layout(Panel(state_text, title="Status"), size=8),
            Layout(Panel(progress_text, title="Progress"), size=8),
            Layout(Panel(controls_text, title="Controls"), size=5),
        )

        return Panel(main_layout, title="MCP Event Viewer")


def load_events(path: Path) -> List[Event]:
    """Load events from JSONL file."""
    events = []
    print(f"Loading events from {path}")  # Debug
    try:
        with open(path) as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    try:
                        raw_event = json.loads(line)
                        # Convert from log format to event format
                        event = Event(
                            type=raw_event.get("level", "info").lower(),
                            namespace=raw_event.get("namespace", ""),
                            message=raw_event.get("message", ""),
                            timestamp=datetime.fromisoformat(raw_event["timestamp"]),
                            data=raw_event.get("data", {}),
                        )
                        events.append(event)
                    except Exception as e:
                        print(f"Error on line {line_num}: {e}")
                        print(f"Line content: {line.strip()}")
                        raise
    except Exception as e:
        print(f"Error loading file: {e}")
        raise

    print(f"Loaded {len(events)} events")  # Debug
    return events


def main(log_file: str) -> None:
    """View MCP Agent events from a log file."""
    events = load_events(Path(log_file))
    if not events:
        print("No events loaded!")
        return

    display = EventDisplay(events)
    console = Console()

    # Main display loop
    while True:
        # Clear screen and show current state
        # TODO turn this in to a live display
        console.clear()
        console.print(display.render())

        # Get input
        try:
            key = get_key()

            if key == "l":  # Next one step
                display.next()
            elif key == "L":  # Next ten steps
                display.next(10)
            elif key == "h":  # Previous one step
                display.prev()
            elif key == "H":  # Previous ten steps
                display.prev(10)
            elif key in {"q", "Q"}:  # Quit
                break
        except Exception as e:
            print(f"\nError handling input: {e}")
            break


if __name__ == "__main__":
    typer.run(main)

--- END OF FILE event_viewer.py ---


--- START OF FILE example.py ---
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "rich",
#     "typer",
# ]
# ///
"""
Run a specific example from the MCP Agent examples/ directory.
"""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import typer
from rich.console import Console

app = typer.Typer(help="Manage MCP Agent examples")
console = Console()


def create_venv(example_dir: Path) -> Path:
    """Create a virtual environment if it doesn't exist."""
    venv_dir = example_dir / ".venv"
    if not venv_dir.exists():
        console.print(f"Creating virtual environment in [cyan]{venv_dir}[/]")
        subprocess.run(["uv", "venv", str(venv_dir)], check=True)
        # venv.create(venv_dir, with_pip=True)
    return venv_dir


def clean_venv(example_dir: Path) -> None:
    """Remove the virtual environment if it exists."""
    venv_dir = example_dir / ".venv"
    if venv_dir.exists():
        console.print(f"Removing virtual environment in [cyan]{venv_dir}[/]")
        shutil.rmtree(venv_dir)


def get_python_path(venv_dir: Path) -> Path:
    """Get the python executable path for the virtual environment."""
    # Run the example using the venv's Python
    python_path = (venv_dir / "bin" / "python").resolve()
    if not python_path.exists():
        python_path = (venv_dir / "Scripts" / "python").resolve()  # Windows path

    return python_path


def get_site_packages(venv_dir: Path, python_path: Path) -> Path:
    """Get the site-packages directory for the virtual environment."""
    # Construct site-packages path based on platform
    if (venv_dir / "lib").exists():  # Unix-like
        # Get Python version (e.g., "3.10")
        result = subprocess.run(
            [
                str(python_path),
                "-c",
                "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        python_version = result.stdout.strip()
        return venv_dir / "lib" / f"python{python_version}" / "site-packages"
    else:  # Windows
        return venv_dir / "Lib" / "site-packages"


def create_requirements_file(example_dir: Path, use_local: bool, version: str | None) -> Path:
    """Create a temporary requirements file with the correct mcp-agent source."""
    temp_req = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt")

    with open(file=example_dir / "requirements.txt", mode="r", encoding="utf-8") as f:
        requirements = f.readlines()

    with open(file=temp_req.name, mode="w", encoding="utf-8") as f:
        # TODO: saqadri - consider just copying the original requirements file
        # f.writelines(requirements)
        for req in requirements:
            if not (req.strip().startswith("-e") or req.strip().startswith("mcp-agent")):
                f.write(req)

        f.write("\n")

        if use_local:
            # Add the local source
            f.write("-e ../../\n")
            # f.write("mcp-agent @ file://../../\n")
        else:
            # Add the PyPI version
            version_str = f"=={version}" if version else ""
            f.write(f"mcp-agent{version_str}\n")

    return Path(temp_req.name)


@app.command(name="list")
def list_examples() -> None:
    """List all available examples."""
    examples_dir = Path("examples")
    if not examples_dir.exists():
        console.print("[red]No examples directory found[/]")
        raise typer.Exit(1)

    examples = [d for d in examples_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]

    if not examples:
        console.print("No examples found")
        return

    console.print("\n[bold]Available examples:[/]")
    for example in examples:
        example_readme = example / "README.md"
        description = ""
        if example_readme.exists():
            with open(file=example_readme, mode="r", encoding="utf-8") as f:
                # Get first line of README as description
                description = f.readline().strip("#").strip()

        console.print(f"• [cyan]{example.name}[/] - {description}")


@app.command()
def run(
    example_name: str = typer.Argument(..., help="Name of the example to run"),
    use_local: bool = typer.Option(True, "--local", "-l", help="Use local version of mcp-agent"),
    version: str | None = typer.Option(None, "--version", "-v", help="Specific version to install from PyPI"),
    clean: bool = typer.Option(False, "--clean", "-c", help="Create a fresh virtual environment"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Print debug information"),
) -> None:
    """Run a specific example."""
    examples_dir = Path("examples").resolve()
    example_dir = (examples_dir / example_name).resolve()
    project_root = Path(__file__).resolve().parent.parent

    if not example_dir.exists():
        console.print(f"[red]Example '{example_name}' not found[/]")
        raise typer.Exit(1)

    # Clean if requested
    if clean:
        clean_venv(example_dir)

    # with console.status(f"Setting up example: {example_name}") as status:
    venv_dir = create_venv(example_dir)
    temp_req = create_requirements_file(example_dir, use_local, version)
    python_path = get_python_path(venv_dir)
    site_packages = get_site_packages(venv_dir, python_path)

    if debug:
        console.print(f"Using Python: {python_path}")
        console.print(f"Using site-packages: {site_packages}")

    env = {
        **os.environ,
        "VIRTUAL_ENV": str(venv_dir),
        "PYTHONPATH": f"{str(site_packages)}:{str(project_root)}/src",
    }

    try:
        # Install dependencies using uv
        console.print("Installing dependencies...")

        result = subprocess.run(
            ["uv", "pip", "install", "-r", str(temp_req)],
            cwd=example_dir,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            console.print(f"[red]Error installing dependencies:[/]\n{result.stderr}")
            raise typer.Exit(1)
        else:
            pass
            # status.update("[green]Dependencies installed successfully[/]")

        # Debug: List installed packages
        if debug:
            console.print("\nInstalled packages:")
            subprocess.run(
                ["uv", "pip", "list"],
                cwd=example_dir,
                env=env,
                check=True,
            )

            console.print("\nPython path:")
            subprocess.run(
                [str(python_path), "-c", "import sys; print('\\n'.join(sys.path))"],
                cwd=example_dir,
                env=env,
                check=True,
            )

        # Run the example
        console.print(f"\n[bold green]Running {example_name}[/]\n")
        # status.update(f"Running {example_name}")
        subprocess.run(
            [str(python_path), "main.py"],
            cwd=example_dir,
            env=env,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error: {e}")
        raise typer.Exit(1)
    finally:
        temp_req.unlink()


@app.command(name="clean")
def clean_env(
    example_name: str | None = typer.Argument(None, help="Name of the example to clean, or all if not specified"),
) -> None:
    """Clean up virtual environments from examples."""
    examples_dir = Path("examples")

    if example_name:
        dirs = [examples_dir / example_name]
    else:
        dirs = [d for d in examples_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]

    for d in dirs:
        clean_venv(d)


if __name__ == "__main__":
    app()

--- END OF FILE example.py ---


--- START OF FILE format.py ---
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "ruff",
#     "typer",
# ]
# ///

import subprocess
import sys

import typer
from rich import print


def main(path: str = None) -> None:
    try:
        command = ["ruff", "format"]

        if path:
            command.append(path)

        # Run `ruff` and pipe output to the terminal
        process = subprocess.run(
            command,
            check=True,
            stdout=sys.stdout,  # Redirect stdout to the terminal
            stderr=sys.stderr,  # Redirect stderr to the terminal
        )
        sys.exit(process.returncode)  # Exit with the same code as the command
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")  # Log the error in a user-friendly way
        sys.exit(e.returncode)  # Exit with the error code from the command
    except FileNotFoundError:
        print("Error: `ruff` command not found. Make sure it's installed in the environment.")
        sys.exit(1)


if __name__ == "__main__":
    typer.run(main)

--- END OF FILE format.py ---


--- START OF FILE gen_schema.py ---
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "rich",
#     "typer",
#     "pydantic>=2.10.4",
#     "pydantic-settings>=2.7.0"
# ]
# ///
"""
Generate JSON schema for MCP Agent configuration (mcp-agent.config.yaml).
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

import typer
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from rich.console import Console

app = typer.Typer()
console = Console()


def extract_model_info(content: str) -> Dict[str, Dict[str, str]]:
    """
    Extract docstrings for all models and their fields.
    Returns a dict mapping model names to their field descriptions.
    """
    models = {}
    current_model = None

    # Split content into lines for processing
    lines = content.splitlines()

    for i, line in enumerate(lines):
        # Look for class definition
        class_match = re.match(r"\s*class\s+(\w+)(?:\([^)]+\))?\s*:", line.strip())
        if class_match:
            current_model = class_match.group(1)
            models[current_model] = {"__doc__": ""}

            # Look for class docstring
            for j in range(i + 1, min(i + 4, len(lines))):
                doc_match = re.match(r'\s*"""(.+?)"""', lines[j], re.DOTALL)
                if doc_match:
                    models[current_model]["__doc__"] = doc_match.group(1).strip()
                    break
            continue

        # If we're inside a model definition, look for field definitions
        if current_model:
            # Check if we've exited the class definition (unindented line that's not empty or comment)
            if line and not line.startswith(" ") and not line.startswith("#"):
                current_model = None
                continue

            # Look for field definitions with type annotations
            field_match = re.match(r"\s+(\w+)\s*:", line)
            if field_match:
                field_name = field_match.group(1)

                # Skip if this is model_config or other special attributes
                if field_name in ("model_config", "Config"):
                    continue

                description = None

                # Look for Field description in the current line
                field_desc_match = re.search(r'Field\([^)]*description="([^"]+)"', line)
                if field_desc_match:
                    description = field_desc_match.group(1).strip()
                else:
                    # Look ahead for docstring until we hit another field definition or non-empty, non-docstring line
                    for j in range(i + 1, min(i + 4, len(lines))):
                        next_line = lines[j].strip()
                        # If we hit a non-empty line that's not a docstring, stop looking
                        if next_line and not next_line.startswith('"""'):
                            break
                        # Try to match docstring
                        doc_match = re.match(r'\s*"""(.+?)"""', lines[j], re.DOTALL)
                        if doc_match:
                            description = doc_match.group(1).strip()
                            break

                if description:
                    models[current_model][field_name] = description

    # Debug output
    console.print("\nFound models and their field descriptions:")
    for model, fields in models.items():
        console.print(f"\n[bold]{model}[/bold]: {fields.get('__doc__', '')}")
        for field, desc in fields.items():
            if field != "__doc__":
                console.print(f"  {field}: {desc}")

    return models


class MockModule:
    """Mock module that returns itself for any attribute access."""

    def __getattr__(self, _: str) -> Any:
        return self

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self


def create_mock_modules() -> None:
    """Create mock modules for imports we want to ignore."""
    mocked_modules = [
        "opentelemetry",
        "opentelemetry.sdk",
        "opentelemetry.sdk.trace",
        "opentelemetry.sdk.resources",
        "opentelemetry.exporter.otlp.proto.http",
        "opentelemetry.trace",
        "mcp_agent.logging",
        "mcp_agent.logging.logger",
        "yaml",
    ]

    for module_name in mocked_modules:
        if module_name not in sys.modules:
            sys.modules[module_name] = MockModule()


def load_settings_class(
    file_path: Path,
) -> Tuple[type[BaseSettings], Dict[str, Dict[str, str]]]:
    """Load Settings class from a Python file."""
    # Add src directory to Python path
    src_dir = file_path.parent.parent.parent / "src"
    sys.path.insert(0, str(src_dir))

    # Mock required modules
    create_mock_modules()

    # Create namespace with required classes
    namespace = {
        "BaseModel": BaseModel,
        "BaseSettings": BaseSettings,
        "Path": Path,
        "Dict": dict,
        "List": list,
        "Literal": str,  # Simplified for schema
    }

    with open(file_path, mode="r", encoding="utf-8") as f:
        content = f.read()

    # Extract all model info before executing
    model_info = extract_model_info(content)

    # Execute the file
    exec(content, namespace)

    return namespace["Settings"], model_info


def apply_descriptions_to_schema(
    schema: Dict[str, Any], model_info: Dict[str, Dict[str, str]]
) -> None:
    """Recursively apply descriptions to schema and all its nested models."""
    if not isinstance(schema, dict):
        return

    # Handle $defs (nested model definitions)
    if "$defs" in schema:
        for model_name, model_schema in schema["$defs"].items():
            if model_name in model_info:
                # Apply class docstring
                doc = model_info[model_name].get("__doc__", "").strip()
                if doc:
                    model_schema["description"] = doc

                # Apply field descriptions
                if "properties" in model_schema:
                    for field_name, field_schema in model_schema["properties"].items():
                        if field_name in model_info[model_name]:
                            field_schema["description"] = model_info[model_name][field_name].strip()

    # Handle root properties
    if "properties" in schema:
        for field_name, field_schema in schema["properties"].items():
            if "Settings" in model_info and field_name in model_info["Settings"]:
                field_schema["description"] = model_info["Settings"][field_name].strip()


@app.command()
def generate(
    config_py: Path = typer.Option(
        Path("src/mcp_agent/config.py"),
        "--config",
        "-c",
        help="Path to the config.py file",
    ),
    output: Path = typer.Option(
        Path(".vscode/fastagent.config.schema.json"),
        "--output",
        "-o",
        help="Output path for the schema file",
    ),
) -> None:
    """Generate JSON schema from Pydantic models in config.py"""
    if not config_py.exists():
        console.print(f"[red]Error:[/] File not found: {config_py}")
        raise typer.Exit(1)

    try:
        Settings, model_info = load_settings_class(config_py)
        schema = Settings.model_json_schema()

        # Debug: Print raw schema structure before modifications
        console.print("\nSchema structure:")
        if "$defs" in schema:
            console.print("Found models in $defs:", list(schema["$defs"].keys()))

        # Add schema metadata
        schema.update(
            {
                "$schema": "http://json-schema.org/draft-07/schema#",
                "title": "MCP Agent Configuration Schema",
                "description": "Configuration schema for MCP Agent applications",
            }
        )

        # Apply descriptions to all nested models recursively
        apply_descriptions_to_schema(schema, model_info)

        # Ensure output directory exists
        output.parent.mkdir(parents=True, exist_ok=True)

        # Make output path absolute if it isn't already
        output = output.absolute()

        # Write schema
        with open(output, "w") as f:
            json.dump(schema, f, indent=2)

        console.print(f"[green]✓[/] Schema written to: {output}")

        # Get path relative to cwd for VS Code settings
        try:
            rel_path = f"./{output.relative_to(Path.cwd())}"
        except ValueError:
            # If can't make relative, use absolute path
            rel_path = str(output)

        # Print VS Code settings suggestion
        vscode_settings = {
            "yaml.schemas": {
                rel_path: [
                    "mcp-agent.config.yaml",
                    "mcp_agent.config.yaml",
                    "mcp-agent.secrets.yaml",
                    "mcp_agent.secrets.yaml",
                ]
            }
        }
        console.print("\n[yellow]VS Code Integration:[/]")
        console.print("Add this to .vscode/settings.json:")
        console.print(json.dumps(vscode_settings, indent=2))

    except Exception as e:
        console.print(f"[red]Error generating schema:[/] {str(e)}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

--- END OF FILE gen_schema.py ---


--- START OF FILE lint.py ---
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "ruff",
#     "typer",
# ]
# ///

import subprocess
import sys

import typer
from rich import print


def main(fix: bool = False, watch: bool = False, path: str = None) -> None:
    try:
        command = ["ruff", "check"]
        if fix:
            command.append("--fix")

        if watch:
            command.append("--watch")

        if path:
            command.append(path)

        # Run `ruff` and pipe output to the terminal
        process = subprocess.run(
            command,
            check=True,
            stdout=sys.stdout,  # Redirect stdout to the terminal
            stderr=sys.stderr,  # Redirect stderr to the terminal
        )
        sys.exit(process.returncode)  # Exit with the same code as the command
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")  # Log the error in a user-friendly way
        sys.exit(e.returncode)  # Exit with the error code from the command
    except FileNotFoundError:
        print("Error: `ruff` command not found. Make sure it's installed in the environment.")
        sys.exit(1)


if __name__ == "__main__":
    typer.run(main)

--- END OF FILE lint.py ---


--- START OF FILE promptify.py ---
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "rich",
#     "typer",
# ]
# ///
"""
Convert the project directory structure and file contents into a single markdown file.
Really helpful for using as a prompt for LLM code generation tasks.
"""

import fnmatch
from pathlib import Path
from typing import List

import typer
from rich.console import Console
from rich.tree import Tree


def parse_gitignore(path: Path) -> List[str]:
    """Parse .gitignore file and return list of patterns."""
    gitigore_path = path / ".gitignore"
    if not gitigore_path.exists():
        return []

    with open(file=gitigore_path, mode="r", encoding="utf-8") as f:
        patterns = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return patterns


def normalize_pattern(pattern: str) -> str:
    """
    Normalize a pattern by removing unnecessary whitespace and escaping special characters.
    """
    # Strip whitespace
    pattern = pattern.strip()
    return pattern


def pattern_match(path: str, pattern: str) -> bool:
    """
    Improved pattern matching that better handles **/ patterns and different path separators.
    """
    # Normalize the pattern first
    pattern = normalize_pattern(pattern)
    path = path.replace("\\", "/")  # Normalize path separators

    # Handle **/ prefix more flexibly
    if pattern.startswith("**/"):
        base_pattern = pattern[3:]  # Pattern without **/ prefix
        # Try matching both with and without the **/ prefix
        return fnmatch.fnmatch(path, base_pattern) or fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(path, f"**/{base_pattern}")

    # Handle *registry.py style patterns
    elif pattern.startswith("*") and not pattern.startswith("**/"):
        return fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(path, f"**/{pattern}")

    return fnmatch.fnmatch(path, pattern)


def should_include(path: Path, include_patterns: List[str]) -> bool:
    """Check if path should be included based on patterns."""
    if not include_patterns:
        return True

    str_path = str(path).replace("\\", "/")

    # For directories, we want to include them if they might contain matching files
    if path.is_dir():
        # If any pattern starts with the directory path, include it
        dir_path = str_path + "/"
        for pattern in include_patterns:
            pattern = normalize_pattern(pattern)
            if pattern.startswith("**/"):
                # Always include directories when we have **/ patterns
                return True
            # Check if this directory might contain matching files
            if fnmatch.fnmatch(dir_path + "anyfile", pattern):
                return True
        return False

    # For files, check against all patterns
    return any(pattern_match(str_path, p) for p in include_patterns)


def should_ignore(path: Path, ignore_patterns: List[str], gitignore_patterns: List[str]) -> bool:
    """Check if path should be ignored based on patterns."""
    str_path = str(path).replace("\\", "/")

    # Check custom ignore patterns
    for pattern in ignore_patterns:
        if pattern_match(str_path, pattern):
            return True

    # Check gitignore patterns
    for pattern in gitignore_patterns:
        if pattern_match(str_path, pattern):
            return True

    return False


def create_tree_structure(
    path: Path,
    include_patterns: List[str],
    ignore_patterns: List[str],
    gitignore_patterns: List[str],
) -> Tree:
    """Create a rich Tree representation of the directory structure."""
    tree = Tree(f"📁 {path.name}")

    def add_to_tree(current_path: Path, tree: Tree):
        items = sorted(current_path.iterdir())
        for item in items:
            # Skip if should be ignored
            if should_ignore(item, ignore_patterns, gitignore_patterns):
                continue

            # Check if item matches include patterns (if any)
            if not should_include(item, include_patterns):
                continue

            if item.is_file():
                tree.add(f"📄 {item.name}")
            elif item.is_dir():
                branch = tree.add(f"📁 {item.name}")
                add_to_tree(item, branch)

    add_to_tree(path, tree)
    return tree


def package_project(
    path: Path,
    output_file: Path,
    include_patterns: List[str],
    ignore_patterns: List[str],
    gitignore_patterns: List[str],
) -> None:
    """Package project files into a single markdown file."""
    # Normalize all patterns first
    include_patterns = [normalize_pattern(p) for p in include_patterns]
    ignore_patterns = [normalize_pattern(p) for p in ignore_patterns]
    gitignore_patterns = [normalize_pattern(p) for p in gitignore_patterns]

    with open(output_file, "w", encoding="utf-8") as f:
        # Write header
        f.write(f"# Project: {path.name}\n\n")

        # Write directory structure
        f.write("## Directory Structure\n\n")
        f.write("```\n")
        console = Console(file=None)
        with console.capture() as capture:
            console.print(create_tree_structure(path, include_patterns, ignore_patterns, gitignore_patterns))
        f.write(capture.get())
        f.write("```\n\n")

        # Write file contents
        f.write("## File Contents\n\n")

        def write_files(current_path: Path):
            for item in sorted(current_path.iterdir()):
                if should_ignore(item, ignore_patterns, gitignore_patterns):
                    continue

                if include_patterns and not should_include(item, include_patterns):
                    continue

                if item.is_file():
                    try:
                        with open(item, "r", encoding="utf-8") as source_file:
                            content = source_file.read()
                            f.write(f"### {item.relative_to(path)}\n\n")
                            f.write("```")
                            # Add file extension for syntax highlighting if available
                            if item.suffix:
                                f.write(item.suffix[1:])  # Remove the dot from extension
                            f.write("\n")
                            f.write(content)
                            f.write("\n```\n\n")
                    except UnicodeDecodeError:
                        f.write(f"### {item.relative_to(path)}\n\n")
                        f.write("```\nBinary file not included\n```\n\n")
                elif item.is_dir():
                    write_files(item)

        write_files(path)


def main(
    path: str = typer.Argument(".", help="Path to the project directory"),
    output: str = typer.Option("project_contents.md", "--output", "-o", help="Output file path"),
    include: List[str] | None = typer.Option(None, "--include", "-i", help="Patterns to include (e.g. '*.py')"),
    ignore: List[str] | None = typer.Option(None, "--ignore", "-x", help="Patterns to ignore"),
    skip_gitignore: bool = typer.Option(False, "--skip-gitignore", help="Skip reading .gitignore patterns"),
) -> None:
    """
    Package project files into a single markdown file with directory structure.
    """
    project_path = Path(path).resolve()
    output_path = Path(output).resolve()

    if not project_path.exists():
        typer.echo(f"Error: Project path '{path}' does not exist")
        raise typer.Exit(1)

    # Parse .gitignore if needed
    gitignore_patterns = [] if skip_gitignore else parse_gitignore(project_path)

    # Convert None to empty lists
    include_patterns = include or []
    ignore_patterns = ignore or []

    # Add some default ignore patterns
    # Default ignore patterns for Python development
    default_ignores = [
        "**/__pycache__/**",
        "**/.git/**",
        "**/.idea/**",
        "**/.vscode/**",
        "**/.ruff_cache/**",
        "**/.venv/**",
        "**/venv/**",
        "**/env/**",
        "**/uv.lock",
        "**/.pytest_cache/**",
        "**/*.pyc",
        "**/.coverage",
        "**/htmlcov/**",
    ]
    ignore_patterns.extend(default_ignores)

    try:
        package_project(
            project_path,
            output_path,
            include_patterns,
            ignore_patterns,
            gitignore_patterns,
        )
        typer.echo(f"Successfully packaged project to {output_path}")
    except Exception as e:
        typer.echo(f"Error packaging project: {str(e)}")
        raise typer.Exit(1)


if __name__ == "__main__":
    typer.run(main)

--- END OF FILE promptify.py ---


--- START OF FILE rich_progress_test.py ---
#!/usr/bin/env python3
"""Test script for demonstrating the Rich progress display."""

import asyncio
import random

from rich import print

from mcp_agent.logging.events import Event
from mcp_agent.logging.listeners import ProgressListener


async def generate_test_events():
    """Generate synthetic progress events for testing."""
    # Simulate an MCP session with multiple activities
    mcp_names = ["Assistant-1", "Helper-2", "Agent-3"]
    models = ["gpt-4", "claude-2", "mistral"]
    tools = [
        "developer__shell",
        "platform__read_resource",
        "computercontroller__web_search",
    ]

    for mcp_name in mcp_names:
        # Starting up
        yield Event(
            namespace="mcp_connection_manager",
            type="info",
            message=f"{mcp_name}: Initializing server session",
            data={},
        )
        # Simulate some other console output
        print(f"Debug: Connection established for {mcp_name}")
        await asyncio.sleep(0.5)

        # Initialized
        yield Event(
            namespace="mcp_connection_manager",
            type="info",
            message=f"{mcp_name}: Session initialized",
            data={},
        )
        await asyncio.sleep(0.5)

        # Simulate some chat turns
        for turn in range(1, 4):
            model = random.choice(models)

            # Start chat turn
            yield Event(
                namespace="mcp_agent.workflow.llm.augmented_llm_openai.myagent",
                type="info",
                message=f"Calling {model}",
                data={"model": model, "chat_turn": turn},
            )
            await asyncio.sleep(1)

            # Maybe call a tool
            if random.random() < 0.7:
                tool = random.choice(tools)
                print(f"Debug: Executing tool {tool}")  # More debug output
                yield Event(
                    namespace="mcp_aggregator",
                    type="info",
                    message=f"Requesting tool call '{tool}'",
                    data={},
                )
                await asyncio.sleep(0.8)

            # Finish chat turn
            yield Event(
                namespace="augmented_llm",
                type="info",
                message="Finished processing response",
                data={"model": model},
            )
            await asyncio.sleep(0.5)

        # Shutdown
        print(f"Debug: Shutting down {mcp_name}")  # More debug output
        yield Event(
            namespace="mcp_connection_manager",
            type="info",
            message=f"{mcp_name}: _lifecycle_task is exiting",
            data={},
        )
        await asyncio.sleep(1)


async def main() -> None:
    """Run the progress display test."""
    # Set up the progress listener
    listener = ProgressListener()
    await listener.start()

    try:
        async for event in generate_test_events():
            await listener.handle_event(event)
    except KeyboardInterrupt:
        print("\nTest interrupted!")
    finally:
        await listener.stop()


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE rich_progress_test.py ---


--- START OF FILE test_package_install.sh ---
#!/bin/bash
# Clean and recreate dist folder
rm -rf dist
mkdir -p dist
# Build the package
uv build

# Extract version from the built wheel
VERSION=$(ls dist/fast_agent_mcp-*.whl | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' | head -1)

# Create test folder
TEST_DIR="dist/test_install"
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Create virtual environment
uv venv .venv
source .venv/bin/activate

# Install the built package
uv pip install ../../dist/fast_agent_mcp-$VERSION-py3-none-any.whl

# Run the quickstart command
fast-agent quickstart workflow

# Check if workflows folder was created AND contains files
if [ -d "workflow" ] && [ -f "workflow/chaining.py" ] && [ -f "workflow/fastagent.config.yaml" ]; then
    echo "✅ Test successful: workflow examples created!"
else
    echo "❌ Test failed: workflow examples not created."
    echo "Contents of workflow directory:"
    ls -la workflow/ 2>/dev/null || echo "Directory doesn't exist"
    exit 1
fi


# Run the quickstart command
fast-agent quickstart state-transfer
if [ -d "state-transfer" ] && [ -f "state-transfer/agent_one.py" ] && [ -f "state-transfer/fastagent.config.yaml" ]; then
    echo "✅ Test successful: state-transfer examples created!"
else
    echo "❌ Test failed: state-transfer examples not created."
    echo "Contents of state-transfer directory:"
    ls -la state-transfer/ 2>/dev/null || echo "Directory doesn't exist"
    exit 1
fi

# Deactivate the virtual environment
deactivate

echo "Test completed successfully!"


--- END OF FILE test_package_install.sh ---



--- PROJECT PACKAGING COMPLETE ---