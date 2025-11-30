from typing import Dict, Any
from google.adk.tools.tool_context import ToolContext

# ============================================================================
# TOOLS: State Management & Memory Operations
# ============================================================================

def set_user_preferences(language: str, difficulty_level: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Set user learning preferences (stored persistently).

    Args:
        language: Preferred language (en, es, fr, etc.)
        difficulty_level: beginner, intermediate, or advanced
    """
    tool_context.state['user:language'] = language
    tool_context.state['user:difficulty_level'] = difficulty_level

    return {
        'status': "success",
        'message': f'Preferences saved: {language} {difficulty_level} level'
    }

def record_topic_completion(topic: str, quiz_score: int, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Record that user completed a topic (stored persistently).

    Args:
        topic: Topic name (e.g., "Python Basics", "Data Structures")
        quiz_score: Score out of 100
    """
    # Get existing lists or create new ones
    topics = tool_context.state.get('user:topic_covered', [])
    scores = tool_context.state.get('user:quiz_scores', {})

    # Update persistent user state
    if topic not in topics:
        topics.append(topic)
    scores[topic] = quiz_score

    tool_context.state['user:topics_covered'] = topics
    tool_context.state['user:quiz_scores'] = scores

    return {
        'status': 'success',
        'topics_count': len(topics),
        'messsage': f'Recorded: {topic} with score {quiz_score}/100'        
    }

def get_user_progress(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Get user's learning progress summary.

    Returns persistent user data across all sessions.
    """
    # Read persistent user state
    language = tool_context.state.get('user: language', 'en')
    difficulty = tool_context.state.get('user.difficulty_level', 'beginner')
    topics = tool_context.state.get('user:topics_covered', [])
    scores = tool_context.state.get('user:quiz_scores', {})

    # Calculate average score
    avg_score = sum(scores.values()) / len(scores) if scores else 0
    
    return {
        'status': 'success',
        'language': language,
        'difficulty_level': difficulty,
        'topics_completed': len(topics),
        'topics': topics,
        'average_quiz_score': round(avg_score, 1),
        'all_scores': scores
    }

def start_learning_session(topic: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Start a new learning session for a topic.

    Uses session state (no prefix) to track current topic.
    """
    # Session-level state (persists within this session only)
    tool_context.state['current_topic'] = topic
    tool_context.state['session_start_time'] = 'now'
    
    # Get user's difficulty level for personalization
    difficulty = tool_context.state.get('user:difficulty_level', 'begginer')

    return {
        'status': 'success',
        'topic': topic,
        'difficulty_level': difficulty,
        'message': f'Started learning session: {topic} at {difficulty} level'
    }

def calculate_quiz_grade(correct_answers: int, total_questions: int, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Calculate quiz grade using temporary state.

    Demonstrates temp: prefix for invocation-scoped data.
    """
    # Store intermediate calculation in temp state (discarded after invocation)
    percentage = (correct_answers / total_questions) * 100
    tool_context.state['temp:raw_score'] = correct_answers
    tool_context.state['temp:quiz_percentage'] = percentage

    # Determine grade letter
    if percentage >= 90:
        grade = 'A'
    elif percentage >= 80:
        grade = 'B'
    elif percentage >= 70:
        grade = 'C'
    elif percentage >=60:
        grade = 'D'
    else:
        grade = 'F'
    
    return {
        'status': 'success',
        'score': f"{correct_answers}/{total_questions}",
        'percentage': round(percentage, 1),
        'grade': grade,
        'message': f'Quiz grade: {grade} ({percentage:.1f}%)'
    }

def search_past_lessons(query: str, tool_context: ToolContext) -> Dict[str, Any]:
    """
    Search memory for relevant past learning sessions.

    This demonstrates memory service integration.
    In production, this would use MemoryService.search_memory().
    """
    # NOTE: This is a simplified simulation
    # Real implementation would use:
    # memory_service = tool_context.memory_service
    # results = await memory_service.search_memory(
    #     app_name=tool_context.app_name,
    #     user_id=tool_context.user_id,
    #     query=query
    # )

    # Simulated memory search results
    topics = tool_context.state.get('user:topics_covered', [])
    relevant = [t for t in topics if query.lower() in t.lower()]

    if relevant:
        return {
            'status': 'success',
            'found': True,
            'relevant_topics': relevant,
            'message': f'Found {len(relevant)} past sessions related to "{query}'
        }
    else:
        return {
            'status': 'success',
            'found': False,
            'message': f'No Past sessions found for "{query}"'
        }

# ============================================================================