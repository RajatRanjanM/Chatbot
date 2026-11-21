import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from toolbox_core import ToolboxSyncClient

from .datastore import search_betty_docs
from .search_agent import search_agent_tool

load_dotenv()

# Configure short-term session storage using InMemorySessionService
session_service = InMemorySessionService()

# Load root agent instructions from agent-prompt.txt
script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

# Connect to MCP Toolbox server and load the product pricing SQL tool
toolbox_url = os.environ.get("TOOLBOX_URL", "http://127.0.0.1:5000")
db_client = ToolboxSyncClient(toolbox_url)
search_products_tool = db_client.load_tool("search-products-by-name")

tools = [
    search_products_tool,
    search_betty_docs,
    search_agent_tool,
]

# Model choice: gemini-3.8-flash balances low latency with strong multi-tool
# orchestration across MCP Toolbox, Vertex AI Search, and Google Search, and is
# the supported Gemini Flash model in this Vertex AI project's global endpoint.
root_agent = Agent(
    name="betty_root_agent",
    model="gemini-3.8-flash",
    description="Customer service agent for Betty's Bird Boutique.",
    instruction=instruction,
    tools=tools,
)
