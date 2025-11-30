from __future__ import annotations
from google.adk.agents import Agent
from dotenv import load_dotenv

# 1. Load environment variables (API keys)
load_dotenv()

# Define your agent Must be named root_agent
root_agent = Agent(
name = "Hello_Assistant", v       1ED`  12  `
    model = "gemini-2.0-flash",
    description = "A Friendly AI Assistant for general conversation",
    instruction = (
        "You are a warm and helpful assistant."
        "Greet users enthusiastically and ask and answer their questions clearly."
        "Be conversational and friendly!"
    )
)
    