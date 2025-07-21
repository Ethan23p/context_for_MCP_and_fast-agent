# Context for: fast-agent

## Directory Structure

```fast-agent/
└── scripts
    ├── event_replay.py
    ├── event_summary.py
    └── test_package_install.sh
```
---

## File Contents

--- START OF FILE scripts/event_replay.py ---
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
--- END OF FILE scripts/event_replay.py ---


--- START OF FILE scripts/event_summary.py ---
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
--- END OF FILE scripts/event_summary.py ---


--- START OF FILE scripts/test_package_install.sh ---
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
--- END OF FILE scripts/test_package_install.sh ---


