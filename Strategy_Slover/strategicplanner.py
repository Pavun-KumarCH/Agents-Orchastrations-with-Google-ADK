
# ============================================================================
# CUSTOM PLANNER IMPLEMENTATION
# ============================================================================

from google.genai import types
from google.adk.planners import BasePlanner
from typing import Any, Dict, List, Optional
from google.adk.models.llm_request import LlmRequest
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.agents.callback_context import CallbackContext


class StrategicPlanner(BasePlanner):
    """
    Custom planner for strategic business problem solving.

    This planner implements a domain-specific workflow for business strategy:
    1. ANALYSIS: Gather market, financial, and risk data
    2. EVALUATION: Assess opportunities and threats
    3. STRATEGY: Develop comprehensive recommendations
    4. VALIDATION: Review and refine the strategy
    """

    def build_planning_instruction(self, readonly_context: ReadonlyContext, llm_request: LlmRequest) -> Optional[str]:
             """Build strategic planning instruction."""
             return """
                You are a strategic business consultant using a systematic approach to solve complex problems.

                Follow this structured methodology:

                <ANALYSIS>
                Gather comprehensive data about the business problem:
                - Market conditions and trends
                - Financial implications and ROI
                - Risk factors and mitigation strategies
                - Stakeholder impacts and requirements
                Use available tools to collect objective data.

                <EVALUATION>
                Analyze the collected data:
                - Identify key opportunities and threats
                - Evaluate financial viability
                - Assess risk levels and mitigation needs
                - Consider strategic implications

                <STRATEGY>
                Develop a comprehensive business strategy:
                - Define clear objectives and goals
                - Outline specific action steps
                - Address identified risks
                - Include success metrics and timelines

                <VALIDATION>
                Review and validate the strategy:
                - Ensure all aspects of the problem are addressed
                - Verify financial and risk assumptions
                - Confirm stakeholder alignment
                - Identify potential implementation challenges

                <FINAL_RECOMMENDATION>
                Provide a complete strategic recommendation with:
                - Executive summary
                - Detailed implementation plan
                - Risk mitigation strategies
                - Success metrics and monitoring approach

                Always use available tools to gather data before making recommendations.
                Be data-driven and objective in your analysis.
                """

    def process_planning_response(self, callback_contet: CallbackContext, response_parts: List[types.Part]) -> Optional[List[types.Part]]:
        """Process strategic planning response."""
        # For this custom planner, we don't modify the response parts
        # but could add metadata or validation here if needed
        return response_parts
