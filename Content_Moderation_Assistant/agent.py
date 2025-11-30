from google.adk.agents import Agent
from .tools import generate_text, check_grammer, get_usage_stats
from .callbacks import (before_agent_callback, after_agent_callback, 
                        before_model_callback, after_model_callback, 
                        before_tool_callback, after_tool_callback)


# ============================================================================
# AGENT DEFINITION
# ============================================================================

root_agent = Agent(
    name = "content_moderator",
    model = "gemini-2.0-flash",
    description = """
    Content moderation assistant with safety guardrails, validation, and monitoring.
    Demonstrates callback patterns for production-ready agents.
    """,
    instruction = 
    """
    You are a writing assistant that helps users create and refine content.

    CAPABILITIES:
    - Generate text on any topic with specified word count
    - Check grammar and suggest corrections
    - Provide usage statistics

    SAFETY:
    - You operate under strict content moderation policies
    - Inappropriate requests will be automatically blocked
    - All interactions are logged for quality assurance

    WORKFLOW:
    1. For generation requests, use generate_text with topic and word count
    2. For grammar checks, use check_grammar with the text
    3. For stats, use get_usage_stats

    Always be helpful, professional, and respectful.
    """,
    tools = [generate_text, check_grammer, get_usage_stats],

    # ============================================================================
    # CALLBACKS CONFIGURATION
    # ============================================================================
    before_agent_callback = before_agent_callback,
    after_agent_callback = after_agent_callback,

    before_model_callback = before_model_callback,
    after_model_callback = after_model_callback,
    
    before_tool_callback = before_tool_callback,
    after_tool_callback = after_tool_callback,
    # ============================================================================
    # OUTPUT KEY
    # ============================================================================
    output_key = "last_moderation_response"
)