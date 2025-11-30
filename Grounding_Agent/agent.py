"""
Grounding Agent - Tutorial 11: Built-in Tools & Grounding

This agent demonstrates web grounding capabilities using Google Search
and other built-in ADK tools for accessing current information.
"""

import os
from google.genai import types
from typing import Any, Dict, List
from google.adk.agents import Agent
from google.adk.tools import google_search, google_maps_grounding, FunctionTool
from .tools import analyze_search_results, save_research_findings

# ============================================================================
# ENVIRONMENT DETECTION & TOOL CONFIGURATION
# ============================================================================

def is_vertexai_enabled() -> bool:
    """
    Check if VertexAI is enabled via environment variable.

    Returns:
        True if GOOGLE_GENAI_USE_VERTEXAI=1, False otherwise
    """
    return os.environ.get('GOOGLE_GENAI_USE_VERTEXAI', '0') == '1'

def get_available_grounding_tools() -> List[str]:
    """
    Get available grounding tools based on environment configuration.

    Returns:
        List of available grounding tools
    """
    tools = [google_search] # Always available
    if is_vertexai_enabled():
        tools.append(google_maps_grounding)

    return tools

def get_agent_capabilities_description() -> str:
    """
    Get description of agent capabilities based on available tools.

    Returns:
        String describing available capabilities
    """
    capabilities = ["web search for current information"]

    if is_vertexai_enabled():
        capabilities = ["web search for current information"]
    
    return " and".join(capabilities)


# ============================================================================
# GROUNDING AGENTS
# ============================================================================

# Basic grounding agent with dynamic tool selection
basic_grounding_agent = Agent(
    name = "basic_grounding_agent",
    model = "gemini-2.0-flash",
    description="Basic web grounding agent with conditional maps support",
    instruction=
    f"""You are a web research assistant with access to {get_agent_capabilities_description()}.

    When asked questions:
    1. Use google_search to find current, accurate information
    {"2. Use google_maps_grounding for location-based queries when available" if is_vertexai_enabled() else ""}
    {("3. " if is_vertexai_enabled() else "2. ")}Provide clear, factual answers based on search results
    {("4. " if is_vertexai_enabled() else "3. ")}Always cite that information comes from web search
    {("5. " if is_vertexai_enabled() else "4. ")}If information seems outdated or uncertain, mention this

    Be helpful, accurate, and indicate when you're using search capabilities.""",
    tools=get_available_grounding_tools(),
    output_key="grounding_response"
)

# Advanced grounding agent - demonstrates pattern for future tool mixing
advance_ground_agent = Agent(
    name = "advance_grounding_agent",
    model = "gemini-2.0-flash",
    description="Advanced grounding agent with search, analysis, and conditional maps tools",
    instruction = 
    f"""You are an advanced research assistant with {get_agent_capabilities_description()} and analysis capabilities.

        For research tasks:
        1. Use google_search to find current information
        {"2. Use google_maps_grounding for location-based research when available" if is_vertexai_enabled() else ""}
        {("3. " if is_vertexai_enabled() else "2. ")}Use analyze_search_results to process and summarize findings
        {("4. " if is_vertexai_enabled() else "3. ")}Use save_research_findings to preserve important research
        {("5. " if is_vertexai_enabled() else "4. ")}Provide a comprehensive summary

        Always be thorough, cite your sources, and explain your process.""",
    tools = get_available_grounding_tools() + [FunctionTool(analyze_search_results),
                                               FunctionTool(save_research_findings)], # Custom tools    
    output_key = "advanced_grounding_response"
)

# Research agent - focuses on analysis capabilities
# Demonstrates custom tools that work with grounding tools
research_assistant = Agent(
    name = "research_assistant",
    model = "gemini-2.0-flash",
    description="Research assistant with analysis, documentation, and conditional maps tools",
    instruction=
    f"""You are a research assistant specializing in analyzing and documenting information.

    Your capabilities:
    - **Web Research**: Access to {get_agent_capabilities_description()}
    - **Analysis**: Use analyze_search_results to process and analyze content
    - **Documentation**: Use save_research_findings to preserve research
    {"- **Location Research**: Use google_maps_grounding for geographic queries when available" if is_vertexai_enabled() else ""}

    Research Process:
    1. {"Use google_search and google_maps_grounding to gather information when available, otherwise " if is_vertexai_enabled() else ""}Analyze provided information using analyze_search_results
    2. Synthesize findings into clear, actionable insights
    3. Docume
    nt important research using save_research_findings

    Guidelines:
    - Be objective and factual in your analysis
    - Provide timestamps for time-sensitive information
    - Save significant findings for future reference

    Note: Full web search integration available when VertexAI is enabled.""",
    tools = get_available_grounding_tools() + [FunctionTool(analyze_search_results),
                                               FunctionTool(save_research_findings)], # Custom tools    
    generate_content_config = types.GenerateContentConfig(
        temperature = 0.7,
        max_output_tokens = 2048
    ),
    output_key = "research_response"
)

# Default agent (used by ADK web interface)
# Use Advanced agent if VertexAI is enabled (includes maps grounding), otherwise basic agent
root_agent = advance_ground_agent if is_vertexai_enabled() else basic_grounding_agent