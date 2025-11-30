"""
Tutorial 04: Sequential Workflows - Blog Creation Pipeline

This tutorial demonstrates how to chain multiple agents in a strict sequence
to create sophisticated pipelines. The blog creation pipeline consists of 4
agents that work together to research, write, edit, and format blog posts.
"""
from __future__ import annotations
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent

# 1. Load environment variables (API keys)
load_dotenv()

# ============================================================================
# AGENT DEFINITIONS
# ============================================================================

# ====== Agent 1: Research Agent ======
# Gather key facts about the topic
research_agent = Agent(
    name = "researcher",
    model = "gemini-2.0-flash",
    description = "Researches a topic and gather key facts and information",
    instruction = (
        "You are a research assistant. Your task is to gather key facts and information "
        "about the topic requested by the user.\n"
        "\n"
        "Output a bulleted list of 5-7 key facts or insights about the topic. "
        "Focus on interesting, specific information that would make a blog post engaging.\n"
        "\n"
        "Format:\n"
        "• Fact 1\n"
        "• Fact 2\n"
        "• etc.\n"
        "\n"
        "Output ONLY the bulleted list, nothing else."
    ),
    output_key = "research_findings" # Saves to state ['research_findings']
)

# ====== Agent 2: Writing Agent ======
# Write a blog post based on the research findings
writer_agent = Agent(
    name = "writer",
    model = "gemini-2.0-flash",
    description = "Writes a blog post based on the research findings",
    instruction = (
        "You are a creative blog writer. Write an engaging blog post based on "
        "the research findings below.\n"
        "\n"
        "**Research Findings:**\n"
        "{research_findings}\n"  # Reads from state!
        "\n"
        "Write a 3-4 paragraph blog post that:\n"
        "- Has an engaging introduction\n"
        "- Incorporates the key facts naturally\n"
        "- Has a conclusion that wraps up the topic\n"
        "- Uses a friendly, conversational tone\n"
        "\n"
        "Output ONLY the blog post text, no meta-commentary."
    ),
    output_key = "draft_post" # Savesto state ['draft_post']
)

# ====== Agent 3: Editing Agent ======
# Reviews the draft and suggests improvements
editior_agent = Agent(
    name = "editor",
    model = "gemini-2.0-flash",
    description = "Reviews the draft and suggests improvements",
    instruction = (
        "You are an experienced editor. Review the blog post draft below and provide "
        "constructive feedback.\n"
        "\n"
        "**Draft Blog Post:**\n"
        "{draft_post}\n"  # Reads from state!
        "\n"
        "Analyze the post for:\n"
        "1. Clarity and flow\n"
        "2. Grammar and style\n"
        "3. Engagement and reader interest\n"
        "4. Structure and organization\n"
        "\n"
        "Provide your feedback as a short list of specific improvements. "
        "If the post is excellent, simply say: 'No revisions needed - post is ready.'\n"
        "\n"
        "Output ONLY the feedback, nothing else."
    ),
    output_key = "editorial_feedback" # Saves to state ['editorial_feedback']
)

# ====== Agent 4: Formatting Agent ======
# Formats the blog post for publication
formatter_agent = Agent(
    name = "formatter",
    model = "gemini-2.0-flash",
    description = "Applies editorial feedback and formats the final blog post",
    instruction=(
        "You are a formatter. Create the final version of the blog post by applying "
        "the editorial feedback to improve the draft.\n"
        "\n"
        "**Original Draft:**\n"
        "{draft_post}\n"  # Reads from state!
        "\n"
        "**Editorial Feedback:**\n"
        "{editorial_feedback}\n"  # Reads from state!
        "\n"
        "Create the final blog post by:\n"
        "1. Applying the suggested improvements\n"
        "2. Formatting as proper markdown with:\n"
        "   - A compelling title (# heading)\n"
        "   - Section headings if appropriate (## subheadings)\n"
        "   - Proper paragraph breaks\n"
        "   - Bold/italic for emphasis where appropriate\n"
        "\n"
        "If feedback said 'No revisions needed', just format the original draft nicely.\n"
        "\n"
        "Output ONLY the final formatted blog post in markdown."
    ),
    output_key = "final_post" # Saves to state ['final_post']
)


# ====== Agent 5: Fact Checking Agent ======
# Fact checks the blog post for accuracy
fact_checker_agent = Agent(
    name = "fact_checker",
    model = "gemini-2.0-flash",
    instruction = "Verify facts in: {draft_post}",
    output_key = "fact_check_results" # Saves to state ['fact_check_results']
)

# ============================================================================
# SEQUENTIAL PIPELINE
# ============================================================================

# Create the sequential pipeline
blog_creation_pipeline = SequentialAgent(
    name = "BlogCreationPipeline",
    sub_agents = [
        research_agent,
        writer_agent,
        fact_checker_agent, # Insert before editor
        editior_agent,
        formatter_agent
    ], # Executes in this exact order!
    description = "Complete blog post creation pipeline from research to publication",
)

# Must be named root_agent for ADK discovery!
root_agent = blog_creation_pipeline