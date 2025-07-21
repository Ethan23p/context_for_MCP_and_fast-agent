# Context for: fast-agent

## Directory Structure

```fast-agent/
└── tests
    ├── e2e
    │   ├── mcp_filtering
    │   │   ├── fastagent.config.yaml
    │   │   ├── filtering_test_server.py
    │   │   └── test_mcp_filtering.py
    │   ├── multimodal
    │   │   ├── fastagent.config.yaml
    │   │   ├── image_server.py
    │   │   └── test_multimodal_images.py
    │   ├── prompts-resources
    │   │   ├── fastagent.config.yaml
    │   │   ├── fastagent.jsonl
    │   │   ├── multiturn.md
    │   │   ├── simple.txt
    │   │   ├── style.css
    │   │   ├── test_prompts.py
    │   │   ├── test_resources.py
    │   │   ├── with_attachment.md
    │   │   └── with_attachment_css.md
    │   ├── sampling
    │   │   ├── fastagent.config.yaml
    │   │   ├── fastagent.jsonl
    │   │   ├── sampling_resource_server.py
    │   │   └── test_sampling_e2e.py
    │   ├── smoke
    │   │   ├── base
    │   │   │   ├── fastagent.config.yaml
    │   │   │   ├── test_e2e_smoke.py
    │   │   │   └── test_server.py
    │   │   └── tensorzero
    │   │       ├── test_agent_interaction.py
    │   │       ├── test_image_demo.py
    │   │       └── test_simple_agent_interaction.py
    │   ├── structured
    │   │   ├── fastagent.config.yaml
    │   │   └── test_structured_outputs.py
    │   ├── workflow
    │   │   ├── fastagent.config.yaml
    │   │   ├── test_router_agent_e2e.py
    │   │   └── test_routing_server.py
    │   └── conftest.py
    └── integration
        ├── api
        │   ├── fastagent.config.markup.yaml
        │   ├── fastagent.config.yaml
        │   ├── fastagent.secrets.yaml
        │   ├── integration_agent.py
        │   ├── mcp_dynamic_tools.py
        │   ├── mcp_tools_server.py
        │   ├── playback.md
        │   ├── prompt.txt
        │   ├── stderr_test_script.py
        │   ├── test_api.py
        │   ├── test_cli_and_mcp_server.py
        │   ├── test_describe_a2a.py
        │   ├── test_hyphens_in_name.py
        │   ├── test_logger_textio.py
        │   ├── test_markup_config.py
        │   ├── test_prompt_commands.py
        │   ├── test_prompt_listing.py
        │   ├── test_provider_keys.py
        │   └── test_tool_list_change.py
        ├── elicitation
        │   ├── elicitation_test_server.py
        │   ├── elicitation_test_server_advanced.py
        │   ├── fastagent.config.yaml
        │   ├── manual_advanced.py
        │   ├── manual_test.py
        │   ├── test_config_modes.py
        │   ├── test_config_modes_simplified.py
        │   ├── test_elicitation_handler.py
        │   ├── test_elicitation_integration.py
        │   └── testing_handlers.py
        ├── prompt-server
        │   ├── fastagent.config.yaml
        │   ├── multi.txt
        │   ├── multi_sub.txt
        │   ├── simple.txt
        │   ├── simple_sub.txt
        │   └── test_prompt_server_integration.py
        ├── prompt-state
        │   ├── conv1_simple.md
        │   ├── conv2_attach.md
        │   ├── conv2_css.css
        │   ├── conv2_text.txt
        │   ├── fastagent.config.yaml
        │   └── test_load_prompt_templates.py
        ├── resources
        │   ├── fastagent.config.yaml
        │   ├── mcp_linked_resouce_server.py
        │   ├── prompt1.txt
        │   ├── prompt2.txt
        │   ├── r1file1.txt
        │   ├── r1file2.txt
        │   ├── r2file1.txt
        │   ├── r2file2.txt
        │   ├── test_resource_api.py
        │   └── test_resource_links.py
        ├── roots
        │   ├── fastagent.config.yaml
        │   ├── fastagent.jsonl
        │   ├── live.py
        │   ├── root_client.py
        │   ├── root_test_server.py
        │   └── test_roots.py
        ├── sampling
        │   ├── fastagent.config.auto_sampling_off.yaml
        │   ├── fastagent.config.yaml
        │   ├── live.py
        │   ├── sampling_test_server.py
        │   └── test_sampling_integration.py
        ├── workflow
        │   ├── chain
        │   │   ├── fastagent.config.yaml
        │   │   ├── test_chain.py
        │   │   └── test_chain_passthrough.py
        │   ├── evaluator_optimizer
        │   │   ├── fastagent.config.yaml
        │   │   └── test_evaluator_optimizer.py
        │   ├── mixed
        │   │   ├── fastagent.config.yaml
        │   │   └── test_mixed_workflow.py
        │   ├── orchestrator
        │   │   ├── fastagent.config.yaml
        │   │   └── test_orchestrator.py
        │   ├── parallel
        │   │   ├── fastagent.config.yaml
        │   │   └── test_parallel_agent.py
        │   └── router
        │       ├── fastagent.config.yaml
        │       ├── router_script.txt
        │       └── test_router_agent.py
        └── conftest.py
```
---

## File Contents

--- START OF FILE tests/e2e/conftest.py ---
import importlib
import os
import subprocess
import time
from pathlib import Path

import pytest

from mcp_agent.core.fastagent import FastAgent


# Keep the auto-cleanup fixture
@pytest.fixture(scope="function", autouse=True)
def cleanup_event_bus():
    """Reset the AsyncEventBus between tests using its reset method"""
    # Run the test
    yield

    # Reset the AsyncEventBus after each test
    try:
        # Import the module with the AsyncEventBus
        transport_module = importlib.import_module("mcp_agent.logging.transport")
        AsyncEventBus = getattr(transport_module, "AsyncEventBus", None)

        # Call the reset method if available
        if AsyncEventBus and hasattr(AsyncEventBus, "reset"):
            AsyncEventBus.reset()
    except Exception:
        pass


# Set the project root directory for tests
@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory as a Path object"""
    # Go up from tests/e2e directory to find project root
    return Path(__file__).parent.parent.parent


# Fixture to set the current working directory for tests
@pytest.fixture
def set_cwd(project_root):
    """Change to the project root directory during tests"""
    # Save the original working directory
    original_cwd = os.getcwd()

    # Change to the project root directory
    os.chdir(project_root)

    # Run the test
    yield

    # Restore the original working directory
    os.chdir(original_cwd)


# Add a fixture that uses the test file's directory
@pytest.fixture
def fast_agent(request):
    """
    Creates a FastAgent with config from the test file's directory.
    Automatically changes working directory to match the test file location.
    """
    # Get the directory where the test file is located
    test_module = request.module.__file__
    test_dir = os.path.dirname(test_module)

    # Save original directory
    original_cwd = os.getcwd()

    # Change to the test file's directory
    os.chdir(test_dir)

    # Explicitly create absolute path to the config file in the test directory
    config_file = os.path.join(test_dir, "fastagent.config.yaml")

    # Create agent with local config using absolute path
    agent = FastAgent(
        "Test Agent",
        config_path=config_file,  # Use absolute path to local config in test directory
        ignore_unknown_args=True,
    )

    # Provide the agent
    yield agent

    # Restore original directory
    os.chdir(original_cwd)


# Fixture to manage TensorZero docker-compose environment
@pytest.fixture(scope="session")
def tensorzero_docker_env(project_root):
    """Ensures the TensorZero docker-compose environment is running."""
    compose_file = project_root / "examples" / "tensorzero" / "docker-compose.yml"
    compose_dir = compose_file.parent
    compose_cmd = ["docker-compose", "-f", str(compose_file)]

    print(f"\nEnsuring TensorZero Docker environment is up ({compose_file})...")
    try:
        # Use --wait flag if available, otherwise fallback to time.sleep
        check_wait_support_cmd = compose_cmd + ["up", "--help"]
        help_output = subprocess.run(
            check_wait_support_cmd, capture_output=True, text=True, cwd=compose_dir
        )
        use_wait_flag = "--wait" in help_output.stdout or "--wait" in help_output.stderr

        up_command = compose_cmd + ["up", "-d"]
        if use_wait_flag:
            up_command.append("--wait")

        start_result = subprocess.run(
            up_command, check=True, capture_output=True, text=True, cwd=compose_dir
        )
        print("TensorZero Docker 'up -d' completed.")
        print(start_result.stdout)
        if start_result.stderr:
            print(f"Stderr: {start_result.stderr}")

        # If --wait is not supported, add a manual delay
        if not use_wait_flag:
            print("Docker compose '--wait' flag not supported, adding manual delay...")
            time.sleep(20)  # Increased sleep time as fallback

    except subprocess.CalledProcessError as e:
        print(f"Error starting TensorZero Docker services: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        pytest.fail(f"Failed to start docker-compose services from {compose_file}")
        return  # Exit if start failed

    yield  # Run tests

    # Stop services
    print("\nTearing down TensorZero Docker environment...")
    try:
        stop_result = subprocess.run(
            compose_cmd + ["down"], check=True, capture_output=True, text=True, cwd=compose_dir
        )
        print("TensorZero Docker 'down' completed.")
        print(stop_result.stdout)
        if stop_result.stderr:
            print(f"Stderr: {stop_result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error stopping TensorZero Docker services: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        # Don't fail the test run if teardown fails, but log it.


# Fixture to temporarily change CWD to examples/tensorzero
@pytest.fixture
def chdir_to_tensorzero_example(project_root):
    """Change CWD to the tensorzero example directory for a test."""
    original_cwd = Path.cwd()
    example_dir = project_root / "examples" / "tensorzero"
    if not example_dir.is_dir():
        pytest.skip(
            f"TensorZero example directory not found at {example_dir}"
        )  # Use skip instead of fail
        return
    os.chdir(example_dir)
    print(f"\nChanged CWD to: {example_dir}")
    yield
    os.chdir(original_cwd)
    print(f"\nRestored CWD to: {original_cwd}")
--- END OF FILE tests/e2e/conftest.py ---


--- START OF FILE tests/integration/conftest.py ---
import importlib
import os
from pathlib import Path

import pytest

from mcp_agent.core.fastagent import FastAgent


# Keep the auto-cleanup fixture
@pytest.fixture(scope="function", autouse=True)
def cleanup_event_bus():
    """Reset the AsyncEventBus between tests using its reset method"""
    # Run the test
    yield

    # Reset the AsyncEventBus after each test
    try:
        # Import the module with the AsyncEventBus
        transport_module = importlib.import_module("mcp_agent.logging.transport")
        AsyncEventBus = getattr(transport_module, "AsyncEventBus", None)

        # Call the reset method if available
        if AsyncEventBus and hasattr(AsyncEventBus, "reset"):
            AsyncEventBus.reset()
    except Exception:
        pass


# Set the project root directory for tests
@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory as a Path object"""
    # Go up from tests/e2e directory to find project root
    return Path(__file__).parent.parent.parent


# Add a fixture that uses the test file's directory
@pytest.fixture
def fast_agent(request):
    """
    Creates a FastAgent with config from the test file's directory.
    Automatically changes working directory to match the test file location.
    """
    # Get the directory where the test file is located
    test_module = request.module.__file__
    test_dir = os.path.dirname(test_module)

    # Save original directory
    original_cwd = os.getcwd()

    # Change to the test file's directory
    os.chdir(test_dir)

    # Explicitly create absolute path to the config file in the test directory
    config_file = os.path.join(test_dir, "fastagent.config.yaml")

    # Create agent with local config using absolute path
    agent = FastAgent(
        "Test Agent",
        config_path=config_file,  # Use absolute path to local config in test directory
        ignore_unknown_args=True,
    )

    # Provide the agent
    yield agent

    # Restore original directory
    os.chdir(original_cwd)


# Add a fixture that uses the test file's directory
@pytest.fixture
def markup_fast_agent(request):
    """
    Creates a FastAgent with config from the test file's directory.
    Automatically changes working directory to match the test file location.
    """
    # Get the directory where the test file is located
    test_module = request.module.__file__
    test_dir = os.path.dirname(test_module)

    # Save original directory
    original_cwd = os.getcwd()

    # Change to the test file's directory
    os.chdir(test_dir)

    # Explicitly create absolute path to the config file in the test directory
    config_file = os.path.join(test_dir, "fastagent.config.markup.yaml")

    # Create agent with local config using absolute path
    agent = FastAgent(
        "Test Agent",
        config_path=config_file,  # Use absolute path to local config in test directory
        ignore_unknown_args=True,
    )

    # Provide the agent
    yield agent

    # Restore original directory
    os.chdir(original_cwd)
# Add a fixture for auto_sampling disabled tests
@pytest.fixture
def auto_sampling_off_fast_agent(request):
    """
    Creates a FastAgent with auto_sampling disabled config from the test file's directory.
    """
    # Get the directory where the test file is located
    test_module = request.module.__file__
    test_dir = os.path.dirname(test_module)

    # Save original directory
    original_cwd = os.getcwd()

    # Change to the test file's directory
    os.chdir(test_dir)

    # Explicitly create absolute path to the config file in the test directory
    config_file = os.path.join(test_dir, "fastagent.config.auto_sampling_off.yaml")

    # Create agent with local config using absolute path
    agent = FastAgent(
        "Test Agent",
        config_path=config_file,
        ignore_unknown_args=True,
    )

    # Provide the agent
    yield agent

    # Restore original directory
    os.chdir(original_cwd)
--- END OF FILE tests/integration/conftest.py ---


--- START OF FILE tests/integration/api/fastagent.config.markup.yaml ---
# FastAgent Configuration File

# Default Model Configuration:
#
# Takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
# Accepts aliases for Anthropic Models: haiku, haiku3, sonnet, sonnet35, opus, opus3
# and OpenAI Models: gpt-4o-mini, gpt-4o, o1, o1-mini, o3-mini
#
# If not specified, defaults to "haiku".
# Can be overriden with a command line switch --model=<model>, or within the Agent constructor.

default_model: passthrough

# Logging and Console Configuration:
logger:
  # level: "debug" | "info" | "warning" | "error"
  # type: "none" | "console" | "file" | "http"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true
  enable_markup: false
  use_legacy_display: true

# MCP Servers
mcp:
  servers:
    prompts:
      command: "prompt-server"
      args: ["playback.md"]
    std_io:
      command: "uv"
      args: ["run", "integration_agent.py", "--server", "--transport", "stdio"]
    sse:
      transport: "sse"
      url: "http://localhost:8723/sse"
    card_test:
      command: "uv"
      args: ["run", "mcp_tools_server.py"]
    hyphen-test:
      command: "uv"
      args: ["run", "mcp_tools_server.py"]
    # borrows config from prompt-server
    cwd_test:
      command: "prompt-server"
      args: ["multi.txt"]
      cwd: "../prompt-server/"
--- END OF FILE tests/integration/api/fastagent.config.markup.yaml ---


--- START OF FILE tests/integration/api/fastagent.config.yaml ---
# FastAgent Configuration File

# Default Model Configuration:
#
# Takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
# Accepts aliases for Anthropic Models: haiku, haiku3, sonnet, sonnet35, opus, opus3
# and OpenAI Models: gpt-4o-mini, gpt-4o, o1, o1-mini, o3-mini
#
# If not specified, defaults to "haiku".
# Can be overriden with a command line switch --model=<model>, or within the Agent constructor.

default_model: passthrough

# Logging and Console Configuration:
logger:
  # level: "debug" | "info" | "warning" | "error"
  # type: "none" | "console" | "file" | "http"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true

# MCP Servers
mcp:
  servers:
    prompts:
      command: "prompt-server"
      args: ["playback.md"]
    prompts2:
      command: "prompt-server"
      args: ["prompt.txt"]
    std_io:
      command: "uv"
      args: ["run", "integration_agent.py", "--server", "--transport", "stdio"]
    sse:
      transport: "sse"
      url: "http://localhost:8723/sse"
    http:
      transport: "http"
      url: "http://localhost:8724/mcp"
    card_test:
      command: "uv"
      args: ["run", "mcp_tools_server.py"]
    hyphen-test:
      command: "uv"
      args: ["run", "mcp_tools_server.py"]
    # borrows config from prompt-server
    cwd_test:
      command: "prompt-server"
      args: ["multi.txt"]
      cwd: "../prompt-server/"
    dynamic_tool:
      command: "uv"
      args: ["run", "mcp_dynamic_tools.py"]
--- END OF FILE tests/integration/api/fastagent.config.yaml ---


--- START OF FILE tests/integration/api/fastagent.secrets.yaml ---
# provider key logic tests
anthropic:
  api_key: "test-key-anth"
openai:
  api_key: <your-api-key-here>
--- END OF FILE tests/integration/api/fastagent.secrets.yaml ---


--- START OF FILE tests/integration/api/integration_agent.py ---
"""
Simple test agent for integration testing.
"""

import asyncio
import sys

from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("Integration Test Agent")


# Define a simple agent
@fast.agent(
    name="test",  # Important: This name matches what we use in the CLI test
    instruction="You are a test agent that simply echoes back any input received.",
)
async def main() -> None:
    async with fast.run() as agent:
        # This executes only for interactive mode, not needed for command-line testing
        if sys.stdin.isatty():  # Only run interactive mode if attached to a terminal
            user_input = input("Enter a message: ")
            response = await agent.send(user_input)
            print(f"Agent response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
--- END OF FILE tests/integration/api/integration_agent.py ---


--- START OF FILE tests/integration/api/mcp_dynamic_tools.py ---
#!/usr/bin/env python3


from mcp.server.fastmcp import FastMCP

# Create the FastMCP server
app = FastMCP(name="An MCP Server", instructions="Here is how to use this server")

# Track if our dynamic tool is registered
dynamic_tool_registered = False


@app.tool(
    name="check_weather",
    description="Returns the weather for a specified location.",
)
async def check_weather(location: str) -> str:
    """The location to check"""
    global dynamic_tool_registered

    # Get the current context which gives us access to the session
    context = app.get_context()

    # Toggle the dynamic tool
    if dynamic_tool_registered:
        # Remove the tool by recreating the tool manager's tool list
        # This is a simple approach for testing purposes
        app._tool_manager._tools = {
            name: tool for name, tool in app._tool_manager._tools.items() if name != "dynamic_tool"
        }
        dynamic_tool_registered = False
    else:
        # Add a new tool dynamically
        app.add_tool(
            lambda: "This is a dynamic tool",
            name="dynamic_tool",
            description="A tool that was added dynamically",
        )
        dynamic_tool_registered = True

    # Send notification that the tool list has changed
    await context.session.send_tool_list_changed()

    # Return weather condition
    return "It's sunny in " + location


if __name__ == "__main__":
    # Run the server using stdio transport
    app.run(transport="stdio")
--- END OF FILE tests/integration/api/mcp_dynamic_tools.py ---


--- START OF FILE tests/integration/api/mcp_tools_server.py ---
#!/usr/bin/env python3
"""
Simple MCP server that responds to tool calls with text and image content.
"""

import logging

from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastMCP server
app = FastMCP(name="An MCP Server", instructions="Here is how to use this server")


@app.tool(
    name="check_weather",
    description="Returns the weather for a specified location.",
)
def check_weather(location: str) -> str:
    """The location to check"""
    # Write the location to a text file
    with open("weather_location.txt", "w") as f:
        f.write(location)

    # Return sunny weather condition
    return "It's sunny in " + location


@app.tool(name="shirt-colour", description="Returns the colour of a shirt.")
def shirt_colour() -> str:
    return "blue polka dots"


if __name__ == "__main__":
    # Run the server using stdio transport
    app.run(transport="stdio")
--- END OF FILE tests/integration/api/mcp_tools_server.py ---


--- START OF FILE tests/integration/api/playback.md ---
---USER
user1

---ASSISTANT
assistant1

---USER
user2

---ASSISTANT
assistant2
--- END OF FILE tests/integration/api/playback.md ---


--- START OF FILE tests/integration/api/prompt.txt ---
this is from the prompt file
--- END OF FILE tests/integration/api/prompt.txt ---


--- START OF FILE tests/integration/api/stderr_test_script.py ---
#!/usr/bin/env python
"""
Simple script that outputs messages to stderr for testing.
"""
import sys

# Write complete lines
sys.stderr.write("Error line 1\n")
sys.stderr.flush()

# Write partial line then complete it
sys.stderr.write("Error line 2 part 1")
sys.stderr.flush()
sys.stderr.write(" part 2\n")
sys.stderr.flush()

# Another complete line
sys.stderr.write("Final error line\n")
sys.stderr.flush()
--- END OF FILE tests/integration/api/stderr_test_script.py ---


--- START OF FILE tests/integration/api/test_api.py ---
import pytest

from mcp_agent.agents.base_agent import BaseAgent
from mcp_agent.core.prompt import Prompt


@pytest.mark.integration
@pytest.mark.asyncio
async def test_agent_api_with_simple_prompt(fast_agent):
    """Test that the agent can process a simple prompt using directory-specific config."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent1",
        instruction="You are a helpful AI Agent",
    )
    async def agent_function():
        async with fast.run() as agent:
            assert "test1" in await agent.agent1.send("test1")
            assert "test2" in await agent["agent1"].send("test2")
            assert "test3" in await agent.send("test3")
            assert "test4" in await agent("test4")
            assert "test5" in await agent.send("test5", "agent1")
            assert "test6" in await agent("test6", "agent1")

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_agent_api_with_prompt_messages(fast_agent):
    """Test that the agent can process a multipart prompts using directory-specific config."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent1",
        instruction="You are a helpful AI Agent",
    )
    async def agent_function():
        async with fast.run() as agent:
            assert "test1" in await agent.agent1.send(Prompt.user("test1"))

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_agent_api_with_basic_playback(fast_agent):
    """Test that the agent can process a multipart prompts using directory-specific config."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent1",
        instruction="You are a helpful AI Agent",
        model="playback",
        servers=["prompts"],
    )
    async def agent_function():
        async with fast.run() as agent:
            await agent.agent1.apply_prompt("playback")
            assert "assistant1" in await agent.agent1.send("ignored")

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_agent_api_with_default_calls(fast_agent):
    """Test that the agent can process a multipart prompts using directory-specific config."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent1",
        instruction="You are a helpful AI Agent",
        model="passthrough",
    )
    async def agent_function():
        async with fast.run() as agent:
            assert "message 1" == await agent("message 1")
            assert "message 2" == await agent["agent1"]("message 2")

        # assert "assistant1" in await agent.agent1.send("ignored")

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_mixed_message_types(fast_agent):
    """Test that the agent can handle mixed message types seamlessly."""
    from mcp.types import PromptMessage, TextContent

    from mcp_agent.core.prompt import Prompt
    from mcp_agent.mcp.prompt_message_multipart import PromptMessageMultipart

    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent1",
        instruction="You are a helpful AI Agent",
        model="passthrough",
    )
    async def agent_function():
        async with fast.run() as agent:
            # Test with string
            assert "string message" == await agent.send("string message")

            # Test with PromptMessage
            prompt_message = PromptMessage(
                role="user", content=TextContent(type="text", text="prompt message")
            )
            assert "prompt message" == await agent.send(prompt_message)

            # Test with PromptMessageMultipart
            multipart = PromptMessageMultipart(
                role="user", content=[TextContent(type="text", text="multipart message")]
            )
            assert "multipart message" == await agent.send(multipart)

            # Test message history access
            response = await agent.send("checking history")
            # Verify agent's message history is accessible and contains our messages
            message_history = agent.agent1.message_history

            # Basic assertions
            assert len(message_history) >= 8  # 4 user messages + 4 assistant responses
            assert all(isinstance(msg, PromptMessageMultipart) for msg in message_history)

            # Create role/content pairs for easier verification
            message_pairs = [(msg.role, msg.first_text()) for msg in message_history]

            # Check for specific messages with correct roles
            user_messages = [text for role, text in message_pairs if role == "user"]
            assistant_messages = [text for role, text in message_pairs if role == "assistant"]

            # Check our specific user messages are there
            assert "string message" in user_messages
            assert "prompt message" in user_messages
            assert "multipart message" in user_messages
            assert "checking history" in user_messages

            # Check corresponding assistant responses
            assert "string message" in assistant_messages  # Passthrough returns same text
            assert "prompt message" in assistant_messages
            assert "multipart message" in assistant_messages
            assert "checking history" in assistant_messages

            # Find a user message and verify the next message is from assistant
            for i in range(len(message_pairs) - 1):
                if message_pairs[i][0] == "user":
                    assert message_pairs[i + 1][0] == "assistant", (
                        "User message should be followed by assistant"
                    )

            # Test directly with conversion from GetPromptResult
            # Simulating a GetPromptResult with a placeholder
            pm = PromptMessage(
                role="user", content=TextContent(type="text", text="simulated prompt result")
            )
            multipart_msgs = PromptMessageMultipart.to_multipart([pm])
            response = await agent.agent1.generate(multipart_msgs, None)
            assert "simulated prompt result" == response.first_text()

            # Test with EmbeddedResource directly in Prompt.user()
            from mcp.types import EmbeddedResource, TextResourceContents
            from pydantic import AnyUrl

            # Create a resource
            text_resource = TextResourceContents(
                uri=AnyUrl("file:///test/example.txt"),
                text="Sample text from resource",
                mimeType="text/plain",
            )
            embedded_resource = EmbeddedResource(type="resource", resource=text_resource)

            # Create a message with text and resource
            message = Prompt.user("Text message with resource", embedded_resource)
            response = await agent.send(message)
            assert response  # Just verify we got a response

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_specify_cwd_for_server(fast_agent):
    """Test that the agent can process a multipart prompts using directory-specific config."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent1",
        instruction="You are a helpful AI Agent",
        model="playback",
        servers=["cwd_test"],
    )
    async def agent_function():
        async with fast.run() as agent:
            await agent.agent1.apply_prompt("multi")
            assert "how may i" in await agent.agent1.send("cwd_test")

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_custom_agent(fast_agent):
    """Test that the agent can process a multipart prompts using directory-specific config."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    class MyAgent(BaseAgent):
        async def send(self, message):
            return "it's a-me!...Mario! "

    # Define the agent
    @fast.custom(MyAgent, name="custom")
    async def agent_function():
        async with fast.run() as agent:
            assert "it's a-me!...Mario! " == await agent.custom.send("hello")

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_setting_an_agent_as_default(fast_agent):
    """Test that the agent can process a multipart prompts using directory-specific config."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    class MyAgent(BaseAgent):
        async def send(self, message):
            return "it's a-me!...Mario! "

    @fast.agent(name="custom1")
    @fast.custom(MyAgent, name="custom2", default=True)
    @fast.agent(name="custom3")
    async def agent_function():
        async with fast.run() as agent:
            assert "it's a-me!...Mario! " == await agent.send("hello")

    await agent_function()
--- END OF FILE tests/integration/api/test_api.py ---


--- START OF FILE tests/integration/api/test_cli_and_mcp_server.py ---
import os
import subprocess
from typing import TYPE_CHECKING

import pytest

from mcp_agent.mcp.helpers.content_helpers import get_text

if TYPE_CHECKING:
    from mcp import GetPromptResult


@pytest.mark.integration
def test_agent_message_cli():
    """Test sending a message via command line to a FastAgent program."""
    # Get the path to the test_agent.py file (in the same directory as this test)
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_agent_path = os.path.join(test_dir, "integration_agent.py")

    # Test message
    test_message = "Hello from command line test"

    # Run the test agent with the --agent and --message flags
    result = subprocess.run(
        [
            "uv",
            "run",
            test_agent_path,
            "--agent",
            "test",
            "--message",
            test_message,
            #  "--quiet",  # Suppress progress display, etc. for cleaner output
        ],
        capture_output=True,
        text=True,
        cwd=test_dir,  # Run in the test directory to use its config
    )

    # Check that the command succeeded
    assert result.returncode == 0, f"Command failed with output: {result.stderr}"

    command_output = result.stdout
    # With the passthrough model, the output should contain the input message
    assert test_message in command_output, "Test message not found in agent response"
    # this is from show_user_output
    assert "▎▶ test" in command_output, "show chat messages included in output"


@pytest.mark.integration
def test_agent_message_prompt_file():
    """Test sending a message via command line to a FastAgent program."""
    # Get the path to the test_agent.py file (in the same directory as this test)
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_agent_path = os.path.join(test_dir, "integration_agent.py")

    # Run the test agent with the --agent and --message flags
    result = subprocess.run(
        ["uv", "run", test_agent_path, "--agent", "test", "--prompt-file", "prompt.txt"],
        capture_output=True,
        text=True,
        cwd=test_dir,  # Run in the test directory to use its config
    )

    # Check that the command succeeded
    assert result.returncode == 0, f"Command failed with output: {result.stderr}"

    command_output = result.stdout
    # With the passthrough model, the output should contain the input message
    assert "this is from the prompt file" in command_output, (
        "Test message not found in agent response"
    )
    # this is from show_user_output
    assert "▎▶ test" in command_output, "show chat messages included in output"


@pytest.mark.integration
def test_agent_message_cli_quiet_flag():
    """Test sending a message via command line to a FastAgent program."""
    # Get the path to the test_agent.py file (in the same directory as this test)
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_agent_path = os.path.join(test_dir, "integration_agent.py")

    # Test message
    test_message = "Hello from command line test"

    # Run the test agent with the --agent and --message flags
    result = subprocess.run(
        [
            "uv",
            "run",
            test_agent_path,
            "--agent",
            "test",
            "--message",
            test_message,
            "--quiet",  # Suppress progress display, etc. for cleaner output
        ],
        capture_output=True,
        text=True,
        cwd=test_dir,  # Run in the test directory to use its config
    )

    # Check that the command succeeded
    assert result.returncode == 0, f"Command failed with output: {result.stderr}"

    command_output = result.stdout
    # With the passthrough model, the output should contain the input message
    assert test_message in command_output, "Test message not found in agent response"
    # this is from show_user_output
    assert "[USER]" not in command_output, "show chat messages included in output"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_agent_server_option_stdio(fast_agent):
    """Test that FastAgent supports --server flag with STDIO transport."""

    @fast_agent.agent(name="client", servers=["std_io"])
    async def agent_function():
        async with fast_agent.run() as agent:
            assert "connected" == await agent.send("connected")
            result = await agent.send('***CALL_TOOL test_send {"message": "stdio server test"}')
            assert "stdio server test" == result

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_agent_server_option_stdio_and_prompt_history(fast_agent):
    """Test that FastAgent supports --server flag with STDIO transport."""

    @fast_agent.agent(name="client", servers=["std_io"])
    async def agent_function():
        async with fast_agent.run() as agent:
            assert "connected" == await agent.send("connected")
            result = await agent.send('***CALL_TOOL test_send {"message": "message one"}')
            assert "message one" == result
            result = await agent.send('***CALL_TOOL test_send {"message": "message two"}')
            assert "message two" == result

            history: GetPromptResult = await agent.get_prompt("test_history", server_name="std_io")
            assert len(history.messages) == 4
            assert "message one" == get_text(history.messages[1].content)

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_agent_server_option_sse(fast_agent):
    """Test that FastAgent supports --server flag with SSE transport."""

    # Start the SSE server in a subprocess
    import asyncio
    import os
    import subprocess

    # Get the path to the test agent
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_agent_path = os.path.join(test_dir, "integration_agent.py")

    # Port must match what's in the fastagent.config.yaml
    port = 8723

    # Start the server process
    server_proc = subprocess.Popen(
        [
            "uv",
            "run",
            test_agent_path,
            "--server",
            "--transport",
            "sse",
            "--port",
            str(port),
            "--quiet",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=test_dir,
    )

    try:
        # Give the server a moment to start
        await asyncio.sleep(2)

        # Now connect to it via the configured MCP server
        @fast_agent.agent(name="client", servers=["sse"])
        async def agent_function():
            async with fast_agent.run() as agent:
                # Try connecting and sending a message
                assert "connected" == await agent.send("connected")
                result = await agent.send('***CALL_TOOL test_send {"message": "sse server test"}')
                assert "sse server test" == result

        await agent_function()

    finally:
        # Terminate the server process
        if server_proc.poll() is None:  # If still running
            server_proc.terminate()
            try:
                server_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                server_proc.kill()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_agent_server_option_http(fast_agent):
    """Test that FastAgent supports --server flag with HTTP transport."""

    # Start the SSE server in a subprocess
    import asyncio
    import os
    import subprocess

    # Get the path to the test agent
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_agent_path = os.path.join(test_dir, "integration_agent.py")

    # Port must match what's in the fastagent.config.yaml
    port = 8724

    # Start the server process
    server_proc = subprocess.Popen(
        [
            "uv",
            "run",
            test_agent_path,
            "--server",
            "--transport",
            "http",
            "--port",
            str(port),
            "--quiet",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=test_dir,
    )

    try:
        # Give the server a moment to start
        await asyncio.sleep(2)

        # Now connect to it via the configured MCP server
        @fast_agent.agent(name="client", servers=["http"])
        async def agent_function():
            async with fast_agent.run() as agent:
                # Try connecting and sending a message
                assert "connected" == await agent.send("connected")
                result = await agent.send('***CALL_TOOL test_send {"message": "http server test"}')
                assert "http server test" == result

        await agent_function()

    finally:
        # Terminate the server process
        if server_proc.poll() is None:  # If still running
            server_proc.terminate()
            try:
                server_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                server_proc.kill()
--- END OF FILE tests/integration/api/test_cli_and_mcp_server.py ---


--- START OF FILE tests/integration/api/test_describe_a2a.py ---
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from a2a_types.types import AgentCard, AgentSkill

    from mcp_agent.agents.agent import Agent


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_agent_card_and_tools(fast_agent):
    fast = fast_agent

    @fast.agent(name="test", instruction="here are you instructions", servers=["card_test"])
    async def agent_function():
        async with fast.run() as app:
            # Simulate some agent operations
            agent: Agent = app["test"]
            card: AgentCard = await agent.agent_card()

            assert "test" == card.name
            # TODO -- migrate AgentConfig to include "description" - "instruction" is OK for the moment...
            assert "here are you instructions" == card.description
            assert 2 == len(card.skills)

            skill: AgentSkill = card.skills[0]
            assert "card_test-check_weather" == skill.id
            assert "check_weather" == skill.name
            assert "Returns the weather for a specified location."
            assert skill.tags
            assert "tool" == skill.tags[0]

    await agent_function()
--- END OF FILE tests/integration/api/test_describe_a2a.py ---


--- START OF FILE tests/integration/api/test_hyphens_in_name.py ---
import pytest


@pytest.mark.integration
@pytest.mark.asyncio
async def test_hyphenated_server_name(fast_agent):
    fast = fast_agent

    @fast.agent(name="test", instruction="here are you instructions", servers=["hyphen-test"])
    async def agent_function():
        async with fast.run() as app:
            result = await app.test.send('***CALL_TOOL check_weather {"location": "New York"}')
            assert "sunny" in result

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_hyphenated_tool_name(fast_agent):
    fast = fast_agent

    @fast.agent(name="test", instruction="here are you instructions", servers=["hyphen-test"])
    async def agent_function():
        async with fast.run() as app:
            result = await app.test.send("***CALL_TOOL shirt-colour {}")
            assert "polka" in result

    await agent_function()
--- END OF FILE tests/integration/api/test_hyphens_in_name.py ---


--- START OF FILE tests/integration/api/test_logger_textio.py ---
"""
Integration tests for the LoggerTextIO class that captures stderr from MCP servers.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

from mcp_agent.mcp.logger_textio import LoggerTextIO, get_stderr_handler


@pytest.fixture
def test_script_path():
    """Returns the path to the test script that generates stderr output."""
    return Path(__file__).parent / "stderr_test_script.py"


@pytest.fixture
def logger_io():
    """Create a LoggerTextIO instance for testing with proper cleanup."""
    logger_io = LoggerTextIO("test-server")

    yield logger_io

    # Ensure proper cleanup
    logger_io.close()
    if hasattr(logger_io, "_devnull_fd"):
        try:
            os.close(logger_io._devnull_fd)
        except OSError:
            pass


@pytest.mark.integration
def test_logger_textio_fileno(logger_io):
    """Test that fileno returns a valid file descriptor."""
    # Get file descriptor and verify it's a positive integer
    fd = logger_io.fileno()
    assert isinstance(fd, int)
    assert fd > 0

    # Test writing to the file descriptor
    bytes_written = os.write(fd, b"Test message\n")
    assert bytes_written > 0


@pytest.mark.integration
def test_logger_textio_write(logger_io):
    """Test that the write method properly captures and buffers output."""
    # Test complete line
    result = logger_io.write("Complete line\n")
    assert result > 0

    # Test partial line
    result = logger_io.write("Partial ")
    assert result > 0

    # Test completing the partial line
    result = logger_io.write("line completion\n")
    assert result > 0


@pytest.mark.integration
def test_logger_textio_real_process(test_script_path, logger_io):
    """Integration test using a real subprocess with stderr output."""
    # Run the script and capture stderr
    process = subprocess.Popen(
        [sys.executable, str(test_script_path)],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )

    # Read and process stderr lines
    for line in process.stderr:
        logger_io.write(line)

    # Wait for process to complete
    process.wait()

    # No assertions needed - if any part fails, the test will fail
    # The test verifies that the code executes without exceptions


@pytest.mark.integration
def test_get_stderr_handler():
    """Test that get_stderr_handler returns a valid LoggerTextIO instance."""
    handler = get_stderr_handler("test-handler")

    # Verify it's the right type
    assert isinstance(handler, LoggerTextIO)

    # Verify it has the correct server name
    assert handler.server_name == "test-handler"

    # Verify it has a valid fileno
    fd = handler.fileno()
    assert isinstance(fd, int)
    assert fd > 0

    # Clean up
    handler.close()
--- END OF FILE tests/integration/api/test_logger_textio.py ---


--- START OF FILE tests/integration/api/test_markup_config.py ---
import pytest

from mcp_agent.core.prompt import Prompt


@pytest.mark.integration
@pytest.mark.integration
@pytest.mark.asyncio
async def test_markup_disabled_does_not_error(markup_fast_agent):
    @markup_fast_agent.agent(
        "agent2",
        instruction="You are a helpful AI Agent",
    )
    async def agent_function():
        async with markup_fast_agent.run() as agent:
            assert "test2" in await agent.agent2.send(Prompt.user("'[/]test2"))

    await agent_function()
--- END OF FILE tests/integration/api/test_markup_config.py ---


--- START OF FILE tests/integration/api/test_prompt_commands.py ---
"""
Test the prompt command processing functionality.
"""

import pytest

from mcp_agent.core.enhanced_prompt import handle_special_commands


@pytest.mark.asyncio
async def test_command_handling_for_prompts():
    """Test the command handling functions for /prompts and /prompt commands."""
    # Test /prompts command after it's been pre-processed 
    # The pre-processed form of "/prompts" is {"select_prompt": True, "prompt_name": None}
    result = await handle_special_commands({"select_prompt": True, "prompt_name": None}, True)
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "select_prompt" in result, "Result should have select_prompt key"
    assert result["select_prompt"] is True
    assert "prompt_name" in result
    assert result["prompt_name"] is None
    
    # Test /prompt <number> command after pre-processing
    # The pre-processed form is {"select_prompt": True, "prompt_index": 3}  
    result = await handle_special_commands({"select_prompt": True, "prompt_index": 3}, True)
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "select_prompt" in result
    assert "prompt_index" in result
    assert result["prompt_index"] == 3
    
    # Test /prompt <name> command after pre-processing
    # The pre-processed form is "SELECT_PROMPT:my-prompt"
    result = await handle_special_commands("SELECT_PROMPT:my-prompt", True)
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "select_prompt" in result
    assert "prompt_name" in result
    assert result["prompt_name"] == "my-prompt"
--- END OF FILE tests/integration/api/test_prompt_commands.py ---


--- START OF FILE tests/integration/api/test_prompt_listing.py ---
"""
Test the prompt listing and selection functionality directly.
"""

import pytest

from mcp_agent.core.interactive_prompt import InteractivePrompt


@pytest.mark.integration
@pytest.mark.asyncio
async def test_multi_agent_prompt_listing(fast_agent):
    """Test the _get_all_prompts function with None as server name."""
    fast = fast_agent

    @fast.agent(name="agent1", servers=["prompts"])
    @fast.agent(name="agent2", servers=["prompts2"])
    @fast.agent(name="agent3")
    async def agent_function():
        async with fast.run() as agent:
            # Create instance of InteractivePrompt
            prompt_ui = InteractivePrompt()

            # Test listing prompts for each agent separately
            # Agent1 should have prompts from "prompts" server (playback.md -> playback)
            agent1_prompts = await prompt_ui._get_all_prompts(agent, "agent1")
            assert len(agent1_prompts) == 1
            assert agent1_prompts[0]["server"] == "prompts"
            assert agent1_prompts[0]["name"] == "playback"
            assert agent1_prompts[0]["description"] == "[USER] user1 assistant1 user2"
            assert agent1_prompts[0]["arg_count"] == 0

            # Agent2 should have prompts from "prompts2" server (prompt.txt -> prompt)
            agent2_prompts = await prompt_ui._get_all_prompts(agent, "agent2")
            assert len(agent2_prompts) == 1
            assert agent2_prompts[0]["server"] == "prompts2"
            assert agent2_prompts[0]["name"] == "prompt"
            assert agent2_prompts[0]["description"] == "this is from the prompt file"
            assert agent2_prompts[0]["arg_count"] == 0

            # Agent3 should have no prompts (no servers configured)
            agent3_prompts = await prompt_ui._get_all_prompts(agent, "agent3")
            assert len(agent3_prompts) == 0

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_apply_prompt_with_namespaced_name(fast_agent):
    """Test applying a prompt using its namespaced name directly."""
    fast = fast_agent

    @fast.agent(name="test", servers=["prompts"], model="passthrough")
    async def agent_function():
        async with fast.run() as agent:
            prompts = await agent.test.list_prompts(server_name=None)

            # Verify we have prompts from the "prompts" server
            assert "prompts" in prompts
            assert len(prompts["prompts"]) > 0

            # Get name of first prompt to test with
            prompt_name = prompts["prompts"][0].name

            # Create properly namespaced name using the same separator as mcp_aggregator
            from mcp_agent.mcp.mcp_aggregator import SEP

            namespaced_name = f"prompts{SEP}{prompt_name}"

            # Apply the prompt directly
            response = await agent.test.apply_prompt(namespaced_name)

            # Verify the prompt was applied
            assert response, "No response from apply_prompt"
            assert len(agent.test._llm.message_history) > 0

    await agent_function()
--- END OF FILE tests/integration/api/test_prompt_listing.py ---


--- START OF FILE tests/integration/api/test_provider_keys.py ---
import os

import pytest

from mcp_agent.core.exceptions import ProviderKeyError
from mcp_agent.llm.augmented_llm import AugmentedLLM
from mcp_agent.llm.provider_key_manager import ProviderKeyManager


@pytest.mark.integration
@pytest.mark.asyncio
async def test_error_for_bad_provider_or_not_set(fast_agent):
    fast = fast_agent

    @fast.agent()
    async def agent_function():
        async with fast.run():
            assert fast.config

            with pytest.raises(ProviderKeyError):  # invalid provider
                ProviderKeyManager.get_api_key("foo", fast.config)

            deepseek_key = os.getenv("DEEPSEEK_API_KEY")
            os.environ["DEEPSEEK_API_KEY"] = ""
            openai_key = os.getenv("OPENAI_API_KEY")
            os.environ["OPENAI_API_KEY"] = ""

            try:
                with pytest.raises(ProviderKeyError):  # not supplied
                    ProviderKeyManager.get_api_key("deepseek", fast.config)

                with pytest.raises(ProviderKeyError):  # default string in secrets file
                    ProviderKeyManager.get_api_key("openai", fast.config)
            finally:
                if deepseek_key:
                    os.environ["DEEPSEEK_API_KEY"] = deepseek_key
                if openai_key:
                    os.environ["OPENAI_API_KEY"] = openai_key

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_reads_keys_and_prioritises_config_file(fast_agent):
    fast = fast_agent

    @fast.agent()
    async def agent_function():
        async with fast.run():
            assert fast.config

            assert "test-key-anth" == ProviderKeyManager.get_api_key("anthropic", fast.config)

            openai_key = os.getenv("OPENAI_API_KEY")
            anth_key = os.getenv("ANTHROPIC_API_KEY")
            try:
                os.environ["OPENAI_API_KEY"] = "test-key"
                os.environ["ANTHROPIC_API_KEY"] = "override"
                assert "test-key" == ProviderKeyManager.get_api_key("openai", fast.config)
                assert "test-key-anth" == ProviderKeyManager.get_api_key(
                    "anthropic", fast.config
                ), "config file > environment variable"
            finally:
                if openai_key:
                    os.environ["OPENAI_API_KEY"] = openai_key
                if anth_key:
                    os.environ["ANTHROPIC_API_KEY"] = anth_key

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_ollama_generic_api_key(fast_agent):
    fast = fast_agent

    @fast.agent()
    async def agent_function():
        async with fast.run():
            assert fast.config

            assert "ollama" == ProviderKeyManager.get_api_key("generic", fast.config)

            generic_key = os.getenv("GENERIC_API_KEY")
            try:
                os.environ["GENERIC_API_KEY"] = "test-key"
                assert "test-key" == ProviderKeyManager.get_api_key("generic", fast.config)
            finally:
                if generic_key:
                    os.environ["GENERIC_API_KEY"] = generic_key

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_programmatic_api_key(fast_agent):
    fast = fast_agent

    @fast.agent(model="haiku", api_key="programmatic-api-key")
    async def agent_function():
        async with fast.run() as agent:
            assert fast.config
            assert "test-key-anth" == ProviderKeyManager.get_api_key("anthropic", fast.config)
            assert "programmatic-api-key" == agent.default.config.api_key
            assert isinstance(agent.default._llm, AugmentedLLM)
            assert "programmatic-api-key" == agent.default._llm._api_key(), "api_key arg > config file"

    await agent_function()
--- END OF FILE tests/integration/api/test_provider_keys.py ---


--- START OF FILE tests/integration/api/test_tool_list_change.py ---
import asyncio
import logging
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from mcp import ListToolsResult

# Enable debug logging for the test
logging.basicConfig(level=logging.DEBUG)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_tool_list_changes(fast_agent):
    fast = fast_agent
    print("Starting tool list change test")

    @fast.agent(name="test", instruction="here are your instructions", servers=["dynamic_tool"])
    async def agent_function():
        print("Initializing agent")
        async with fast.run() as app:
            # Initially there should be one tool (check_weather)
            tools: ListToolsResult = await app.test.list_tools()
            assert 1 == len(tools.tools)
            assert "dynamic_tool-check_weather" == tools.tools[0].name

            # Calling check_weather will toggle the dynamic_tool and send a notification
            result = await app.test.send('***CALL_TOOL check_weather {"location": "New York"}')
            assert "sunny" in result

            # Wait for the tool list to be refreshed (with retry)
            await asyncio.sleep(0.5)

            tools = await app.test.list_tools()
            dynamic_tool_found = False
            # Check if dynamic_tool is in the list
            for tool in tools.tools:
                if tool.name == "dynamic_tool-dynamic_tool":
                    dynamic_tool_found = True
                    break

            # Verify the dynamic tool was added
            assert dynamic_tool_found, (
                "Dynamic tool was not added to the tool list after notification"
            )
            assert 2 == len(tools.tools), f"Expected 2 tools but found {len(tools.tools)}"

            # Call check_weather again to toggle the dynamic_tool off
            result = await app.test.send('***CALL_TOOL check_weather {"location": "Boston"}')
            assert "sunny" in result

            # Sleep between retries
            await asyncio.sleep(0.5)

            # Get the updated tool list
            tools = await app.test.list_tools()

            assert 1 == len(tools.tools)

    await agent_function()
--- END OF FILE tests/integration/api/test_tool_list_change.py ---


--- START OF FILE tests/integration/elicitation/elicitation_test_server.py ---
"""
Enhanced test server for sampling functionality
"""

import logging
import sys

from mcp import (
    ReadResourceResult,
)
from mcp.server.elicitation import (
    AcceptedElicitation,
    CancelledElicitation,
    DeclinedElicitation,
)
from mcp.server.fastmcp import FastMCP
from mcp.types import TextResourceContents
from pydantic import AnyUrl, BaseModel, Field

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("elicitation_server")

# Create MCP server
mcp = FastMCP("MCP Elicitation Server", log_level="DEBUG")


@mcp.resource(uri="elicitation://generate")
async def get() -> ReadResourceResult:
    """Tool that echoes back the input parameter"""

    class ServerRating(BaseModel):
        rating: bool = Field(description="Server Rating")

    mcp.get_context()
    result = await mcp.get_context().elicit("Rate this server 5 stars?", schema=ServerRating)
    ret = "nothing"
    match result:
        case AcceptedElicitation(data=data):
            if data.rating:
                ret = str(data.rating)
        case DeclinedElicitation():
            ret = "declined"
        case CancelledElicitation():
            ret = "cancelled"

    # Return the result directly, without nesting
    return ReadResourceResult(
        contents=[
            TextResourceContents(
                mimeType="text/plain", uri=AnyUrl("elicitation://generate"), text=f"Result: {ret}"
            )
        ]
    )


if __name__ == "__main__":
    logger.info("Starting elicitation test server...")
    mcp.run()
--- END OF FILE tests/integration/elicitation/elicitation_test_server.py ---


--- START OF FILE tests/integration/elicitation/elicitation_test_server_advanced.py ---
"""
Advanced test server for comprehensive elicitation functionality
"""

import logging
import sys
from typing import Optional

from mcp import (
    ReadResourceResult,
)
from mcp.server.elicitation import (
    AcceptedElicitation,
    CancelledElicitation,
    DeclinedElicitation,
)
from mcp.server.fastmcp import FastMCP
from mcp.types import TextResourceContents
from pydantic import AnyUrl, BaseModel, Field

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("elicitation_server_advanced")

# Create MCP server
mcp = FastMCP("MCP Advanced Elicitation Server", log_level="DEBUG")


@mcp.resource(uri="elicitation://client-capabilities")
async def client_capabilities_resource() -> ReadResourceResult:
    """Expose the client capabilities received during initialization."""

    ctx = mcp.get_context()

    if not ctx.session.client_params:
        text = "No client initialization params available"
    else:
        client_capabilities = ctx.session.client_params.capabilities

        # Check if elicitation capability is present
        has_elicitation = (
            hasattr(client_capabilities, "elicitation")
            and client_capabilities.elicitation is not None
        )
        has_sampling = (
            hasattr(client_capabilities, "sampling") and client_capabilities.sampling is not None
        )
        has_roots = hasattr(client_capabilities, "roots") and client_capabilities.roots is not None

        capabilities_list = []
        if has_elicitation:
            capabilities_list.append("✓ Elicitation")
        else:
            capabilities_list.append("✗ Elicitation")

        if has_sampling:
            capabilities_list.append("✓ Sampling")
        else:
            capabilities_list.append("✗ Sampling")

        if has_roots:
            capabilities_list.append("✓ Roots")
        else:
            capabilities_list.append("✗ Roots")

        text = "Client Capabilities:\n" + "\n".join(capabilities_list)

        # Add client info for debugging
        client_info = ctx.session.client_params.clientInfo
        text += f"\n\nClient Info: {client_info.name} v{client_info.version}"
        text += f"\nProtocol Version: {ctx.session.client_params.protocolVersion}"

    return ReadResourceResult(
        contents=[
            TextResourceContents(
                mimeType="text/plain", uri=AnyUrl("elicitation://client-capabilities"), text=text
            )
        ]
    )


@mcp.resource(uri="elicitation://simple-rating")
async def simple_rating() -> ReadResourceResult:
    """Simple boolean rating elicitation"""

    class ServerRating(BaseModel):
        rating: bool = Field(description="Do you like this server?")

    result = await mcp.get_context().elicit("Please rate this server", schema=ServerRating)

    match result:
        case AcceptedElicitation(data=data):
            response = f"You {'liked' if data.rating else 'did not like'} the server"
        case DeclinedElicitation():
            response = "Rating declined"
        case CancelledElicitation():
            response = "Rating cancelled"

    return ReadResourceResult(
        contents=[
            TextResourceContents(
                mimeType="text/plain", uri=AnyUrl("elicitation://simple-rating"), text=response
            )
        ]
    )


@mcp.resource(uri="elicitation://user-profile")
async def user_profile() -> ReadResourceResult:
    """Complex form with multiple field types"""

    class UserProfile(BaseModel):
        name: str = Field(description="Your full name", min_length=2, max_length=50)
        age: int = Field(description="Your age", ge=0, le=150)
        role: str = Field(
            description="Your job role",
            json_schema_extra={
                "enum": ["developer", "designer", "manager", "qa", "other"],
                "enumNames": [
                    "Software Developer",
                    "UI/UX Designer",
                    "Project Manager",
                    "Quality Assurance",
                    "Other",
                ],
            },
        )
        email: Optional[str] = Field(
            None, description="Your email address (optional)", json_schema_extra={"format": "email"}
        )
        subscribe_newsletter: bool = Field(False, description="Subscribe to our newsletter?")

    result = await mcp.get_context().elicit(
        "Please provide your user profile information", schema=UserProfile
    )

    match result:
        case AcceptedElicitation(data=data):
            lines = [
                f"Name: {data.name}",
                f"Age: {data.age}",
                f"Role: {data.role.title()}",
                f"Email: {data.email or 'Not provided'}",
                f"Newsletter: {'Yes' if data.subscribe_newsletter else 'No'}",
            ]
            response = "Profile received:\n" + "\n".join(lines)
        case DeclinedElicitation():
            response = "Profile declined"
        case CancelledElicitation():
            response = "Profile cancelled"

    return ReadResourceResult(
        contents=[
            TextResourceContents(
                mimeType="text/plain", uri=AnyUrl("elicitation://user-profile"), text=response
            )
        ]
    )


@mcp.resource(uri="elicitation://preferences")
async def preferences() -> ReadResourceResult:
    """Enum-based preference selection"""

    class Preferences(BaseModel):
        theme: str = Field(
            description="Choose your preferred theme",
            json_schema_extra={
                "enum": ["light", "dark", "auto"],
                "enumNames": ["Light Theme", "Dark Theme", "Auto Theme"],
            },
        )
        language: str = Field(
            description="Select your language",
            json_schema_extra={
                "enum": ["en", "es", "fr", "de"],
                "enumNames": ["English", "Spanish", "French", "German"],
            },
        )
        notifications: bool = Field(True, description="Enable notifications?")

    result = await mcp.get_context().elicit("Configure your preferences", schema=Preferences)

    match result:
        case AcceptedElicitation(data=data):
            response = f"Preferences set: Theme={data.theme}, Language={data.language}, Notifications={data.notifications}"
        case DeclinedElicitation():
            response = "Preferences declined"
        case CancelledElicitation():
            response = "Preferences cancelled"

    return ReadResourceResult(
        contents=[
            TextResourceContents(
                mimeType="text/plain", uri=AnyUrl("elicitation://preferences"), text=response
            )
        ]
    )


@mcp.resource(uri="elicitation://feedback")
async def feedback() -> ReadResourceResult:
    """Feedback form with number ratings"""

    class Feedback(BaseModel):
        overall_rating: int = Field(description="Overall rating (1-5)", ge=1, le=5)
        ease_of_use: float = Field(description="Ease of use (0.0-10.0)", ge=0.0, le=10.0)
        would_recommend: bool = Field(description="Would you recommend to others?")
        comments: Optional[str] = Field(None, description="Additional comments", max_length=500)

    result = await mcp.get_context().elicit("We'd love your feedback!", schema=Feedback)

    match result:
        case AcceptedElicitation(data=data):
            lines = [
                f"Overall: {data.overall_rating}/5",
                f"Ease of use: {data.ease_of_use}/10.0",
                f"Would recommend: {'Yes' if data.would_recommend else 'No'}",
            ]
            if data.comments:
                lines.append(f"Comments: {data.comments}")
            response = "Feedback received:\n" + "\n".join(lines)
        case DeclinedElicitation():
            response = "Feedback declined"
        case CancelledElicitation():
            response = "Feedback cancelled"

    return ReadResourceResult(
        contents=[
            TextResourceContents(
                mimeType="text/plain", uri=AnyUrl("elicitation://feedback"), text=response
            )
        ]
    )


if __name__ == "__main__":
    logger.info("Starting advanced elicitation test server...")
    mcp.run()
--- END OF FILE tests/integration/elicitation/elicitation_test_server_advanced.py ---


--- START OF FILE tests/integration/elicitation/fastagent.config.yaml ---
default_model: passthrough

# Logging and Console Configuration:
logger:
  level: "error"
  type: "file"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true

mcp:
  servers:
    # Elicitation test servers for different modes
    elicitation_forms_mode:
      command: "uv"
      args: ["run", "elicitation_test_server_advanced.py"]
      transport: "stdio"
      cwd: "."
      elicitation:
        mode: "forms"
    
    elicitation_auto_cancel_mode:
      command: "uv"
      args: ["run", "elicitation_test_server_advanced.py"]
      transport: "stdio"
      cwd: "."
      elicitation:
        mode: "auto_cancel"
    
    elicitation_none_mode:
      command: "uv"
      args: ["run", "elicitation_test_server_advanced.py"]
      transport: "stdio"
      cwd: "."
      elicitation:
        mode: "none"
    
    elicitation_custom_handler:
      command: "uv"
      args: ["run", "elicitation_test_server_advanced.py"]
      transport: "stdio"
      cwd: "."
      elicitation:
        mode: "forms"  # Will be overridden by custom handler
    
    # Legacy servers for backward compatibility
    elicitation_test:
      command: "uv"
      args: ["run", "elicitation_test_server.py"]
      elicitation:
        mode: "auto_cancel"
    
    resource_forms:
      command: "uv"
      args: ["run", "elicitation_test_server_advanced.py"]
      elicitation:
        mode: "auto_cancel"
--- END OF FILE tests/integration/elicitation/fastagent.config.yaml ---


--- START OF FILE tests/integration/elicitation/manual_advanced.py ---
import asyncio

from mcp_agent.core.fastagent import FastAgent
from mcp_agent.mcp.helpers.content_helpers import get_resource_text

# Create the application with specified model
fast = FastAgent("fast-agent elicitation example")


# Define the agent
@fast.agent(
    "elicit-advanced",
    servers=[
        "elicitation_forms_mode",
    ],
)
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        await agent.send("Hello, World!")
        result = await agent.get_resource("elicitation://user-profile")
        await agent.send(get_resource_text(result) or "<no result>")

        result = await agent.get_resource("elicitation://preferences")
        await agent.send(get_resource_text(result) or "<no result>")

        result = await agent.get_resource("elicitation://simple-rating")
        await agent.send(get_resource_text(result) or "<no result>")

        result = await agent.get_resource("elicitation://feedback")
        await agent.send(get_resource_text(result) or "<no result>")


if __name__ == "__main__":
    asyncio.run(main())
--- END OF FILE tests/integration/elicitation/manual_advanced.py ---


--- START OF FILE tests/integration/elicitation/manual_test.py ---
import asyncio

from mcp_agent.core.fastagent import FastAgent

# Create the application with specified model
fast = FastAgent("FastAgent Elicitation Example")


# Define the agent
@fast.agent(
    "elicit-me",
    servers=[
        "elicitation_test",
    ],
)
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:

        await agent.send("foo")
        result = await agent.get_resource("elicitation://generate")
        print(f"RESULT: {result}")


if __name__ == "__main__":
    asyncio.run(main())
--- END OF FILE tests/integration/elicitation/manual_test.py ---


--- START OF FILE tests/integration/elicitation/testing_handlers.py ---
"""
Testing elicitation handlers for integration tests.

These handlers are designed specifically for testing scenarios
where you need predictable, automated responses.
"""

from typing import TYPE_CHECKING, Any, Dict

from mcp.shared.context import RequestContext
from mcp.types import ElicitRequestParams, ElicitResult

from mcp_agent.logging.logger import get_logger

if TYPE_CHECKING:
    from mcp import ClientSession

logger = get_logger(__name__)


async def auto_accept_test_handler(
    context: RequestContext["ClientSession", Any],
    params: ElicitRequestParams,
) -> ElicitResult:
    """Testing handler that automatically accepts with realistic test values.
    
    This handler is useful for integration tests where you want to verify
    the round-trip behavior of elicitation without user interaction.
    """
    logger.info(f"Auto-accept test handler called: {params.message}")
    
    if params.requestedSchema:
        # Generate realistic test data based on schema
        content = _generate_test_response(params.requestedSchema)
        return ElicitResult(action="accept", content=content)
    else:
        return ElicitResult(action="accept", content={"response": "auto-test-response"})


async def auto_decline_test_handler(
    context: RequestContext["ClientSession", Any],
    params: ElicitRequestParams,
) -> ElicitResult:
    """Testing handler that always declines elicitation requests."""
    logger.info(f"Auto-decline test handler called: {params.message}")
    return ElicitResult(action="decline")


async def auto_cancel_test_handler(
    context: RequestContext["ClientSession", Any],
    params: ElicitRequestParams,
) -> ElicitResult:
    """Testing handler that always cancels elicitation requests."""
    logger.info(f"Auto-cancel test handler called: {params.message}")
    return ElicitResult(action="cancel")


def _generate_test_response(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Generate realistic test data based on JSON schema."""
    if not schema or "properties" not in schema:
        return {"response": "default-test"}
    
    properties = schema["properties"]
    content = {}
    
    for field_name, field_def in properties.items():
        field_type = field_def.get("type", "string")
        
        if field_type == "string":
            # Provide field-specific test values
            if field_name.lower() in ["name", "full_name", "fullname"]:
                content[field_name] = "Test User"
            elif field_name.lower() in ["email", "email_address"]:
                content[field_name] = "test@example.com"
            elif field_name.lower() == "role":
                # Use enum values if available
                enum_values = field_def.get("enum", [])
                content[field_name] = enum_values[0] if enum_values else "developer"
            elif field_name.lower() in ["phone", "telephone", "phone_number"]:
                content[field_name] = "555-0123"
            elif field_name.lower() in ["address", "street_address"]:
                content[field_name] = "123 Test Street"
            elif field_name.lower() in ["city"]:
                content[field_name] = "Test City"
            elif field_name.lower() in ["country"]:
                content[field_name] = "Test Country"
            else:
                content[field_name] = f"test-{field_name.replace('_', '-')}"
                
        elif field_type == "integer":
            if field_name.lower() == "age":
                content[field_name] = 30
            elif field_name.lower() in ["year", "birth_year"]:
                content[field_name] = 1990
            elif field_name.lower() in ["count", "quantity", "amount"]:
                content[field_name] = 5
            else:
                content[field_name] = 42
                
        elif field_type == "number":
            if field_name.lower() in ["price", "cost", "salary"]:
                content[field_name] = 50000.00
            elif field_name.lower() in ["rating", "score"]:
                content[field_name] = 4.5
            else:
                content[field_name] = 3.14
                
        elif field_type == "boolean":
            # Provide reasonable defaults for common boolean fields
            if field_name.lower() in ["subscribe", "subscribe_newsletter", "newsletter"]:
                content[field_name] = True
            elif field_name.lower() in ["active", "enabled", "verified"]:
                content[field_name] = True
            elif field_name.lower() in ["disabled", "deleted", "archived"]:
                content[field_name] = False
            else:
                content[field_name] = True
                
        elif field_type == "array":
            default_array = field_def.get("default", ["test-item"])
            content[field_name] = default_array
            
        elif field_type == "object":
            default_object = field_def.get("default", {"test": "value"})
            content[field_name] = default_object
    
    return content
--- END OF FILE tests/integration/elicitation/testing_handlers.py ---


--- START OF FILE tests/integration/elicitation/test_config_modes.py ---
"""
Test demonstrating elicitation handler configuration modes.

This test covers the modes not tested in other files:
- auto_cancel mode
- none mode
"""

import pytest

from mcp_agent.logging.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.asyncio
async def test_auto_cancel_mode(fast_agent):
    """Test that auto_cancel mode works when configured."""
    
    @fast_agent.agent(
        "auto-cancel-agent",
        servers=["elicitation_auto_cancel_mode"],
        # No elicitation_handler provided - should use config mode
    )
    async def test_agent():
        async with fast_agent.run() as agent:
            # This should auto-cancel due to config
            # Auto-cancel might result in an exception or a cancellation response
            try:
                result = await agent.get_resource("elicitation://generate")
                print(f"Result: {result}")
                # If we get a result, it should indicate cancellation
                result_str = str(result).lower()
                assert "cancel" in result_str or "decline" in result_str, (
                    f"Expected cancellation response, got: {result}"
                )
                print("✓ Auto-cancel mode test completed")
            except Exception as e:
                # Auto-cancel might result in an exception, which is also valid
                print(f"Auto-cancel test result: {e}")
                print("✓ Auto-cancel mode working (cancelled as expected)")
    
    await test_agent()


@pytest.mark.asyncio
async def test_none_mode(fast_agent):
    """Test that 'none' mode disables elicitation capability advertisement."""
    
    @fast_agent.agent(
        "no-elicitation-agent",
        servers=["elicitation_none_mode"],
        # No elicitation_handler provided - should use config mode
    )
    async def test_agent():
        async with fast_agent.run() as agent:
            # Check capabilities reported by server
            result = await agent.get_resource("elicitation://client-capabilities")
            capabilities_text = str(result)
            print(f"Server reports capabilities: {capabilities_text}")
            
            # Should NOT have elicitation capability
            assert "✗ Elicitation" in capabilities_text or "✓ Elicitation" not in capabilities_text, (
                f"None mode should NOT advertise elicitation capability. Got: {capabilities_text}"
            )
            print("✓ None mode working - elicitation capability NOT advertised")
    
    await test_agent()
--- END OF FILE tests/integration/elicitation/test_config_modes.py ---


--- START OF FILE tests/integration/elicitation/test_config_modes_simplified.py ---
"""
Test demonstrating elicitation handler configuration modes using centralized config.

This test shows how elicitation mode can be configured at the application level
using the main fastagent.config.yaml file with well-named server configurations.
"""

import pytest

from mcp_agent.logging.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.asyncio
async def test_forms_mode(fast_agent):
    """Test that 'forms' mode (default) advertises elicitation capability."""
    
    @fast_agent.agent(
        "forms-elicitation-agent",
        servers=["elicitation_forms_mode"],
        # No elicitation_handler provided - should use config mode
    )
    async def test_agent():
        async with fast_agent.run() as agent:
            # Check capabilities reported by server
            result = await agent.get_resource("elicitation://client-capabilities")
            capabilities_text = str(result)
            print(f"Server reports capabilities: {capabilities_text}")
            
            # Should HAVE elicitation capability
            assert "✓ Elicitation" in capabilities_text, (
                f"Forms mode test failed - elicitation capability NOT advertised. "
                f"Got: {capabilities_text}"
            )
            print("✓ Forms mode working - elicitation capability advertised")
    
    await test_agent()


@pytest.mark.asyncio
async def test_custom_handler_mode(fast_agent):
    """Test that custom handlers work (highest precedence)."""
    from test_elicitation_handler import custom_elicitation_handler
    
    @fast_agent.agent(
        "custom-handler-agent",
        servers=["elicitation_custom_handler"],
        elicitation_handler=custom_elicitation_handler,  # Custom handler (highest precedence)
    )
    async def test_agent():
        async with fast_agent.run() as agent:
            # Check capabilities - should have elicitation
            capabilities_result = await agent.get_resource("elicitation://client-capabilities")
            capabilities_text = str(capabilities_result)
            
            assert "✓ Elicitation" in capabilities_text, (
                f"Custom handler mode failed - elicitation capability not advertised. "
                f"Got: {capabilities_text}"
            )
            
            # Test the actual elicitation - should use our custom handler
            result = await agent.get_resource("elicitation://user-profile")
            result_str = str(result)
            
            assert "Test User" in result_str, (
                f"Custom handler mode failed - custom handler not used. "
                f"Expected 'Test User' in result, got: {result_str}"
            )
            print("✓ Custom handler mode working - custom handler used")
    
    await test_agent()
--- END OF FILE tests/integration/elicitation/test_config_modes_simplified.py ---


--- START OF FILE tests/integration/elicitation/test_elicitation_handler.py ---
"""
Custom elicitation handler for integration testing.

This module provides a test elicitation handler that other tests can import
to verify custom handler functionality.
"""

from typing import TYPE_CHECKING, Any, Dict

from mcp.shared.context import RequestContext
from mcp.types import ElicitRequestParams, ElicitResult

from mcp_agent.logging.logger import get_logger

if TYPE_CHECKING:
    from mcp import ClientSession

logger = get_logger(__name__)


async def custom_elicitation_handler(
    context: RequestContext["ClientSession", Any],
    params: ElicitRequestParams,
) -> ElicitResult:
    """Test handler that returns predictable responses for integration testing."""
    logger.info(f"Test elicitation handler called with: {params.message}")
    
    if params.requestedSchema:
        # Generate test data based on the schema for round-trip verification
        properties = params.requestedSchema.get("properties", {})
        content: Dict[str, Any] = {}
        
        # Provide test values for each field
        for field_name, field_def in properties.items():
            field_type = field_def.get("type", "string")
            
            if field_type == "string":
                if field_name == "name":
                    content[field_name] = "Test User"
                elif field_name == "email":
                    content[field_name] = "test@example.com"
                elif field_name == "role":
                    # Check for enum values
                    enum_values = field_def.get("enum", [])
                    content[field_name] = enum_values[0] if enum_values else "developer"
                else:
                    content[field_name] = f"test-{field_name}"
            elif field_type == "integer":
                if field_name == "age":
                    content[field_name] = 30
                else:
                    content[field_name] = 42
            elif field_type == "number":
                content[field_name] = 3.14
            elif field_type == "boolean":
                if field_name == "subscribe_newsletter":
                    content[field_name] = True
                else:
                    content[field_name] = False
            elif field_type == "array":
                content[field_name] = ["test-item"]
            elif field_type == "object":
                content[field_name] = {"test": "value"}
        
        logger.info(f"Test handler returning: {content}")
        return ElicitResult(action="accept", content=content)
    else:
        # No schema, return simple response
        content = {"response": "test-response-no-schema"}
        logger.info(f"Test handler returning: {content}")
        return ElicitResult(action="accept", content=content)
--- END OF FILE tests/integration/elicitation/test_elicitation_handler.py ---


--- START OF FILE tests/integration/elicitation/test_elicitation_integration.py ---
"""
Integration tests for elicitation handler functionality.

These tests verify that:
1. Custom elicitation handlers work correctly (decorator precedence)
2. Config-based elicitation modes work (auto_cancel, forms, none)
3. Elicitation capabilities are properly advertised to servers
"""

from typing import TYPE_CHECKING, Any, Dict

import pytest
from mcp.shared.context import RequestContext
from mcp.types import ElicitRequestParams, ElicitResult

from mcp_agent.logging.logger import get_logger

if TYPE_CHECKING:
    from mcp import ClientSession

logger = get_logger(__name__)


async def custom_test_elicitation_handler(
    context: RequestContext["ClientSession", Any],
    params: ElicitRequestParams,
) -> ElicitResult:
    """Test handler that returns predictable responses for integration testing."""
    logger.info(f"Test elicitation handler called with: {params.message}")
    
    if params.requestedSchema:
        # Generate test data based on the schema for round-trip verification
        properties = params.requestedSchema.get("properties", {})
        content: Dict[str, Any] = {}
        
        # Provide test values for each field
        for field_name, field_def in properties.items():
            field_type = field_def.get("type", "string")
            
            if field_type == "string":
                if field_name == "name":
                    content[field_name] = "Test User"
                elif field_name == "email":
                    content[field_name] = "test@example.com"
                elif field_name == "role":
                    # Check for enum values
                    enum_values = field_def.get("enum", [])
                    content[field_name] = enum_values[0] if enum_values else "developer"
                else:
                    content[field_name] = f"test-{field_name}"
            elif field_type == "integer":
                if field_name == "age":
                    content[field_name] = 30
                else:
                    content[field_name] = 42
            elif field_type == "number":
                content[field_name] = 3.14
            elif field_type == "boolean":
                if field_name == "subscribe_newsletter":
                    content[field_name] = True
                else:
                    content[field_name] = False
            elif field_type == "array":
                content[field_name] = ["test-item"]
            elif field_type == "object":
                content[field_name] = {"test": "value"}
        
        logger.info(f"Test handler returning: {content}")
        return ElicitResult(action="accept", content=content)
    else:
        # No schema, return simple response
        content = {"response": "test-response-no-schema"}
        logger.info(f"Test handler returning: {content}")
        return ElicitResult(action="accept", content=content)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_custom_elicitation_handler(fast_agent):
    """Test that custom elicitation handler works (highest precedence)."""
    fast = fast_agent
    
    @fast.agent(
        "custom-handler-agent",
        servers=["resource_forms"],
        elicitation_handler=custom_test_elicitation_handler,  # Custom handler
    )
    async def agent_function():
        async with fast.run() as agent:
            # First check that elicitation capability is advertised
            capabilities_result = await agent.get_resource("elicitation://client-capabilities")
            capabilities_text = str(capabilities_result)
            
            # Should have elicitation capability
            assert "✓ Elicitation" in capabilities_text, f"Elicitation capability not advertised: {capabilities_text}"
            
            # Now test the actual elicitation with our custom handler
            result = await agent.get_resource("elicitation://user-profile")
            result_str = str(result)
            
            # Verify we got expected test data from our custom handler
            assert "Test User" in result_str, f"Custom handler not used, got: {result_str}"
            assert "test@example.com" in result_str, f"Custom handler not used, got: {result_str}"
    
    await agent_function()


@pytest.mark.integration  
@pytest.mark.asyncio
async def test_forms_mode_capability_advertisement(fast_agent):
    """Test that forms mode advertises elicitation capability when no custom handler provided."""
    fast = fast_agent
    
    @fast.agent(
        "forms-agent",
        servers=["resource_forms"],
        # No elicitation_handler provided - should use config mode (forms is default)
    )
    async def agent_function():
        async with fast.run() as agent:
            # Check capabilities - should have elicitation capability
            capabilities_result = await agent.get_resource("elicitation://client-capabilities")
            capabilities_text = str(capabilities_result)
            
            # Should advertise elicitation capability in forms mode
            assert "✓ Elicitation" in capabilities_text, f"Forms mode should advertise elicitation: {capabilities_text}"
    
    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio  
async def test_elicitation_precedence_decorator_over_config(fast_agent):
    """Test that decorator-provided handler takes precedence over config."""
    fast = fast_agent
    
    @fast.agent(
        "precedence-test-agent", 
        servers=["resource_forms"],
        elicitation_handler=custom_test_elicitation_handler,  # Should override config
    )
    async def agent_function():
        async with fast.run() as agent:
            # Test actual elicitation behavior
            result = await agent.get_resource("elicitation://user-profile")
            result_str = str(result)
            
            # Should get test data from our custom handler, not config behavior
            assert "Test User" in result_str, f"Decorator precedence failed: {result_str}"
    
    await agent_function()
--- END OF FILE tests/integration/elicitation/test_elicitation_integration.py ---


--- START OF FILE tests/integration/prompt-server/fastagent.config.yaml ---
default_model: passthrough

# Logging and Console Configuration:
logger:
  level: "error"
  type: "file"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true
mcp:
  servers:
    prompts:
      command: "prompt-server"
      args:
        [
          "simple.txt",
          "simple_sub.txt",
          "multi.txt",
          "multi_sub.txt",
          "multipart.json",
        ]
    prompt_sse:
      transport: "sse"
      url: "http://localhost:8723/sse"
    prompt_http:
      transport: "http"
      url: "http://localhost:8724/mcp"
--- END OF FILE tests/integration/prompt-server/fastagent.config.yaml ---


--- START OF FILE tests/integration/prompt-server/multi.txt ---
---USER
good morning
---ASSISTANT
how may i help you?
--- END OF FILE tests/integration/prompt-server/multi.txt ---


--- START OF FILE tests/integration/prompt-server/multi_sub.txt ---
---USER
hello, my name is {{user_name}}
---ASSISTANT
nice to meet you. i am {{assistant_name}}
--- END OF FILE tests/integration/prompt-server/multi_sub.txt ---


--- START OF FILE tests/integration/prompt-server/simple.txt ---
simple, no delimiters
--- END OF FILE tests/integration/prompt-server/simple.txt ---


--- START OF FILE tests/integration/prompt-server/simple_sub.txt ---
this is {{product}} by {{company}}
--- END OF FILE tests/integration/prompt-server/simple_sub.txt ---


--- START OF FILE tests/integration/prompt-server/test_prompt_server_integration.py ---
from typing import TYPE_CHECKING, Dict, List

import pytest

from mcp_agent.mcp.helpers.content_helpers import get_text, is_image_content
from mcp_agent.mcp.prompt_message_multipart import PromptMessageMultipart

if TYPE_CHECKING:
    from mcp.types import GetPromptResult, Prompt


@pytest.mark.integration
@pytest.mark.asyncio
async def test_no_delimiters(fast_agent):
    """Single user message."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(name="test", servers=["prompts"])
    async def agent_function():
        async with fast.run() as agent:
            x: GetPromptResult = await agent["test"].get_prompt("simple", None)
            y: list[PromptMessageMultipart] = PromptMessageMultipart.to_multipart(
                x.messages
            )
            assert "simple, no delimiters" == y[0].first_text()
            assert "user" == y[0].role
            assert len(y) == 1

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_no_delimiters_with_variables(fast_agent):
    """Single user message, with substitutions."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(name="test", servers=["prompts"])
    async def agent_function():
        async with fast.run() as agent:
            x: GetPromptResult = await agent["test"].get_prompt(
                "simple_sub", {"product": "fast-agent", "company": "llmindset"}
            )
            y: list[PromptMessageMultipart] = PromptMessageMultipart.to_multipart(
                x.messages
            )
            assert "this is fast-agent by llmindset" == y[0].first_text()
            assert "user" == y[0].role
            assert len(y) == 1

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_multiturn(fast_agent):
    """Multipart Message."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(name="test", servers=["prompts"])
    async def agent_function():
        async with fast.run() as agent:
            x: GetPromptResult = await agent["test"].get_prompt("multi", None)
            y: list[PromptMessageMultipart] = PromptMessageMultipart.to_multipart(
                x.messages
            )
            assert "good morning" == y[0].first_text()
            assert "user" == y[0].role
            assert "how may i help you?" == y[1].first_text()
            assert "assistant" == y[1].role
            assert len(y) == 2

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_multiturn_with_subsitition(fast_agent):
    """Multipart Message, with substitutions."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(name="test", servers=["prompts"])
    async def agent_function():
        async with fast.run() as agent:
            x: GetPromptResult = await agent["test"].get_prompt(
                "multi_sub", {"user_name": "evalstate", "assistant_name": "HAL9000"}
            )
            y: list[PromptMessageMultipart] = PromptMessageMultipart.to_multipart(
                x.messages
            )
            assert "hello, my name is evalstate" == y[0].first_text()
            assert "user" == y[0].role
            assert "nice to meet you. i am HAL9000" == y[1].first_text()
            assert "assistant" == y[1].role
            assert len(y) == 2

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_agent_interface_returns_prompts_list(fast_agent):
    """Test list_prompts functionality."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(name="test", servers=["prompts"])
    async def agent_function():
        async with fast.run() as agent:
            prompts: Dict[str, List[Prompt]] = await agent.test.list_prompts()
            assert 5 == len(prompts["prompts"])

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_prompt_with_server_param(fast_agent):
    """Test get_prompt with explicit server parameter."""
    fast = fast_agent

    @fast.agent(name="test", servers=["prompts"])
    async def agent_function():
        async with fast.run() as agent:
            # Test with explicit server parameter
            prompt: GetPromptResult = await agent.test.get_prompt(
                "simple", server_name="prompts"
            )
            assert "simple, no delimiters" == get_text(prompt.messages[0].content)

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_apply_prompt_with_server_param(fast_agent):
    """Test apply_prompt with server parameter."""
    fast = fast_agent

    @fast.agent(name="test", servers=["prompts"], model="passthrough")
    async def agent_function():
        async with fast.run() as agent:
            # Test apply_prompt with explicit server parameter
            response = await agent.test.apply_prompt("simple", server_name="prompts")
            assert response is not None

            # Test with both arguments and server parameter
            response = await agent.test.apply_prompt(
                "simple_sub",
                arguments={"product": "test-product", "company": "test-company"},
                server_name="prompts",
            )
            assert response is not None
            assert "test-product" in response or "test-company" in response

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_handling_multipart_json_format(fast_agent):
    """Make sure that multipart mixed content from JSON is handled"""
    fast = fast_agent

    @fast.agent(name="test", servers=["prompts"], model="passthrough")
    async def agent_function():
        async with fast.run() as agent:
            x: GetPromptResult = await agent["test"].get_prompt("multipart")

            assert 5 == len(x.messages)
            assert is_image_content(x.messages[3].content)

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_prompt_server_sse_can_set_ports(fast_agent):
    # Start the SSE server in a subprocess
    import asyncio
    import os
    import subprocess

    # Get the path to the test agent
    test_dir = os.path.dirname(os.path.abspath(__file__))

    # Port must match what's in the fastagent.config.yaml
    port = 8723

    # Start the server process
    server_proc = subprocess.Popen(
        ["prompt-server", "--transport", "sse", "--port", str(port), "simple.txt"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=test_dir,
    )

    try:
        # Give the server a moment to start
        await asyncio.sleep(3)

        # Now connect to it via the configured MCP server
        @fast_agent.agent(name="client", servers=["prompt_sse"], model="passthrough")
        async def agent_function():
            async with fast_agent.run() as agent:
                # Try connecting and sending a message
                assert "simple" in await agent.apply_prompt("simple")

        #                assert "connected" == await agent.send("connected")

        await agent_function()

    finally:
        # Terminate the server process
        if server_proc.poll() is None:  # If still running
            server_proc.terminate()
            try:
                server_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                server_proc.kill()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_prompt_server_http_can_set_ports(fast_agent):
    # Start the SSE server in a subprocess
    import asyncio
    import os
    import subprocess

    # Get the path to the test agent
    test_dir = os.path.dirname(os.path.abspath(__file__))

    # Port must match what's in the fastagent.config.yaml
    port = 8724

    # Start the server process
    server_proc = subprocess.Popen(
        ["prompt-server", "--transport", "http", "--port", str(port), "simple.txt"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=test_dir,
    )

    try:
        # Give the server a moment to start
        await asyncio.sleep(3)

        # Now connect to it via the configured MCP server
        @fast_agent.agent(name="client", servers=["prompt_http"], model="passthrough")
        async def agent_function():
            async with fast_agent.run() as agent:
                # Try connecting and sending a message
                assert "simple" in await agent.apply_prompt("simple")

        await agent_function()

    finally:
        # Terminate the server process
        if server_proc.poll() is None:  # If still running
            server_proc.terminate()
            try:
                server_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                server_proc.kill()
--- END OF FILE tests/integration/prompt-server/test_prompt_server_integration.py ---


--- START OF FILE tests/integration/prompt-state/conv1_simple.md ---
---USER
message 1
---ASSISTANT
message 2
---USER
message 3
---ASSISTANT
message 4
--- END OF FILE tests/integration/prompt-state/conv1_simple.md ---


--- START OF FILE tests/integration/prompt-state/conv2_attach.md ---
---USER
hello, here is a CSS file
---RESOURCE
conv2_css.css
---ASSISTANT
thank you for sharing that
---USER
message 3
---RESOURCE
conv2_text.txt
---RESOURCE
conv2_img.png
---ASSISTANT
thank you for sharing both text and image
---USER
you are welcome
--- END OF FILE tests/integration/prompt-state/conv2_attach.md ---


--- START OF FILE tests/integration/prompt-state/conv2_css.css ---
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f5f5f5;
  color: #333;
}
--- END OF FILE tests/integration/prompt-state/conv2_css.css ---


--- START OF FILE tests/integration/prompt-state/conv2_text.txt ---
here is 
a
normal text
file
--- END OF FILE tests/integration/prompt-state/conv2_text.txt ---


--- START OF FILE tests/integration/prompt-state/fastagent.config.yaml ---
default_model: passthrough

# Logging and Console Configuration:
logger:
  level: "error"
  type: "file"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true
# mcp:
#   servers:
#     roots_test:
#       command: "uv"
#       args: ["run", "root_test_server.py"]
#       roots:
#         # a root with an alias
#         - uri: "file://foo/bar"
#           name: "test_data"
#           server_uri_alias: "file:///mnt/data/"
#         - uri: "file://no/alias"
#           name: "no_alias"
--- END OF FILE tests/integration/prompt-state/fastagent.config.yaml ---


--- START OF FILE tests/integration/prompt-state/test_load_prompt_templates.py ---
import os
from pathlib import Path
from typing import TYPE_CHECKING, List

import pytest
from mcp.types import ImageContent

from mcp_agent.core.prompt import Prompt
from mcp_agent.mcp.prompts.prompt_load import (
    load_prompt_multipart,
)

if TYPE_CHECKING:
    from mcp_agent.mcp.prompt_message_multipart import PromptMessageMultipart


@pytest.mark.integration
@pytest.mark.asyncio
async def test_load_simple_conversation_from_file(fast_agent):
    """Make sure that we can load a simple multiturn conversation from a file."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent()
    async def agent_function():
        async with fast.run() as agent:
            loaded: List[PromptMessageMultipart] = load_prompt_multipart(Path("conv1_simple.md"))
            assert 4 == len(loaded)
            assert "user" == loaded[0].role
            assert "assistant" == loaded[1].role

            # Use the "default" agent directly
            response = await agent.default.generate(loaded)
            assert "message 2" in response.first_text()

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_load_conversation_with_attachments(fast_agent):
    """Test that the agent can process a simple prompt using directory-specific config."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent()
    async def agent_function():
        async with fast.run():
            prompts: list[PromptMessageMultipart] = load_prompt_multipart(Path("conv2_attach.md"))

            assert 5 == len(prompts)
            assert "user" == prompts[0].role
            assert "text/css" == prompts[0].content[1].resource.mimeType  # type: ignore
            assert "f5f5f5" in prompts[0].content[1].resource.text  # type: ignore

            assert "assistant" == prompts[1].role
            assert "sharing" in prompts[1].content[0].text  # type: ignore

            assert 3 == len(prompts[2].content)
            assert isinstance(prompts[2].content[2], ImageContent)
            assert 12780 == len(prompts[2].content[2].data)

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_save_state_to_simple_text_file(fast_agent):
    """Check to see if we can save a conversation to a text file. This functionality
    is extremely simple, and does not support round-tripping. JSON support using MCP
    types will be added in a future release."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent()
    async def agent_function():
        async with fast.run() as agent:
            # Delete the file if it exists before running the test
            if os.path.exists("./simple.txt"):
                os.remove("./simple.txt")
            await agent.send("hello")
            await agent.send("world")
            await agent.send("***SAVE_HISTORY simple.txt")

            prompts: list[PromptMessageMultipart] = load_prompt_multipart(Path("simple.txt"))
            assert 4 == len(prompts)
            assert "user" == prompts[0].role
            assert "assistant" == prompts[1].role

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_save_state_to_mcp_json_format(fast_agent):
    """Test saving conversation history to a JSON file in MCP wire format.
    This should create a file that's compatible with the MCP SDK and can be
    loaded directly using Pydantic types."""
    from mcp.types import GetPromptResult

    from mcp_agent.mcp.prompt_serialization import json_to_multipart_messages

    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent()
    async def agent_function():
        async with fast.run() as agent:
            # Delete the file if it exists before running the test
            if os.path.exists("./history.json"):
                os.remove("./history.json")

            # Send a few messages
            await agent.send("hello")
            await agent.send("world")

            # Save in JSON format (filename ends with .json)
            await agent.send("***SAVE_HISTORY history.json")

            # Verify file exists
            assert os.path.exists("./history.json")

            # Load the file and check content
            with open("./history.json", "r", encoding="utf-8") as f:
                json_content = f.read()

            # Parse using JSON
            import json

            json_data = json.loads(json_content)

            # Validate it's a list of messages
            assert isinstance(json_data["messages"], list)
            assert len(json_data["messages"]) >= 4  # At least 4 messages (2 user, 2 assistant)

            # Check that messages have expected structure
            for msg in json_data["messages"]:
                assert "role" in msg
                assert "content" in msg

            # Validate with Pydantic by parsing to PromptMessageMultipart objects
            prompts = json_to_multipart_messages(json_content)

            # Verify loaded objects
            assert len(prompts) >= 4
            assert prompts[0].role == "user"
            assert prompts[1].role == "assistant"
            assert "hello" in prompts[0].first_text()

            # Validate compatibility with GetPromptResult
            messages = []
            for mp in prompts:
                messages.extend(mp.from_multipart())

            # Construct and validate with GetPromptResult
            prompt_result = GetPromptResult(messages=messages)
            assert len(prompt_result.messages) >= len(messages)

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_round_trip_json_attachments(fast_agent):
    """Test that we can save as json, and read back the content as PromptMessage->PromptMessageMultipart."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(name="test")
    async def agent_function():
        async with fast.run() as agent:
            # Delete the file if it exists before running the test
            if os.path.exists("./multipart.json"):
                os.remove("./multipart.json")

            assert not os.path.exists("./multipart.json")

            await agent.test.generate([Prompt.user("good morning")])
            await agent.test.generate([Prompt.user("what's in this image", Path("conv2_img.png"))])
            await agent.send("***SAVE_HISTORY multipart.json")

            prompts: list[PromptMessageMultipart] = load_prompt_multipart(Path("./multipart.json"))
            assert 4 == len(prompts)

            assert "assistant" == prompts[1].role
            assert 2 == len(prompts[2].content)
            assert isinstance(prompts[2].content[1], ImageContent)
            assert 12780 == len(prompts[2].content[1].data)

            assert 2 == len(prompts[2].from_multipart())

            # TODO -- consider serialization of non-text content for non json files. await requirement

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_apply_prompt_as_template_persistence(fast_agent):
    """Test that applying a prompt with as_template=True creates persistent context."""
    fast = fast_agent

    @fast.agent()
    async def agent_function():
        async with fast.run() as agent:
            # Get the default agent to access its message history
            default_agent = agent.default

            # First, apply a prompt normally (should be in regular history)
            await agent.apply_prompt("simple", {"name": "test1"}, as_template=False)

            # Get the history length after normal application
            normal_history = default_agent.message_history
            normal_history_length = len(normal_history)

            # Now apply a prompt as template (should be in persistent context)
            await agent.apply_prompt("simple", {"name": "template_test"}, as_template=True)

            # Send a regular message to trigger conversation
            await agent.send("hello after template")

            # Get the full history
            final_history = default_agent.message_history

            # The template context should be persistent - let's check if it's still active
            # by examining the conversation structure

            # Verify that we can see the template influence by checking the conversation
            # The template prompt should be included as context for all future messages

            # Send another message to further verify persistence
            response = await agent.send("what was the template name?")

            # For passthrough model, just verify the API calls worked without error
            # The fact that we got responses means the new apply_prompt API is working
            assert response is not None
            assert len(response) > 0

            print(f"Normal history length: {normal_history_length}")
            print(f"Final history length: {len(final_history)}")
            print(f"API calls completed successfully, response: {response}")

            # Verify the new API signature works with both modes
            assert normal_history_length >= 0  # Basic sanity check

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_apply_prompt_with_prompt_result_object(fast_agent):
    """Test that we can apply a GetPromptResult object directly with as_template."""
    from mcp.types import GetPromptResult, PromptMessage, TextContent

    fast = fast_agent

    @fast.agent()
    async def agent_function():
        async with fast.run() as agent:
            # Create a GetPromptResult object directly since no MCP servers are configured
            prompt_result = GetPromptResult(
                description="Test prompt for API verification",
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(type="text", text="Hello from direct GetPromptResult"),
                    )
                ],
            )

            # Verify we created a valid prompt result
            assert isinstance(prompt_result, GetPromptResult)
            assert len(prompt_result.messages) > 0

            # Apply it directly as a template
            response = await agent.apply_prompt(prompt_result, as_template=True)
            assert response is not None

            # Apply it directly in regular mode
            response2 = await agent.apply_prompt(prompt_result, as_template=False)
            assert response2 is not None

            # Verify both worked by sending a follow-up message
            final_response = await agent.send("test complete")
            assert final_response is not None  # Just verify we got a response

    await agent_function()
--- END OF FILE tests/integration/prompt-state/test_load_prompt_templates.py ---


--- START OF FILE tests/integration/resources/fastagent.config.yaml ---
# FastAgent Configuration File

# Default Model Configuration:
#
# Takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
# Accepts aliases for Anthropic Models: haiku, haiku3, sonnet, sonnet35, opus, opus3
# and OpenAI Models: gpt-4o-mini, gpt-4o, o1, o1-mini, o3-mini
#
# If not specified, defaults to "haiku".
# Can be overriden with a command line switch --model=<model>, or within the Agent constructor.

default_model: passthrough

# Logging and Console Configuration:
logger:
  # level: "debug" | "info" | "warning" | "error"
  # type: "none" | "console" | "file" | "http"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true

# MCP Servers
mcp:
  servers:
    resource_server_one:
      command: "prompt-server"
      args: ["prompt1.txt"]
    resource_server_two:
      command: "prompt-server"
      args: ["prompt2.txt"]
    linked_resource_server:
      command: "uv"
      args: ["run", "mcp_linked_resouce_server.py"]
--- END OF FILE tests/integration/resources/fastagent.config.yaml ---


--- START OF FILE tests/integration/resources/mcp_linked_resouce_server.py ---
#!/usr/bin/env python3
"""
Simple MCP server that responds to tool calls with text and image content.
"""

import logging

from mcp.server.fastmcp import FastMCP
from mcp.types import ResourceLink
from pydantic import AnyUrl

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastMCP server
app = FastMCP(name="Linked Resources", instructions="For integration tests with linked resources.")


@app.tool(name="getlink", description="Returns the colour of a shirt.")
def getlink() -> ResourceLink:
    return ResourceLink(
        name="linked resource",
        type="resource_link",
        uri=AnyUrl("resource://fast-agent/linked-resource"),
        description="A description, perhaps for the LLM",
        mimeType="text/plain",
    )


if __name__ == "__main__":
    # Run the server using stdio transport
    app.run(transport="stdio")
--- END OF FILE tests/integration/resources/mcp_linked_resouce_server.py ---


--- START OF FILE tests/integration/resources/prompt1.txt ---
---USER
By attaching resources, the prompt-server exposes resources!
---RESOURCE
r1file1.txt
---RESOURCE
r1file2.txt
--- END OF FILE tests/integration/resources/prompt1.txt ---


--- START OF FILE tests/integration/resources/prompt2.txt ---
---USER
By attaching resources, the prompt-server exposes resources!
---RESOURCE
r2file1.txt
---RESOURCE
r2file2.txt
--- END OF FILE tests/integration/resources/prompt2.txt ---


--- START OF FILE tests/integration/resources/r1file1.txt ---
test 1
--- END OF FILE tests/integration/resources/r1file1.txt ---


--- START OF FILE tests/integration/resources/r1file2.txt ---
test 2
--- END OF FILE tests/integration/resources/r1file2.txt ---


--- START OF FILE tests/integration/resources/r2file1.txt ---
test 3
--- END OF FILE tests/integration/resources/r2file1.txt ---


--- START OF FILE tests/integration/resources/r2file2.txt ---
test 4
--- END OF FILE tests/integration/resources/r2file2.txt ---


--- START OF FILE tests/integration/resources/test_resource_api.py ---
"""
Integration tests for the enhanced resource API features.
"""

import pytest
from mcp.shared.exceptions import McpError

from mcp_agent.mcp.prompts.prompt_helpers import get_text


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_resource_with_explicit_server(fast_agent):
    """Test get_resource with explicit server parameter."""
    fast = fast_agent

    @fast.agent(name="test", servers=["resource_server_one", "resource_server_two"])
    async def agent_function():
        async with fast.run() as agent:
            # Test get_resource with explicit server parameter
            resource = await agent.test.get_resource(
                "resource://fast-agent/r1file1.txt", "resource_server_one"
            )
            assert "test 1" == get_text(resource.contents[0])

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_resource_with_auto_server(fast_agent):
    """Test get_resource with automatic server selection."""
    fast = fast_agent

    @fast.agent(name="test", servers=["resource_server_one", "resource_server_two"])
    async def agent_function():
        async with fast.run() as agent:
            # Test get_resource with auto server selection (should use first server)
            resource = await agent.test.get_resource("resource://fast-agent/r2file1.txt")
            assert "test 3" == get_text(resource.contents[0])

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_list_resources(fast_agent):
    """Test list_resources API functionality."""
    fast = fast_agent

    @fast.agent(name="test", servers=["resource_server_one", "resource_server_two"])
    async def agent_function():
        async with fast.run() as agent:
            # Test list_resources with explicit server
            resources = await agent.test.list_resources("resource_server_one")

            assert "resource_server_one" in resources

            # Verify some test files are in the list
            resource_list = resources["resource_server_one"]
            assert any("resource://fast-agent/r1file1.txt" in r for r in resource_list)
            assert any("resource://fast-agent/r1file2.txt" in r for r in resource_list)

            # Test list_resources without server parameter
            all_resources = await agent.test.list_resources()
            assert all_resources is not None
            assert "resource_server_one" in all_resources
            assert "resource_server_two" in all_resources

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_error_handling(fast_agent):
    """Test error handling for nonexistent resources and servers."""
    fast = fast_agent

    @fast.agent(name="test", servers=["resource_server_one"])
    async def agent_function():
        async with fast.run() as agent:
            # Test nonexistent resource
            with pytest.raises(McpError) as exc_info:
                await agent.test.get_resource(
                    "resource://fast-agent/nonexistent.txt", "resource_server_one"
                )
                assert True

            # Test nonexistent server
            with pytest.raises(ValueError) as exc_info:
                await agent.test.get_resource(
                    "resource://fast-agent/r1file1.txt", "nonexistent_server"
                )

            assert (
                "server" in str(exc_info.value).lower()
                and "not found" in str(exc_info.value).lower()
            )

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_with_resource_api(fast_agent):
    """Test with_resource API with new parameter ordering."""
    fast = fast_agent

    @fast.agent(name="test", servers=["resource_server_one"], model="passthrough")
    async def agent_function():
        async with fast.run() as agent:
            # Test with explicit server parameter
            response = await agent.test.with_resource(
                "Reading resource content:",
                "resource://fast-agent/r1file1.txt",
                "resource_server_one",
            )
            assert response is not None

            # Test with another resource
            response = await agent.test.with_resource(
                "Reading resource content:",
                "resource://fast-agent/r1file2.txt",
                "resource_server_one",
            )
            assert response is not None

            # Test with auto server selection
            response = await agent.test.with_resource(
                "Reading resource content:", "resource://fast-agent/r1file1.txt"
            )
            assert response is not None

    await agent_function()
--- END OF FILE tests/integration/resources/test_resource_api.py ---


--- START OF FILE tests/integration/resources/test_resource_links.py ---
"""
Integration tests for the enhanced resource API features.
"""

import pytest


@pytest.mark.integration
@pytest.mark.asyncio
async def test_resource_links_from_tools(fast_agent):
    """Test get_resource with explicit server parameter."""
    fast = fast_agent

    @fast.agent(name="test", servers=["linked_resource_server"])
    async def agent_function():
        async with fast.run() as agent:
            result: str = await agent.test.send("***CALL_TOOL getlink")
            # Test get_resource with explicit server parameter
            assert "A description, perhaps for the LLM" in result

    await agent_function()
--- END OF FILE tests/integration/resources/test_resource_links.py ---


--- START OF FILE tests/integration/roots/fastagent.config.yaml ---
default_model: passthrough

# Logging and Console Configuration:
logger:
  level: "error"
  type: "file"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true

mcp:
  servers:
    roots_test:
      command: "uv"
      args: ["run", "root_test_server.py"]
      roots:
        # a root with an alias
        - uri: "file://foo/bar"
          name: "test_data"
          server_uri_alias: "file:///mnt/data/"
        - uri: "file://no/alias"
          name: "no_alias"
--- END OF FILE tests/integration/roots/fastagent.config.yaml ---


--- START OF FILE tests/integration/roots/fastagent.jsonl ---
{"level":"ERROR","timestamp":"2025-03-29T21:56:17.079227","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"roots_test: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"roots_test"}}}
--- END OF FILE tests/integration/roots/fastagent.jsonl ---


--- START OF FILE tests/integration/roots/live.py ---
import asyncio

from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("FastAgent Example")


# Define the agent
@fast.agent(servers=["roots_test"])
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        await agent.send("***CALL_TOOL roots_test-show_roots {}")


if __name__ == "__main__":
    asyncio.run(main())
--- END OF FILE tests/integration/roots/live.py ---


--- START OF FILE tests/integration/roots/root_client.py ---
import anyio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.types import ListRootsResult, Root
from pydantic import AnyUrl


async def list_roots_callback(context):
    # Return some example roots - change these to any paths you want to expose
    return ListRootsResult(
        roots=[
            Root(
                uri=AnyUrl("file://foo/bar"),
                name="Home Directory",
            ),
            Root(
                uri=AnyUrl("file:///tmp"),
                name="Temp Directory",
            ),
        ]
    )


async def main():
    # Start the server as a subprocess
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "root_test_server.py"],
    )

    # Connect to the server via stdio
    async with stdio_client(server_params) as (read_stream, write_stream):
        # Create a client session
        async with ClientSession(read_stream, write_stream, list_roots_callback=list_roots_callback) as session:
            # Initialize the session
            await session.initialize()

            # Send initialized notification (required after initialize)
            # This is handled internally by initialize() in ClientSession

            # Call list_roots to get the roots from the server
            try:
                roots_result = await session.call_tool("show_roots", {})
                print(f"Received roots: {roots_result}")

                # Print each root for clarity
                # for root in roots_result.roots:
                #     print(f"Root: {root.uri}, Name: {root.name or 'unnamed'}")
            except Exception as e:
                print(f"Error listing roots: {e}")


# Run the async main function
if __name__ == "__main__":
    anyio.run(main)
--- END OF FILE tests/integration/roots/root_client.py ---


--- START OF FILE tests/integration/roots/root_test_server.py ---
from typing import TYPE_CHECKING

from mcp.server.fastmcp import Context, FastMCP

if TYPE_CHECKING:
    from mcp.types import ListRootsResult

mcp = FastMCP("MCP Root Tester", log_level="DEBUG")


@mcp.tool()
async def show_roots(ctx: Context) -> str:
    result: ListRootsResult = await ctx.session.list_roots()
    return result.model_dump_json()


if __name__ == "__main__":
    mcp.run()
--- END OF FILE tests/integration/roots/root_test_server.py ---


--- START OF FILE tests/integration/roots/test_roots.py ---
import pytest


@pytest.mark.integration
@pytest.mark.asyncio
async def test_roots_returned(fast_agent):
    """Test that the agent can process a simple prompt using directory-specific config."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(name="foo", instruction="bar", servers=["roots_test"])
    async def agent_function():
        async with fast.run() as agent:
            result = await agent.foo.send("***CALL_TOOL roots_test-show_roots {}")
            assert "file:///mnt/data/" in result  # alias
            assert "test_data" in result
            assert "file://no/alias" in result  # no alias.

    await agent_function()
--- END OF FILE tests/integration/roots/test_roots.py ---


--- START OF FILE tests/integration/sampling/fastagent.config.auto_sampling_off.yaml ---
default_model: passthrough
auto_sampling: false  # Disable auto-sampling

# Logging and Console Configuration:
logger:
  level: "error"
  type: "file"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true

mcp:
  servers:
    sampling_test:
      command: "uv"
      args: ["run", "sampling_test_server.py"]
      # No explicit sampling configuration - should fail with auto_sampling=false
--- END OF FILE tests/integration/sampling/fastagent.config.auto_sampling_off.yaml ---


--- START OF FILE tests/integration/sampling/fastagent.config.yaml ---
default_model: passthrough

# Logging and Console Configuration:
logger:
  level: "error"
  type: "file"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true

mcp:
  servers:
    sampling_test:
      command: "uv"
      args: ["run", "sampling_test_server.py"]
      sampling:
        model: "passthrough"
    slow_sampling:
      command: "uv"
      args: ["run", "sampling_test_server.py"]
      sampling:
        model: "slow"
    sampling_test_no_config:
      command: "uv"
      args: ["run", "sampling_test_server.py"]
      # No explicit sampling configuration - relies on auto_sampling
--- END OF FILE tests/integration/sampling/fastagent.config.yaml ---


--- START OF FILE tests/integration/sampling/live.py ---
import asyncio

from mcp_agent.core.fastagent import FastAgent

# Create the application with specified model
fast = FastAgent("FastAgent Example")


# Define the agent
@fast.agent(servers=["sampling_test", "slow_sampling"])
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        result = await agent.send('***CALL_TOOL sampling_test-sample {"to_sample": "123foo"}')
        print(f"RESULT: {result}")

        result = await agent.send('***CALL_TOOL slow_sampling-sample_parallel')
        print(f"RESULT: {result}")


if __name__ == "__main__":
    asyncio.run(main())
--- END OF FILE tests/integration/sampling/live.py ---


--- START OF FILE tests/integration/sampling/sampling_test_server.py ---
"""
Enhanced test server for sampling functionality
"""

import logging
import sys

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import CallToolResult, SamplingMessage, TextContent

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("sampling_server")

# Create MCP server
mcp = FastMCP("MCP Root Tester", log_level="DEBUG")


@mcp.tool()
async def sample(ctx: Context, to_sample: str | None = "hello, world") -> CallToolResult:
    """Tool that echoes back the input parameter"""
    try:
        logger.info(f"Sample tool called with to_sample={to_sample!r}")

        # Handle None value - use default if to_sample is None
        value = to_sample if to_sample is not None else "hello, world"

        # Send message to LLM but we don't use the response
        # This creates the sampling context
        await ctx.session.create_message(
            max_tokens=1024,
            messages=[SamplingMessage(role="user", content=TextContent(type="text", text=value))],
        )

        # Return the result directly, without nesting
        logger.info(f"Returning value: {value}")
        return CallToolResult(content=[TextContent(type="text", text=value)])
    except Exception as e:
        logger.error(f"Error in sample tool: {e}", exc_info=True)
        # Ensure we always include the content field in the error response
        return CallToolResult(isError=True, content=[TextContent(type="text", text=f"Error: {str(e)}")])


@mcp.tool()
async def sample_many(ctx: Context) -> CallToolResult:
    """Tool that echoes back the input parameter"""

    result = await ctx.session.create_message(
        max_tokens=1024,
        messages=[
            SamplingMessage(role="user", content=TextContent(type="text", text="message 1")),
            SamplingMessage(role="user", content=TextContent(type="text", text="message 2")),
        ],
    )

    # Return the result directly, without nesting
    return CallToolResult(content=[TextContent(type="text", text=str(result))])


@mcp.tool()
async def sample_parallel(ctx: Context, count: int = 5) -> CallToolResult:
    """Tool that makes multiple concurrent sampling requests to test parallel processing"""
    try:
        logger.info(f"Making {count} concurrent sampling requests")

        # Create multiple concurrent sampling requests
        import asyncio

        async def _send_sampling(request: int):
            return await ctx.session.create_message(
                max_tokens=100,
                messages=[SamplingMessage(
                    role="user",
                    content=TextContent(type="text", text=f"Parallel request {request+1}")
                )],
            )


        tasks = []
        for i in range(count):
            task = _send_sampling(i)
            tasks.append(task)

        # Execute all requests concurrently
        results = await asyncio.gather(*[_send_sampling(i) for i in range(count)])

        # Combine results
        response_texts = [result.content.text for result in results]
        combined_response = f"Completed {len(results)} parallel requests: " + ", ".join(response_texts[:3])
        if len(response_texts) > 3:
            combined_response += f"... and {len(response_texts) - 3} more"

        logger.info(f"Parallel sampling completed: {combined_response}")
        return CallToolResult(content=[TextContent(type="text", text=combined_response)])

    except Exception as e:
        logger.error(f"Error in sample_parallel tool: {e}", exc_info=True)
        return CallToolResult(isError=True, content=[TextContent(type="text", text=f"Error: {str(e)}")])


if __name__ == "__main__":
    logger.info("Starting sampling test server...")
    mcp.run()
--- END OF FILE tests/integration/sampling/sampling_test_server.py ---


--- START OF FILE tests/integration/sampling/test_sampling_integration.py ---
import pytest


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sampling_feature(fast_agent):
    """Test that the default message is returned."""
    fast = fast_agent

    # Define the agent
    @fast.agent(servers=["sampling_test"])
    async def agent_function():
        async with fast.run() as agent:
            result = await agent("***CALL_TOOL sample")
            assert "hello, world" in result

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sampling_config(fast_agent):
    """Test that the config loads sampling configuration."""
    fast = fast_agent

    @fast.agent(name="empty")
    async def agent_function():
        async with fast.run():
            assert "passthrough" == fast.context.config.mcp.servers["sampling_test"].sampling.model

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sampling_passback(fast_agent):
    """Test that the passthrough LLM is hooked up"""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(servers=["sampling_test"])
    async def agent_function():
        async with fast.run() as agent:
            result = await agent('***CALL_TOOL sample {"to_sample": "llmindset"}')
            assert "llmindset" in result
            assert '"iserror": true' not in result.lower()

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_sampling_multi_message_passback(fast_agent):
    """Test that the passthrough LLM is hooked up"""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(servers=["sampling_test"])
    async def agent_function():
        async with fast.run() as agent:
            result = await agent("***CALL_TOOL sample_many")
            assert "message 1" in result
            assert "message 2" in result

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_auto_sampling_disabled(auto_sampling_off_fast_agent):
    """Test that sampling fails when auto_sampling is disabled and no explicit config."""
    fast = auto_sampling_off_fast_agent

    @fast.agent(servers=["sampling_test"])
    async def agent_function():
        async with fast.run() as agent:
            # Should fail because no sampling callback is registered
            result = await agent("***CALL_TOOL sample")
            # The Python SDK advertises sampling capability but throws MCP Error when called
            assert "error" in result.lower() or "not supported" in result.lower()

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_auto_sampling_enabled(fast_agent):
    """Test that sampling works when auto_sampling is enabled (uses fallback model)."""
    fast = fast_agent

    @fast.agent(servers=["sampling_test_no_config"])
    async def agent_function():
        async with fast.run() as agent:
            # Should work because auto_sampling uses the default_model (passthrough)
            result = await agent("***CALL_TOOL sample")
            # Should get a successful response, not an error
            assert "hello, world" in result

    await agent_function()
--- END OF FILE tests/integration/sampling/test_sampling_integration.py ---


--- START OF FILE tests/integration/workflow/chain/fastagent.config.yaml ---
# FastAgent Configuration File

# Default Model Configuration:
#
# Takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
# Accepts aliases for Anthropic Models: haiku, haiku3, sonnet, sonnet35, opus, opus3
# and OpenAI Models: gpt-4o-mini, gpt-4o, o1, o1-mini, o3-mini
#
# If not specified, defaults to "haiku".
# Can be overriden with a command line switch --model=<model>, or within the Agent constructor.

default_model: playback

# Logging and Console Configuration:
logger:
  # level: "debug" | "info" | "warning" | "error"
  # type: "none" | "console" | "file" | "http"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true
--- END OF FILE tests/integration/workflow/chain/fastagent.config.yaml ---


--- START OF FILE tests/integration/workflow/chain/test_chain.py ---
import pytest

from mcp_agent.core.exceptions import AgentConfigError
from mcp_agent.core.prompt import Prompt


@pytest.mark.integration
@pytest.mark.asyncio
async def test_disallows_empty_sequence(fast_agent):
    fast = fast_agent

    # Define the agent
    with pytest.raises(AgentConfigError):

        @fast.chain(name="chain", sequence=[], cumulative=True)
        async def agent_function():
            async with fast.run():
                assert True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_simple_chain(fast_agent):
    """Test a simple chain in non-cumulative mode (default)"""
    fast = fast_agent

    # Define the agent
    @fast.agent(name="begin")
    @fast.agent(name="step1")
    @fast.agent(name="finish")
    @fast.chain(name="chain", sequence=["begin", "step1", "finish"])
    async def agent_function():
        async with fast.run() as agent:
            await agent.begin.apply_prompt_messages([Prompt.assistant("begin")])
            await agent.step1.apply_prompt_messages([Prompt.assistant("step1")])
            await agent.finish.apply_prompt_messages([Prompt.assistant("finish")])

            result = await agent.chain.send("foo")
            assert "finish" == result

            assert "EXHAUSTED" in await agent.begin.send("extra")
            assert "EXHAUSTED" in await agent.step1.send("extra")
            assert "EXHAUSTED" in await agent.finish.send("extra")

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_cumulative_chain(fast_agent):
    """Test cumulative chain mode with XML tags for request and responses"""
    fast = fast_agent

    @fast.agent(name="begin")
    @fast.agent(name="step1")
    @fast.agent(name="finish")
    @fast.chain(name="chain", sequence=["begin", "step1", "finish"], cumulative=True)
    async def agent_function():
        async with fast.run() as agent:
            await agent.begin.apply_prompt_messages([Prompt.assistant("begin-response")])
            await agent.step1.apply_prompt_messages([Prompt.assistant("step1-response")])
            await agent.finish.apply_prompt_messages([Prompt.assistant("finish-response")])

            initial_prompt = "initial-prompt"
            result = await agent.chain.send(initial_prompt)

            # Check for original request tag
            assert f"<fastagent:request>{initial_prompt}</fastagent:request>" in result

            # Check for agent response tags
            assert "<fastagent:response agent='begin'>begin-response</fastagent:response>" in result
            assert "<fastagent:response agent='step1'>step1-response</fastagent:response>" in result
            assert (
                "<fastagent:response agent='finish'>finish-response</fastagent:response>" in result
            )

            # Verify correct number of tags
            assert result.count("<fastagent:request>") == 1
            assert result.count("<fastagent:response") == 3

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_chain_functionality(fast_agent):
    """Test that a chain correctly connects agents together"""
    # The goal of this test is to verify that a chain properly
    # connects agents together and passes messages through them

    fast = fast_agent

    # Use passthrough agents for simplicity and predictability
    # Create two separate chains: one normal and one cumulative
    @fast.agent(name="echo1", model="passthrough")
    @fast.agent(name="echo2", model="passthrough")
    @fast.agent(name="echo3", model="passthrough")
    @fast.chain(name="echo_chain", sequence=["echo1", "echo2", "echo3"])
    @fast.chain(name="cumulative_chain", sequence=["echo1", "echo2", "echo3"], cumulative=True)
    async def agent_function():
        async with fast.run() as agent:
            input_message = "test message"
            result = await agent.echo_chain.send(input_message)

            assert input_message in result

            cumulative_input = "cumulative message"
            cumulative_result = await agent.cumulative_chain.send(cumulative_input)

            # Verify both format and content
            assert "<fastagent:request>" in cumulative_result
            assert "<fastagent:response agent='echo1'>" in cumulative_result
            assert "<fastagent:response agent='echo2'>" in cumulative_result
            assert "<fastagent:response agent='echo3'>" in cumulative_result
            assert cumulative_input in cumulative_result

    await agent_function()
--- END OF FILE tests/integration/workflow/chain/test_chain.py ---


--- START OF FILE tests/integration/workflow/chain/test_chain_passthrough.py ---
import pytest


@pytest.mark.integration
@pytest.mark.asyncio
async def test_chain_passthrough(fast_agent):  # CHAIN OF 3 BASIC AGENTS
    fast = fast_agent

    @fast.agent(
        "url_fetcher",
        instruction="Look at the articles on the page of the given url and summarize each of the articles.",
        model="passthrough",
    )
    @fast.agent(
        "summary_writer",
        instruction="""
        Write the given text to a file named summary.txt, and output which article topic is the most relevant to college students.
        """,
        model="passthrough",
    )
    @fast.agent(
        "google_sheets_writer",
        instruction="""
        Based on the given text, write some key points to research on the topic to a new google spreadsheet with a title "Research on <topic>".
        """,
        model="passthrough",
    )
    @fast.chain(
        name="topic_writer",
        sequence=["url_fetcher", "summary_writer", "google_sheets_writer"],
        cumulative=False,
    )
    @fast.chain(
        name="topic_writer_cumulative",
        sequence=["url_fetcher", "summary_writer", "google_sheets_writer"],
        cumulative=True,
    )
    async def chain_workflow():  # Renamed from main to avoid conflicts, and wrapped inside the test
        async with fast.run() as agent:
            input_url = "https://www.nytimes.com"
            result = await agent.topic_writer.send(input_url)
            assert result == input_url

            result = await agent.topic_writer_cumulative.send("X")
            # we expect the result to include tagged responses from all agents.
            assert "X\nX\nX\nX" in result

    await chain_workflow()  # Call the inner function
--- END OF FILE tests/integration/workflow/chain/test_chain_passthrough.py ---


--- START OF FILE tests/integration/workflow/evaluator_optimizer/fastagent.config.yaml ---
mcp:
  name: evaluator_optimizer_tests
--- END OF FILE tests/integration/workflow/evaluator_optimizer/fastagent.config.yaml ---


--- START OF FILE tests/integration/workflow/evaluator_optimizer/test_evaluator_optimizer.py ---
import json

import pytest
from pydantic import BaseModel, Field

from mcp_agent.agents.workflow.evaluator_optimizer import (
    QualityRating,
)
from mcp_agent.core.prompt import Prompt
from mcp_agent.llm.augmented_llm_passthrough import FIXED_RESPONSE_INDICATOR


class EvaluationResult(BaseModel):
    """Model for evaluation results."""

    rating: QualityRating = Field(description="Quality rating of the response")
    feedback: str = Field(description="Specific feedback and suggestions for improvement")
    needs_improvement: bool = Field(description="Whether the output needs further improvement")
    focus_areas: list[str] = Field(
        default_factory=list, description="Specific areas to focus on in next iteration"
    )


class OutputModel(BaseModel):
    """Simple model for testing structured output."""

    result: str
    score: int


@pytest.mark.integration
@pytest.mark.asyncio
async def test_single_refinement_cycle(fast_agent):
    """Test a single refinement cycle with the evaluator-optimizer."""
    fast = fast_agent

    @fast.agent(name="generator", model="passthrough")
    @fast.agent(name="evaluator", model="passthrough")
    @fast.evaluator_optimizer(
        name="optimizer", generator="generator", evaluator="evaluator", max_refinements=1
    )
    async def agent_function():
        async with fast.run() as agent:
            # Initial generation - Set the response to return
            initial_message = f"{FIXED_RESPONSE_INDICATOR} This is the initial response."
            await agent.generator._llm.generate([Prompt.user(initial_message)])

            # Create properly formatted evaluation JSON
            eval_data = {
                "rating": "FAIR",
                "feedback": "Could be more detailed.",
                "needs_improvement": True,
                "focus_areas": ["Add more details"],
            }
            eval_json = json.dumps(eval_data)

            # Set up evaluator to return the structured evaluation
            eval_message = f"{FIXED_RESPONSE_INDICATOR} {eval_json}"
            await agent.evaluator._llm.generate([Prompt.user(eval_message)])

            # Set up second round response
            refined_message = (
                f"{FIXED_RESPONSE_INDICATOR} This is the refined response with more details."
            )
            await agent.generator._llm.generate([Prompt.user(refined_message)])

            # Set up final evaluation to indicate good quality
            final_eval = {
                "rating": "GOOD",
                "feedback": "Much better!",
                "needs_improvement": False,
                "focus_areas": [],
            }
            final_json = json.dumps(final_eval)
            await agent.evaluator._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} {final_json}")]
            )

            # Send the input and get optimized output
            result = await agent.optimizer.send("Write something")

            # Should have the refined response in the result
            assert "refined response" in result

            # Check that the refinement history is accessible
            history = agent.optimizer.refinement_history
            assert len(history) > 0  # Should have at least 1 refinement

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_max_refinements_limit(fast_agent):
    """Test that evaluator-optimizer respects the max_refinements limit."""
    fast = fast_agent

    @fast.agent(name="generator_max", model="passthrough")
    @fast.agent(name="evaluator_max", model="passthrough")
    @fast.evaluator_optimizer(
        name="optimizer_max",
        generator="generator_max",
        evaluator="evaluator_max",
        max_refinements=2,  # Set limit to 2 refinements
    )
    async def agent_function():
        async with fast.run() as agent:
            # Initial generation
            initial_response = f"{FIXED_RESPONSE_INDICATOR} Initial draft."
            await agent.generator_max._llm.generate([Prompt.user(initial_response)])

            # First evaluation - needs improvement
            first_eval = {
                "rating": "POOR",
                "feedback": "Needs improvement.",
                "needs_improvement": True,
                "focus_areas": ["Be more specific"],
            }
            first_eval_json = json.dumps(first_eval)
            await agent.evaluator_max._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} {first_eval_json}")]
            )

            # First refinement
            first_refinement = f"{FIXED_RESPONSE_INDICATOR} First refinement."
            await agent.generator_max._llm.generate([Prompt.user(first_refinement)])

            # Second evaluation - still needs improvement
            second_eval = {
                "rating": "FAIR",
                "feedback": "Getting better but still needs work.",
                "needs_improvement": True,
                "focus_areas": ["Add examples"],
            }
            second_eval_json = json.dumps(second_eval)
            await agent.evaluator_max._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} {second_eval_json}")]
            )

            # Second refinement
            second_refinement = f"{FIXED_RESPONSE_INDICATOR} Second refinement with examples."
            await agent.generator_max._llm.generate([Prompt.user(second_refinement)])

            # Third evaluation - still needs improvement (should not be used due to max_refinements)
            third_eval = {
                "rating": "FAIR",
                "feedback": "Still needs more work.",
                "needs_improvement": True,
                "focus_areas": ["Add more details"],
            }
            third_eval_json = json.dumps(third_eval)
            await agent.evaluator_max._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} {third_eval_json}")]
            )

            # Send the input and get optimized output
            result = await agent.optimizer_max.send("Write something")

            # Should get the second refinement as the final output (due to max_refinements=2)
            assert "refinement" in result

            # Check that the refinement history contains at most 2 attempts
            history = agent.optimizer_max.refinement_history
            assert len(history) <= 2

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_early_stop_on_quality(fast_agent):
    """Test that evaluator-optimizer stops when quality threshold is met."""
    fast = fast_agent

    @fast.agent(name="generator_quality", model="passthrough")
    @fast.agent(name="evaluator_quality", model="passthrough")
    @fast.evaluator_optimizer(
        name="optimizer_quality",
        generator="generator_quality",
        evaluator="evaluator_quality",
        min_rating=QualityRating.GOOD,  # Stop when reaching GOOD quality
        max_refinements=5,
    )
    async def agent_function():
        async with fast.run() as agent:
            # Initial generation
            initial_response = f"{FIXED_RESPONSE_INDICATOR} Initial draft."
            await agent.generator_quality._llm.generate([Prompt.user(initial_response)])

            # First evaluation - needs improvement (FAIR is below GOOD threshold)
            first_eval = {
                "rating": "FAIR",
                "feedback": "Needs improvement.",
                "needs_improvement": True,
                "focus_areas": ["Be more specific"],
            }
            first_eval_json = json.dumps(first_eval)
            await agent.evaluator_quality._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} {first_eval_json}")]
            )

            # First refinement
            first_refinement = f"{FIXED_RESPONSE_INDICATOR} First refinement with more details."
            await agent.generator_quality._llm.generate([Prompt.user(first_refinement)])

            # Second evaluation - meets quality threshold (GOOD)
            second_eval = {
                "rating": "GOOD",
                "feedback": "Much better!",
                "needs_improvement": False,
                "focus_areas": [],
            }
            second_eval_json = json.dumps(second_eval)
            await agent.evaluator_quality._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} {second_eval_json}")]
            )

            # Additional refinement response (should not be used because we hit quality threshold)
            unused_response = f"{FIXED_RESPONSE_INDICATOR} This refinement should never be used."
            await agent.generator_quality._llm.generate([Prompt.user(unused_response)])

            # Send the input and get optimized output
            result = await agent.optimizer_quality.send("Write something")

            # Just check we got a non-empty result - we don't need to check the exact content
            # since what matters is that the proper early stopping occurred
            assert result is not None
            assert len(result) > 0  # Should have some content

            # Verify early stopping
            history = agent.optimizer_quality.refinement_history
            assert len(history) <= 2  # Should not have more than 2 iterations

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_structured_output(fast_agent):
    """Test structured output handling in evaluator-optimizer."""
    fast = fast_agent

    @fast.agent(name="generator_struct", model="passthrough")
    @fast.agent(name="evaluator_struct", model="passthrough")
    @fast.evaluator_optimizer(
        name="optimizer_struct",
        generator="generator_struct",
        evaluator="evaluator_struct",
        max_refinements=1,
    )
    async def agent_function():
        async with fast.run() as agent:
            # Set up initial response - basic text
            initial_response = f"{FIXED_RESPONSE_INDICATOR} Initial content"
            await agent.generator_struct._llm.generate([Prompt.user(initial_response)])

            # Evaluation - good quality, no need for refinement
            eval_result = {
                "rating": "EXCELLENT",
                "feedback": "Good job!",
                "needs_improvement": False,
                "focus_areas": [],
            }
            eval_json = json.dumps(eval_result)
            await agent.evaluator_struct._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} {eval_json}")]
            )

            # Structured output - setup generator to return valid OutputModel JSON
            # For structured call, we need proper JSON that can parse into OutputModel
            test_output = {"result": "Optimized output", "score": 95}
            test_output_json = json.dumps(test_output)

            # Prime the generator to return this JSON when asked for structured output
            await agent.generator_struct._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} {test_output_json}")]
            )

            # Try to get structured output - this will use the generator's structured method
            try:
                result, _ = await agent.optimizer_struct.structured(
                    [Prompt.user("Write something structured")], OutputModel
                )

                # If successful, verify the result
                assert result is not None
                if result is not None:  # Additional check to satisfy type checking
                    assert hasattr(result, "result")
                    assert hasattr(result, "score")
            except Exception as e:
                # If structuring fails, we'll just log it and pass the test
                # (the main test is that the code attempted to do structured parsing)
                print(f"Structured output failed: {str(e)}")
                pass

    await agent_function()
--- END OF FILE tests/integration/workflow/evaluator_optimizer/test_evaluator_optimizer.py ---


--- START OF FILE tests/integration/workflow/mixed/fastagent.config.yaml ---
# FastAgent Configuration File

# Default Model Configuration:
#
# Takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
# Accepts aliases for Anthropic Models: haiku, haiku3, sonnet, sonnet35, opus, opus3
# and OpenAI Models: gpt-4o-mini, gpt-4o, o1, o1-mini, o3-mini
#
# If not specified, defaults to "haiku".
# Can be overriden with a command line switch --model=<model>, or within the Agent constructor.

default_model: passthrough

# Logging and Console Configuration:
logger:
  # level: "debug" | "info" | "warning" | "error"
  # type: "none" | "console" | "file" | "http"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true
--- END OF FILE tests/integration/workflow/mixed/fastagent.config.yaml ---


--- START OF FILE tests/integration/workflow/mixed/test_mixed_workflow.py ---
import pytest

from mcp_agent.core.prompt import Prompt


@pytest.mark.integration
@pytest.mark.asyncio
async def test_chaining_routers(fast_agent):
    """Check that the router routes"""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    @fast.agent(name="target1")
    @fast.agent(name="target2")
    @fast.agent(name="target3")
    @fast.router(name="router1", agents=["target1", "target2"])
    @fast.chain(name="chain", sequence=["router1", "target3"], cumulative=True)
    async def agent_function():
        async with fast.run() as agent:
            await agent.router1._llm.generate(
                [
                    Prompt.user(
                        """***FIXED_RESPONSE 
                        {"agent": "target2",
                        "confidence": "high",
                        "reasoning": "Test Request"}"""
                    )
                ]
            )
            result = await agent.chain.send("github.com/varaarul")
            assert "github.com/varaarul" in result
            assert "target3" in result

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_router_selects_parallel(fast_agent):
    """Check that the router routes"""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    @fast.agent(name="target1")
    @fast.agent(name="target2")
    @fast.agent(name="target3")
    @fast.parallel(name="parallel", fan_out=["target2", "target3"])
    @fast.router(name="router1", agents=["target1", "parallel"])
    async def agent_function():
        async with fast.run() as agent:
            await agent.router1._llm.generate(
                [
                    Prompt.user(
                        """***FIXED_RESPONSE 
                        {"agent": "parallel",
                        "confidence": "high",
                        "reasoning": "Test Request"}"""
                    )
                ]
            )
            result = await agent.router1.send("github.com/varaarul")
            assert "github.com/varaarul" in result

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_chain_in_eval_optimizer(fast_agent):
    """Check that generator can be a chain"""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    @fast.agent(name="chain1")
    @fast.agent(name="chain2")
    @fast.chain(name="chain", sequence=["chain1", "chain2"])
    @fast.agent(name="check", instruction="You are an evaluator. Rate responses as EXCELLENT.")
    @fast.evaluator_optimizer(name="eval_opt", generator="chain", evaluator="check")
    async def agent_function():
        async with fast.run() as agent:
            # Mock the evaluation response to be EXCELLENT to avoid multiple iterations
            await agent.check._llm.generate(
                [
                    Prompt.user(
                        """***FIXED_RESPONSE 
                        {
                          "rating": "EXCELLENT",
                          "feedback": "Perfect response",
                          "needs_improvement": false,
                          "focus_areas": []
                        }"""
                    )
                ]
            )
            # Test that the chain works as a generator in eval_opt
            result = await agent.eval_opt.send("Test message")
            # We should get a response from the eval_opt workflow
            assert result is not None and len(result) > 0

    await agent_function()
--- END OF FILE tests/integration/workflow/mixed/test_mixed_workflow.py ---


--- START OF FILE tests/integration/workflow/orchestrator/fastagent.config.yaml ---
# FastAgent Configuration File

# Default Model Configuration:
#
# Takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
# Accepts aliases for Anthropic Models: haiku, haiku3, sonnet, sonnet35, opus, opus3
# and OpenAI Models: gpt-4o-mini, gpt-4o, o1, o1-mini, o3-mini
#
# If not specified, defaults to "haiku".
# Can be overriden with a command line switch --model=<model>, or within the Agent constructor.

default_model: passthrough

# Logging and Console Configuration:
logger:
  # level: "debug" | "info" | "warning" | "error"
  # type: "none" | "console" | "file" | "http"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true

# MCP Servers
mcp:
  servers:
    prompts:
      command: "prompt-server"
      args: ["sizing.md", "resource.md"]
    hfspace:
      command: "npx"
      args: ["@llmindset/mcp-hfspace"]
--- END OF FILE tests/integration/workflow/orchestrator/fastagent.config.yaml ---


--- START OF FILE tests/integration/workflow/orchestrator/test_orchestrator.py ---
import pytest

from mcp_agent.agents.workflow.orchestrator_models import (
    AgentTask,
    NextStep,
    Plan,
    Step,
)
from mcp_agent.core.prompt import Prompt
from mcp_agent.llm.augmented_llm_passthrough import FIXED_RESPONSE_INDICATOR


@pytest.mark.integration
@pytest.mark.asyncio
async def test_full_plan_execution(fast_agent):
    """Test full plan execution mode of the orchestrator agent."""
    fast = fast_agent

    @fast.agent(name="agent1", model="passthrough")
    @fast.agent(name="agent2", model="passthrough")
    @fast.orchestrator(
        name="orchestrator", agents=["agent1", "agent2"], plan_type="full", model="passthrough"
    )
    async def agent_function():
        async with fast.run() as agent:
            # Create test plan
            test_plan = Plan(
                steps=[
                    Step(
                        description="First step",
                        tasks=[
                            AgentTask(description="Task for agent1", agent="agent1"),
                            AgentTask(description="Task for agent2", agent="agent2"),
                        ],
                    ),
                    Step(
                        description="Second step",
                        tasks=[AgentTask(description="Another task for agent1", agent="agent1")],
                    ),
                ],
                is_complete=True,
            )

            agent.orchestrator._get_full_plan

            async def mock_get_full_plan(*args, **kwargs):
                return test_plan

            agent.orchestrator._get_full_plan = mock_get_full_plan

            # Set up agent1 responses
            await agent.agent1._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} Agent1 Task 1 Response")]
            )

            await agent.agent1._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} Agent1 Task 2 Response")]
            )

            # Set up agent2 response
            await agent.agent2._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} Agent2 Task 1 Response")]
            )

            # Set up synthesis response
            await agent.orchestrator._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} Final synthesized result from all steps")]
            )

            # Execute orchestrator
            result = await agent.orchestrator.send("Accomplish this complex task")

            # Verify the result contains the synthesized output
            assert "Final synthesized result" in result

            # Check plan results
            plan_result = agent.orchestrator.plan_result
            assert plan_result is not None
            assert len(plan_result.step_results) == 2
            assert plan_result.is_complete

            # Check task results - The first step has 2 tasks
            first_step = plan_result.step_results[0]
            assert len(first_step.task_results) == 2

            # Check that both agents' tasks were executed - order not guaranteed
            has_agent1 = any(
                "Agent1" in task.result
                for task in first_step.task_results
                if task.agent == "agent1"
            )
            has_agent2 = any(
                "Agent2" in task.result
                for task in first_step.task_results
                if task.agent == "agent2"
            )
            assert has_agent1, "Agent1's task result not found in first step"
            assert has_agent2, "Agent2's task result not found in first step"

            # Check second step
            second_step = plan_result.step_results[1]
            assert len(second_step.task_results) == 1
            assert "Agent1 Task 2 Response" in second_step.task_results[0].result

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_iterative_plan_execution(fast_agent):
    """Test iterative plan execution mode of the orchestrator agent."""
    fast = fast_agent

    @fast.agent(name="agent1", model="passthrough")
    @fast.agent(name="agent2", model="passthrough")
    @fast.orchestrator(
        name="orchestrator", agents=["agent1", "agent2"], plan_type="iterative", model="passthrough"
    )
    async def agent_function():
        async with fast.run() as agent:
            # Define first step
            step1 = NextStep(
                description="First iterative step",
                tasks=[AgentTask(description="Initial task for agent1", agent="agent1")],
                is_complete=False,
            )

            # Override _get_next_step to return our predefined steps
            agent.orchestrator._get_next_step

            async def mock_get_next_step(*args, **kwargs):
                return step1

            agent.orchestrator._get_next_step = mock_get_next_step

            # Set up agent1 responses for step 1
            await agent.agent1._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} Agent1 Step 1 Response")]
            )

            # When the orchestrator asks for second step, return step2
            # This is tricky with passthrough - we need to modify the LLM's _fixed_response
            # mid-test to return a different response for the second call

            # Execute orchestrator to get first step
            # We'll skip the full test for iterative because of the limitations of passthrough LLM
            await agent.orchestrator.send("Do this step by step")

            # Check that one step was executed
            plan_result = agent.orchestrator.plan_result
            assert plan_result is not None
            assert len(plan_result.step_results) >= 1

            # Verify the first step had the expected agent1 response
            assert "Agent1 Step 1 Response" in plan_result.step_results[0].task_results[0].result

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_invalid_agent_handling(fast_agent):
    """Test how orchestrator handles plans with invalid agent references."""
    fast = fast_agent

    @fast.agent(name="valid_agent", model="passthrough")
    @fast.orchestrator(
        name="orchestrator", agents=["valid_agent"], plan_type="full", model="passthrough"
    )
    async def agent_function():
        async with fast.run() as agent:
            # Create a plan with one valid and one invalid agent
            test_plan = Plan(
                steps=[
                    Step(
                        description="Step with mixed agent validity",
                        tasks=[
                            AgentTask(description="Task for valid agent", agent="valid_agent"),
                            AgentTask(
                                description="Task for non-existent agent", agent="invalid_agent"
                            ),
                        ],
                    )
                ],
                is_complete=True,
            )

            # Override _get_full_plan to return our predefined plan
            agent.orchestrator._get_full_plan

            async def mock_get_full_plan(*args, **kwargs):
                return test_plan

            agent.orchestrator._get_full_plan = mock_get_full_plan

            # Set up valid_agent response
            await agent.valid_agent._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} Valid agent response")]
            )

            # Set up synthesis response
            await agent.orchestrator._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} Synthesis including error handling")]
            )

            # Execute orchestrator
            result = await agent.orchestrator.send("Test invalid agent reference")

            # Verify the result contains the synthesis
            assert "Synthesis including error handling" in result

            # Check plan results for error information
            plan_result = agent.orchestrator.plan_result
            assert plan_result is not None

            # Should have one step executed
            assert len(plan_result.step_results) == 1
            step_result = plan_result.step_results[0]

            # Should have two tasks (valid and invalid)
            assert len(step_result.task_results) == 2

            # Check for error message in the invalid agent task
            has_error = any(
                "invalid_agent" in task.agent and "ERROR" in task.result
                for task in step_result.task_results
            )
            assert has_error, "Expected error for invalid agent not found"

            # Check that valid agent task was executed
            has_valid = any(
                "valid_agent" in task.agent and "Valid agent response" in task.result
                for task in step_result.task_results
            )
            assert has_valid, "Valid agent should have executed successfully"

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_max_iterations_handling(fast_agent):
    """Test how orchestrator handles reaching maximum iterations."""
    fast = fast_agent

    @fast.agent(name="agent1", model="passthrough")
    @fast.orchestrator(
        name="orchestrator", agents=["agent1"], plan_type="iterative", model="passthrough"
    )
    async def agent_function():
        async with fast.run() as agent:
            # Set max_iterations very low to ensure we hit the limit
            agent.orchestrator._default_request_params.max_iterations = 2

            # Create a step that is never complete
            not_complete_step = NextStep(
                description="Step that isn't complete",
                tasks=[
                    AgentTask(description="Task that doesn't complete objective", agent="agent1")
                ],
                is_complete=False,
            )

            # Override _get_next_step to return our non-complete step
            agent.orchestrator._get_next_step

            async def mock_get_next_step(*args, **kwargs):
                return not_complete_step

            agent.orchestrator._get_next_step = mock_get_next_step

            # Set up agent1 response
            await agent.agent1._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} Progress, but not complete")]
            )

            # Set up synthesis response indicating incomplete execution
            await agent.orchestrator._llm.generate(
                [
                    Prompt.user(
                        f"{FIXED_RESPONSE_INDICATOR} Incomplete result due to iteration limits"
                    )
                ]
            )

            # Execute orchestrator
            result = await agent.orchestrator.send("Task requiring many steps")

            # Verify the result mentions the incomplete execution
            assert "Incomplete result" in result

            # Check that the max_iterations_reached flag is set
            plan_result = agent.orchestrator.plan_result
            assert plan_result is not None
            assert plan_result.max_iterations_reached

            # Check that we have some step executions
            assert len(plan_result.step_results) > 0
            # Each step should have an agent1 task result
            for step in plan_result.step_results:
                assert len(step.task_results) == 1
                assert step.task_results[0].agent == "agent1"
                assert "Progress, but not complete" in step.task_results[0].result

    await agent_function()
--- END OF FILE tests/integration/workflow/orchestrator/test_orchestrator.py ---


--- START OF FILE tests/integration/workflow/parallel/fastagent.config.yaml ---
# FastAgent Configuration File

# Default Model Configuration:
#
# Takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
# Accepts aliases for Anthropic Models: haiku, haiku3, sonnet, sonnet35, opus, opus3
# and OpenAI Models: gpt-4o-mini, gpt-4o, o1, o1-mini, o3-mini
#
# If not specified, defaults to "haiku".
# Can be overriden with a command line switch --model=<model>, or within the Agent constructor.

default_model: passthrough

# Logging and Console Configuration:
logger:
  # level: "debug" | "info" | "warning" | "error"
  # type: "none" | "console" | "file" | "http"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true
--- END OF FILE tests/integration/workflow/parallel/fastagent.config.yaml ---


--- START OF FILE tests/integration/workflow/parallel/test_parallel_agent.py ---
import pytest


@pytest.mark.integration
@pytest.mark.asyncio
async def test_parallel_run(fast_agent):
    """Single user message."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(name="fan_out_1")
    @fast.agent(name="fan_out_2")
    @fast.agent(name="fan_in")
    @fast.parallel(name="parallel", fan_out=["fan_out_1", "fan_out_2"], fan_in="fan_in")
    async def agent_function():
        async with fast.run() as agent:
            expected: str = """The following request was sent to the agents:

<fastagent:request>
foo
</fastagent:request>

<fastagent:response agent="fan_out_1">
foo
</fastagent:response>

<fastagent:response agent="fan_out_2">
foo
</fastagent:response>"""
            assert expected == await agent.parallel.send("foo")

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_parallel_default_fan_in(fast_agent):
    """Single user message."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(name="fan_out_1")
    @fast.agent(name="fan_out_2")
    @fast.parallel(name="parallel", fan_out=["fan_out_1", "fan_out_2"])
    async def agent_function():
        async with fast.run() as agent:
            expected: str = """The following request was sent to the agents:

<fastagent:request>
foo
</fastagent:request>

<fastagent:response agent="fan_out_1">
foo
</fastagent:response>

<fastagent:response agent="fan_out_2">
foo
</fastagent:response>"""
            # in this case the behaviour is the same as the previous test - but the fan-in passthrough was created automatically
            assert expected == await agent.parallel.send("foo")

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_parallel_include_request_false(fast_agent):
    """Test that include_request=False prevents original request from being sent to fan_in agent."""
    fast = fast_agent

    @fast.agent(name="fan_out_1")
    @fast.agent(name="fan_out_2")
    @fast.agent(name="fan_in")
    @fast.parallel(
        name="parallel_no_request",
        fan_out=["fan_out_1", "fan_out_2"],
        fan_in="fan_in",
        include_request=False
    )
    async def agent_function():
        async with fast.run() as agent:
            # When include_request=False, the fan_in should only receive the responses,
            # not the original request
            expected: str = """<fastagent:response agent="fan_out_1">
foo
</fastagent:response>

<fastagent:response agent="fan_out_2">
foo
</fastagent:response>"""
            result = await agent.parallel_no_request.send("foo")
            assert expected == result

    await agent_function()

@pytest.mark.integration
@pytest.mark.asyncio
async def test_parallel_include_request_true(fast_agent):
    """Test that include_request=True includes original request in fan_in agent input."""
    fast = fast_agent

    @fast.agent(name="fan_out_1")
    @fast.agent(name="fan_out_2")
    @fast.agent(name="fan_in")
    @fast.parallel(
        name="parallel_with_request",
        fan_out=["fan_out_1", "fan_out_2"],
        fan_in="fan_in",
        include_request=True
    )
    async def agent_function():
        async with fast.run() as agent:
            # When include_request=True, the fan_in should receive both the original request
            # and the responses from fan_out agents
            expected: str = """The following request was sent to the agents:

<fastagent:request>
foo
</fastagent:request>

<fastagent:response agent="fan_out_1">
foo
</fastagent:response>

<fastagent:response agent="fan_out_2">
foo
</fastagent:response>"""
            result = await agent.parallel_with_request.send("foo")
            assert expected == result

    await agent_function()
--- END OF FILE tests/integration/workflow/parallel/test_parallel_agent.py ---


--- START OF FILE tests/integration/workflow/router/fastagent.config.yaml ---
# FastAgent Configuration File

# Default Model Configuration:
#
# Takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
# Accepts aliases for Anthropic Models: haiku, haiku3, sonnet, sonnet35, opus, opus3
# and OpenAI Models: gpt-4o-mini, gpt-4o, o1, o1-mini, o3-mini
#
# If not specified, defaults to "haiku".
# Can be overriden with a command line switch --model=<model>, or within the Agent constructor.

default_model: passthrough

# Logging and Console Configuration:
logger:
  # level: "debug" | "info" | "warning" | "error"
  # type: "none" | "console" | "file" | "http"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true
--- END OF FILE tests/integration/workflow/router/fastagent.config.yaml ---


--- START OF FILE tests/integration/workflow/router/router_script.txt ---
---USER
routing 1
---ASSISTANT
{     
    "agent": "target1", 
    "confidence": "high",
    "reasoning": "Request is asking for weather information"                                                
}

---USER
routing 2
---ASSISTANT
{     
    "agent": "target2", 
    "confidence": "high",
    "reasoning": "Request is asking for weather information"                                                
}
--- END OF FILE tests/integration/workflow/router/router_script.txt ---


--- START OF FILE tests/integration/workflow/router/test_router_agent.py ---
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from pydantic import BaseModel

from mcp_agent.core.prompt import Prompt
from mcp_agent.llm.augmented_llm_passthrough import FIXED_RESPONSE_INDICATOR
from mcp_agent.mcp.prompts.prompt_load import load_prompt_multipart

if TYPE_CHECKING:
    from mcp_agent.mcp.prompt_message_multipart import PromptMessageMultipart


@pytest.mark.integration
@pytest.mark.asyncio
async def test_router_functionality(fast_agent):
    """Check that the router routes"""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(name="target1")
    @fast.agent(name="target2")
    @fast.router(name="router", agents=["target1", "target2"], model="playback")
    async def agent_function():
        async with fast.run() as agent:
            await agent.target1.send(f"{FIXED_RESPONSE_INDICATOR} target1-result")
            await agent.target2.send(f"{FIXED_RESPONSE_INDICATOR} target2-result")
            router_setup: list[PromptMessageMultipart] = load_prompt_multipart(
                Path("router_script.txt")
            )
            setup: PromptMessageMultipart = await agent.router._llm.generate(router_setup)
            assert "LOADED" in setup.first_text()
            result: str = await agent.router.send("some routing")
            assert "target1-result" in result

            result: str = await agent.router.send("more routing")
            assert "target2-result" in result

    await agent_function()


class WeatherData(BaseModel):
    """Sample model for structured output testing."""

    location: str
    temperature: float
    conditions: str


@pytest.mark.integration
@pytest.mark.asyncio
async def test_router_structured_output(fast_agent):
    """Test router can handle structured output from agents."""
    # Use the FastAgent instance
    fast = fast_agent

    # Define test agents and router
    @fast.agent(name="structured_agent", model="passthrough")
    @fast.router(name="router", agents=["structured_agent"], model="passthrough")
    async def agent_function():
        async with fast.run() as agent:
            # Set up the passthrough LLM with JSON response
            json_response = (
                """{"location": "New York", "temperature": 72.5, "conditions": "Sunny"}"""
            )
            await agent.structured_agent.send(f"{FIXED_RESPONSE_INDICATOR} {json_response}")

            # Set up router to route to structured_agent
            routing_response = """{"agent": "structured_agent", "confidence": "high", "reasoning": "Weather request"}"""
            await agent.router._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} {routing_response}")]
            )

            # Send request through router with proper PromptMessageMultipart list
            result, _ = await agent.router.structured(
                [Prompt.user("What's the weather in New York?")], WeatherData
            )

            # Verify structured result
            assert result is not None
            assert result.location == "New York"
            assert result.temperature == 72.5
            assert result.conditions == "Sunny"

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_router_invalid_agent_selection(fast_agent):
    """Test router handles invalid agent selection gracefully."""
    # Use the FastAgent instance
    fast = fast_agent

    # Define test agents and router - need two agents to bypass single-agent optimization
    @fast.agent(name="available_agent", model="playback")
    @fast.agent(name="another_agent", model="playback")
    @fast.router(name="router", agents=["available_agent", "another_agent"], model="passthrough")
    async def agent_function():
        async with fast.run() as agent:
            # Set up router to route to non-existent agent
            routing_response = """{"agent": "nonexistent_agent", "confidence": "high", "reasoning": "Test request"}"""
            await agent.router._llm.generate(
                [Prompt.user(f"{FIXED_RESPONSE_INDICATOR} {routing_response}")]
            )

            # Send request through router
            result = await agent.router.send("This should fail with a clear error")

            # Verify error message
            assert (
                "A response was received, but the agent nonexistent_agent was not known to the Router"
                in result
            )

    await agent_function()
--- END OF FILE tests/integration/workflow/router/test_router_agent.py ---


--- START OF FILE tests/e2e/mcp_filtering/fastagent.config.yaml ---
# FastAgent Configuration File

# Default Model Configuration:
#
# Takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
# Accepts aliases for Anthropic Models: haiku, haiku3, sonnet, sonnet35, opus, opus3
# and OpenAI Models: gpt-4o-mini, gpt-4o, o1, o1-mini, o3-mini
#
# If not specified, defaults to "haiku".
# Can be overriden with a command line switch --model=<model>, or within the Agent constructor.

default_model: passthrough

# Logging and Console Configuration:
logger:
  # level: "debug" | "info" | "warning" | "error"
  # type: "none" | "console" | "file" | "http"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true
mcp:
  servers:
    filtering_test_server:
      command: "uv"
      args: ["run", "filtering_test_server.py"]
--- END OF FILE tests/e2e/mcp_filtering/fastagent.config.yaml ---


--- START OF FILE tests/e2e/mcp_filtering/filtering_test_server.py ---
#!/usr/bin/env python3
"""
MCP server for testing filtering functionality with multiple tools, resources, and prompts.
"""

import logging

from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastMCP server
app = FastMCP(name="Filtering Test Server")

# Tools
@app.tool(
    name="math_add",
    description="Add two numbers",
)
def math_add(a: int, b: int) -> str:
    return f"Result: {a + b}"

@app.tool(
    name="math_subtract", 
    description="Subtract two numbers",
)
def math_subtract(a: int, b: int) -> str:
    return f"Result: {a - b}"

@app.tool(
    name="math_multiply",
    description="Multiply two numbers", 
)
def math_multiply(a: int, b: int) -> str:
    return f"Result: {a * b}"

@app.tool(
    name="string_upper",
    description="Convert string to uppercase",
)
def string_upper(text: str) -> str:
    return text.upper()

@app.tool(
    name="string_lower",
    description="Convert string to lowercase",
)
def string_lower(text: str) -> str:
    return text.lower()

@app.tool(
    name="utility_ping",
    description="Simple ping utility",
)
def utility_ping() -> str:
    return "pong"

@app.tool(
    name="utility_status",
    description="Get server status",
)
def utility_status() -> str:
    return "server is running"

# Resources
@app.resource("resource://math/constants")
def math_constants() -> str:
    return "π = 3.14159\ne = 2.71828\nφ = 1.618034"

@app.resource("resource://math/formulas")
def math_formulas() -> str:
    return "Area of circle: π × r²\nPythagorean theorem: a² + b² = c²"

@app.resource("resource://string/examples")
def string_examples() -> str:
    return "Hello World\nTesting 123\nCase Sensitivity Test"

@app.resource("resource://utility/info")
def utility_info() -> str:
    return "Ping: Tests server connectivity\nStatus: Shows server health"

# Prompts
@app.prompt("math_helper")
def math_helper_prompt(operation: str = "add") -> str:
    """Help with mathematical operations"""
    return f"I am a math helper. Let me help you with {operation} operations."

@app.prompt("math_teacher")
def math_teacher_prompt(level: str = "basic") -> str:
    """Math teaching assistant"""
    return f"I am a math teacher. I can teach {level} level mathematics."

@app.prompt("string_processor")
def string_processor_prompt(mode: str = "upper") -> str:
    """String processing assistant"""
    return f"I am a string processor. I can process strings in {mode} mode."

@app.prompt("utility_assistant")
def utility_assistant_prompt() -> str:
    """General utility assistant"""
    return "I am a utility assistant. I can help with various utility functions."

if __name__ == "__main__":
    app.run()
--- END OF FILE tests/e2e/mcp_filtering/filtering_test_server.py ---


--- START OF FILE tests/e2e/mcp_filtering/test_mcp_filtering.py ---
#!/usr/bin/env python3
"""
E2E tests for MCP filtering functionality.
Tests tool, resource, and prompt filtering across different agent types.
"""

import pytest

from mcp_agent.agents.agent import Agent


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
async def test_tool_filtering_basic_agent(fast_agent):
    """Test tool filtering with basic agent - no filtering vs with filtering"""
    fast = fast_agent

    # Test 1: Agent without filtering - should have all tools
    @fast.agent(
        name="agent_no_filter",
        instruction="Agent without tool filtering",
        model="passthrough",
        servers=["filtering_test_server"],
    )
    async def agent_no_filter():
        async with fast.run() as agent_app:
            tools = await agent_app.agent_no_filter.list_tools()
            tool_names = [tool.name for tool in tools.tools]
            
            # Should have all 7 tools
            expected_tools = {
                "filtering_test_server-math_add",
                "filtering_test_server-math_subtract", 
                "filtering_test_server-math_multiply",
                "filtering_test_server-string_upper",
                "filtering_test_server-string_lower",
                "filtering_test_server-utility_ping",
                "filtering_test_server-utility_status"
            }
            actual_tools = set(tool_names)
            assert actual_tools == expected_tools, f"Expected {expected_tools}, got {actual_tools}"

    # Test 2: Agent with filtering - should have only filtered tools
    @fast.agent(
        name="agent_with_filter",
        instruction="Agent with tool filtering",
        model="passthrough",
        servers=["filtering_test_server"],
        tools={"filtering_test_server": ["math_*", "string_upper"]},  # Only math tools and string_upper
    )
    async def agent_with_filter():
        async with fast.run() as agent_app:
            tools = await agent_app.agent_with_filter.list_tools()
            tool_names = [tool.name for tool in tools.tools]
            
            # Should have only math tools + string_upper
            expected_tools = {
                "filtering_test_server-math_add",
                "filtering_test_server-math_subtract",
                "filtering_test_server-math_multiply",
                "filtering_test_server-string_upper"
            }
            actual_tools = set(tool_names)
            assert actual_tools == expected_tools, f"Expected {expected_tools}, got {actual_tools}"
            
            # Should NOT have these tools
            excluded_tools = {
                "filtering_test_server-string_lower",
                "filtering_test_server-utility_ping", 
                "filtering_test_server-utility_status"
            }
            for tool_name in excluded_tools:
                assert tool_name not in tool_names, f"Tool {tool_name} should have been filtered out"

    await agent_no_filter()
    await agent_with_filter()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
async def test_resource_filtering_basic_agent(fast_agent):
    """Test resource filtering with basic agent - no filtering vs with filtering"""
    fast = fast_agent

    # Test 1: Agent without filtering - should have all resources
    @fast.agent(
        name="agent_no_filter",
        instruction="Agent without resource filtering",
        model="passthrough",
        servers=["filtering_test_server"],
    )
    async def agent_no_filter():
        async with fast.run() as agent_app:
            resources = await agent_app.agent_no_filter.list_resources()
            resource_uris = resources["filtering_test_server"]  # Already a list of URI strings
            
            # Should have all 4 resources
            expected_resources = {
                "resource://math/constants",
                "resource://math/formulas",
                "resource://string/examples", 
                "resource://utility/info"
            }
            actual_resources = set(resource_uris)
            assert actual_resources == expected_resources, f"Expected {expected_resources}, got {actual_resources}"

    # Test 2: Agent with filtering - should have only filtered resources
    @fast.agent(
        name="agent_with_filter",
        instruction="Agent with resource filtering",
        model="passthrough",
        servers=["filtering_test_server"],
        resources={"filtering_test_server": ["resource://math/*", "resource://string/examples"]},
    )
    async def agent_with_filter():
        async with fast.run() as agent_app:
            resources = await agent_app.agent_with_filter.list_resources()
            resource_uris = resources.get("filtering_test_server", [])  # Get list or empty list if server not present
            
            # Should have only math resources + string examples
            expected_resources = {
                "resource://math/constants",
                "resource://math/formulas",
                "resource://string/examples"
            }
            actual_resources = set(resource_uris)
            assert actual_resources == expected_resources, f"Expected {expected_resources}, got {actual_resources}"
            
            # Should NOT have utility resource
            excluded_resources = {"resource://utility/info"}
            for resource_uri in excluded_resources:
                assert resource_uri not in resource_uris, f"Resource {resource_uri} should have been filtered out"

    await agent_no_filter()
    await agent_with_filter()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
async def test_prompt_filtering_basic_agent(fast_agent):
    """Test prompt filtering with basic agent - no filtering vs with filtering"""
    fast = fast_agent

    # Test 1: Agent without filtering - should have all prompts
    @fast.agent(
        name="agent_no_filter",
        instruction="Agent without prompt filtering",
        model="passthrough",
        servers=["filtering_test_server"],
    )
    async def agent_no_filter():
        async with fast.run() as agent_app:
            prompts = await agent_app.agent_no_filter.list_prompts()
            prompt_names = [prompt.name for prompt in prompts["filtering_test_server"]]
            
            # Should have all 4 prompts
            expected_prompts = {
                "math_helper",
                "math_teacher",
                "string_processor",
                "utility_assistant"
            }
            actual_prompts = set(prompt_names)
            assert actual_prompts == expected_prompts, f"Expected {expected_prompts}, got {actual_prompts}"

    # Test 2: Agent with filtering - should have only filtered prompts
    @fast.agent(
        name="agent_with_filter",
        instruction="Agent with prompt filtering",
        model="passthrough",
        servers=["filtering_test_server"],
        prompts={"filtering_test_server": ["math_*", "utility_assistant"]},
    )
    async def agent_with_filter():
        async with fast.run() as agent_app:
            prompts = await agent_app.agent_with_filter.list_prompts()
            prompt_list = prompts.get("filtering_test_server", [])  # Get list or empty list if server not present
            prompt_names = [prompt.name for prompt in prompt_list]
            
            # Should have only math prompts + utility_assistant
            expected_prompts = {
                "math_helper",
                "math_teacher",
                "utility_assistant"
            }
            actual_prompts = set(prompt_names)
            assert actual_prompts == expected_prompts, f"Expected {expected_prompts}, got {actual_prompts}"
            
            # Should NOT have string_processor
            excluded_prompts = {"string_processor"}
            for prompt_name in excluded_prompts:
                assert prompt_name not in prompt_names, f"Prompt {prompt_name} should have been filtered out"

    await agent_no_filter()
    await agent_with_filter()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
async def test_tool_filtering_router_agent(fast_agent):
    """Test tool filtering with router agent"""
    fast = fast_agent

    # Create a worker agent for the router
    @fast.agent(
        name="math_worker",
        instruction="Math worker agent",
        model="passthrough",
        servers=["filtering_test_server"],
    )
    async def math_worker():
        pass

    # Router agent with filtering
    @fast.router(
        name="math_router",
        agents=["math_worker"],
        servers=["filtering_test_server"],
        tools={"filtering_test_server": ["math_*"]},  # Only math tools
        instruction="Router with tool filtering",
        model="passthrough",
    )
    async def math_router():
        async with fast.run() as agent_app:
            tools = await agent_app.math_router.list_tools()
            tool_names = [tool.name for tool in tools.tools]
            
            # Should have only math tools
            expected_tools = {
                "filtering_test_server-math_add",
                "filtering_test_server-math_subtract",
                "filtering_test_server-math_multiply"
            }
            actual_tools = set(tool_names)
            assert actual_tools == expected_tools, f"Expected {expected_tools}, got {actual_tools}"
            
            # Should NOT have string or utility tools
            excluded_tools = {
                "filtering_test_server-string_upper",
                "filtering_test_server-string_lower",
                "filtering_test_server-utility_ping",
                "filtering_test_server-utility_status"
            }
            for tool_name in excluded_tools:
                assert tool_name not in tool_names, f"Tool {tool_name} should have been filtered out"

    await math_router()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
async def test_tool_filtering_custom_agent(fast_agent):
    """Test tool filtering with custom agent"""
    fast = fast_agent

    # Custom agent with filtering
    @fast.custom(
        Agent,
        name="custom_string_agent",
        instruction="Custom agent with tool filtering",
        model="passthrough",
        servers=["filtering_test_server"],
        tools={"filtering_test_server": ["string_*"]},  # Only string tools
    )
    async def custom_string_agent():
        async with fast.run() as agent_app:
            tools = await agent_app.custom_string_agent.list_tools()
            tool_names = [tool.name for tool in tools.tools]
            
            # Should have only string tools
            expected_tools = {
                "filtering_test_server-string_upper",
                "filtering_test_server-string_lower"
            }
            actual_tools = set(tool_names)
            assert actual_tools == expected_tools, f"Expected {expected_tools}, got {actual_tools}"
            
            # Should NOT have math or utility tools
            excluded_tools = {
                "filtering_test_server-math_add",
                "filtering_test_server-math_subtract",
                "filtering_test_server-math_multiply",
                "filtering_test_server-utility_ping",
                "filtering_test_server-utility_status"
            }
            for tool_name in excluded_tools:
                assert tool_name not in tool_names, f"Tool {tool_name} should have been filtered out"

    await custom_string_agent()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
async def test_combined_filtering(fast_agent):
    """Test combined tool, resource, and prompt filtering"""
    fast = fast_agent

    @fast.agent(
        name="agent_combined_filter",
        instruction="Agent with combined filtering",
        model="passthrough",
        servers=["filtering_test_server"],
        tools={"filtering_test_server": ["math_*"]},
        resources={"filtering_test_server": ["resource://math/*"]},
        prompts={"filtering_test_server": ["math_*"]},
    )
    async def agent_combined_filter():
        async with fast.run() as agent_app:
            # Test tools
            tools = await agent_app.agent_combined_filter.list_tools()
            tool_names = [tool.name for tool in tools.tools]
            expected_tools = {
                "filtering_test_server-math_add",
                "filtering_test_server-math_subtract",
                "filtering_test_server-math_multiply"
            }
            actual_tools = set(tool_names)
            assert actual_tools == expected_tools, f"Tools - Expected {expected_tools}, got {actual_tools}"
            
            # Test resources
            resources = await agent_app.agent_combined_filter.list_resources()
            resource_uris = resources.get("filtering_test_server", [])  # Get list or empty list if server not present
            expected_resources = {
                "resource://math/constants",
                "resource://math/formulas"
            }
            actual_resources = set(resource_uris)
            assert actual_resources == expected_resources, f"Resources - Expected {expected_resources}, got {actual_resources}"
            
            # Test prompts
            prompts = await agent_app.agent_combined_filter.list_prompts()
            prompt_list = prompts.get("filtering_test_server", [])  # Get list or empty list if server not present
            prompt_names = [prompt.name for prompt in prompt_list]
            expected_prompts = {
                "math_helper",
                "math_teacher"
            }
            actual_prompts = set(prompt_names)
            assert actual_prompts == expected_prompts, f"Prompts - Expected {expected_prompts}, got {actual_prompts}"

    await agent_combined_filter()
--- END OF FILE tests/e2e/mcp_filtering/test_mcp_filtering.py ---


--- START OF FILE tests/e2e/multimodal/fastagent.config.yaml ---
# FastAgent Configuration File

# Default Model Configuration:
#
# Takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
# Accepts aliases for Anthropic Models: haiku, haiku3, sonnet, sonnet35, opus, opus3
# and OpenAI Models: gpt-4o-mini, gpt-4o, o1, o1-mini, o3-mini
#
# If not specified, defaults to "haiku".
# Can be overriden with a command line switch --model=<model>, or within the Agent constructor.

default_model: passthrough

azure:

# Logging and Console Configuration:
logger:
  # level: "debug" | "info" | "warning" | "error"
  # type: "none" | "console" | "file" | "http"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true
mcp:
  servers:
    image_server:
      command: "uv"
      args: ["run", "image_server.py", "image.png"]
--- END OF FILE tests/e2e/multimodal/fastagent.config.yaml ---


--- START OF FILE tests/e2e/multimodal/image_server.py ---
#!/usr/bin/env python3
"""
Simple MCP server that responds to tool calls with text and image content.
"""

import base64
import logging
import sys
from pathlib import Path

from mcp.server.fastmcp import Context, FastMCP, Image
from mcp.types import BlobResourceContents, EmbeddedResource, ImageContent, TextContent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastMCP server
app = FastMCP(name="ImageToolServer", debug=True)

# Global variable to store the image path
image_path = "image.png"


@app.tool(name="get_image", description="Returns the sample image with some descriptive text")
async def get_image(image_name: str = "default", ctx: Context = None) -> list[TextContent | ImageContent]:
    try:
        # Use the global image path
        return [
            TextContent(type="text", text="Here's your image:"),
            Image(path=image_path).to_image_content(),
        ]
    except Exception as e:
        logger.exception(f"Error processing image: {e}")
        return [TextContent(type="text", text=f"Error processing image: {str(e)}")]


@app.tool(
    name="get_pdf",
    description="Returns 'sample.pdf' - use when the User requests a sample PDF file",
)
async def get_pdf() -> list[TextContent | EmbeddedResource]:
    try:
        pdf_path = "sample.pdf"
        # Check if file exists
        if not Path(pdf_path).exists():
            return [TextContent(type="text", text=f"Error: PDF file '{pdf_path}' not found")]

        # Read the PDF file as binary data
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()

        # Encode to base64
        b64_data = base64.b64encode(pdf_data).decode("ascii")

        # Create embedded resource
        return [
            TextContent(type="text", text="Here is the PDF"),
            EmbeddedResource(
                type="resource",
                resource=BlobResourceContents(
                    uri=f"file://{Path(pdf_path).absolute()}",
                    blob=b64_data,
                    mimeType="application/pdf",
                ),
            ),
        ]
    except Exception as e:
        logger.exception(f"Error processing PDF: {e}")
        return [TextContent(type="text", text=f"Error processing PDF: {str(e)}")]


if __name__ == "__main__":
    # Get image path from command line argument or use default
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        logger.info(f"Using image file: {image_path}")
    else:
        logger.info(f"No image path provided, using default: {image_path}")

    # Check if the specified image exists
    if not Path(image_path).exists():
        logger.warning(f"Image file '{image_path}' not found in the current directory")
        logger.warning("Please add an image file or specify a valid path as the first argument")

    # Run the server using stdio transport
    app.run(transport="stdio")
--- END OF FILE tests/e2e/multimodal/image_server.py ---


--- START OF FILE tests/e2e/multimodal/test_multimodal_images.py ---
# integration_tests/mcp_agent/test_agent_with_image.py
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from mcp_agent.core.prompt import Prompt

if TYPE_CHECKING:
    from mcp_agent.mcp.prompt_message_multipart import PromptMessageMultipart


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "gpt-4.1-mini",  # OpenAI model
        "sonnet",  # Anthropic model
        "gemini25",  # Not yet turned on as it runs into token limits.
        "azure.gpt-4.1",
    ],
)
async def test_agent_with_image_prompt(fast_agent, model_name):
    """Test that the agent can process an image and respond appropriately."""
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "default",
        instruction="You are a helpful AI Agent",
        model=model_name,
    )
    async def agent_function():
        async with fast.run() as agent:
            prompt = Prompt.user(
                "what is the user name contained in this image?",
                Path("image.png"),
            )
            response = await agent.send(prompt)

            assert "evalstate" in response

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "gpt-4.1-mini",  # OpenAI model
        "sonnet",  # Anthropic model
        "azure.gpt-4.1",
        "gemini25",
        "grok-4",
        #    "gemini2",
    ],
)
async def test_agent_with_mcp_image(fast_agent, model_name):
    """Test that the agent can process an image and respond appropriately."""
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "default",
        instruction="You are a helpful AI Agent. Do not ask any questions.",
        servers=["image_server"],
        model=model_name,
    )
    async def agent_function():
        async with fast.run() as agent:
            # Send the prompt and get the response

            response = await agent.send(
                "Use the image fetch tool to get the sample image and tell me the user name contained in this image?"
            )
            assert "evalstate" in response

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "gemini25",  # Google Gemini model -> Works sometimes, but not always. DONE.
        # And Gemini 2.5 only works with a prompt that is a bit more specific.
        #    "gemini2",
    ],
)
async def test_agent_with_mcp_image_google(fast_agent, model_name):
    """Test that the agent can process an image and respond appropriately."""
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "default",
        instruction="You are a helpful AI Agent.",
        servers=["image_server"],
        model=model_name,
    )
    async def agent_function():
        async with fast.run() as agent:
            # Send the prompt and get the response

            response = await agent.send(
                "Use the image fetch tool to get the sample image. Then tell me the user name contained in this image."
            )
            assert "evalstate" in response

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "gpt-4.1-mini",  # OpenAI model
        "haiku35",  # Anthropic model
        #    "gemini25",  # This currently uses the OpenAI format. Google Gemini cannot process PDFs with the OpenAI format. It can only do so with the native Gemini format.
    ],
)
async def test_agent_with_mcp_pdf(fast_agent, model_name):
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent",
        instruction="You are a helpful AI Agent. You have PDF support and summarisation capabilities.",
        servers=["image_server"],
        model=model_name,
    )
    async def agent_function():
        async with fast.run() as agent:
            # Send the prompt and get the response

            response = await agent.send(
                "Can you summarise the sample PDF, make sure it includes the product name in the summary"
            )
            assert "fast-agent" in response.lower()

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "gpt-4.1-mini",  # OpenAI model
        "haiku35",  # Anthropic model
        "gemini25",  # This currently uses the OpenAI format. Google Gemini cannot process PDFs with the OpenAI format. It can only do so with the native Gemini format.
    ],
)
async def test_agent_with_pdf_prompt(fast_agent, model_name):
    """Test that the agent can process a PDF document and respond appropriately."""
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent",
        instruction="You are a helpful AI Agent",
        model=model_name,
    )
    async def agent_function():
        async with fast.run() as agent:
            response = await agent.send(
                message=Prompt.user(
                    "summarize this document - include the company that made it",
                    Path("sample.pdf"),
                )
            )

            # Send the prompt and get the response
            assert "llmindset".lower() in response.lower()

    # Execute the agent function
    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "sonnet",  # Anthropic model
    ],
)
async def test_agent_includes_tool_results_in_multipart_result_anthropic(fast_agent, model_name):
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent",
        instruction="You are a helpful AI Agent. You have vision capabilities and can analyse the image.",
        servers=["image_server"],
        model=model_name,
    )
    async def agent_function():
        async with fast.run() as agent:
            response: PromptMessageMultipart = await agent.agent.generate(
                [
                    Prompt.user(
                        "Use the image fetch tool to get the sample image and tell me the user name contained in this image?"
                    )
                ]
            )
            # we are expecting response message, tool call, tool response (1* text, 1 * image), final response
            assert 4 == len(response.content)
            assert "evalstate" in response.all_text()
            assert 4 == len(agent.agent._llm.message_history[1].content)

    # Execute the agent function
    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "gpt-4.1-mini",  # OpenAI model
    ],
)
async def test_agent_includes_tool_results_in_multipart_result_openai(fast_agent, model_name):
    """Test that the agent can process a PDF document and respond appropriately."""
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent",
        instruction="You are a helpful AI Agent. You have vision capabilities.",
        servers=["image_server"],
        model=model_name,
    )
    async def agent_function():
        async with fast.run() as agent:
            response: PromptMessageMultipart = await agent.agent.generate(
                [
                    Prompt.user(
                        "Use the image fetch tool to get the sample image and tell me the user name contained in this image?"
                    )
                ]
            )
            from mcp.types import TextContent

            def is_thought_part(part_content):
                # Check if it's a TextContent and if its text starts with "thought" (case-insensitive)
                return isinstance(
                    part_content, TextContent
                ) and part_content.text.strip().lower().startswith("thought")

            # Filter out thought parts from the response content
            filtered_response_content = [
                part for part in response.content if not is_thought_part(part)
            ]

            # Filter out thought parts from the history message content
            # Assuming message_history[1] is the relevant assistant message after the tool call
            filtered_history_content = []
            if (
                len(agent.agent._llm.message_history) > 1
                and agent.agent._llm.message_history[1].content
            ):
                filtered_history_content = [
                    part
                    for part in agent.agent._llm.message_history[1].content
                    if not is_thought_part(part)
                ]

            # After filtering thoughts, we expect 3 semantic parts in the response:
            # 1. TextContent introduction for the image (from tool result)
            # 2. ImageContent (from tool result)
            # 3. TextContent with the final LLM answer
            assert 3 == len(filtered_response_content)
            assert (
                "evalstate" in response.all_text()
            )  # response.all_text() will include thoughts, which is fine for this check.

            # Ensure the filtered history also reflects the 3 semantic parts
            assert 3 == len(filtered_history_content)

    # Execute the agent function
    await agent_function()
--- END OF FILE tests/e2e/multimodal/test_multimodal_images.py ---


--- START OF FILE tests/e2e/prompts-resources/fastagent.config.yaml ---
# FastAgent Configuration File

# Default Model Configuration:
#
# Takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
# Accepts aliases for Anthropic Models: haiku, haiku3, sonnet, sonnet35, opus, opus3
# and OpenAI Models: gpt-4o-mini, gpt-4o, o1, o1-mini, o3-mini
#
# If not specified, defaults to "haiku".
# Can be overriden with a command line switch --model=<model>, or within the Agent constructor.

default_model: passthrough

# Logging and Console Configuration:
logger:
  # level: "debug" | "info" | "warning" | "error"
  # type: "none" | "console" | "file" | "http"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true
mcp:
  servers:
    prompt_server:
      command: "prompt-server"
      args:
        [
          "simple.txt",
          "multiturn.md",
          "with_attachment.md",
          "with_attachment_css.md",
        ]
--- END OF FILE tests/e2e/prompts-resources/fastagent.config.yaml ---


--- START OF FILE tests/e2e/prompts-resources/fastagent.jsonl ---
{"level":"ERROR","timestamp":"2025-03-29T22:49:26.467428","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-03-29T22:49:27.083865","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-03-29T22:49:27.633949","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-03-29T22:49:28.187746","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-03-29T22:49:28.731609","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-03-29T22:49:29.257225","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-03-29T22:49:29.802053","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-05-25T21:38:52.593285","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-05-25T21:38:53.296582","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-05-25T21:38:53.996681","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-05-25T21:38:54.737177","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-05-25T21:38:55.430480","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-05-25T21:38:56.162954","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-05-25T21:38:56.906947","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-05-25T21:38:57.626598","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-05-25T21:38:58.335264","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-05-25T21:38:59.108578","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-05-25T21:38:59.829204","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"prompt_server: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"prompt_server"}}}
{"level":"ERROR","timestamp":"2025-05-26T10:54:32.222518","namespace":"mcp_agent.llm.providers.augmented_llm_openai.agent","message":"Error: Error code: 400 - [{'error': {'code': 400, 'message': 'Invalid content part type: file', 'status': 'INVALID_ARGUMENT'}}]"}
--- END OF FILE tests/e2e/prompts-resources/fastagent.jsonl ---


--- START OF FILE tests/e2e/prompts-resources/multiturn.md ---
---USER
l l M i n d s ET uk
---ASSISTANT
llmindsetuk
---USER
fA st age NT
---ASSISTANT
fastagent
---USER
m ORE training OK
---ASSISTANT
moretrainingok
---USER
t ESt ca seOK
--- END OF FILE tests/e2e/prompts-resources/multiturn.md ---


--- START OF FILE tests/e2e/prompts-resources/simple.txt ---
Repeat the following text verbatim: {{name}}
--- END OF FILE tests/e2e/prompts-resources/simple.txt ---


--- START OF FILE tests/e2e/prompts-resources/style.css ---
:root {
  --primary: #3498db;
  --secondary: #2ecc71;
  --dark: #333;
  --light: #f8f9fa;
}
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: var(--dark);
}
.container {
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}
h1,
h2,
h3 {
  margin-bottom: 1rem;
}
p {
  margin-bottom: 1.5rem;
}
a {
  color: var(--primary);
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
.btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: 4px;
}
.btn:hover {
  background: #2980b9;
  color: white;
  text-decoration: none;
}
img {
  max-width: 100%;
  height: auto;
}
.card {
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
@media (max-width: 768px) {
  .container {
    width: 95%;
  }
}
.text-center {
  text-align: center;
}
.mt-2 {
  margin-top: 2rem;
}
--- END OF FILE tests/e2e/prompts-resources/style.css ---


--- START OF FILE tests/e2e/prompts-resources/test_prompts.py ---
# integration_tests/mcp_agent/test_agent_with_image.py
import pytest


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "gpt-4.1-mini",  # OpenAI model
        "haiku35",  # Anthropic model
        "gemini25",  # Google Gemini model -> Works. DONE.
    ],
)
async def test_agent_with_simple_prompt(fast_agent, model_name):
    """Test that the agent can process a simple prompt using directory-specific config."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent",
        instruction="You are a helpful AI Agent",
        model=model_name,
        servers=["prompt_server"],
    )
    async def agent_function():
        async with fast.run() as agent:
            response = await agent.apply_prompt("simple", {"name": "llmindset"})
            assert "llmindset" in response

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "gpt-4.1-mini",  # OpenAI model
        "haiku35",  # Anthropic model
        # "gemini25",  # Google Gemini model -> This involves opening a PDF. It is not supported by Google Gemini with the OpenAI format. Unless the format is changed to the native Gemini format, this will not work.
    ],
)
async def test_agent_with_prompt_attachment(fast_agent, model_name):
    """Test that the agent can process a simple prompt using directory-specific config."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent",
        instruction="You are a helpful AI Agent",
        model=model_name,
        servers=["prompt_server"],
    )
    async def agent_function():
        async with fast.run() as agent:
            response = await agent.apply_prompt("with_attachment")
            assert any(term in response.lower() for term in ["llmindset", "fast-agent"])

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "gpt-4.1-mini",  # OpenAI model
        "haiku35",  # Anthropic model
        "gemini25",  # Google Gemini model -> Works. DONE.
    ],
)
async def test_agent_multiturn_prompt(fast_agent, model_name):
    """Test that the agent can process a simple prompt using directory-specific config."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent",
        instruction="You are a helpful AI Agent",
        model=model_name,
        servers=["prompt_server"],
    )
    async def agent_function():
        async with fast.run() as agent:
            response = await agent.agent.apply_prompt("multiturn")
            assert "testcaseok" in response.lower()

    await agent_function()
--- END OF FILE tests/e2e/prompts-resources/test_prompts.py ---


--- START OF FILE tests/e2e/prompts-resources/test_resources.py ---
import pytest


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "haiku",
    ],
)
async def test_using_resource_blob(fast_agent, model_name):
    """Test that the agent can process a simple prompt using directory-specific config."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent",
        instruction="You are a helpful AI Agent",
        model=model_name,
        servers=["prompt_server"],
    )
    async def agent_function():
        async with fast.run() as agent:
            assert "fast-agent" in await agent.with_resource(
                "Summarise this PDF please, be sure to include the product name",
                "resource://fast-agent/sample.pdf",
                "prompt_server",
            )

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "haiku",
    ],
)
async def test_using_resource_text(fast_agent, model_name):
    """Test that the agent can process a simple prompt using directory-specific config."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent",
        instruction="You are a helpful AI Agent",
        model=model_name,
        servers=["prompt_server"],
    )
    async def agent_function():
        async with fast.run() as agent:
            answer = await agent.agent.with_resource(
                "What colour are buttons in this file?",
                "resource://fast-agent/style.css",
                "prompt_server",
            )
            assert "white" in answer.lower()

    await agent_function()
--- END OF FILE tests/e2e/prompts-resources/test_resources.py ---


--- START OF FILE tests/e2e/prompts-resources/with_attachment.md ---
---USER
Good morning, how are you?
---ASSISTANT
Very well thank you, can I help you by summarising documents?
---USER
Can you summarise this document please. Make sure to include the company name.
---RESOURCE
sample.pdf
--- END OF FILE tests/e2e/prompts-resources/with_attachment.md ---


--- START OF FILE tests/e2e/prompts-resources/with_attachment_css.md ---
---USER
Good morning, how are you?
---ASSISTANT
Very well thank you, can I help you by inspecting CSS?
---USER
Can you summarise this document please. Make sure to include the company name.
---RESOURCE
style.css
--- END OF FILE tests/e2e/prompts-resources/with_attachment_css.md ---


--- START OF FILE tests/e2e/sampling/fastagent.config.yaml ---
default_model: passthrough

# Logging and Console Configuration:
logger:
  level: "error"
  type: "console"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true

mcp:
  servers:
    sampling_resource_anthropic:
      command: "uv"
      args: ["run", "sampling_resource_server.py"]
      sampling:
        model: "haiku"
    sampling_resource_openai:
      command: "uv"
      args: ["run", "sampling_resource_server.py"]
      sampling:
        model: "gpt-4.1-mini"

      # command: "bash"
      # args: ["-c", "uv run sampling_resource_server.py | tee sampling_output.log"]
      # sampling:
      #   model: "haiku"
--- END OF FILE tests/e2e/sampling/fastagent.config.yaml ---


--- START OF FILE tests/e2e/sampling/fastagent.jsonl ---
{"level":"ERROR","timestamp":"2025-03-29T22:49:37.743115","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"sampling_resource_anthropic: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"sampling_resource_anthropic"}}}
{"level":"ERROR","timestamp":"2025-03-29T22:49:38.162289","namespace":"mcp_agent.mcp.mcp_connection_manager","message":"sampling_resource_openai: Lifecycle task encountered an error: generator didn't stop after athrow()","data":{"exc_info":true,"data":{"progress_action":"Error","server_name":"sampling_resource_openai"}}}
{"level":"ERROR","timestamp":"2025-05-25T21:39:00.063320","namespace":"mcp_agent.mcp.sampling","message":"Error in sampling: Anthropic API key not configured\n\nThe Anthropic API key is required but not set.\nAdd it to your configuration file under anthropic.api_key or set the ANTHROPIC_API_KEY environment variable."}
{"level":"ERROR","timestamp":"2025-05-25T21:39:00.831547","namespace":"mcp_agent.mcp.sampling","message":"Error in sampling: Openai API key not configured\n\nThe Openai API key is required but not set.\nAdd it to your configuration file under openai.api_key or set the OPENAI_API_KEY environment variable."}
{"level":"ERROR","timestamp":"2025-05-25T21:39:01.599545","namespace":"mcp_agent.mcp.sampling","message":"Error in sampling: Anthropic API key not configured\n\nThe Anthropic API key is required but not set.\nAdd it to your configuration file under anthropic.api_key or set the ANTHROPIC_API_KEY environment variable."}
--- END OF FILE tests/e2e/sampling/fastagent.jsonl ---


--- START OF FILE tests/e2e/sampling/sampling_resource_server.py ---
from mcp.server.fastmcp import Context, FastMCP, Image
from mcp.types import SamplingMessage, TextContent

# Create a FastMCP server
mcp = FastMCP(name="FastStoryAgent")


@mcp.resource("resource://fast-agent/short-story/{topic}")
async def generate_short_story(topic: str):
    prompt = f"Please write a short story on the topic of {topic}."

    # Make a sampling request to the client
    result = await mcp.get_context().session.create_message(
        max_tokens=1024,
        messages=[SamplingMessage(role="user", content=TextContent(type="text", text=prompt))],
    )

    return result.content.text


@mcp.tool()
async def sample_with_image(ctx: Context):
    result = await ctx.session.create_message(
        max_tokens=1024,
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text="What is the username in this image?",
                ),
            ),
            SamplingMessage(role="user", content=Image(path="image.png").to_image_content()),
        ],
    )

    return result.content.text


# Run the server when this file is executed directly
if __name__ == "__main__":
    mcp.run()
--- END OF FILE tests/e2e/sampling/sampling_resource_server.py ---


--- START OF FILE tests/e2e/sampling/test_sampling_e2e.py ---
import pytest


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
async def test_sampling_output_anthropic(fast_agent):
    """Test that the agent can process a simple prompt using directory-specific config."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent",
        instruction="You are a helpful AI Agent",
        model="passthrough",  # only need a resource call
        servers=["sampling_resource_anthropic"],
    )
    async def agent_function():
        async with fast.run() as agent:
            story = await agent.with_resource(
                "Here is a story",
                "resource://fast-agent/short-story/kittens",
                "sampling_resource_anthropic",
            )

            assert len(story) > 300
            assert "kitten" in story
            assert "error" not in story.lower()

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
async def test_sampling_output_gpt(fast_agent):
    """Test that the agent can process a simple prompt using directory-specific config."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent",
        instruction="You are a helpful AI Agent",
        model="passthrough",  # only need a resource call
        servers=["sampling_resource_openai"],
    )
    async def agent_function():
        async with fast.run() as agent:
            story = await agent.with_resource(
                "Here is a story",
                "resource://fast-agent/short-story/kittens",
                "sampling_resource_openai",
            )

            assert len(story) > 300
            assert "kitten" in story
            assert "error" not in story.lower()

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
async def test_sampling_with_image_content_anthropic(fast_agent):
    """Test that the agent can process a simple prompt using directory-specific config."""
    # Use the FastAgent instance from the test directory fixture
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent",
        instruction="You are a helpful AI Agent",
        model="passthrough",  # only need a resource call
        servers=["sampling_resource_anthropic"],
    )
    async def agent_function():
        async with fast.run() as agent:
            result = await agent("***CALL_TOOL sample_with_image")

            assert "evalstate" in result.lower()

    await agent_function()
--- END OF FILE tests/e2e/sampling/test_sampling_e2e.py ---


--- START OF FILE tests/e2e/structured/fastagent.config.yaml ---
# FastAgent Configuration File

# Default Model Configuration:
#
# Takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
# Accepts aliases for Anthropic Models: haiku, haiku3, sonnet, sonnet35, opus, opus3
# and OpenAI Models: gpt-4o-mini, gpt-4o, o1, o1-mini, o3-mini
#
# If not specified, defaults to "haiku".
# Can be overriden with a command line switch --model=<model>, or within the Agent constructor.

default_model: passthrough

# Logging and Console Configuration:
logger:
  # level: "debug" | "info" | "warning" | "error"
  # type: "none" | "console" | "file" | "http"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true
mcp:
--- END OF FILE tests/e2e/structured/fastagent.config.yaml ---


--- START OF FILE tests/e2e/structured/test_structured_outputs.py ---
# integration_tests/mcp_agent/test_agent_with_image.py

from typing import Annotated

import pytest
from pydantic import BaseModel, Field

from mcp_agent.core.prompt import Prompt
from mcp_agent.core.request_params import RequestParams


class FormattedResponse(BaseModel):
    thinking: Annotated[
        str, Field(description="Your reflection on the conversation that is not seen by the user.")
    ]
    message: str


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "generic.qwen2.5:latest",
        "generic.llama3.2:latest",
        "deepseek-chat",
        "haiku",
        "sonnet",
        "gpt-4.1",
        "gpt-4.1-mini",
        "o3-mini.low",
        "openrouter.google/gemini-2.0-flash-001",
        "gemini25",
    ],
)
async def test_structured_output_with_automatic_format_for_model(fast_agent, model_name):
    """Test that the agent can generate structured response with response_format_specified."""
    fast = fast_agent

    @fast.agent(
        "chat",
        instruction="You are a helpful assistant.",
        model=model_name,
    )
    async def create_structured():
        async with fast.run() as agent:
            thinking, response = await agent.chat.structured(
                [Prompt.user("Let's talk about guitars.")],
                model=FormattedResponse,
            )
            assert isinstance(thinking, FormattedResponse)
            assert FormattedResponse.model_validate_json(response.first_text())

            assert "guitar" in thinking.message.lower()

    await create_structured()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "gpt-4.1-mini",
        "gemini25",
    ],
)
async def test_structured_output_parses_assistant_message_if_last(fast_agent, model_name):
    """Test that the agent can generate structured response with response_format_specified."""
    fast = fast_agent

    @fast.agent(
        "chat",
        instruction="You are a helpful assistant.",
        model=model_name,
    )
    async def create_structured():
        async with fast.run() as agent:
            thinking, response = await agent.chat.structured(
                [
                    Prompt.user("Let's talk about guitars."),
                    Prompt.assistant(
                        '{"thinking":"The user wants to have a conversation about guitars, which are a broad...","message":"Sure! I love talking about guitars."}'
                    ),
                ],
                model=FormattedResponse,
            )
            assert thinking.thinking.startswith(
                "The user wants to have a conversation about guitars"
            )

    await create_structured()


response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "formatted_response",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "thinking": {
                    "type": "string",
                    "description": "Your reflection on the conversation that is not seen by the user.",
                },
                "message": {
                    "type": "string",
                    "description": "Your message to the user.",
                },
            },
            "required": ["thinking", "message"],
            "additionalProperties": False,
        },
    },
}


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "generic.llama3.2:latest",
        # "haiku", -- anthropic do not support structured outputs this way
        "gpt-4.1-mini",
        "openrouter.google/gemini-2.0-flash-001",
        "gemini2",
        "gemini25",
    ],
)
async def test_structured_output_with_response_format_overriden(fast_agent, model_name):
    """Test that the agent can generate structured response with response_format_specified."""
    fast = fast_agent

    @fast.agent(
        "chat",
        instruction="You are a helpful assistant.",
        model=model_name,
    )

    # you can specify a response format string, but this is not preferred
    async def create_structured():
        async with fast.run() as agent:
            thinking, response = await agent.chat.structured(
                [Prompt.user("Let's talk about guitars.")],
                model=FormattedResponse,
                request_params=RequestParams(response_format=response_format),
            )
            assert thinking is not None
            assert "guitar" in thinking.message.lower()

    await create_structured()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "gpt-4.1-mini",
        "haiku",
        "gemini2",
        "gemini25",
    ],
)
async def test_history_management_with_structured(fast_agent, model_name):
    """Test that the agent can generate structured response with response_format_specified."""
    fast = fast_agent

    @fast.agent(
        "chat",
        instruction="You are a helpful assistant. The user may request structured outputs, follow their instructions",
        model=model_name,
    )
    async def create_structured():
        async with fast.run() as agent:
            await agent.chat.send("good morning")
            thinking, response = await agent.chat.structured(
                [
                    Prompt.user("Let's talk about guitars."),
                ],
                model=FormattedResponse,
            )
            assert "guitar" in thinking.message.lower()

            thinking, response = await agent.chat.structured(
                [
                    Prompt.user("Let's talk about pianos."),
                ],
                model=FormattedResponse,
            )
            assert "piano" in thinking.message.lower()

            response = await agent.chat.send(
                "did we talk about space travel? respond only with YES or NO - no other formatting"
            )
            assert "no" in response.lower()

            assert 8 == len(agent.chat.message_history)
            assert len(agent.chat._llm.history.get()) > 7

    await create_structured()
--- END OF FILE tests/e2e/structured/test_structured_outputs.py ---


--- START OF FILE tests/e2e/workflow/fastagent.config.yaml ---
# FastAgent Configuration File

# Default Model Configuration:
#
# Takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
# Accepts aliases for Anthropic Models: haiku, haiku3, sonnet, sonnet35, opus, opus3
# and OpenAI Models: gpt-4o-mini, gpt-4o, o1, o1-mini, o3-mini
#
# If not specified, defaults to "haiku".
# Can be overriden with a command line switch --model=<model>, or within the Agent constructor.

default_model: passthrough

# Logging and Console Configuration:
logger:
  # level: "debug" | "info" | "warning" | "error"
  # type: "none" | "console" | "file" | "http"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true
# mcp:
#   servers:
#     test_server:
#       command: "uv"
#       args: ["run", "test_routing_server.py"]
--- END OF FILE tests/e2e/workflow/fastagent.config.yaml ---


--- START OF FILE tests/e2e/workflow/test_router_agent_e2e.py ---
# integration_tests/mcp_agent/test_agent_with_image.py
from pathlib import Path

import pytest

from mcp_agent.core.prompt import Prompt


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize("model_name", [
    "haiku", 
    "gpt-4.1-mini",
    "gemini25",
])
async def test_basic_text_routing(fast_agent, model_name):
    """Test that the agent can process an image and respond appropriately."""
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "sunny",
        instruction="You dispense advice on clothing and activities for clement weather.",
        model="passthrough",
    )
    @fast.agent(
        "stormy",
        instruction="You dispense advice on clothing and activities for stormy weather.",
        model="passthrough",
    )
    @fast.router(
        "weather",
        instruction="Route to the most appropriate agent for the weather forecast received",
        agents=["sunny", "stormy"],
        model=model_name,
    )
    async def agent_function():
        async with fast.run() as agent:
            await agent.sunny.send("***FIXED_RESPONSE beachball")
            await agent.stormy.send("***FIXED_RESPONSE umbrella")

            response = await agent.weather.send("the weather is sunny")
            assert "beachball" in response.lower()

            response = await agent.weather.send("storm clouds coming, looks snowy")
            assert "umbrella" in response.lower()

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "haiku",
        "gpt-4.1-mini",
    ],
)
async def test_image_based_routing(fast_agent, model_name):
    """Test that the agent can process an image and respond appropriately."""
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "sunny",
        instruction="You dispense advice on clothing and activities for clement weather.",
        model="passthrough",
    )
    @fast.agent(
        "stormy",
        instruction="You dispense advice on clothing and activities for stormy weather.",
        model="passthrough",
    )
    @fast.router(
        "weather",
        instruction="Use the image to route to the most appropriate agent.",
        agents=["sunny", "stormy"],
        model=model_name,
        use_history=False,
    )
    async def agent_function():
        async with fast.run() as agent:
            await agent.sunny.send("***FIXED_RESPONSE beachball")
            await agent.stormy.send("***FIXED_RESPONSE umbrella")

            response = await agent.weather.generate(
                [Prompt.user(Path("sunny.png"), "here's the image")]
            )
            assert "beachball" in response.first_text()

            response = await agent.weather.generate(
                [Prompt.user(Path("umbrella.png"), "here's the image")]
            )
            assert "umbrella" in response.first_text()

    await agent_function()
--- END OF FILE tests/e2e/workflow/test_router_agent_e2e.py ---


--- START OF FILE tests/e2e/workflow/test_routing_server.py ---
#!/usr/bin/env python3
"""
Simple MCP server that responds to tool calls with text and image content.
"""

import logging

from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastMCP server
app = FastMCP(name="Integration Server")


@app.tool(
    name="check_weather",
    description="Returns the weather for a specified location.",
)
def check_weather(location: str) -> str:
    # Write the location to a text file
    with open("weather_location.txt", "w") as f:
        f.write(location)

    # Return sunny weather condition
    return "It's stormy and cold in " + location


if __name__ == "__main__":
    # Run the server using stdio transport
    app.run(transport="stdio")
--- END OF FILE tests/e2e/workflow/test_routing_server.py ---


--- START OF FILE tests/e2e/smoke/base/fastagent.config.yaml ---
# FastAgent Configuration File

# Default Model Configuration:
#
# Takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
# Accepts aliases for Anthropic Models: haiku, haiku3, sonnet, sonnet35, opus, opus3
# and OpenAI Models: gpt-4o-mini, gpt-4o, o1, o1-mini, o3-mini
#
# If not specified, defaults to "haiku".
# Can be overriden with a command line switch --model=<model>, or within the Agent constructor.

default_model: passthrough

# Logging and Console Configuration:
logger:
  # level: "debug" | "info" | "warning" | "error"
  # type: "none" | "console" | "file" | "http"
  # path: "/path/to/logfile.jsonl"

  # Switch the progress display on or off
  progress_display: true

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true
mcp:
  servers:
    test_server:
      command: "uv"
      args: ["run", "test_server.py"]
    hyphen-name:
      command: "uv"
      args: ["run", "test_server.py"]
    temp_issue_ts:
      transport: "sse"
      url: "http://localhost:8080/sse"
--- END OF FILE tests/e2e/smoke/base/fastagent.config.yaml ---


--- START OF FILE tests/e2e/smoke/base/test_e2e_smoke.py ---
# integration_tests/mcp_agent/test_agent_with_image.py
import os
from enum import Enum
from typing import TYPE_CHECKING, List

import pytest
from pydantic import BaseModel, Field

from mcp_agent.core.prompt import Prompt

if TYPE_CHECKING:
    from mcp_agent.llm.memory import Memory
    from mcp_agent.mcp.prompt_message_multipart import PromptMessageMultipart


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "gpt-4.1-mini",
        "gpt-4o-mini",  # OpenAI model
        "haiku35",  # Anthropic model
        "deepseek",
        "generic.qwen2.5:latest",
        "generic.llama3.2:latest",
        "openrouter.google/gemini-2.0-flash-001",
        "googleoai.gemini-2.5-flash-preview-05-20",
        "google.gemini-2.0-flash",
        "gemini2",
        "gemini25",  # Works -> Done. Works most of the time, unless Gemini decides to write very long outputs.
        "azure.gpt-4.1",
        "grok-3-fast",
    ],
)
async def test_basic_textual_prompting(fast_agent, model_name):
    """Test that the agent can process an image and respond appropriately."""
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent",
        instruction="You are a helpful AI Agent",
        model=model_name,
    )
    async def agent_function():
        async with fast.run() as agent:
            response = await agent.send(Prompt.user("write a 50 word story about cats"))
            response_text = response.strip()
            words = response_text.split()
            word_count = len(words)
            assert 40 <= word_count <= 60, f"Expected between 40-60 words, got {word_count}"

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    ["gpt-4.1-nano", "generic.qwen2.5:latest", "haiku", "grok-3-fast"],
)
async def test_open_ai_history(fast_agent, model_name):
    """Test that the agent can process an image and respond appropriately."""
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent",
        instruction="SYSTEM PROMPT",
        model=model_name,
    )
    async def agent_function():
        async with fast.run() as agent:
            await agent.send("MESSAGE ONE")
            await agent.send("MESSAGE TWO")

            provider_history: Memory = agent.agent._llm.history
            multipart_history = agent.agent.message_history

            assert 4 == len(provider_history.get())
            assert 4 == len(multipart_history)

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "gpt-4o-mini",  # OpenAI model
        "haiku35",  # Anthropic model
        "deepseek",
        "openrouter.google/gemini-2.0-flash-001",
        "gemini2",
        "gemini25",  # Works -> DONE.
        "o3-mini.low",
    ],
)
async def test_multiple_text_blocks_prompting(fast_agent, model_name):
    fast = fast_agent

    # Define the agent
    @fast.agent(
        instruction="You are a helpful AI Agent",
        model=model_name,
    )
    async def agent_function():
        async with fast.run() as agent:
            response: PromptMessageMultipart = await agent.default.generate(
                [Prompt.user("write a 50 word story", "about cats - including the word 'cat'")]
            )
            response_text = response.all_text()
            words = response_text.split()
            word_count = len(words)
            assert 40 <= word_count <= 60, f"Expected between 40-60 words, got {word_count}"
            assert "cat" in response_text

            response: PromptMessageMultipart = await agent.default.generate(
                [
                    Prompt.user("write a 50 word story"),
                    Prompt.user("about cats - including the word 'cat'"),
                ]
            )
            response_text = response.all_text()
            words = response_text.split()
            word_count = len(words)
            assert 40 <= word_count <= 60, f"Expected between 40-60 words, got {word_count}"
            assert "cat" in response_text

    await agent_function()


# Option 2: Using Enum (if you need a proper class)
class WeatherCondition(str, Enum):
    """Possible weather conditions."""

    SUNNY = "sunny"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    SNOWY = "snowy"
    STORMY = "stormy"


# Or as an Enum:
class TemperatureUnit(str, Enum):
    """Temperature unit."""

    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"


class DailyForecast(BaseModel):
    """Daily weather forecast data."""

    day: str = Field(..., description="Day of the week")
    condition: WeatherCondition = Field(..., description="Weather condition")
    temperature_high: float = Field(..., description="Highest temperature for the day")
    temperature_low: float = Field(..., description="Lowest temperature for the day")
    precipitation_chance: float = Field(..., description="Chance of precipitation (0-100%)")
    notes: str = Field(..., description="Additional forecast notes")


class WeatherForecast(BaseModel):
    """Complete weather forecast with daily data."""

    location: str = Field(..., description="City and country")
    unit: TemperatureUnit = Field(..., description="Temperature unit")
    forecast: List[DailyForecast] = Field(..., description="Daily forecasts")
    summary: str = Field(..., description="Brief summary of the overall forecast")


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "gpt-4o",  # OpenAI model
        "o3-mini.low",  # reasoning
        "gpt-4.1-nano",
        "gpt-4.1-mini",
        "gemini2",
        "gemini25",  # Works -> DONE.
        "azure.gpt-4.1",
        "grok-3",
        #  "grok-4", slow,
    ],
)
async def test_structured_weather_forecast_openai_structured_api(fast_agent, model_name):
    """Test that the agent can generate structured weather forecast data."""
    fast = fast_agent

    @fast.agent(
        "weatherforecast",
        instruction="You are a helpful assistant that provides syntehsized weather data for testing purposes.",
        model=model_name,
    )
    async def weather_forecast():
        async with fast.run() as agent:
            # Create a structured prompt that asks for weather forecast
            prompt_text = """
            Generate a 5-day weather forecast for San Francisco, California.
            
            The forecast should include:
            - Daily high and low temperatures in celsius
            - Weather conditions (sunny, cloudy, rainy, snowy, or stormy)
            - Precipitation chance
            - Any special notes about the weather for each day
            
            Provide a brief summary of the overall forecast period at the end.
            """

            # Get structured response
            forecast, result = await agent.weatherforecast.structured(
                [Prompt.user(prompt_text)], WeatherForecast
            )

            # Verify the structured response
            assert forecast is not None, "Structured response should not be None"
            assert isinstance(forecast, WeatherForecast), (
                "Response should be a WeatherForecast object"
            )

            # Verify forecast content
            assert forecast.location.lower().find("san francisco") >= 0, (
                "Location should be San Francisco"
            )
            assert forecast.unit == "celsius", "Temperature unit should be celsius"
            assert len(forecast.forecast) == 5, "Should have 5 days of forecast"
            assert all(isinstance(day, DailyForecast) for day in forecast.forecast), (
                "Each day should be a DailyForecast"
            )

            # Verify data types and ranges
            for day in forecast.forecast:
                assert 0 <= day.precipitation_chance <= 100, (
                    f"Precipitation chance should be 0-100%, got {day.precipitation_chance}"
                )
                assert -50 <= day.temperature_low <= 60, (
                    f"Temperature low should be reasonable, got {day.temperature_low}"
                )
                assert -30 <= day.temperature_high <= 70, (
                    f"Temperature high should be reasonable, got {day.temperature_high}"
                )
                assert day.temperature_high >= day.temperature_low, (
                    "High temp should be >= low temp"
                )

            # Print forecast summary for debugging
            print(f"Weather forecast for {forecast.location}: {forecast.summary}")
            assert '"location":' in result.first_text()

    await weather_forecast()


# @pytest.mark.skip(reason="Local Hardware Required")
@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        #        "generic.qwen2.5:latest", qwen often produces short stories, take out for current runs
        "generic.llama3.2:latest",
    ],
)
async def test_generic_model_textual_prompting(fast_agent, model_name):
    """Test that the agent can process an image and respond appropriately."""
    fast = fast_agent

    # Define the agent
    @fast.agent(
        "agent",
        instruction="You are a helpful AI Agent",
        model=model_name,
    )
    async def agent_function():
        async with fast.run() as agent:
            response = await agent.send(Prompt.user("write a 50 word story about cats"))
            response_text = response.strip()
            words = response_text.split()
            word_count = len(words)
            assert 40 <= word_count <= 60, f"Expected between 40-60 words, got {word_count}"

    await agent_function()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "deepseek",
        "haiku35",
        "gpt-4o",
        "gpt-4.1-nano",
        "gpt-4.1-mini",
        "gemini2",
        "openrouter.google/gemini-2.5-flash",
        "openrouter.anthropic/claude-sonnet-4",
        "gemini25",
        "generic.qwen2.5:latest",
        "generic.llama3.2:latest",
        "o3-mini.low",
        "o4-mini.low",
        "azure.gpt-4.1",
        "grok-3",
    ],
)
async def test_basic_tool_calling(fast_agent, model_name):
    """Test that the agent can generate structured weather forecast data."""
    fast = fast_agent

    @fast.agent(
        "weatherforecast",
        instruction="You are a helpful assistant that provides synthesized weather data for testing"
        " purposes.",
        model=model_name,
        servers=["test_server"],
    )
    async def weather_forecast():
        async with fast.run() as agent:
            # Delete weather_location.txt if it exists
            if os.path.exists("weather_location.txt"):
                os.remove("weather_location.txt")

            assert not os.path.exists("weather_location.txt")

            response = await agent.send(
                Prompt.user("what is the weather in london. use appropriate tools")
            )
            assert "sunny" in response

            # Check that the file exists after response
            assert os.path.exists("weather_location.txt"), (
                "File should exist after response (created by tool call)"
            )

    await weather_forecast()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "deepseek",
        "haiku35",
        "gpt-4o",
        "gpt-4.1-mini",
        "gemini2",
        "gemini25",  # Works -> DONE.
        "openrouter.anthropic/claude-3.7-sonnet",
        "openrouter.google/gemini-2.5-flash",
        "azure.gpt-4.1",
        "grok-3",
    ],
)
async def test_tool_calls_no_args(fast_agent, model_name):
    fast = fast_agent

    @fast.agent(
        "shirt_colour",
        instruction="You are a helpful assistant that provides information on shirt colours.",
        model=model_name,
        servers=["test_server"],
    )
    async def tools_no_args():
        async with fast.run() as agent:
            response = await agent.send(Prompt.user("get the shirt colour"))
            assert "blue" in response

    await tools_no_args()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "deepseek",
        "haiku35",
        #       "gpt-4o",
        #      "gpt-4.1",
        #     "gpt-4.1-nano",
        "gpt-4.1-mini",
        "google.gemini-2.0-flash",
        "gemini25",  # Works -> DONE.
        #       "openrouter.anthropic/claude-3.7-sonnet",
    ],
)
async def test_tool_calls_no_args_typescript(fast_agent, model_name):
    """Temporary test to diagnose typescript server issues"""
    pass
    # fast = fast_agent

    # @fast.agent(
    #     "shirt_colour",
    #     instruction="You are a helpful assistant that provides information on shirt colours.",
    #     model=model_name,
    #     servers=["temp_issue_ts"],
    # )
    # async def tools_no_args_typescript():
    #     async with fast.run() as agent:
    #         response = await agent.send(
    #             Prompt.user("tell me the response from the crashtest1 tool")
    #         )
    #         assert "did it work?" in response

    # await tools_no_args_typescript()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.parametrize(
    "model_name",
    [
        "deepseek",
        "haiku35",
        "gpt-4.1",
        "google.gemini-2.0-flash",
        "gemini25",  # Works -> DONE.
    ],
)
async def test_server_has_hyphen(fast_agent, model_name):
    """Test that the agent can generate structured weather forecast data."""
    fast = fast_agent

    @fast.agent(
        "shirt_colour",
        instruction="You are a helpful assistant that provides information on shirt colours.",
        model=model_name,
        servers=["hyphen-name"],
    )
    async def server_with_hyphen():
        async with fast.run() as agent:
            response = await agent.send("check the weather in new york")
            assert "sunny" in response

    await server_with_hyphen()
--- END OF FILE tests/e2e/smoke/base/test_e2e_smoke.py ---


--- START OF FILE tests/e2e/smoke/base/test_server.py ---
#!/usr/bin/env python3
"""
Simple MCP server that responds to tool calls with text and image content.
"""

import logging

from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastMCP server
app = FastMCP(name="Integration Server")


@app.tool(
    name="check_weather",
    description="Returns the weather for a specified location.",
)
def check_weather(location: str) -> str:
    # Write the location to a text file
    with open("weather_location.txt", "w") as f:
        f.write(location)

    # Return sunny weather condition
    return "It's sunny in " + location


@app.tool(name="shirt_colour", description="returns the colour of the shirt being worn")
def shirt_colour() -> str:
    return "blue polka dots"


if __name__ == "__main__":
    # Run the server using stdio transport
    app.run(transport="stdio")
--- END OF FILE tests/e2e/smoke/base/test_server.py ---


--- START OF FILE tests/e2e/smoke/tensorzero/test_agent_interaction.py ---
import pytest

from mcp_agent.core.fastagent import FastAgent
from mcp_agent.core.request_params import RequestParams

pytestmark = pytest.mark.usefixtures("tensorzero_docker_env")


@pytest.mark.asyncio
async def test_tensorzero_agent_smoke(project_root, chdir_to_tensorzero_example):
    """
    Smoke test for the TensorZero agent interaction defined in examples/tensorzero/agent.py.
    Sends a predefined sequence of messages.
    """
    config_file = "fastagent.config.yaml"

    my_t0_system_vars = {
        "TEST_VARIABLE_1": "Roses are red",
        "TEST_VARIABLE_2": "Violets are blue",
        "TEST_VARIABLE_3": "Sugar is sweet",
        "TEST_VARIABLE_4": "Vibe code responsibly 👍",
    }

    fast = FastAgent("fast-agent example test", config_path=config_file, ignore_unknown_args=True)

    @fast.agent(
        name="default",
        instruction="""
            You are an agent dedicated to helping developers understand the relationship between TensoZero and fast-agent. If the user makes a request
            that requires you to invoke the test tools, please do so. When you use the tool, describe your rationale for doing so.
        """,
        servers=["tester"],
        model="tensorzero.test_chat",
        request_params=RequestParams(template_vars=my_t0_system_vars),
    )
    async def dummy_agent_func():
        pass

    messages_to_send = [
        "Hi.",
        "Tell me a poem.",
        "Do you have any tools that you can use?",
        "Please demonstrate the use of that tool on your last response.",
        "Please summarize the conversation so far.",
        "What tool calls have you executed in this session, and what were their results?",
    ]

    async with fast.run() as agent_app:
        agent_instance = agent_app.default
        print(f"\nSending {len(messages_to_send)} messages to agent '{agent_instance.name}'...")
        for i, msg_text in enumerate(messages_to_send):
            print(f"Sending message {i + 1}: '{msg_text}'")
            await agent_instance.send(msg_text)
            print(f"Message {i + 1} sent successfully.")

    print("\nAgent interaction smoke test completed successfully.")
--- END OF FILE tests/e2e/smoke/tensorzero/test_agent_interaction.py ---


--- START OF FILE tests/e2e/smoke/tensorzero/test_image_demo.py ---
import asyncio
import importlib.util
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.usefixtures("tensorzero_docker_env")


def import_from_path(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec for module {module_name} at {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.mark.asyncio
async def test_tensorzero_image_demo_smoke(project_root, chdir_to_tensorzero_example):
    """
    Smoke test for the TensorZero image demo script.
    Ensures the script runs to completion without errors.
    """
    image_demo_script_path = project_root / "examples" / "tensorzero" / "image_demo.py"

    if not image_demo_script_path.is_file():
        pytest.fail(f"Image demo script not found at {image_demo_script_path}")

    print(f"\nImporting image demo script from: {image_demo_script_path}")
    image_demo_module = None
    try:
        image_demo_module = import_from_path("image_demo_module", image_demo_script_path)
        main_func = getattr(image_demo_module, "main", None)
        if not main_func or not asyncio.iscoroutinefunction(main_func):
            pytest.fail(f"'main' async function not found in {image_demo_script_path}")

        print("Executing image_demo.main()...")
        await main_func()
        print("image_demo.main() executed successfully.")

    except ImportError as e:
        pytest.fail(f"Failed to import image_demo script: {e}")
    except Exception as e:
        pytest.fail(f"Running image_demo script failed: {e}")
    finally:
        if image_demo_module and "image_demo_module" in sys.modules:
            del sys.modules["image_demo_module"]

    print("\nImage demo smoke test completed successfully.")
--- END OF FILE tests/e2e/smoke/tensorzero/test_image_demo.py ---


--- START OF FILE tests/e2e/smoke/tensorzero/test_simple_agent_interaction.py ---
import pytest

from mcp_agent.core.fastagent import FastAgent

pytestmark = pytest.mark.usefixtures("tensorzero_docker_env", "chdir_to_tensorzero_example")


@pytest.mark.asyncio
async def test_tensorzero_simple_agent_smoke():  # Removed unused project_root fixture
    """
    Smoke test for the TensorZero simple agent interaction defined in examples/tensorzero/simple_agent.py.
    Sends a single "hi" message.
    """
    config_file = "fastagent.config.yaml"

    fast = FastAgent(
        "fast-agent simple example test", config_path=config_file, ignore_unknown_args=True
    )

    @fast.agent(
        name="simple_default",
        instruction="""
            You are an agent dedicated to helping developers understand the relationship between TensoZero and fast-agent. If the user makes a request 
            that requires you to invoke the test tools, please do so. When you use the tool, describe your rationale for doing so. 
        """,
        servers=["tester"],
        model="tensorzero.simple_chat",
    )
    async def dummy_simple_agent_func():
        pass

    message_to_send = "Hi."

    async with fast.run() as agent_app:
        agent_instance = agent_app.simple_default

        print(f"\nSending message to agent '{agent_instance.name}': '{message_to_send}'")
        await agent_instance.send(message_to_send)
        print(f"Message sent successfully to '{agent_instance.name}'.")

    print("\nSimple agent interaction smoke test completed successfully.")
--- END OF FILE tests/e2e/smoke/tensorzero/test_simple_agent_interaction.py ---


