import os
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "search-prompt.txt")
with open(instruction_file_path, "r") as f:
    instruction = f.read()

# Model choice: gemini-3.8-flash provides fast, low-latency responses for web
# search grounding and is the active Gemini Flash model available in this lab's
# Vertex AI global endpoint (older 2.0/2.5 aliases returned 404 NOT_FOUND).
search_agent = Agent(
    name="search_agent",
    model="gemini-3.8-flash",
    description="Searches the web using Google Search for external bird care info and current trends.",
    instruction=instruction,
    tools=[google_search],
)

search_agent_tool = AgentTool(agent=search_agent)
