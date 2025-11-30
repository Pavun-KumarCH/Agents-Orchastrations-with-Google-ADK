from google.adk.agents import Agent
from tools.tools import (
    calculate_compound_interest,
    calculate_loan_payment,
    calculate_monthly_savings
)

# Create the finance assistant agent

root_agent = Agent(
    name = "finance_assistant",
    model = "gemini-2.0-flash",
    description = """A financial calculation assistant that can help with:
    - Compound interest calculations for investments
    - Loan payment calculations for mortgages or other loans
    - Monthly savings calculations to reach financial goals

    I can perform multiple calculations simultaneously for comparison purposes.
    All calculations include detailed explanations and formatted reports.
    """,
    tools = [
        calculate_compound_interest,
        calculate_loan_payment,
        calculate_monthly_savings
    ]
)