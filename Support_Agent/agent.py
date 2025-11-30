"""
Customer Support Agent - For Evaluation Testing Demonstration

This agent demonstrates testable patterns:
- Clear tool usage (easy to validate trajectory)
- Structured responses (easy to compare)
- Deterministic behavior (where possible)
"""
from google.adk.agents import Agent
from .tools import search_knowledge_base, create_ticket, ticket_status

# ============================================================================
# AGENT DEFINITION
# ============================================================================
root_agent = Agent(
    name = "support_agent",
    model = "gemini-2.0-flash",
    description="Customer support agent that can search knowledge base, create tickets, and check ticket status",
    instruction = 
    """
    You are a helpful customer support agent. Help customers by:

    1. First, try to answer their question using the knowledge base search tool
    2. If you can't find relevant information, create a support ticket
    3. If they mention a ticket ID, check its status

    Always be polite, clear, and provide specific next steps. Use the tools appropriately based on the customer's needs.""",

    tools = [search_knowledge_base, create_ticket, ticket_status],
    output_key = "last_support_response"
)