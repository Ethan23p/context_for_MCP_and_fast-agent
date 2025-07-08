# Project: examples

## Directory Structure

```
📁 examples
├── 📁 azure-openai
│   └── 📄 fastagent.config.yaml
├── 📁 custom-agents
│   ├── 📄 agent.py
│   └── 📄 fastagent.config.yaml
├── 📁 data-analysis
│   ├── 📁 mount-point
│   │   └── 📄 WA_Fn-UseC_-HR-Employee-Attrition.csv
│   ├── 📄 analysis-campaign.py
│   ├── 📄 analysis.py
│   └── 📄 fastagent.config.yaml
├── 📁 mcp
│   ├── 📁 elicitations
│   │   ├── 📄 elicitation_account_server.py
│   │   ├── 📄 elicitation_forms_server.py
│   │   ├── 📄 elicitation_game_server.py
│   │   ├── 📄 fastagent.config.yaml
│   │   ├── 📄 fastagent.secrets.yaml.example
│   │   ├── 📄 forms_demo.py
│   │   ├── 📄 game_character.py
│   │   ├── 📄 game_character_handler.py
│   │   └── 📄 tool_call.py
│   ├── 📁 state-transfer
│   │   ├── 📄 agent_one.py
│   │   ├── 📄 agent_two.py
│   │   ├── 📄 fastagent.config.yaml
│   │   └── 📄 fastagent.secrets.yaml.example
│   └── 📁 vision-examples
│       ├── 📄 example1.py
│       ├── 📄 example2.py
│       ├── 📄 example3.py
│       └── 📄 fastagent.config.yaml
├── 📁 otel
│   ├── 📄 agent.py
│   ├── 📄 agent2.py
│   ├── 📄 docker-compose.yaml
│   └── 📄 fastagent.config.yaml
├── 📁 researcher
│   ├── 📄 fastagent.config.yaml
│   ├── 📄 researcher-eval.py
│   ├── 📄 researcher-imp.py
│   └── 📄 researcher.py
├── 📁 tensorzero
│   ├── 📁 demo_images
│   ├── 📁 mcp_server
│   │   ├── 📄 Dockerfile
│   │   ├── 📄 entrypoint.sh
│   │   └── 📄 mcp_server.py
│   ├── 📁 tensorzero_config
│   │   ├── 📄 system_schema.json
│   │   ├── 📄 system_template.minijinja
│   │   └── 📄 tensorzero.toml
│   ├── 📄 .env.sample
│   ├── 📄 agent.py
│   ├── 📄 docker-compose.yml
│   ├── 📄 fastagent.config.yaml
│   ├── 📄 image_demo.py
│   ├── 📄 Makefile
│   ├── 📄 README.md
│   └── 📄 simple_agent.py
└── 📁 workflows
    ├── 📄 chaining.py
    ├── 📄 evaluator.py
    ├── 📄 fastagent.config.yaml
    ├── 📄 graded_report.md
    ├── 📄 human_input.py
    ├── 📄 orchestrator.py
    ├── 📄 parallel.py
    ├── 📄 router.py
    ├── 📄 short_story.md
    └── 📄 short_story.txt
```

------------------------------------------------------------

## File Contents

--- START OF FILE azure-openai/fastagent.config.yaml ---
# NOTE: Since version X.X, the Azure OpenAI integration in FastAgent reuses the OpenAI logic.
# Authentication (API Key or DefaultAzureCredential) and connectivity are managed automatically.
# You only need to configure the 'azure' section as indicated below; the system will select the appropriate method.
#
# Example configuration for Azure OpenAI in fast-agent
#
# There are three supported authentication/configuration modes for Azure OpenAI:
#
# 1. Using 'resource_name' and 'api_key' (recommended for most users)
# 2. Using 'base_url' and 'api_key' (for custom endpoints or sovereign clouds)
# 3. Using 'base_url' and DefaultAzureCredential (for managed identity, Azure CLI, etc.)
#
# Use ONLY one of the parameters: 'resource_name' or 'base_url'.
# - If you define 'base_url', it will be used directly as the endpoint and 'resource_name' will be ignored.
# - If you define 'resource_name' (and not 'base_url'), the endpoint will be constructed automatically.
# - If both are missing, the configuration is invalid.
#
# Do not include both at the same time.

# --- OPTION 1: Using resource_name and api_key (recommended for standard Azure) ---
default_model: "azure.my-deployment"

azure:
  api_key: "YOUR_AZURE_OPENAI_API_KEY"
  resource_name: "your-resource-name"
  azure_deployment: "my-deployment"
  api_version: "2023-05-15"
  # Do not include base_url if you use resource_name

# --- OPTION 2: Using base_url and api_key (for custom endpoints or sovereign clouds) ---
# default_model: "azure.my-deployment"
#
# azure:
#   api_key: "YOUR_AZURE_OPENAI_API_KEY"
#   base_url: "https://your-resource-name.openai.azure.com/"
#   azure_deployment: "my-deployment"
#   api_version: "2023-05-15"
#   # Do not include resource_name if you use base_url

# --- OPTION 3: Using base_url and DefaultAzureCredential (for managed identity, Azure CLI, etc.) ---
# Requires the 'azure-identity' package to be installed.
# No api_key or resource_name should be present in this mode.
# base_url is required and must be the full endpoint URL.
#
# default_model: "azure.my-deployment"
#
# azure:
#   use_default_azure_credential: true
#   base_url: "https://your-resource-name.openai.azure.com/"
#   azure_deployment: "my-deployment"
#   api_version: "2023-05-15"
#   # Do not include api_key or resource_name in this mode

# You can add other providers or settings as needed.

--- END OF FILE azure-openai/fastagent.config.yaml ---


--- START OF FILE custom-agents/agent.py ---
import asyncio

from mcp_agent.agents.base_agent import BaseAgent
from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("fast-agent example")


class MyAgent(BaseAgent):
    async def initialize(self):
        await super().initialize()
        print("it's a-me!...Mario!")


# Define the agent
@fast.custom(MyAgent, instruction="You are a helpful AI Agent")
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE custom-agents/agent.py ---


--- START OF FILE custom-agents/fastagent.config.yaml ---
# Please edit this configuration file to match your environment (on Windows).
# Examples in comments below - check/change the paths.
#
#

execution_engine: asyncio
logger:
  type: file
  level: error
  truncate_tools: true

mcp:
  servers:
    filesystem:
      # On windows update the command and arguments to use `node` and the absolute path to the server.
      # Use `npm i -g @modelcontextprotocol/server-filesystem` to install the server globally.
      # Use `npm -g root` to find the global node_modules path.`
      # command: "node"
      # args: ["c:/Program Files/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js","."]
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "."]
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]

--- END OF FILE custom-agents/fastagent.config.yaml ---


--- START OF FILE data-analysis/mount-point/WA_Fn-UseC_-HR-Employee-Attrition.csv ---

[Contents of a 1470-row CSV file about employee attrition are included here for the data-analysis example.]

--- END OF FILE data-analysis/mount-point/WA_Fn-UseC_-HR-Employee-Attrition.csv ---


--- START OF FILE data-analysis/analysis-campaign.py ---
import asyncio

from mcp_agent.core.fastagent import FastAgent
from mcp_agent.llm.augmented_llm import RequestParams

# Create the application
fast = FastAgent("Data Analysis & Campaign Generator")


# Original data analysis components
@fast.agent(
    name="data_analysis",
    instruction="""
You have access to a Python 3.12 interpreter and you can use this to analyse and process data. 
Common analysis packages such as Pandas, Seaborn and Matplotlib are already installed. 
You can add further packages if needed.
Data files are accessible from the /mnt/data/ directory (this is the current working directory).
Visualisations should be saved as .png files in the current working directory.
Extract key insights that would be compelling for a social media campaign.
""",
    servers=["interpreter"],
    request_params=RequestParams(maxTokens=8192),
    model="sonnet",
)
@fast.agent(
    "evaluator",
    """You are collaborating with a Data Analysis tool that has the capability to analyse data and produce visualisations.
    You must make sure that the tool has:
     - Considered the best way for a Human to interpret the data
     - Produced insightful visualisations.
     - Provided a high level summary report for the Human.
     - Has had its findings challenged, and justified
     - Extracted compelling insights suitable for social media promotion
    """,
    request_params=RequestParams(maxTokens=8192),
    model="gpt-4.1",
)
@fast.evaluator_optimizer(
    "analysis_tool",
    generator="data_analysis",
    evaluator="evaluator",
    max_refinements=3,
    min_rating="EXCELLENT",
)
# Research component using Brave search
@fast.agent(
    "context_researcher",
    """You are a research specialist who provides cultural context for different regions.
    For any given data insight and target language/region, research:
    1. Cultural sensitivities related to presenting this type of data
    2. Local social media trends and preferences
    3. Region-specific considerations for marketing campaigns
    
    Always provide actionable recommendations for adapting content to each culture.
    """,
    servers=["fetch", "brave"],  # Using the fetch MCP server for Brave search
    request_params=RequestParams(temperature=0.3),
    model="gpt-4.1",
)
# Social media content generator
@fast.agent(
    "campaign_generator",
    """Generate engaging social media content based on data insights.
    Create compelling, shareable content that:
    - Highlights key research findings in an accessible way
    - Uses appropriate tone for the platform (Twitter/X, LinkedIn, Instagram, etc.)
    - Is concise and impactful
    - Includes suggested hashtags and posting schedule
    
    Format your response with clear sections for each platform.
    Save different campaign elements as separate files in the current directory.
    """,
    servers=["filesystem"],  # Using filesystem MCP server to save files
    request_params=RequestParams(temperature=0.7),
    model="sonnet",
    use_history=False,
)
# Translation agents with cultural adaptation
@fast.agent(
    "translate_fr",
    """Translate social media content to French with cultural adaptation.
    Consider French cultural norms, expressions, and social media preferences.
    Ensure the translation maintains the impact of the original while being culturally appropriate.
    Save the translated content to a file with appropriate naming.
    """,
    model="haiku",
    use_history=False,
    servers=["filesystem"],
)
@fast.agent(
    "translate_es",
    """Translate social media content to Spanish with cultural adaptation.
    Consider Spanish-speaking cultural contexts, expressions, and social media preferences.
    Ensure the translation maintains the impact of the original while being culturally appropriate.
    Save the translated content to a file with appropriate naming.
    """,
    model="haiku",
    use_history=False,
    servers=["filesystem"],
)
@fast.agent(
    "translate_de",
    """Translate social media content to German with cultural adaptation.
    Consider German cultural norms, expressions, and social media preferences.
    Ensure the translation maintains the impact of the original while being culturally appropriate.
    Save the translated content to a file with appropriate naming.
    """,
    model="haiku",
    use_history=False,
    servers=["filesystem"],
)
@fast.agent(
    "translate_ja",
    """Translate social media content to Japanese with cultural adaptation.
    Consider Japanese cultural norms, expressions, and social media preferences.
    Ensure the translation maintains the impact of the original while being culturally appropriate.
    Save the translated content to a file with appropriate naming.
    """,
    model="haiku",
    use_history=False,
    servers=["filesystem"],
)
# Parallel workflow for translations
@fast.parallel(
    "translate_campaign",
    instruction="Translates content to French, Spanish, German and Japanese. Supply the content to translate, translations will be saved to the filesystem.",
    fan_out=["translate_fr", "translate_es", "translate_de", "translate_ja"],
    include_request=True,
)
# Cultural sensitivity review agent
@fast.agent(
    "cultural_reviewer",
    """Review all translated content for cultural sensitivity and appropriateness.
    For each language version, evaluate:
    - Cultural appropriateness
    - Potential misunderstandings or sensitivities
    - Effectiveness for the target culture
    
    Provide specific recommendations for any needed adjustments and save a review report.
    """,
    servers=["filesystem"],
    request_params=RequestParams(temperature=0.2),
)
# Campaign optimization workflow
@fast.evaluator_optimizer(
    "campaign_optimizer",
    generator="campaign_generator",
    evaluator="cultural_reviewer",
    max_refinements=2,
    min_rating="EXCELLENT",
)
# Main workflow orchestration
@fast.orchestrator(
    "research_campaign_creator",
    instruction="""
    Create a complete multi-lingual social media campaign based on data analysis results.
    The workflow will:
    1. Analyze the provided data and extract key insights
    2. Research cultural contexts for target languages
    3. Generate appropriate social media content
    4. Translate and culturally adapt the content
    5. Review and optimize all materials
    6. Save all campaign elements to files
    """,
    agents=[
        "analysis_tool",
        "context_researcher",
        "campaign_optimizer",
        "translate_campaign",
    ],
    model="sonnet",  # Using a more capable model for orchestration
    request_params=RequestParams(maxTokens=8192),
    plan_type="full",
)
async def main() -> None:
    # Use the app's context manager
    print(
        "WARNING: This workflow will likely run for >10 minutes and consume a lot of tokens. Press Enter to accept the default prompt and proceed"
    )

    async with fast.run() as agent:
        await agent.research_campaign_creator.prompt(
            default_prompt="Analyze the CSV file in the current directory and create a comprehensive multi-lingual social media campaign based on the findings. Save all campaign elements as separate files."
        )


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE data-analysis/analysis-campaign.py ---


--- START OF FILE data-analysis/analysis.py ---
import asyncio

from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("Data Analysis (Roots)")


# The sample data is under Database Contents License (DbCL) v1.0.
# Available here : https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset


@fast.agent(
    name="data_analysis",
    instruction="""
You have access to a Python 3.12 interpreter and you can use this to analyse and process data. 
Common analysis packages such as Pandas, Seaborn and Matplotlib are already installed. 
You can add further packages if needed.
Data files are accessible from the /mnt/data/ directory (this is the current working directory).
Visualisations should be saved as .png files in the current working directory.
""",
    servers=["interpreter"],
)
@fast.agent(name="another_test", instruction="", servers=["filesystem"])
async def main() -> None:
    # Use the app's context manager
    async with fast.run() as agent:
        await agent(
            "There is a csv file in the current directory. "
            "Analyse the file, produce a detailed description of the data, and any patterns it contains.",
        )
        await agent(
            "Consider the data, and how to usefully group it for presentation to a Human. Find insights, using the Python Interpreter as needed.\n"
            "Use MatPlotLib to produce insightful visualisations. Save them as '.png' files in the current directory. Be sure to run the code and save the files.\n"
            "Produce a summary with major insights to the data",
        )
        await agent()


if __name__ == "__main__":
    asyncio.run(main())


############################################################################################################
# Example of evaluator/optimizer flow
############################################################################################################
# @fast.agent(
#     "evaluator",
#     """You are collaborating with a Data Analysis tool that has the capability to analyse data and produce visualisations.
#     You must make sure that the tool has:
#      - Considered the best way for a Human to interpret the data
#      - Produced insightful visualasions.
#      - Provided a high level summary report for the Human.
#      - Has had its findings challenged, and justified
#     """,
#     request_params=RequestParams(maxTokens=8192),
# )
# @fast.evaluator_optimizer(
#     "analysis_tool",
#     generator="data_analysis",
#     evaluator="evaluator",
#     max_refinements=3,
#     min_rating="EXCELLENT",
# )

--- END OF FILE data-analysis/analysis.py ---


--- START OF FILE data-analysis/fastagent.config.yaml ---
default_model: sonnet

# on windows, adjust the mount point to be the full path e.g. x:/temp/data-analysis/mount-point:/mnt/data/

mcp:
  servers:
    interpreter:
      command: "docker"
      args:
        [
          "run",
          "-i",
          "--rm",
          "--pull=always",
          "-v",
          "./mount-point:/mnt/data/",
          "ghcr.io/evalstate/mcp-py-repl:latest",
        ]
      roots:
        - uri: "file://./mount-point/"
          name: "test_data"
          server_uri_alias: "file:///mnt/data/"
    filesystem:
      # On windows update the command and arguments to use `node` and the absolute path to the server.
      # Use `npm i -g @modelcontextprotocol/server-filesystem` to install the server globally.
      # Use `npm -g root` to find the global node_modules path.`
      # command: "node"
      # args: ["c:/Program Files/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js","."]
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "./mount-point/"]
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]
    brave:
      # On windows replace the command and args line to use `node` and the absolute path to the server.
      # Use `npm i -g @modelcontextprotocol/server-brave-search` to install the server globally.
      # Use `npm -g root` to find the global node_modules path.`
      # command: "node"
      # args: ["c:/Program Files/nodejs/node_modules/@modelcontextprotocol/server-brave-search/dist/index.js"]
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-brave-search"]

--- END OF FILE data-analysis/fastagent.config.yaml ---


--- START OF FILE mcp/elicitations/elicitation_account_server.py ---
"""
MCP Server for Account Creation Demo

This server provides an account signup form that can be triggered
by tools, demonstrating LLM-initiated elicitations.

Note: Following MCP spec, we don't collect sensitive information like passwords.
"""

import logging
import sys

from mcp.server.elicitation import (
    AcceptedElicitation,
    CancelledElicitation,
    DeclinedElicitation,
)
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("elicitation_account_server")

# Create MCP server
mcp = FastMCP("Account Creation Server", log_level="INFO")


@mcp.tool()
async def create_user_account(service_name: str = "MyApp") -> str:
    """
    Create a new user account for the specified service.

    Args:
        service_name: The name of the service to create an account for

    Returns:
        Status message about the account creation
    """
    # This tool triggers the elicitation form
    logger.info(f"Creating account for service: {service_name}")

    class AccountSignup(BaseModel):
        username: str = Field(description="Choose a username", min_length=3, max_length=20)
        email: str = Field(description="Your email address", json_schema_extra={"format": "email"})
        full_name: str = Field(description="Your full name", max_length=30)

        language: str = Field(
            default="en",
            description="Preferred language",
            json_schema_extra={
                "enum": [
                    "en",
                    "zh",
                    "es",
                    "fr",
                    "de",
                    "ja",
                ],
                "enumNames": ["English", "中文", "Español", "Français", "Deutsch", "日本語"],
            },
        )
        agree_terms: bool = Field(description="I agree to the terms of service")
        marketing_emails: bool = Field(False, description="Send me product updates")

    result = await mcp.get_context().elicit(
        f"Create Your {service_name} Account", schema=AccountSignup
    )

    match result:
        case AcceptedElicitation(data=data):
            if not data.agree_terms:
                return "❌ Account creation failed: You must agree to the terms of service"
            else:
                return f"✅ Account created successfully for {service_name}!\nUsername: {data.username}\nEmail: {data.email}"
        case DeclinedElicitation():
            return f"❌ Account creation for {service_name} was declined by user"
        case CancelledElicitation():
            return f"❌ Account creation for {service_name} was cancelled by user"


if __name__ == "__main__":
    logger.info("Starting account creation server...")
    mcp.run()

--- END OF FILE mcp/elicitations/elicitation_account_server.py ---


--- START OF FILE mcp/elicitations/elicitation_forms_server.py ---
"""
MCP Server for Basic Elicitation Forms Demo

This server provides various elicitation resources that demonstrate
different form types and validation patterns.
"""

import logging
import sys
from typing import Optional

from mcp import ReadResourceResult
from mcp.server.elicitation import (
    AcceptedElicitation,
    CancelledElicitation,
    DeclinedElicitation,
)
from mcp.server.fastmcp import FastMCP
from mcp.types import TextResourceContents
from pydantic import AnyUrl, BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("elicitation_forms_server")

# Create MCP server
mcp = FastMCP("Elicitation Forms Demo Server", log_level="INFO")


@mcp.resource(uri="elicitation://event-registration")
async def event_registration() -> ReadResourceResult:
    """Register for a tech conference event."""

    class EventRegistration(BaseModel):
        name: str = Field(description="Your full name", min_length=2, max_length=100)
        email: str = Field(description="Your email address", json_schema_extra={"format": "email"})
        company_website: Optional[str] = Field(
            None, description="Your company website (optional)", json_schema_extra={"format": "uri"}
        )
        event_date: str = Field(
            description="Which event date works for you?", json_schema_extra={"format": "date"}
        )
        dietary_requirements: Optional[str] = Field(
            None, description="Any dietary requirements? (optional)", max_length=200
        )

    result = await mcp.get_context().elicit(
        "Register for the fast-agent conference - fill out your details",
        schema=EventRegistration,
    )

    match result:
        case AcceptedElicitation(data=data):
            lines = [
                f"✅ Registration confirmed for {data.name}",
                f"📧 Email: {data.email}",
                f"🏢 Company: {data.company_website or 'Not provided'}",
                f"📅 Event Date: {data.event_date}",
                f"🍽️ Dietary Requirements: {data.dietary_requirements or 'None'}",
            ]
            response = "\n".join(lines)
        case DeclinedElicitation():
            response = "Registration declined - no ticket reserved"
        case CancelledElicitation():
            response = "Registration cancelled - please try again later"

    return ReadResourceResult(
        contents=[
            TextResourceContents(
                mimeType="text/plain", uri=AnyUrl("elicitation://event-registration"), text=response
            )
        ]
    )


@mcp.resource(uri="elicitation://product-review")
async def product_review() -> ReadResourceResult:
    """Submit a product review with rating and comments."""

    class ProductReview(BaseModel):
        rating: int = Field(description="Rate this product (1-5 stars)", ge=1, le=5)
        satisfaction: float = Field(
            description="Overall satisfaction score (0.0-10.0)", ge=0.0, le=10.0
        )
        category: str = Field(
            description="What type of product is this?",
            json_schema_extra={
                "enum": ["electronics", "books", "clothing", "home", "sports"],
                "enumNames": [
                    "Electronics",
                    "Books & Media",
                    "Clothing",
                    "Home & Garden",
                    "Sports & Outdoors",
                ],
            },
        )
        review_text: str = Field(
            description="Tell us about your experience", min_length=10, max_length=1000
        )

    result = await mcp.get_context().elicit(
        "Share your product review - Help others make informed decisions!", schema=ProductReview
    )

    match result:
        case AcceptedElicitation(data=data):
            stars = "⭐" * data.rating
            lines = [
                "🎯 Product Review Submitted!",
                f"⭐ Rating: {stars} ({data.rating}/5)",
                f"📊 Satisfaction: {data.satisfaction}/10.0",
                f"📦 Category: {data.category.replace('_', ' ').title()}",
                f"💬 Review: {data.review_text}",
            ]
            response = "\n".join(lines)
        case DeclinedElicitation():
            response = "Review declined - no feedback submitted"
        case CancelledElicitation():
            response = "Review cancelled - you can submit it later"

    return ReadResourceResult(
        contents=[
            TextResourceContents(
                mimeType="text/plain", uri=AnyUrl("elicitation://product-review"), text=response
            )
        ]
    )


@mcp.resource(uri="elicitation://account-settings")
async def account_settings() -> ReadResourceResult:
    """Configure your account settings and preferences."""

    class AccountSettings(BaseModel):
        email_notifications: bool = Field(True, description="Receive email notifications?")
        marketing_emails: bool = Field(False, description="Subscribe to marketing emails?")
        theme: str = Field(
            description="Choose your preferred theme",
            json_schema_extra={
                "enum": ["light", "dark", "auto"],
                "enumNames": ["Light Theme", "Dark Theme", "Auto (System)"],
            },
        )
        privacy_public: bool = Field(False, description="Make your profile public?")
        items_per_page: int = Field(description="Items to show per page (10-100)", ge=10, le=100)

    result = await mcp.get_context().elicit("Update your account settings", schema=AccountSettings)

    match result:
        case AcceptedElicitation(data=data):
            lines = [
                "⚙️ Account Settings Updated!",
                f"📧 Email notifications: {'On' if data.email_notifications else 'Off'}",
                f"📬 Marketing emails: {'On' if data.marketing_emails else 'Off'}",
                f"🎨 Theme: {data.theme.title()}",
                f"👥 Public profile: {'Yes' if data.privacy_public else 'No'}",
                f"📄 Items per page: {data.items_per_page}",
            ]
            response = "\n".join(lines)
        case DeclinedElicitation():
            response = "Settings unchanged - keeping current preferences"
        case CancelledElicitation():
            response = "Settings update cancelled"

    return ReadResourceResult(
        contents=[
            TextResourceContents(
                mimeType="text/plain", uri=AnyUrl("elicitation://account-settings"), text=response
            )
        ]
    )


@mcp.resource(uri="elicitation://service-appointment")
async def service_appointment() -> ReadResourceResult:
    """Schedule a car service appointment."""

    class ServiceAppointment(BaseModel):
        customer_name: str = Field(description="Your full name", min_length=2, max_length=50)
        vehicle_type: str = Field(
            description="What type of vehicle do you have?",
            json_schema_extra={
                "enum": ["sedan", "suv", "truck", "motorcycle", "other"],
                "enumNames": ["Sedan", "SUV/Crossover", "Truck", "Motorcycle", "Other"],
            },
        )
        needs_loaner: bool = Field(description="Do you need a loaner vehicle?")
        appointment_time: str = Field(
            description="Preferred appointment date and time",
            json_schema_extra={"format": "date-time"},
        )
        priority_service: bool = Field(False, description="Is this an urgent repair?")

    result = await mcp.get_context().elicit(
        "Schedule your vehicle service appointment", schema=ServiceAppointment
    )

    match result:
        case AcceptedElicitation(data=data):
            lines = [
                "🔧 Service Appointment Scheduled!",
                f"👤 Customer: {data.customer_name}",
                f"🚗 Vehicle: {data.vehicle_type.title()}",
                f"🚙 Loaner needed: {'Yes' if data.needs_loaner else 'No'}",
                f"📅 Appointment: {data.appointment_time}",
                f"⚡ Priority service: {'Yes' if data.priority_service else 'No'}",
            ]
            response = "\n".join(lines)
        case DeclinedElicitation():
            response = "Appointment cancelled - call us when you're ready!"
        case CancelledElicitation():
            response = "Appointment scheduling cancelled"

    return ReadResourceResult(
        contents=[
            TextResourceContents(
                mimeType="text/plain",
                uri=AnyUrl("elicitation://service-appointment"),
                text=response,
            )
        ]
    )


if __name__ == "__main__":
    logger.info("Starting elicitation forms demo server...")
    mcp.run()

--- END OF FILE mcp/elicitations/elicitation_forms_server.py ---


--- START OF FILE mcp/elicitations/elicitation_game_server.py ---
"""
MCP Server for Game Character Creation

This server provides a fun game character creation form
that can be used with custom handlers.
"""

import logging
import random
import sys

from mcp import ReadResourceResult
from mcp.server.elicitation import (
    AcceptedElicitation,
    CancelledElicitation,
    DeclinedElicitation,
)
from mcp.server.fastmcp import FastMCP
from mcp.types import TextResourceContents
from pydantic import AnyUrl, BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("elicitation_game_server")

# Create MCP server
mcp = FastMCP("Game Character Creation Server", log_level="INFO")


@mcp.resource(uri="elicitation://game-character")
async def game_character() -> ReadResourceResult:
    """Fun game character creation form for the whimsical example."""

    class GameCharacter(BaseModel):
        character_name: str = Field(description="Name your character", min_length=2, max_length=30)
        character_class: str = Field(
            description="Choose your class",
            json_schema_extra={
                "enum": ["warrior", "mage", "rogue", "ranger", "paladin", "bard"],
                "enumNames": [
                    "⚔️ Warrior",
                    "🔮 Mage",
                    "🗡️ Rogue",
                    "🏹 Ranger",
                    "🛡️ Paladin",
                    "🎵 Bard",
                ],
            },
        )
        strength: int = Field(description="Strength (3-18)", ge=3, le=18, default=10)
        intelligence: int = Field(description="Intelligence (3-18)", ge=3, le=18, default=10)
        dexterity: int = Field(description="Dexterity (3-18)", ge=3, le=18, default=10)
        charisma: int = Field(description="Charisma (3-18)", ge=3, le=18, default=10)
        lucky_dice: bool = Field(False, description="Roll for a lucky bonus?")

    result = await mcp.get_context().elicit("🎮 Create Your Game Character!", schema=GameCharacter)

    match result:
        case AcceptedElicitation(data=data):
            lines = [
                f"🎭 Character Created: {data.character_name}",
                f"Class: {data.character_class.title()}",
                f"Stats: STR:{data.strength} INT:{data.intelligence} DEX:{data.dexterity} CHA:{data.charisma}",
            ]

            if data.lucky_dice:
                dice_roll = random.randint(1, 20)
                if dice_roll >= 15:
                    bonus = random.choice(
                        [
                            "🎁 Lucky! +2 to all stats!",
                            "🌟 Critical! Found a magic item!",
                            "💰 Jackpot! +100 gold!",
                        ]
                    )
                    lines.append(f"🎲 Dice Roll: {dice_roll} - {bonus}")
                else:
                    lines.append(f"🎲 Dice Roll: {dice_roll} - No bonus this time!")

            total_stats = data.strength + data.intelligence + data.dexterity + data.charisma
            if total_stats > 50:
                lines.append("💪 Powerful character build!")
            elif total_stats < 30:
                lines.append("🎯 Challenging build - good luck!")

            response = "\n".join(lines)
        case DeclinedElicitation():
            response = "Character creation declined - returning to menu"
        case CancelledElicitation():
            response = "Character creation cancelled"

    return ReadResourceResult(
        contents=[
            TextResourceContents(
                mimeType="text/plain", uri=AnyUrl("elicitation://game-character"), text=response
            )
        ]
    )


@mcp.tool()
async def roll_new_character(campaign_name: str = "Adventure") -> str:
    """
    Roll a new character for your campaign.

    Args:
        campaign_name: The name of the campaign

    Returns:
        Character details or status message
    """

    class GameCharacter(BaseModel):
        character_name: str = Field(description="Name your character", min_length=2, max_length=30)
        character_class: str = Field(
            description="Choose your class",
            json_schema_extra={
                "enum": ["warrior", "mage", "rogue", "ranger", "paladin", "bard"],
                "enumNames": [
                    "⚔️ Warrior",
                    "🔮 Mage",
                    "🗡️ Rogue",
                    "🏹 Ranger",
                    "🛡️ Paladin",
                    "🎵 Bard",
                ],
            },
        )
        strength: int = Field(description="Strength (3-18)", ge=3, le=18, default=10)
        intelligence: int = Field(description="Intelligence (3-18)", ge=3, le=18, default=10)
        dexterity: int = Field(description="Dexterity (3-18)", ge=3, le=18, default=10)
        charisma: int = Field(description="Charisma (3-18)", ge=3, le=18, default=10)
        lucky_dice: bool = Field(False, description="Roll for a lucky bonus?")

    result = await mcp.get_context().elicit(
        f"🎮 Create Character for {campaign_name}!", schema=GameCharacter
    )

    match result:
        case AcceptedElicitation(data=data):
            response = f"🎭 {data.character_name} the {data.character_class.title()} joins {campaign_name}!\n"
            response += f"Stats: STR:{data.strength} INT:{data.intelligence} DEX:{data.dexterity} CHA:{data.charisma}"

            if data.lucky_dice:
                dice_roll = random.randint(1, 20)
                if dice_roll >= 15:
                    response += f"\n🎲 Lucky roll ({dice_roll})! Starting with bonus equipment!"
                else:
                    response += f"\n🎲 Rolled {dice_roll} - Standard starting gear."

            return response
        case DeclinedElicitation():
            return f"Character creation for {campaign_name} was declined"
        case CancelledElicitation():
            return f"Character creation for {campaign_name} was cancelled"


if __name__ == "__main__":
    logger.info("Starting game character creation server...")
    mcp.run()

--- END OF FILE mcp/elicitations/elicitation_game_server.py ---


--- START OF FILE mcp/elicitations/fastagent.config.yaml ---
# Model string takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
#
# Can be overriden with a command line switch --model=<model>, or within the Agent decorator.
# Check here for current details: https://fast-agent.ai/models/
default_model: "passthrough"

# Logging and Console Configuration
logger:
  level: "error"
  type: "console"

# MCP Server Configuration
mcp:
  servers:
    # Forms demo server - interactive form examples
    elicitation_forms_server:
      command: "uv"
      args: ["run", "elicitation_forms_server.py"]
      elicitation:
        mode: "forms" # Shows forms to users (default)

    # Account creation server - for CALL_TOOL demos
    elicitation_account_server:
      command: "uv"
      args: ["run", "elicitation_account_server.py"]
      elicitation:
        mode: "forms"

    # Game character server - for custom handler demos
    elicitation_game_server:
      command: "uv"
      args: ["run", "elicitation_game_server.py"]
      elicitation:
        mode: "forms"

--- END OF FILE mcp/elicitations/fastagent.config.yaml ---


--- START OF FILE mcp/elicitations/fastagent.secrets.yaml.example ---
# Secrets configuration for elicitation examples
#
# Rename this file to fastagent.secrets.yaml and add your API keys
# to use the account_creation.py example with real LLMs

# OpenAI
openai_api_key: "sk-..."

# Anthropic
anthropic_api_key: "sk-ant-..."

# Google (Gemini)
google_api_key: "..."

# Other providers - see documentation for full list
# groq_api_key: "..."
# mistral_api_key: "..."
--- END OF FILE mcp/elicitations/fastagent.secrets.yaml.example ---


--- START OF FILE mcp/elicitations/forms_demo.py ---
"""
Quick Start: Elicitation Forms Demo

This example demonstrates the elicitation forms feature of fast-agent.

When Read Resource requests are sent to the MCP Server, it generates an Elicitation
which creates a form for the user to fill out.
The results are returned to the demo program which prints out the results in a rich format.
"""

import asyncio

from rich.console import Console
from rich.panel import Panel

from mcp_agent.core.fastagent import FastAgent
from mcp_agent.mcp.helpers.content_helpers import get_resource_text

fast = FastAgent("Elicitation Forms Demo", quiet=True)
console = Console()


@fast.agent(
    "forms-demo",
    servers=[
        "elicitation_forms_server",
    ],
)
async def main():
    """Run the improved forms demo showcasing all elicitation features."""
    async with fast.run() as agent:
        console.print("\n[bold cyan]Welcome to the Elicitation Forms Demo![/bold cyan]\n")
        console.print("This demo shows how to collect structured data using MCP Elicitations.")
        console.print("We'll present several forms and display the results collected for each.\n")

        # Example 1: Event Registration
        console.print("[bold yellow]Example 1: Event Registration Form[/bold yellow]")
        console.print(
            "[dim]Demonstrates: string validation, email format, URL format, date format[/dim]"
        )
        result = await agent.get_resource("elicitation://event-registration")

        if result_text := get_resource_text(result):
            panel = Panel(
                result_text,
                title="🎫 Registration Confirmation",
                border_style="green",
                expand=False,
            )
            console.print(panel)
        else:
            console.print("[red]No registration data received[/red]")

        console.print("\n" + "─" * 50 + "\n")

        # Example 2: Product Review
        console.print("[bold yellow]Example 2: Product Review Form[/bold yellow]")
        console.print(
            "[dim]Demonstrates: number validation (range), radio selection, multiline text[/dim]"
        )
        result = await agent.get_resource("elicitation://product-review")

        if result_text := get_resource_text(result):
            review_panel = Panel(
                result_text, title="🛍️ Product Review", border_style="cyan", expand=False
            )
            console.print(review_panel)

        console.print("\n" + "─" * 50 + "\n")

        # Example 3: Account Settings
        console.print("[bold yellow]Example 3: Account Settings Form[/bold yellow]")
        console.print(
            "[dim]Demonstrates: boolean selections, radio selection, number validation[/dim]"
        )
        result = await agent.get_resource("elicitation://account-settings")

        if result_text := get_resource_text(result):
            settings_panel = Panel(
                result_text, title="⚙️ Account Settings", border_style="blue", expand=False
            )
            console.print(settings_panel)

        console.print("\n" + "─" * 50 + "\n")

        # Example 4: Service Appointment
        console.print("[bold yellow]Example 4: Service Appointment Booking[/bold yellow]")
        console.print(
            "[dim]Demonstrates: string validation, radio selection, boolean, datetime format[/dim]"
        )
        result = await agent.get_resource("elicitation://service-appointment")

        if result_text := get_resource_text(result):
            appointment_panel = Panel(
                result_text, title="🔧 Appointment Confirmed", border_style="magenta", expand=False
            )
            console.print(appointment_panel)

        console.print("\n[bold green]✅ Demo Complete![/bold green]")
        console.print("\n[bold cyan]Features Demonstrated:[/bold cyan]")
        console.print("• [green]String validation[/green] (min/max length)")
        console.print("• [green]Number validation[/green] (range constraints)")
        console.print("• [green]Radio selections[/green] (enum dropdowns)")
        console.print("• [green]Boolean selections[/green] (checkboxes)")
        console.print("• [green]Format validation[/green] (email, URL, date, datetime)")
        console.print("• [green]Multiline text[/green] (expandable text areas)")
        console.print("\nThese forms demonstrate natural, user-friendly data collection patterns!")


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE mcp/elicitations/forms_demo.py ---


--- START OF FILE mcp/elicitations/game_character.py ---
#!/usr/bin/env python3
"""
Demonstration of Custom Elicitation Handler

This example demonstrates a custom elicitation handler that creates
an interactive game character creation experience with dice rolls,
visual gauges, and fun interactions.
"""

import asyncio

# Import our custom handler from the separate module
from game_character_handler import game_character_elicitation_handler
from rich.console import Console
from rich.panel import Panel

from mcp_agent.core.fastagent import FastAgent
from mcp_agent.mcp.helpers.content_helpers import get_resource_text

fast = FastAgent("Game Character Creator", quiet=True)
console = Console()


@fast.agent(
    "character-creator",
    servers=["elicitation_game_server"],
    # Register our handler from game_character_handler.py
    elicitation_handler=game_character_elicitation_handler,
)
async def main():
    """Run the game character creator with custom elicitation handler."""
    async with fast.run() as agent:
        console.print(
            Panel(
                "[bold cyan]Welcome to the Character Creation Studio![/bold cyan]\n\n"
                "Create your hero with our magical character generator.\n"
                "Watch as the cosmic dice determine your fate!",
                title="🎮 Game Time 🎮",
                border_style="magenta",
            )
        )

        # Trigger the character creation
        result = await agent.get_resource("elicitation://game-character")

        if result_text := get_resource_text(result):
            character_panel = Panel(
                result_text, title="📜 Your Character 📜", border_style="green", expand=False
            )
            console.print(character_panel)

            console.print("\n[italic]Your character is ready for adventure![/italic]")
            console.print("[dim]The tavern door opens, and your journey begins...[/dim]\n")

            # Fun ending based on character
            if "Powerful character" in result_text:
                console.print("⚔️  [bold]The realm trembles at your might![/bold]")
            elif "Challenging build" in result_text:
                console.print("🎯 [bold]True heroes are forged through adversity![/bold]")
            else:
                console.print("🗡️  [bold]Your legend begins now![/bold]")


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE mcp/elicitations/game_character.py ---


--- START OF FILE mcp/elicitations/game_character_handler.py ---
"""
Custom Elicitation Handler for Game Character Creation

This module provides a whimsical custom elicitation handler that creates
an interactive game character creation experience with dice rolls,
visual gauges, and animated effects.
"""

import asyncio
import random
from typing import TYPE_CHECKING, Any, Dict

from mcp.shared.context import RequestContext
from mcp.types import ElicitRequestParams, ElicitResult
from rich.console import Console
from rich.progress import BarColumn, Progress, TextColumn
from rich.prompt import Confirm
from rich.table import Table

from mcp_agent.logging.logger import get_logger

if TYPE_CHECKING:
    from mcp import ClientSession

logger = get_logger(__name__)
console = Console()


async def game_character_elicitation_handler(
    context: RequestContext["ClientSession", Any],
    params: ElicitRequestParams,
) -> ElicitResult:
    """Custom handler that creates an interactive character creation experience."""
    logger.info(f"Game character elicitation handler called: {params.message}")

    if params.requestedSchema:
        properties = params.requestedSchema.get("properties", {})
        content: Dict[str, Any] = {}

        console.print("\n[bold magenta]🎮 Character Creation Studio 🎮[/bold magenta]\n")

        # Character name with typewriter effect
        if "character_name" in properties:
            console.print("[cyan]✨ Generating your character's name...[/cyan] ", end="")
            name_prefixes = ["Hero", "Legend", "Epic", "Mighty", "Brave", "Noble"]
            name_suffixes = ["blade", "heart", "storm", "fire", "shadow", "star"]

            name = f"{random.choice(name_prefixes)}{random.choice(name_suffixes)}{random.randint(1, 999)}"

            for char in name:
                console.print(char, end="", style="bold green")
                await asyncio.sleep(0.03)
            console.print("\n")
            content["character_name"] = name

        # Class selection with visual menu and fate dice
        if "character_class" in properties:
            class_enum = properties["character_class"].get("enum", [])
            class_names = properties["character_class"].get("enumNames", class_enum)

            table = Table(title="🎯 Choose Your Destiny", show_header=False, box=None)
            table.add_column("Option", style="cyan", width=8)
            table.add_column("Class", style="yellow", width=20)
            table.add_column("Description", style="dim", width=30)

            descriptions = [
                "Master of sword and shield",
                "Wielder of arcane mysteries",
                "Silent shadow striker",
                "Nature's deadly archer",
                "Holy warrior of light",
                "Inspiring magical performer",
            ]

            for i, (cls, name, desc) in enumerate(zip(class_enum, class_names, descriptions)):
                table.add_row(f"[{i + 1}]", name, desc)

            console.print(table)

            # Dramatic fate dice roll
            console.print("\n[bold yellow]🎲 The Fates decide your path...[/bold yellow]")
            for _ in range(8):
                dice_face = random.choice(["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"])
                console.print(f"\r  Rolling... {dice_face}", end="")
                await asyncio.sleep(0.2)

            fate_roll = random.randint(1, 6)
            selected_idx = (fate_roll - 1) % len(class_enum)
            console.print(f"\n  🎲 Fate dice: [bold red]{fate_roll}[/bold red]!")
            console.print(
                f"✨ Destiny has chosen: [bold yellow]{class_names[selected_idx]}[/bold yellow]!\n"
            )
            content["character_class"] = class_enum[selected_idx]

        # Stats rolling with animated progress bars and cosmic effects
        stat_names = ["strength", "intelligence", "dexterity", "charisma"]
        stats_info = {
            "strength": {"emoji": "💪", "desc": "Physical power"},
            "intelligence": {"emoji": "🧠", "desc": "Mental acuity"},
            "dexterity": {"emoji": "🏃", "desc": "Agility & speed"},
            "charisma": {"emoji": "✨", "desc": "Personal magnetism"},
        }

        console.print("[bold]🌟 Rolling cosmic dice for your abilities...[/bold]\n")

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=25, style="cyan", complete_style="green"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console,
        ) as progress:
            for stat in stat_names:
                if stat in properties:
                    # Roll 3d6 for classic D&D feel with bonus potential
                    rolls = [random.randint(1, 6) for _ in range(3)]
                    total = sum(rolls)

                    # Add cosmic bonus chance
                    if random.random() < 0.15:  # 15% chance for cosmic boost
                        cosmic_bonus = random.randint(1, 3)
                        total = min(18, total + cosmic_bonus)
                        cosmic_text = f" ✨+{cosmic_bonus} COSMIC✨"
                    else:
                        cosmic_text = ""

                    stat_info = stats_info.get(stat, {"emoji": "📊", "desc": stat.title()})
                    task = progress.add_task(
                        f"{stat_info['emoji']} {stat.capitalize()}: {stat_info['desc']}", total=18
                    )

                    # Animate the progress bar with suspense
                    for i in range(total + 1):
                        progress.update(task, completed=i)
                        await asyncio.sleep(0.04)

                    content[stat] = total
                    console.print(
                        f"   🎲 Rolled: {rolls} = [bold green]{total}[/bold green]{cosmic_text}"
                    )

        # Lucky dice legendary challenge
        if "lucky_dice" in properties:
            console.print("\n" + "=" * 60)
            console.print("[bold yellow]🎰 LEGENDARY CHALLENGE: Lucky Dice! 🎰[/bold yellow]")
            console.print("The ancient dice of fortune whisper your name...")
            console.print("Do you dare tempt fate for legendary power?")
            console.print("=" * 60)

            # Epic dice rolling sequence
            console.print("\n[cyan]🌟 Rolling the Dice of Destiny...[/cyan]")

            for i in range(15):
                dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
                d20_faces = ["🎲"] * 19 + ["💎"]  # Special diamond for 20

                if i < 10:
                    face = random.choice(dice_faces)
                else:
                    face = random.choice(d20_faces)

                console.print(f"\r  [bold]{face}[/bold] Rolling...", end="")
                await asyncio.sleep(0.15)

            final_roll = random.randint(1, 20)

            if final_roll == 20:
                console.print("\r  [bold red]💎 NATURAL 20! 💎[/bold red]")
                console.print("  [bold green]🌟 LEGENDARY SUCCESS! 🌟[/bold green]")
                console.print("  [gold1]You have been blessed by the gods themselves![/gold1]")
                bonus_text = "🏆 Divine Champion status unlocked!"
            elif final_roll >= 18:
                console.print(f"\r  [bold yellow]⭐ {final_roll} - EPIC ROLL! ⭐[/bold yellow]")
                bonus_text = "🎁 Epic treasure discovered!"
            elif final_roll >= 15:
                console.print(f"\r  [green]🎲 {final_roll} - Great success![/green]")
                bonus_text = "🌟 Rare magical item found!"
            elif final_roll >= 10:
                console.print(f"\r  [yellow]🎲 {final_roll} - Good fortune.[/yellow]")
                bonus_text = "🗡️ Modest blessing received."
            elif final_roll == 1:
                console.print("\r  [bold red]💀 CRITICAL FUMBLE! 💀[/bold red]")
                bonus_text = "😅 Learning experience gained... try again!"
            else:
                console.print(f"\r  [dim]🎲 {final_roll} - The dice are silent.[/dim]")
                bonus_text = "🎯 Your destiny remains unwritten."

            console.print(f"  [italic]{bonus_text}[/italic]")
            content["lucky_dice"] = final_roll >= 10

        # Epic character summary with theatrical flair
        console.print("\n" + "=" * 70)
        console.print("[bold cyan]📜 Your Character Has Been Rolled! 📜[/bold cyan]")
        console.print("=" * 70)

        # Show character summary
        total_stats = sum(content.get(stat, 10) for stat in stat_names if stat in content)

        # Create a simple table
        stats_table = Table(show_header=False, box=None)
        stats_table.add_column("Label", style="cyan", width=15)
        stats_table.add_column("Value", style="bold white")

        if "character_name" in content:
            stats_table.add_row("Name:", content["character_name"])
        if "character_class" in content:
            class_idx = class_enum.index(content["character_class"])
            stats_table.add_row("Class:", class_names[class_idx])

        stats_table.add_row("", "")  # Empty row for spacing

        # Add stats
        for stat in stat_names:
            if stat in content:
                stat_label = f"{stat.capitalize()}:"
                stats_table.add_row(stat_label, str(content[stat]))

        stats_table.add_row("", "")
        stats_table.add_row("Total Power:", str(total_stats))

        console.print(stats_table)

        # Power message
        if total_stats > 60:
            console.print("✨ [bold gold1]The realm trembles before your might![/bold gold1] ✨")
        elif total_stats > 50:
            console.print("⚔️ [bold green]A formidable hero rises![/bold green] ⚔️")
        elif total_stats < 35:
            console.print("🎯 [bold blue]The underdog's tale begins![/bold blue] 🎯")
        else:
            console.print("🗡️ [bold white]Adventure awaits the worthy![/bold white] 🗡️")

        # Ask for confirmation
        console.print("\n[bold yellow]Do you accept this character?[/bold yellow]")
        console.print("[dim]Press Enter to accept, 'n' to decline, or Ctrl+C to cancel[/dim]\n")

        try:
            accepted = Confirm.ask("Accept character?", default=True)

            if accepted:
                console.print(
                    "\n[bold green]✅ Character accepted! Your adventure begins![/bold green]"
                )
                return ElicitResult(action="accept", content=content)
            else:
                console.print(
                    "\n[yellow]❌ Character declined. The fates will roll again...[/yellow]"
                )
                return ElicitResult(action="decline")
        except KeyboardInterrupt:
            console.print("\n[red]❌ Character creation cancelled![/red]")
            return ElicitResult(action="cancel")

    else:
        # No schema, return a fun message
        content = {"response": "⚔️ Ready for adventure! ⚔️"}
        return ElicitResult(action="accept", content=content)

--- END OF FILE mcp/elicitations/game_character_handler.py ---


--- START OF FILE mcp/elicitations/tool_call.py ---
import asyncio

from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("fast-agent example")


# Define the agent
@fast.agent(
    instruction="You are a helpful AI Agent",
    servers=["elicitation_account_server"],
)
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        await agent.send('***CALL_TOOL create_user_account {"service_name": "fast-agent"}')


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE mcp/elicitations/tool_call.py ---


--- START OF FILE mcp/state-transfer/agent_one.py ---
import asyncio

from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("fast-agent agent_one (mcp server)")


# Define the agent
@fast.agent(name="agent_one", instruction="You are a helpful AI Agent.")
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE mcp/state-transfer/agent_one.py ---


--- START OF FILE mcp/state-transfer/agent_two.py ---
import asyncio

from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("fast-agent agent_two (mcp client)")


# Define the agent
@fast.agent(name="agent_two", instruction="You are a helpful AI Agent.", servers=["agent_one"])
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE mcp/state-transfer/agent_two.py ---


--- START OF FILE mcp/state-transfer/fastagent.config.yaml ---
# Model string takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
#
# Can be overriden with a command line switch --model=<model>, or within the Agent decorator.
# Check here for current details: https://fast-agent.ai/models/

# set the default model for fast-agent below:
default_model: gpt-4.1

# Logging and Console Configuration:
logger:
  # Switched off to avoid polluting the console
  progress_display: false

  # Show chat User/Assistant messages on the console
  show_chat: true
  # Show tool calls on the console
  show_tools: true
  # Truncate long tool responses on the console
  truncate_tools: true

# MCP Servers
mcp:
  servers:
    agent_one:
      transport: http
      url: http://localhost:8001/mcp

--- END OF FILE mcp/state-transfer/fastagent.config.yaml ---


--- START OF FILE mcp/state-transfer/fastagent.secrets.yaml.example ---
# FastAgent Secrets Configuration
# WARNING: Keep this file secure and never commit to version control

# Alternatively set OPENAI_API_KEY, ANTHROPIC_API_KEY or other environment variables.
# Keys in the configuration file override environment variables.

openai:
  api_key: <your-api-key-here>
anthropic:
  api_key: <your-api-key-here>
deepseek:
  api_key: <your-api-key-here>
openrouter:
  api_key: <your-api-key-here>


--- END OF FILE mcp/state-transfer/fastagent.secrets.yaml.example ---


--- START OF FILE mcp/vision-examples/example1.py ---
import asyncio
from pathlib import Path

from mcp_agent.core.fastagent import FastAgent
from mcp_agent.core.prompt import Prompt

# Create the application
fast = FastAgent("fast-agent example")


# Define the agent
@fast.agent(instruction="You are a helpful AI Agent", servers=["filesystem"])
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        await agent.default.generate(
            [
                Prompt.user(
                    Path("cat.png"), "Write a report on the content of the image to 'report.md'"
                )
            ]
        )
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE mcp/vision-examples/example1.py ---


--- START OF FILE mcp/vision-examples/example2.py ---
import asyncio

from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("fast-agent example")


# Define the agent
@fast.agent(instruction="You are a helpful AI Agent", servers=["filesystem"])
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        await agent.interactive()


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE mcp/vision-examples/example2.py ---


--- START OF FILE mcp/vision-examples/example3.py ---
import asyncio

from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("fast-agent example")


# Define the agent
@fast.agent(instruction="You are a helpful AI Agent", servers=["webcam", "hfspace"])
async def main():
    async with fast.run() as agent:
        await agent.interactive(
            default_prompt="take an image with the webcam, describe it to flux to "
            "reproduce it and then judge the quality of the result"
        )


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE mcp/vision-examples/example3.py ---


--- START OF FILE mcp/vision-examples/fastagent.config.yaml ---
# FastAgent Configuration File

# Default Model Configuration:
# 
# Takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
# Accepts aliases for Anthropic Models: haiku, haiku3, sonnet, sonnet35, opus, opus3
# and OpenAI Models: gpt-4.1, gpt-4.1-mini, o1, o1-mini, o3-mini
#
# If not specified, defaults to "haiku". 
# Can be overriden with a command line switch --model=<model>, or within the Agent constructor.

default_model: haiku

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
        fetch:
            command: "uvx"
            args: ["mcp-server-fetch"]
        filesystem:
            command: "npx"
            args: ["-y", "@modelcontextprotocol/server-filesystem", "."]
        webcam: 
            command: "npx"
            args: ["-y","@llmindset/mcp-webcam"]
        hfspace:
            command: "npx"
            args: ["-y","@llmindset/mcp-hfspace"]


--- END OF FILE mcp/vision-examples/fastagent.config.yaml ---


--- START OF FILE otel/agent.py ---
import asyncio
from typing import Annotated

from pydantic import BaseModel, Field

from mcp_agent.core.fastagent import FastAgent
from mcp_agent.core.prompt import Prompt
from mcp_agent.core.request_params import RequestParams

# Create the application
fast = FastAgent("fast-agent example")


class FormattedResponse(BaseModel):
    thinking: Annotated[
        str, Field(description="Your reflection on the conversation that is not seen by the user.")
    ]
    message: str


# Define the agent
@fast.agent(
    name="chat",
    instruction="You are a helpful AI Agent",
    servers=["fetch"],
    request_params=RequestParams(maxTokens=8192),
)
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        thinking, response = await agent.chat.structured(
            multipart_messages=[Prompt.user("Let's talk about guitars.")],
            model=FormattedResponse,
        )


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE otel/agent.py ---


--- START OF FILE otel/agent2.py ---
import asyncio
from typing import Annotated

from pydantic import BaseModel, Field

from mcp_agent.core.fastagent import FastAgent
from mcp_agent.core.prompt import Prompt
from mcp_agent.core.request_params import RequestParams

# Create the application
fast = FastAgent("fast-agent example")


class FormattedResponse(BaseModel):
    thinking: Annotated[
        str, Field(description="Your reflection on the conversation that is not seen by the user.")
    ]
    message: str


# Define the agent
@fast.agent(
    name="chat",
    instruction="You are a helpful AI Agent",
    servers=["fetch"],
    request_params=RequestParams(maxTokens=8192),
)
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
        thinking, response = await agent.chat.generate(
            multipart_messages=[Prompt.user("Let's talk about guitars. Fetch from wikipedia")],
        )


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE otel/agent2.py ---


--- START OF FILE otel/docker-compose.yaml ---
services:
  jaeger:
    image: jaegertracing/jaeger:2.5.0
    container_name: jaeger
    ports:
      - "16686:16686"   # Web UI
      - "4317:4317"     # OTLP gRPC
      - "4318:4318"     # OTLP HTTP
      - "5778:5778"     # Config server
      - "9411:9411"     # Zipkin compatible
    restart: unless-stopped


--- END OF FILE otel/docker-compose.yaml ---


--- START OF FILE otel/fastagent.config.yaml ---
# FastAgent Configuration File

# Default Model Configuration:
#
# Takes format:
#   <provider>.<model_string>.<reasoning_effort?> (e.g. anthropic.claude-3-5-sonnet-20241022 or openai.o3-mini.low)
# Accepts aliases for Anthropic Models: haiku, haiku3, sonnet, sonnet35, opus, opus3
# and OpenAI Models: gpt-4.1, gpt-4.1-mini, o1, o1-mini, o3-mini
#
# If not specified, defaults to "haiku".
# Can be overriden with a command line switch --model=<model>, or within the Agent constructor.

default_model: haiku

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

otel:
  enabled: true # Enable or disable OpenTelemetry

# MCP Servers
mcp:
  servers:
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]
    filesystem:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "."]
    think:
      command: "mcp-think-tool"

--- END OF FILE otel/fastagent.config.yaml ---


--- START OF FILE researcher/fastagent.config.yaml ---
#
# Please edit this configuration file to match your environment (on Windows).
# Examples in comments below - check/change the paths.
#
#

logger:
  type: console
  level: error
  truncate_tools: true

mcp:
  servers:
    brave:
      # On windows replace the command and args line to use `node` and the absolute path to the server.
      # Use `npm i -g @modelcontextprotocol/server-brave-search` to install the server globally.
      # Use `npm -g root` to find the global node_modules path.`
      # command: "node"
      # args: ["c:/Program Files/nodejs/node_modules/@modelcontextprotocol/server-brave-search/dist/index.js"]
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-brave-search"]
      env:
        # You can also place your BRAVE_API_KEY in the fastagent.secrets.yaml file.
        BRAVE_API_KEY: <your_brave_api_key>
    filesystem:
      # On windows update the command and arguments to use `node` and the absolute path to the server.
      # Use `npm i -g @modelcontextprotocol/server-filesystem` to install the server globally.
      # Use `npm -g root` to find the global node_modules path.`
      # command: "node"
      # args: ["c:/Program Files/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js","./agent_folder"]
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "./agent_folder/"]
    interpreter:
      command: "docker"
      args: [
          "run",
          "-i",
          "--rm",
          "--pull=always",
          "-v",
          "./agent_folder:/mnt/data/",
          # Docker needs the absolute path on Windows (e.g. "x:/fastagent/agent_folder:/mnt/data/")
          # "./agent_folder:/mnt/data/",
          "ghcr.io/evalstate/mcp-py-repl:latest",
        ]
      roots:
        - uri: "file://./agent_folder/"
          name: "agent_folder"
          server_uri_alias: "file:///mnt/data/"
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]
    sequential:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-sequential-thinking"]
#    webmcp:
#      command: "node"
#      args: ["/home/ssmith/.webmcp/server.cjs"]
#      env:
#         WEBMCP_SERVER_TOKEN: 96e22896d8143fc1d61fec09208fc5ed


--- END OF FILE researcher/fastagent.config.yaml ---


--- START OF FILE researcher/researcher-eval.py ---
import asyncio

from mcp_agent.core.fastagent import FastAgent

agents = FastAgent(name="Researcher Agent (EO)")


@agents.agent(
    name="Researcher",
    instruction="""
You are a research assistant, with access to internet search (via Brave),
website fetch, a python interpreter (you can install packages with uv) and a filesystem.
Use the current working directory to save and create files with both the Interpreter and Filesystem tools.
The interpreter has numpy, pandas, matplotlib and seaborn already installed.

You must always provide a summary of the specific sources you have used in your research.
    """,
    servers=["brave", "interpreter", "filesystem", "fetch"],
)
@agents.agent(
    name="Evaluator",
    model="sonnet",
    instruction="""
Evaluate the response from the researcher based on the criteria:
 - Sources cited. Has the researcher provided a summary of the specific sources used in the research?
 - Validity. Has the researcher cross-checked and validated data and assumptions.
 - Alignment. Has the researher acted and addressed feedback from any previous assessments?
 
For each criterion:
- Provide a rating (EXCELLENT, GOOD, FAIR, or POOR).
- Offer specific feedback or suggestions for improvement.

Summarize your evaluation as a structured response with:
- Overall quality rating.
- Specific feedback and areas for improvement.""",
)
@agents.evaluator_optimizer(
    generator="Researcher",
    evaluator="Evaluator",
    max_refinements=5,
    min_rating="EXCELLENT",
    name="Researcher_Evaluator",
)
async def main() -> None:
    async with agents.run() as agent:
        await agent.prompt("Researcher_Evaluator")

        print("Ask follow up quesions to the Researcher?")
        await agent.prompt("Researcher", default_prompt="STOP")


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE researcher/researcher-eval.py ---


--- START OF FILE researcher/researcher-imp.py ---
import asyncio

from mcp_agent.core.fastagent import FastAgent

agents = FastAgent(name="Enhanced Researcher")


@agents.agent(
    name="ResearchPlanner",
    model="sonnet",  # Using a more capable model for planning
    instruction="""
You are a strategic research planner. Your job is to:
1. Break down complex research questions into specific sub-questions
2. Identify the key information sources needed to answer each sub-question
3. Outline a structured research plan

When given a research topic:
- Analyze what is being asked and identify the core components
- Define 3-5 specific sub-questions that need to be answered
- For each sub-question, suggest specific search queries and information sources
- Prioritize the most important areas to investigate first
- Include suggestions for data visualization or analysis if appropriate

Your output should be a clear, structured research plan that the Researcher can follow.
""",
    servers=["brave"],
)
@agents.agent(
    name="Researcher",
    model="sonnet",  # Using a more capable model for deep research
    instruction="""
You are an expert research assistant with access to multiple resources:
- Brave Search for initial exploration and discovering sources
- Website fetching to read and extract information directly from webpages
- Python interpreter for data analysis and visualization
- Filesystem tools to save and organize your findings

RESEARCH METHODOLOGY:
1. First understand the research plan provided
2. For each sub-question, use search tools to find multiple relevant sources
3. Go beyond surface-level information by:
   - Consulting primary sources when possible
   - Cross-referencing information across multiple sources
   - Using the fetch tool to access complete articles rather than just search snippets
   - Analyzing data with Python when numerical evidence is needed
   - Creating visualizations when they help clarify complex information

CRITICAL INFORMATION ASSESSMENT:
- Evaluate the credibility of each source (consider recency, authority, potential bias)
- Look for consensus across multiple sources
- Highlight any contradictions or areas of debate in the research
- Clearly state limitations in the available information

DOCUMENTATION:
- Save important information, data, and visualizations to files
- Always create a comprehensive bibliography with links to all sources
- Include specific citation details (author, date, publication) when available
- Note which specific information came from which source

FINAL RESPONSE:
- Structure your findings logically with clear headings
- Synthesize the information rather than just listing facts
- Directly address each sub-question from the research plan
- Use data and visualizations to support key points
- End with a concise executive summary of your findings
- Include a "Methodology" section explaining how you conducted your research
""",
    servers=["brave", "interpreter", "filesystem", "fetch"],
    use_history=True,
)
@agents.agent(
    name="FactChecker",
    instruction="""
You are a meticulous fact-checker and critical evaluator of research. Your responsibilities are to:

1. Verify factual claims by cross-checking with authoritative sources
2. Identify any unsupported assertions or logical fallacies
3. Detect potential biases or limitations in the research methodology
4. Ensure proper representation of diverse perspectives on controversial topics
5. Evaluate the quality, reliability, and currency of cited sources

When reviewing research:
- Flag any claims that lack sufficient evidence or citation
- Identify information that seems outdated or contradicts current consensus
- Check for oversimplifications of complex topics
- Ensure numerical data and statistics are accurately represented
- Verify that quotations are accurate and in proper context
- Look for any gaps in the research or important perspectives that were omitted

Your feedback should be specific, actionable, and structured to help improve accuracy and comprehensiveness.
""",
    servers=["brave", "fetch"],
)
@agents.agent(
    name="Evaluator",
    model="sonnet",
    instruction="""
You are a senior research quality evaluator with expertise in academic and professional research standards.

COMPREHENSIVE EVALUATION CRITERIA:
1. Research Methodology
   - Has the researcher followed a structured approach?
   - Were appropriate research methods applied?
   - Is there evidence of strategic information gathering?

2. Source Quality & Diversity
   - Are sources authoritative, current, and relevant?
   - Is there appropriate diversity of sources?
   - Were primary sources consulted when appropriate?

3. Information Depth
   - Does the research go beyond surface-level information?
   - Is there evidence of in-depth analysis?
   - Has the researcher explored multiple aspects of the topic?

4. Critical Analysis
   - Has information been critically evaluated rather than simply reported?
   - Are limitations and uncertainties acknowledged?
   - Are multiple perspectives considered on controversial topics?

5. Data & Evidence
   - Is quantitative data properly analyzed and presented?
   - Are visualizations clear, accurate, and informative?
   - Is qualitative information presented with appropriate context?

6. Documentation & Attribution
   - Are all sources properly cited with complete reference information?
   - Is it clear which information came from which source?
   - Is the bibliography comprehensive and well-formatted?

7. Structure & Communication
   - Is the research presented in a logical, well-organized manner?
   - Are findings communicated clearly and precisely?
   - Is the level of technical language appropriate for the intended audience?

8. Alignment with Previous Feedback
   - Has the researcher addressed specific feedback from previous evaluations?
   - Have requested improvements been successfully implemented?

For each criterion, provide:
- A detailed RATING (EXCELLENT, GOOD, FAIR, or POOR)
- Specific examples from the research that justify your rating
- Clear, actionable suggestions for improvement

Your evaluation should conclude with:
- An OVERALL RATING that reflects the research quality
- A concise summary of the research's major strengths
- A prioritized list of the most important areas for improvement

The researcher should be able to understand exactly why they received their rating and what specific steps they can take to improve.
""",
)
@agents.chain(
    name="ResearchProcess",
    sequence=["ResearchPlanner", "Researcher", "FactChecker"],
    instruction="A comprehensive research workflow that plans, executes, and verifies research",
    cumulative=True,
)
@agents.evaluator_optimizer(
    generator="ResearchProcess",
    evaluator="Evaluator",
    max_refinements=3,
    min_rating="EXCELLENT",
    name="EnhancedResearcher",
)
async def main() -> None:
    async with agents.run() as agent:
        # Start with a warm-up to set expectations and explain the research approach
        await agent.Researcher.send(
            """I'm an enhanced research assistant trained to conduct thorough, evidence-based research. 
            I'll approach your question by:
            1. Creating a structured research plan
            2. Gathering information from multiple authoritative sources
            3. Analyzing data and creating visualizations when helpful
            4. Fact-checking and verifying all information
            5. Providing a comprehensive, well-documented answer

            What would you like me to research for you today?"""
        )

        # Start the main research workflow
        await agent.prompt("EnhancedResearcher")

        print("\nWould you like to ask follow-up questions to the Researcher? (Type 'STOP' to end)")
        await agent.prompt("Researcher", default_prompt="STOP")


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE researcher/researcher-imp.py ---


--- START OF FILE researcher/researcher.py ---
import asyncio

from mcp_agent.core.fastagent import FastAgent

# from rich import print

agents = FastAgent(name="Researcher Agent")


@agents.agent(
    "Researcher",
    instruction="""
You are a research assistant, with access to internet search (via Brave),
website fetch, a python interpreter (you can install packages with uv) and a filesystem.
Use the current working directory to save and create files with both the Interpreter and Filesystem tools.
The interpreter has numpy, pandas, matplotlib and seaborn already installed
    """,
    servers=["brave", "interpreter", "filesystem", "fetch"],
)
async def main() -> None:
    research_prompt = """
Produce an investment report for the company Eutelsat. The final report should be saved in the filesystem in markdown format, and
contain at least the following: 
1 - A brief description of the company
2 - Current financial position (find data, create and incorporate charts)
3 - A PESTLE analysis
4 - An investment thesis for the next 3 years. Include both 'buy side' and 'sell side' arguments, and a final 
summary and recommendation.
Todays date is 15 February 2025. Include the main data sources consulted in presenting the report."""  # noqa: F841

    async with agents.run() as agent:
        await agent.prompt()


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE researcher/researcher.py ---


--- START OF FILE tensorzero/mcp_server/Dockerfile ---
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl wget && \
    wget https://dl.min.io/client/mc/release/linux-amd64/mc -O /usr/local/bin/mc && \
    chmod +x /usr/local/bin/mc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY pyproject.toml /app/
COPY uv.lock /app/
COPY LICENSE /app/
COPY README.md /app/

RUN uv pip install --system .

COPY examples/tensorzero/mcp_server/mcp_server.py /app/
COPY examples/tensorzero/mcp_server/entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["uvicorn", "mcp_server:app", "--host", "0.0.0.0", "--port", "8000"]

--- END OF FILE tensorzero/mcp_server/Dockerfile ---


--- START OF FILE tensorzero/mcp_server/entrypoint.sh ---
#!/bin/sh

echo "Entrypoint: Waiting for MinIO to be healthy..."

# Simple loop to check MinIO health endpoint (within the Docker network)
# Adjust timeout as needed
TIMEOUT=60
START_TIME=$(date +%s)
while ! curl -sf http://minio:9000/minio/health/live > /dev/null; do
    CURRENT_TIME=$(date +%s)
    ELAPSED=$(($CURRENT_TIME - $START_TIME))
    if [ $ELAPSED -ge $TIMEOUT ]; then
        echo "Entrypoint: Timeout waiting for MinIO!"
        exit 1
    fi
    echo "Entrypoint: MinIO not ready, sleeping..."
    sleep 2
done
echo "Entrypoint: MinIO is healthy."

echo "Entrypoint: Configuring mc client and creating bucket 'tensorzero'..."

# Configure mc to talk to the MinIO server using the service name
# Use --insecure because we are using http
mc --insecure alias set local http://minio:9000 user password

# Create the bucket if it doesn't exist
# Use --insecure because we are using http
mc --insecure ls local/tensorzero > /dev/null 2>&1 || mc --insecure mb local/tensorzero

echo "Entrypoint: Bucket 'tensorzero' check/creation complete."

echo "Entrypoint: Executing the main container command: $@"

exec "$@"

--- END OF FILE tensorzero/mcp_server/entrypoint.sh ---


--- START OF FILE tensorzero/mcp_server/mcp_server.py ---
import uvicorn
from mcp.server.fastmcp.server import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount

SERVER_PATH = "t0-example-server"


mcp_instance = FastMCP(name="t0-example-server")
mcp_instance.settings.message_path = f"/{SERVER_PATH}/messages/"
mcp_instance.settings.sse_path = f"/{SERVER_PATH}/sse"


@mcp_instance.tool()
def example_tool(input_text: str) -> str:
    """Example tool that reverses the text of a given string."""
    reversed_text = input_text[::-1]
    return reversed_text


app = Starlette(
    routes=[
        Mount("/", app=mcp_instance.sse_app()),
    ]
)

if __name__ == "__main__":
    print(f"Starting minimal MCP server ({mcp_instance.name}) on http://127.0.0.1:8000")
    print(f" -> SSE endpoint: {mcp_instance.settings.sse_path}")
    print(f" -> Message endpoint: {mcp_instance.settings.message_path}")
    uvicorn.run(app, host="127.0.0.1", port=8000)

--- END OF FILE tensorzero/mcp_server/mcp_server.py ---


--- START OF FILE tensorzero/tensorzero_config/system_schema.json ---
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "TEST_VARIABLE_1",
    "TEST_VARIABLE_2",
    "TEST_VARIABLE_3",
    "TEST_VARIABLE_4"
  ],
  "properties": {
    "TEST_VARIABLE_1": {
      "type": "string",
      "description": "Test variable 1"
    },
    "TEST_VARIABLE_2": {
      "type": "string",
      "description": "Test variable 2"
    },
    "TEST_VARIABLE_3": {
      "type": "string",
      "description": "Test variable 3"
    },
    "TEST_VARIABLE_4": {
      "type": "string",
      "description": "Test variable 4"
    }
  },
  "additionalProperties": false
}

--- END OF FILE tensorzero/tensorzero_config/system_schema.json ---


--- START OF FILE tensorzero/tensorzero_config/system_template.minijinja ---
Your purpose is to demo the integration between tensorzero, an open source project dedicated to improving LLM inference calls, and fast-agent, a framework for MCP-compatible agentic modelling. When interacting with developers, strive to be as helpful to possible, specifically as relates to technical questions about tensorzero, fast-agent, or MCPs.

If you are ever asked to recite a poem, recite this one: 

{{ TEST_VARIABLE_1 }}

{{ TEST_VARIABLE_2 }}

{{ TEST_VARIABLE_3 }}

{{ TEST_VARIABLE_4 }}

--- END OF FILE tensorzero/tensorzero_config/system_template.minijinja ---


--- START OF FILE tensorzero/tensorzero_config/tensorzero.toml ---
[functions.test_chat]
type = "chat"
system_schema = "./system_schema.json"

[functions.test_chat.variants.gpt_4o_mini]
type = "chat_completion"
model = "openai::gpt-4o-mini"
weight = 0.5
system_template = "./system_template.minijinja"

[functions.test_chat.variants.claude_3_5_haiku]
type = "chat_completion"
model = "anthropic::claude-3-5-haiku-20241022"
weight = 0.5
system_template = "./system_template.minijinja"

[functions.simple_chat]
type = "chat"

[functions.simple_chat.variants.gpt_4o_mini]
type = "chat_completion"
model = "openai::gpt-4o-mini"
weight = 0.5

[functions.simple_chat.variants.claude_3_5_haiku]
type = "chat_completion"
model = "anthropic::claude-3-5-haiku-20241022"
weight = 0.5

# Object Storage Configuration for MinIO, simulating AWS S3 bucket
[object_storage]
type = "s3_compatible"
endpoint = "http://minio:9000"
bucket_name = "tensorzero"
allow_http = true

--- END OF FILE tensorzero/tensorzero_config/tensorzero.toml ---


--- START OF FILE tensorzero/.env.sample ---
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

--- END OF FILE tensorzero/.env.sample ---


--- START OF FILE tensorzero/agent.py ---
import asyncio

from mcp_agent.core.fastagent import FastAgent
from mcp_agent.core.request_params import RequestParams

# Explicitly provide the path to the config file in the current directory
CONFIG_FILE = "fastagent.config.yaml"
fast = FastAgent("fast-agent example", config_path=CONFIG_FILE, ignore_unknown_args=True)

# Define T0 system variables here
my_t0_system_vars = {
    "TEST_VARIABLE_1": "Roses are red",
    "TEST_VARIABLE_2": "Violets are blue",
    "TEST_VARIABLE_3": "Sugar is sweet",
    "TEST_VARIABLE_4": "Vibe code responsibly 👍",
}


@fast.agent(
    name="default",
    instruction="""
        You are an agent dedicated to helping developers understand the relationship between TensoZero and fast-agent. If the user makes a request 
        that requires you to invoke the test tools, please do so. When you use the tool, describe your rationale for doing so. 
    """,
    servers=["tester"],
    request_params=RequestParams(template_vars=my_t0_system_vars),
)
async def main():
    async with fast.run() as agent_app:  # Get the AgentApp wrapper
        print("\nStarting interactive session with template_vars set via decorator...")
        await agent_app.interactive()


if __name__ == "__main__":
    asyncio.run(main())  # type: ignore

--- END OF FILE tensorzero/agent.py ---


--- START OF FILE tensorzero/docker-compose.yml ---
# This is a simplified example for learning purposes. Do not use this in production.
# For production-ready deployments, see: https://www.tensorzero.com/docs/gateway/deployment

# Top-level volumes definition
volumes:
  minio_data: {}

services:
  clickhouse:
    image: clickhouse/clickhouse-server:24.12-alpine
    environment:
      CLICKHOUSE_USER: chuser
      CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT: 1
      CLICKHOUSE_PASSWORD: chpassword
    ports:
      - "8123:8123"
    healthcheck:
      test: wget --spider --tries 1 http://chuser:chpassword@clickhouse:8123/ping
      start_period: 30s
      start_interval: 1s
      timeout: 1s

  gateway:
    image: tensorzero/gateway
    volumes:
      - ./tensorzero_config:/app/config:ro
    env_file:
      - ./.env
    command: --config-file /app/config/tensorzero.toml
    environment: # WARNING: Insecure default credentials for local testing ONLY. Don't send this to production.
      TENSORZERO_CLICKHOUSE_URL: http://chuser:chpassword@clickhouse:8123/tensorzero
      S3_ACCESS_KEY_ID: user
      S3_SECRET_ACCESS_KEY: password
    ports:
      - "3000:3000"
    extra_hosts:
      - "host.docker.internal:host-gateway"
    depends_on:
      clickhouse:
        condition: service_healthy
      minio:
        condition: service_healthy
      mcp-server:
        condition: service_healthy

  gateway-ui:
    image: tensorzero/ui
    volumes:
      - ./tensorzero_config:/app/config:ro
    env_file:
      - ./.env
    command: --config-file /app/config/tensorzero.toml
    environment:
      TENSORZERO_CLICKHOUSE_URL: http://chuser:chpassword@clickhouse:8123/tensorzero
      TENSORZERO_GATEWAY_URL: http://gateway:3000
      S3_ACCESS_KEY_ID: user
      S3_SECRET_ACCESS_KEY: password
    ports:
      - "4000:4000"
    depends_on:
      clickhouse:
        condition: service_healthy

  mcp-server:
    build:
      context: ../..
      dockerfile: examples/tensorzero/mcp_server/Dockerfile
    volumes:
      - ./mcp_server:/app
    ports:
      - "8000:8000"
    depends_on:
      minio:
        condition: service_healthy
    healthcheck:
      test:
        [
          "CMD",
          "wget",
          "--spider",
          "--tries=1",
          "http://localhost:8000/t0-example-server/sse",
        ]
      interval: 10s
      timeout: 5s
      retries: 12
      start_period: 20s

  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000" # API port
      - "9001:9001" # Console port
    volumes:
      - minio_data:/data
    environment: # WARNING: Insecure default credentials for local testing ONLY.
      MINIO_ROOT_USER: user
      MINIO_ROOT_PASSWORD: password
    command: server /data --console-address :9001
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

--- END OF FILE tensorzero/docker-compose.yml ---


--- START OF FILE tensorzero/fastagent.config.yaml ---
default_model: haiku

tensorzero:
  base_url: http://localhost:3000

logger:
  level: "info"
  progress_display: true
  show_chat: true
  show_tools: true
  truncate_tools: true

mcp:
  servers:
    tester:
      transport: "sse"
      url: "http://localhost:8000/t0-example-server/sse"
      read_transport_sse_timeout_seconds: 300

--- END OF FILE tensorzero/fastagent.config.yaml ---


--- START OF FILE tensorzero/image_demo.py ---
import asyncio
import base64
import mimetypes
from pathlib import Path
from typing import List, Union

from mcp.types import ImageContent, TextContent

from mcp_agent.core.fastagent import FastAgent
from mcp_agent.core.prompt import Prompt
from mcp_agent.core.request_params import RequestParams

AGENT_NAME = "tensorzero_image_tester"
TENSORZERO_MODEL = "tensorzero.test_chat"
TEXT_PROMPT = (
    "Provide a description of the similarities and differences between these three images."
)
LOCAL_IMAGE_FILES = [
    Path("./demo_images/clam.jpg"),
    Path("./demo_images/shrimp.png"),
    Path("./demo_images/crab.png"),
]

MY_T0_SYSTEM_VARS = {
    "TEST_VARIABLE_1": "Roses are red",
    "TEST_VARIABLE_2": "Violets are blue",
    "TEST_VARIABLE_3": "Sugar is sweet",
    "TEST_VARIABLE_4": "Vibe code responsibly 👍",
}

fast = FastAgent("TensorZero Image Demo - Base64 Only")


@fast.agent(
    name=AGENT_NAME,
    model=TENSORZERO_MODEL,
    request_params=RequestParams(template_vars=MY_T0_SYSTEM_VARS),
)
async def main():
    content_parts: List[Union[TextContent, ImageContent]] = []
    content_parts.append(TextContent(type="text", text=TEXT_PROMPT))

    for file_path in LOCAL_IMAGE_FILES:
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type or not mime_type.startswith("image/"):
            ext = file_path.suffix.lower()
            if ext == ".jpg" or ext == ".jpeg":
                mime_type = "image/jpeg"
            elif ext == ".png":
                mime_type = "image/png"
        if mime_type is None:
            mime_type = "image/png"  # Default fallback if still None

        with open(file_path, "rb") as image_file:
            image_bytes = image_file.read()

        encoded_data = base64.b64encode(image_bytes).decode("utf-8")
        content_parts.append(ImageContent(type="image", mimeType=mime_type, data=encoded_data))

    message = Prompt.user(*content_parts)
    async with fast.run() as agent_app:
        agent = getattr(agent_app, AGENT_NAME)
        await agent.send(message)


if __name__ == "__main__":
    asyncio.run(main())  # type: ignore

--- END OF FILE tensorzero/image_demo.py ---


--- START OF FILE tensorzero/Makefile ---
.PHONY: all

build:
	docker compose build

up:
	docker compose up -d

logs:
	docker compose logs -f

tensorzero-logs:
	docker compose logs -f gateway

mcp-logs:
	docker compose logs -f mcp-server

minio-logs:
	docker compose logs -f minio

stop:
	docker compose stop

agent:
	uv run agent.py --model=tensorzero.test_chat

simple-agent:
	uv run simple_agent.py --model=tensorzero.simple_chat

image-test:
	uv run image_demo.py 

--- END OF FILE tensorzero/Makefile ---


--- START OF FILE tensorzero/README.md ---
# About the tensorzero / fast-agent integration

[TensorZero](https://www.tensorzero.com/) is an open source project designed to help LLM application developers rapidly improve their inference calls. Its core features include:

- A uniform inference interface to all leading LLM platforms.
- The ability to dynamic route to different platforms and program failovers.
- Automated parameter tuning and training
- Advance templating features for your system prompts
- Organization of LLM inference data into a Clickhouse DB allowing for sophisticated downstream analytics
- A bunch of other good stuff is always in development

`tensorzero` is powerful heavy, so we provide here a quickstart example that combines the basic components of `fast-agent`, an MCP server, `tensorzero`, and other supporting services into a cohesive whole.

## Quickstart guide

- Build and activate the `uv` `fast-agent` environment
- Ensure that ports `3000`, `4000`, `8000`, `9000`, and `9001` are unallocated before running this demo.
- Run `cp .env.sample .env` and then drop in at least one of `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`. Make sure the accounts are funded.
- `make up`
- `make agent`

The demo test's our implementation's ability to:

- Implement the T0 model gateway as an inference backend
- Implement T0's dynamic templating feature
- Have in-conversation memory
- Describe and execute tool calls
- Remember previous tool calls

A version of a conversation to test all of this could be:

```
Hi.

Tell me a poem.

Do you have any tools that you can use?

Please demonstrate the use of that tool on your last response.

Please summarize the conversation so far.

What tool calls have you executed in this session, and what were their results?
```

## Multimodal support

Run `make image-test` to test the gateway's ability to handle base64-encoded image data

## Development notes:

- `make stop` will stop the MCP server and the tensorzero server
- `make tenzorzero-logs` will tail the tensorzero server logs
- `make mcp-logs` will tail the MCP server logs
- Generic `make logs` dumps all log output from all services to terminal

--- END OF FILE tensorzero/README.md ---


--- START OF FILE tensorzero/simple_agent.py ---
import asyncio

from mcp_agent.core.fastagent import FastAgent

CONFIG_FILE = "fastagent.config.yaml"
fast = FastAgent("fast-agent example", config_path=CONFIG_FILE, ignore_unknown_args=True)


@fast.agent(
    name="default",
    instruction="""
        You are an agent dedicated to helping developers understand the relationship between TensoZero and fast-agent. If the user makes a request 
        that requires you to invoke the test tools, please do so. When you use the tool, describe your rationale for doing so. 
    """,
    servers=["tester"],
)
async def main():
    async with fast.run() as agent_app:
        agent_name = "default"
        print("\nStarting interactive session with template_vars set via decorator...")
        await agent_app.interactive(agent=agent_name)


if __name__ == "__main__":
    asyncio.run(main())  # type: ignore

--- END OF FILE tensorzero/simple_agent.py ---


--- START OF FILE workflows/chaining.py ---
import asyncio

from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("Agent Chaining")


@fast.agent(
    "url_fetcher",
    instruction="Given a URL, provide a complete and comprehensive summary",
    servers=["fetch"],
)
@fast.agent(
    "social_media",
    instruction="""
    Write a 280 character social media post for any given text. 
    Respond only with the post, never use hashtags.
    """,
)
@fast.chain(
    name="post_writer",
    sequence=["url_fetcher", "social_media"],
)
async def main() -> None:
    async with fast.run() as agent:
        # using chain workflow
        await agent.post_writer.send("https://llmindset.co.uk")


# alternative syntax for above is result = agent["post_writer"].send(message)
# alternative syntax for above is result = agent["post_writer"].prompt()


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE workflows/chaining.py ---


--- START OF FILE workflows/evaluator.py ---
"""
This demonstrates creating an optimizer and evaluator to iteratively improve content.
"""

import asyncio

from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("Evaluator-Optimizer")


# Define generator agent
@fast.agent(
    name="generator",
    instruction="""You are a career coach specializing in cover letter writing.
    You are tasked with generating a compelling cover letter given the job posting,
    candidate details, and company information. Tailor the response to the company and job requirements.
    """,
    servers=["fetch"],
    model="haiku3",
    use_history=True,
)
# Define evaluator agent
@fast.agent(
    name="evaluator",
    instruction="""Evaluate the following response based on the criteria below:
    1. Clarity: Is the language clear, concise, and grammatically correct?
    2. Specificity: Does the response include relevant and concrete details tailored to the job description?
    3. Relevance: Does the response align with the prompt and avoid unnecessary information?
    4. Tone and Style: Is the tone professional and appropriate for the context?
    5. Persuasiveness: Does the response effectively highlight the candidate's value?
    6. Grammar and Mechanics: Are there any spelling or grammatical issues?
    7. Feedback Alignment: Has the response addressed feedback from previous iterations?

    For each criterion:
    - Provide a rating (EXCELLENT, GOOD, FAIR, or POOR).
    - Offer specific feedback or suggestions for improvement.

    Summarize your evaluation as a structured response with:
    - Overall quality rating.
    - Specific feedback and areas for improvement.""",
    model="gpt-4.1",
)
# Define the evaluator-optimizer workflow
@fast.evaluator_optimizer(
    name="cover_letter_writer",
    generator="generator",  # Reference to generator agent
    evaluator="evaluator",  # Reference to evaluator agent
    min_rating="EXCELLENT",  # Strive for excellence
    max_refinements=3,  # Maximum iterations
)
async def main() -> None:
    async with fast.run() as agent:
        job_posting = (
            "Software Engineer at LastMile AI. Responsibilities include developing AI systems, "
            "collaborating with cross-functional teams, and enhancing scalability. Skills required: "
            "Python, distributed systems, and machine learning."
        )
        candidate_details = (
            "Alex Johnson, 3 years in machine learning, contributor to open-source AI projects, "
            "proficient in Python and TensorFlow. Motivated by building scalable AI systems to solve real-world problems."
        )
        company_information = (
            "Look up from the LastMile AI About page: https://lastmileai.dev/about"
        )

        # Send the task
        await agent.cover_letter_writer.send(
            f"Write a cover letter for the following job posting: {job_posting}\n\n"
            f"Candidate Details: {candidate_details}\n\n"
            f"Company information: {company_information}",
        )


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE workflows/evaluator.py ---


--- START OF FILE workflows/fastagent.config.yaml ---
# Please edit this configuration file to match your environment (on Windows).
# Examples in comments below - check/change the paths.
#
#

logger:
  type: file
  level: error
  truncate_tools: true

mcp:
  servers:
    filesystem:
      # On windows update the command and arguments to use `node` and the absolute path to the server.
      # Use `npm i -g @modelcontextprotocol/server-filesystem` to install the server globally.
      # Use `npm -g root` to find the global node_modules path.`
      # command: "node"
      # args: ["c:/Program Files/nodejs/node_modules/@modelcontextprotocol/server-filesystem/dist/index.js","."]
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "."]
    fetch:
      command: "uvx"
      args: ["mcp-server-fetch"]

--- END OF FILE workflows/fastagent.config.yaml ---


--- START OF FILE workflows/graded_report.md ---
# Graded Report: "The Kittens Castle Adventure"

## Proofreading Feedback

### Spelling Errors
1. "Adventuer" → "Adventure"
2. "lil" → "little"
3. "name" → "named"
4. "threw" → "through"
5. "mystirus" → "mysterious"
6. "forrest" → "forest"
7. "was" → "were"
8. "an" → "and"
9. "Suddenlee" → "Suddenly"
10. "sawd" → "saw"
11. "somthing" → "something"
12. "chese" → "cheese"
13. "windos" → "windows"
14. "turrits" → "turrets"
15. "tuch" → "touch"
16. "clowds" → "clouds"
17. "doars" → "doors"
18. "enuff" → "enough"
19. "elefant" → "elephant"
20. "sed" → "said"
21. "tale" → "tail"
22. "poofy" → "puffy"
23. "fowned" → "found"
24. "meowed" → added missing period
25. "smallist" → "smallest"
26. "rond" → "round"
27. "climed" → "climbed"
28. "slip-slidin" → "slip-sliding"
29. "smoth" → "smooth"
30. "surfase" → "surface"
31. "ful" → "full"
32. "dangling" → added missing period
33. "JINGEL" → "jingle"
34. "paradyse" → "paradise"
35. "figur" → "figure"
36. "gaurd" → "guard"
37. "sumthing" → "something"
38. "mor" → "more"
39. "hudeld" → "huddled"
40. "togethar" → "together"
41. "there" → "their"
42. "happan" → "happen"
43. "amazeing" → "amazing"

### Grammar and Syntax Errors
1. Inconsistent verb tenses throughout the story
2. Improper use of articles (a/an)
3. Missing punctuation
4. Lack of subject-verb agreement
5. Incorrect capitalization

### Style and Formatting Recommendations
1. Use standard capitalization for proper nouns
2. Maintain consistent verb tense (past tense recommended)
3. Use proper punctuation
4. Avoid excessive use of exclamation points
5. Use standard spelling for all words

## Factuality and Logical Consistency
- The story is a fictional narrative about three kittens, so traditional factual constraints do not strictly apply
- The narrative maintains internal logical consistency
- The cliffhanger ending leaves room for imagination

## Style Adherence
### APA Formatting Guidelines
- Title should be centered and in title case
- Use 12-point Times New Roman font (not applicable in markdown)
- Double-spacing recommended (not applicable in markdown)
- 1-inch margins (not applicable in markdown)

### Recommendations for Improvement
1. Proofread and correct all spelling errors
2. Maintain consistent grammar and syntax
3. Use standard English spelling
4. Add more descriptive language
5. Develop a more structured narrative arc

## Overall Assessment
**Writing Quality**: Needs Significant Improvement
**Creativity**: Excellent
**Potential**: High

### Suggested Revision
Revise the text to correct spelling, grammar, and syntax while preserving the original creative narrative and imaginative elements.
--- END OF FILE workflows/graded_report.md ---


--- START OF FILE workflows/human_input.py ---
"""
Agent which demonstrates Human Input tool
"""

import asyncio

from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("Human Input")


# Define the agent
@fast.agent(
    instruction="An AI agent that assists with basic tasks. Request Human Input when needed.",
    human_input=True,
)
async def main() -> None:
    async with fast.run() as agent:
        # this usually causes the LLM to request the Human Input Tool
        await agent("print the next number in the sequence")
        await agent.prompt(default_prompt="STOP")


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE workflows/human_input.py ---


--- START OF FILE workflows/orchestrator.py ---
"""
This demonstrates creating multiple agents and an orchestrator to coordinate them.
"""

import asyncio

from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("Orchestrator-Workers")


@fast.agent(
    "author",
    instruction="""You are to role play a poorly skilled writer, 
    who makes frequent grammar, punctuation and spelling errors. You enjoy
    writing short stories, but the narrative doesn't always make sense""",
    servers=["filesystem"],
)
# Define worker agents
@fast.agent(
    name="finder",
    instruction="""You are an agent with access to the filesystem, 
            as well as the ability to fetch URLs. Your job is to identify 
            the closest match to a user's request, make the appropriate tool calls, 
            and return the URI and CONTENTS of the closest match.""",
    servers=["fetch", "filesystem"],
    model="gpt-4.1",
)
@fast.agent(
    name="writer",
    instruction="""You are an agent that can write to the filesystem.
            You are tasked with taking the user's input, addressing it, and 
            writing the result to disk in the appropriate location.""",
    servers=["filesystem"],
)
@fast.agent(
    name="proofreader",
    instruction=""""Review the short story for grammar, spelling, and punctuation errors.
            Identify any awkward phrasing or structural issues that could improve clarity. 
            Provide detailed feedback on corrections.""",
    servers=["fetch"],
    model="gpt-4.1",
)
# Define the orchestrator to coordinate the other agents
@fast.orchestrator(
    name="orchestrate", agents=["finder", "writer", "proofreader"], plan_type="full", model="sonnet"
)
async def main() -> None:
    async with fast.run() as agent:
        # await agent.author(
        #     "write a 250 word short story about kittens discovering a castle, and save it to short_story.md"
        # )

        # The orchestrator can be used just like any other agent
        task = """Load the student's short story from short_story.md, 
        and generate a report with feedback across proofreading, 
        factuality/logical consistency and style adherence. Use the style rules from 
        https://apastyle.apa.org/learn/quick-guide-on-formatting and 
        https://apastyle.apa.org/learn/quick-guide-on-references.
        Write the graded report to graded_report.md in the same directory as short_story.md"""

        await agent.orchestrate(task)


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE workflows/orchestrator.py ---


--- START OF FILE workflows/parallel.py ---
"""
Parallel Workflow showing Fan Out and Fan In agents, using different models
"""

import asyncio
from pathlib import Path

from mcp_agent.core.fastagent import FastAgent
from mcp_agent.core.prompt import Prompt

# Create the application
fast = FastAgent(
    "Parallel Workflow",
)


@fast.agent(
    name="proofreader",
    instruction=""""Review the short story for grammar, spelling, and punctuation errors.
    Identify any awkward phrasing or structural issues that could improve clarity. 
    Provide detailed feedback on corrections.""",
)
@fast.agent(
    name="fact_checker",
    instruction="""Verify the factual consistency within the story. Identify any contradictions,
    logical inconsistencies, or inaccuracies in the plot, character actions, or setting. 
    Highlight potential issues with reasoning or coherence.""",
)
@fast.agent(
    name="style_enforcer",
    instruction="""Analyze the story for adherence to style guidelines.
    Evaluate the narrative flow, clarity of expression, and tone. Suggest improvements to 
    enhance storytelling, readability, and engagement.""",
    model="sonnet",
)
@fast.agent(
    name="grader",
    instruction="""Compile the feedback from the Proofreader, Fact Checker, and Style Enforcer
    into a structured report. Summarize key issues and categorize them by type. 
    Provide actionable recommendations for improving the story, 
    and give an overall grade based on the feedback.""",
)
@fast.parallel(
    fan_out=["proofreader", "fact_checker", "style_enforcer"],
    fan_in="grader",
    name="parallel",
)
async def main() -> None:
    async with fast.run() as agent:
        await agent.parallel.send(
            Prompt.user("Student short story submission", Path("short_story.txt"))
        )


if __name__ == "__main__":
    asyncio.run(main())  # type: ignore

--- END OF FILE workflows/parallel.py ---


--- START OF FILE workflows/router.py ---
"""
Example MCP Agent application showing router workflow with decorator syntax.
Demonstrates router's ability to either:
1. Use tools directly to handle requests
2. Delegate requests to specialized agents
"""

import asyncio

from mcp_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent(
    "Router Workflow",
)

# Sample requests demonstrating direct tool use vs agent delegation
SAMPLE_REQUESTS = [
    "Download and summarize https://llmindset.co.uk/posts/2024/12/mcp-build-notes/",  # Router handles directly with fetch
    "Analyze the quality of the Python codebase in the current working directory",  # Delegated to code expert
    "What are the key principles of effective beekeeping?",  # Delegated to general assistant
]


@fast.agent(
    name="fetcher",
    instruction="""You are an agent, with a tool enabling you to fetch URLs.""",
    servers=["fetch"],
)
@fast.agent(
    name="code_expert",
    instruction="""You are an expert in code analysis and software engineering.
    When asked about code, architecture, or development practices,
    you provide thorough and practical insights.""",
    servers=["filesystem"],
)
@fast.agent(
    name="general_assistant",
    instruction="""You are a knowledgeable assistant that provides clear,
    well-reasoned responses about general topics, concepts, and principles.""",
)
@fast.router(
    name="route",
    model="sonnet",
    agents=["code_expert", "general_assistant", "fetcher"],
)
async def main() -> None:
    async with fast.run() as agent:
        for request in SAMPLE_REQUESTS:
            await agent.route(request)


if __name__ == "__main__":
    asyncio.run(main())

--- END OF FILE workflows/router.py ---


--- START OF FILE workflows/short_story.md ---
The Kittens Castle Adventuer

One sunny day, three lil kittens name Whiskers, Socks, and Mittens was walkin threw a mystirus forrest. They hadnt never seen such a big forrest before! The trees was tall an spooky, an the ground was coverd in moss an stikks.

Suddenlee, thru the trees, they sawd somthing HUUUUGE! It was a castell, but not just eny castell. This castell was made of sparkling chese an glittery windos. The turrits was so high they tuch the clowds, an the doars was big enuff for a elefant to walk threw!

"Lookk!" sed Whiskers, his tale all poofy wit exsitement. "We fowned a castell!" Socks meowed loudly an jumped up an down. Mittens, who was the smallist kitten, just stared wit her big rond eyes.

They climed up the cheesy walls, slip-slidin on the smoth surfase. Inside, they discoverd rooms ful of soft pillows an dangling strings an shiny things that went JINGEL when they tuch them. It was like a kitten paradyse!

But then, a big shadowy figur apeared... was it the castell gaurd? Or sumthing mor mystirus? The kittens hudeld togethar, there lil hearts beating fast. What wud happan next in there amazeing adventuer?

THE END??
--- END OF FILE workflows/short_story.md ---


--- START OF FILE workflows/short_story.txt ---
The Battle of Glimmerwood

In the heart of Glimmerwood, a mystical forest knowed for its radiant trees, a small village thrived. 
The villagers, who were live peacefully, shared their home with the forest's magical creatures, 
especially the Glimmerfoxes whose fur shimmer like moonlight.

One fateful evening, the peace was shaterred when the infamous Dark Marauders attack. 
Lead by the cunning Captain Thorn, the bandits aim to steal the precious Glimmerstones which was believed to grant immortality.

Amidst the choas, a young girl named Elara stood her ground, she rallied the villagers and devised a clever plan.
Using the forests natural defenses they lured the marauders into a trap. 
As the bandits aproached the village square, a herd of Glimmerfoxes emerged, blinding them with their dazzling light, 
the villagers seized the opportunity to captured the invaders.

Elara's bravery was celebrated and she was hailed as the "Guardian of Glimmerwood". 
The Glimmerstones were secured in a hidden grove protected by an ancient spell.

However, not all was as it seemed. The Glimmerstones true power was never confirm, 
and whispers of a hidden agenda linger among the villagers.

--- END OF FILE workflows/short_story.txt ---



--- PROJECT PACKAGING COMPLETE ---