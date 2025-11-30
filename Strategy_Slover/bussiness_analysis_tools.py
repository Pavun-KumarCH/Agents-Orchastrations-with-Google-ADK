# ============================================================================
# BUSINESS ANALYSIS TOOLS
# ============================================================================

from datetime import datetime
from typing import Dict, Any, List
from google.adk.tools.tool_context import ToolContext

def analyze_market(industry: str, region: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Analyze market conditions for strategic planning.

    Args:
        industry: The industry sector to analyze
        region: Geographic region for analysis
        tool_context: ADK tool context

    Returns:
        Dict with market analysis results
    """
    try:
        # Simulate market analysis (in production, this would call real APIs)
        # Using deterministic data for demo purpose
        market_data = {
                'healthcare': {
                    'growth_rate': '8.5%',
                    'competition': 'High',
                    'trends': ['Digital transformation', 'AI adoption', 'Telemedicine'],
                    'opportunities': ['Emerging markets', 'Specialized AI solutions'],
                    'threats': ['Regulatory changes', 'Data privacy concerns']
                },
                'finance': {
                    'growth_rate': '6.2%',
                    'competition': 'Very High',
                    'trends': ['FinTech innovation', 'Blockchain', 'Open banking'],
                    'opportunities': ['AI-driven insights', 'Personalized services'],
                    'threats': ['Cybersecurity risks', 'Regulatory compliance']
                },
                'retail': {
                    'growth_rate': '4.1%',
                    'competition': 'High',
                    'trends': ['E-commerce growth', 'Omnichannel retail', 'Sustainability'],
                    'opportunities': ['Direct-to-consumer models', 'Personalization'],
                    'threats': ['Supply chain disruptions', 'Economic uncertainty']
                }
            }
        # Default data for unknown industries
        if industry.lower() not in market_data:
            analysis = {
                'industry': industry,
                'region': region,
                'growth_rate': '5.0%',
                'competition': 'Medium',
                'trends': ['Digital transformation', 'Innovation'],
                'opportunities': ['Market expansion', 'Technology adoption'],
                'threats': ['Competition', 'Economic factors']
            }
        else:
            analysis = market_data[industry.lower()]
            analysis.update({
                'industry': industry,
                'region': region
            })
        analysis['timestamp'] = datetime.now().isoformat()
        return {
            'status': 'success',
            'analysis': analysis,
            'report': f'Analyzed market for {industry} in {region}. Growth rate: {analysis["growth_rate"]}, Competition: {analysis["competition"]}',
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to analyze market for {industry} in {region}: {str(e)}'
        }
    
def calculate_roi(investment: float, annual_return: float, years: int, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Calculate return on investment for financial planning.

    Args:
        investment: Initial investment amount
        annual_return: Expected annual return rate (percentage)
        years: Investment time horizon
        tool_context: ADK tool context

    Returns:
        Dict with ROI calculation results
    """
    try:
        # validate inputs
        if investment <= 0:
            raise ValueError("Investment amount must be positive")
        if annual_return < -100:
            raise ValueError("Annual return cannot be less than -100%")
        if years <= 0:
            raise ValueError("Investment period must be positive")

        # Calculate compound growth
        annual_rate = annual_return / 100
        total_return = investment * ((1 + annual_rate) ** years)
        profit = total_return - investment
        roi_percentage = (profit / investment) * 100

        # Calculate annual growth details
        annual_growth = []
        for year in range(1, years  + 1):
            year_end_value = investment * ((1 + annual_rate) ** year)
            year_profit = year_end_value - investment
            annual_growth.append({
                'year': year,
                'value': round(year_end_value, 2),
                'profit': round(year_profit,  2),
                'roi': round((year_profit / investment) * 100, 2)
            })
            result = {
                        'initial_investment': investment,
                        'annual_return_rate': f"{annual_return}%",
                        'years': years,
                        'final_value': round(total_return, 2),
                        'total_profit': round(profit, 2),
                        'roi_percentage': round(roi_percentage, 2),
                        'annual_breakdown': annual_growth,
                        'timestamp': datetime.now().isoformat()
                    }

        return {
            'status': 'success',
            'result': result,
            'report': f'Calculated ROI for investment of ${investment:,.2f} at {annual_return}% annual return over {years} years. Final value: ${total_return:,.2f}, Profit: ${profit:,.2f}, ROI: {roi_percentage:.1f}%',
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to calculate ROI: {str(e)}'
        }
    
def assess_risk(factors: List[str], tool_context: ToolContext) -> Dict[str, Any]:
    """
    Assess business risks based on provided factors.

    Args:
        factors: List of risk factors to evaluate
        tool_context: ADK tool context

    Returns:
        Dict with risk assessment results
    """
    try:
        # Risk scoring ssytem (higher = more risky)
        risk_scores = {
            'market_volatility': 7,
            'regulatory_changes': 6,
            'competition': 8,
            'technology_disruption': 7,
            'economic_uncertainty': 6,
            'supply_chain_issues': 5,
            'cybersecurity_threats': 8,
            'talent_shortage': 4,
            'geopolitical_risks': 6,
            'climate_change': 5,
            'pandemic_risks': 7,
            'currency_fluctuation': 5,
            'interest_rate_changes': 4,
            'customer_behavior': 6,
            'vendor_reliability': 5
        }

        # Calculate risk scores
        assessed_factors = {}
        total_score = 0

        for factor in factors:
            # Find closest matching factor
            factor_lower = factor.lower().replace(' ',"_")
            score = 5 # Default medium risk

            for risk_factor, risk_score in risk_scores.items():
                if risk_factor in factor_lower or factor_lower in risk_factor:
                    score = risk_score
                    break
            
            assessed_factors[factor] = score
            total_score += score

        # Calculate overall risk level
        avg_score = total_score / len(factors) if factors else 5

        if avg_score >= 7:
            risk_level = 'High'
            mitigation_priority = 'Critical'
        elif avg_score >= 5:
            risk_level = 'Medium'
            mitigation_priority = 'Important'
        else:
            risk_level = 'Low'
            mitigation_priority = 'Monitor'

        # Generate mitigation suggestions
        mitigation_suggestions = []
        for factor, score in assessed_factors.items():
            if score >= 7:
                mitigation_suggestions.append(f"Immediate action needed for: {factor}")
            elif score >= 5:
                mitigation_suggestions.append(f"Develop contingency plan for: {factor}")

        assessment = {
            'factors_assessed': factors,
            'factor_scores': assessed_factors,
            'total_score': total_score,
            'average_score': round(avg_score, 2),
            'risk_level': risk_level,
            'mitigation_priority': mitigation_priority,
            'mitigation_suggestions': mitigation_suggestions[:5],  # Top 5
            'timestamp': datetime.now().isoformat()
        }

        return {
            'status': 'success',
            'report': f'Risk assessment complete: {risk_level} risk level (avg: {avg_score:.1f}/10)',
            'assessment': assessment
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to assess risk: {str(e)}'
        }

async def save_strategy_report(
    problem: str,
    strategy: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Save strategic plan as an artifact.

    Args:
        problem: The business problem being solved
        strategy: The recommended strategy
        tool_context: ADK tool context

    Returns:
        Dict with save operation results
    """
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create markdown report
        report_content = f"""# Strategic Business Plan
Generated: {timestamp}

## Problem Statement
{problem}

## Recommended Strategy
{strategy}

## Analysis Tools Used
- Market Analysis
- ROI Calculations
- Risk Assessment

## Generated By
- Agent: Strategic Problem Solver
- Framework: Google ADK
- Model: Gemini 2.0 Flash
- Planners: BuiltInPlanner, PlanReActPlanner, StrategicPlanner
"""

        # In a real implementation, this would save to artifact service
        # For demo purposes, we'll simulate saving
        filename = f"strategy_{problem[:30].replace(' ', '_').replace('/', '_')}.md"

        # Store in tool context for demo purposes
        if not hasattr(tool_context, 'saved_reports'):
            tool_context.saved_reports = []

        tool_context.saved_reports.append({
            'filename': filename,
            'content': report_content,
            'timestamp': timestamp
        })

        return {
            'status': 'success',
            'report': f'Strategy saved as {filename}',
            'filename': filename,
            'content_length': len(report_content),
            'timestamp': timestamp
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to save strategy report: {str(e)}'
        }