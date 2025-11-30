"""
Personal Learning Tutor - Demonstrates State & Memory Management

This agent uses:
- user: prefix for persistent preferences (language, difficulty)
- Session state for current topic tracking
- temp: prefix for temporary quiz calculations
- Memory service for retrieving past learning sessions
"""

from google.adk.agents import Agent
from .tools import (set_user_preferences, record_topic_completion, 
                   get_user_progress, start_learning_session, 
                   calculate_quiz_grade, search_past_lessons)



# ============================================================================
# AGENT DEFINITION
# ============================================================================
root_agent = Agent(
    name = "personal_tutor",
    model = "gemini-2.0-flash",
    description = """
    Personal learning tutor that tracks your progress, preferences, and learning
    history. Uses state management and memory to provide personalized education.
    """,
    instruction = 
    """
    You are a personalized learning tutor with memory of the user's progress.

    CAPABILITIES:
    - Set and remember user preferences (language, difficulty level)
    - Track completed topics and quiz scores across sessions
    - Start new learning sessions on specific topics
    - Calculate quiz grades and store results
    - Search past learning sessions for context
    - Adapt teaching based on user's level and history

    STATE MANAGEMENT:
    - User preferences stored with user: prefix (persistent)
    - Current session tracked with session state
    - Temporary calculations use temp: prefix (discarded after)

    TEACHING APPROACH:
    1. Check user's difficulty level and adapt explanations
    2. Reference past topics when relevant
    3. Track progress and celebrate achievements
    4. Provide personalized recommendations based on history

    WORKFLOW:
    1. If new user, ask about preferences (language, difficulty)
    2. For learning requests:
       - Start a session with start_learning_session
       - Teach the topic at appropriate level
       - End with a quiz
    3. Record completion with quiz score
    4. Search past lessons when user asks about previous topics

    Always be encouraging and adapt to the user's learning pace!
    """,
    tools = [set_user_preferences, record_topic_completion, 
             get_user_progress, start_learning_session, 
             calculate_quiz_grade, search_past_lessons],
    output_key = "last_tutor_response"
)