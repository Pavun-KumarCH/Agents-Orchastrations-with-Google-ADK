"""
Strategic Problem Solver - Tutorial 12: Planners & Thinking Configuration

This agent demonstrates advanced reasoning capabilities using:
- BuiltInPlanner with extended thinking
- PlanReActPlanner for structured reasoning
- Custom BasePlanner for domain-specific workflows

The agent solves complex business problems using market analysis, ROI calculations,
risk assessment, and strategic planning tools.
"""


# ============================================================================
# AGENT IMPLEMENTATIONS
# ============================================================================
from google.genai import types
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.planners import BuiltInPlanner, PlanReActPlanner
from google.genai.types import GenerateContentConfig

from .strategicplanner import StrategicPlanner
from .bussiness_analysis_tools import analyze_market, calculate_roi, assess_risk, save_strategy_report

# BuiltInPlanner Agent - Uses Gemini's native thinking capabilities
builtin_planner_agent = Agent(
    name="builtin_planner_strategic_solver",
    model="gemini-2.0-flash",
    description="Strategic business consultant using BuiltInPlanner with transparent thinking",
    instruction="""You are an expert strategic consultant who thinks deeply before providing recommendations.

When solving business problems:
1. Use analyze_market to understand industry conditions
2. Use calculate_roi for financial analysis
3. Use assess_risk to evaluate potential threats
4. Use save_strategy_report to document your final recommendations

Think step-by-step about market opportunities, financial implications, and risk factors.
Provide data-driven recommendations with clear reasoning.
Always show your analytical process and assumptions.""",
    tools=[
        FunctionTool(analyze_market),
        FunctionTool(calculate_roi),
        FunctionTool(assess_risk),
        FunctionTool(save_strategy_report)
    ],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(include_thoughts=True)
    ),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3,  # Lower temperature for strategic thinking
        max_output_tokens=3000
    ),
    output_key="builtin_strategy_result"
)

# PlanReActPlanner Agent - Uses structured Plan → Reason → Act → Observe → Replan
plan_react_agent = Agent(
    name="plan_react_strategic_solver",
    model="gemini-2.0-flash",
    description="Strategic business consultant using PlanReActPlanner for structured reasoning",
    instruction="""You are a systematic strategic consultant who follows a structured problem-solving approach.

When analyzing business problems:
1. PLAN your analysis approach using available tools
2. REASON about market conditions, financials, and risks
3. ACT by using tools to gather specific data
4. OBSERVE results and adjust your understanding
5. REPLAN if your initial approach needs modification

Always use the structured format with planning tags.
Be thorough and methodical in your analysis.""",
    tools=[
        FunctionTool(analyze_market),
        FunctionTool(calculate_roi),
        FunctionTool(assess_risk),
        FunctionTool(save_strategy_report)
    ],
    planner=PlanReActPlanner(),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.4,
        max_output_tokens=3000
    ),
    output_key="plan_react_strategy_result"
)

# Custom StrategicPlanner Agent - Domain-specific business strategy worflow
strategic_planner_agent = Agent(
    name = "strategic_planner_solver",
    model = "gemini-2.0-flash",
    description = "Strategic business consultant using custom StrategicPlanner for domain-specific analysis",
    instruction = 
    """You are a specialized business strategy consultant following a proven methodology.

    Use the structured strategic planning framework:
    - ANALYSIS: Gather market, financial, and risk data
    - EVALUATION: Analyze opportunities and threats
    - STRATEGY: Develop comprehensive recommendations
    - VALIDATION: Review and refine your approach

    Leverage all available tools to build data-driven strategies.
    Focus on actionable recommendations with clear implementation steps.""",
    tools = [
        FunctionTool(analyze_market),
        FunctionTool(calculate_roi),
        FunctionTool(assess_risk),
        FunctionTool(save_strategy_report)
    ],
    planner = StrategicPlanner(),
    generate_content_config = types.GenerateContentConfig(
        temperature = 0.3,
        max_output_tokens = 3000
    ),
    output_key = "strategic_planner_result"
)


# Default agent - showcases all planner types
# Uses PlanReActPlanner as default for most structured business problems
root_agent = plan_react_agent


# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

async def demo_strategic_planning():
    """Demonstrate strategic planning with different planner types."""

    from google.adk.runners import InMemoryRunner

    problems = [
        "Should we expand into the Asian healthcare market?",
        "Is this $2M investment in AI technology worth the risk?",
        "How should we mitigate cybersecurity threats in our fintech startup?"
    ]

    agents = [
        ("BuiltInPlanner", builtin_planner_agent),
        ("PlanReActPlanner", plan_react_agent),
        ("StrategicPlanner", strategic_planner_agent)
    ]

    for problem in problems:
        print(f"\n{'='*80}")
        print(f"PROBLEM: {problem}")
        print(f"{'='*80}")

        for agent_name, agent in agents:
            print(f"\n--- {agent_name} Analysis ---")

            try:
                runner = InMemoryRunner(agent=agent, app_name=f"strategic_solver_{agent_name.lower()}")
                events = []
                async for event in runner.run_async(
                    user_id="demo_user",
                    session_id=f"demo_session_{agent_name.lower()}",
                    new_message={"role": "user", "parts": [{"text": problem}]}
                ):
                    events.append(event)
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                print(part.text[:500] + "..." if len(part.text) > 500 else part.text)
                                break  # Only print first part
            except Exception as e:
                print(f"Error with {agent_name}: {e}")

        print(f"\n{'='*80}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_strategic_planning())