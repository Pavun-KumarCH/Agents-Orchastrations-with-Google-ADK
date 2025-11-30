
# ============================================================================
# CUSTOM TOOLS
# ============================================================================
from datetime import datetime
from typing import Dict, Any
from google.adk.tools.tool_context import ToolContext

def analyze_search_results(query: str, search_context: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Analyze search results and extract key insights.

    Args:
        query: The original search query
        search_content: The search results content
        tool_context: ADK tool context

    Returns:
        Dict with analysis results
    """
    try:
        # Simple analysis - count words and extract key phrase
        word_count = len(search_context.split())
        sentences = search_context.split('.')

        # Extract what appers to be key information
        key_insights = []
        for sentence in sentences[:5]: # First 5 sentences
            sentence = sentence.strip()
            if len(sentence) > 20: # Meaningful sentences only
                key_insights.append(sentence)

        analysis = {
            'query': query,
            'word_count': word_count,
            'key-insights': key_insights,
            'content_quality': 'good' if word_count > 50 else 'limited',
            'timestamp': datetime.now().isoformat()
        }
        return {
            'status': 'success',
            'analysis': analysis,
            'report': f'Analyzed {word_count} words from search results for "{query}". Found {len(key_insights)} key insights.',
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to analyze search results for "{query}": {str(e)}'
        }

def save_research_findings(topic: str, findings: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Save research findings as an artifact.

    Args:
        topic: Research topic
        findings: Research findings to save
        tool_context: ADK tool context

    Returns:
        Dict with save results
    """
    try:
        # Save as artifact
        filename = f"research_{topic.replace(' ','_').lower()}.md"

        # Note: In a real implementation, this would save to artifact service
        # For demo purposes, we'll just return success
        version = "1.0"

        return {
            'status': 'success',
            'report': f'Research findings saved as {filename} (version {version})',
            'filename': filename,
            'version': version
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to save research findings: {str(e)}'
        }