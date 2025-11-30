"""
Content Moderation Assistant - Demonstrates Callbacks & Guardrails

This agent uses callbacks for:
- Guardrails: Block inappropriate content (before_model_callback)
- Validation: Check tool arguments (before_tool_callback)
- Logging: Track all operations (multiple callbacks)
- Modification: Add safety instructions (before_model_callback)
- Filtering: Remove PII from responses (after_model_callback)
- Metrics: Track usage statistics (state management)
"""

import re, logging
from google.genai import types
from typing import Dict, Any, Optional
from google.adk.models.llm_response import LlmResponse
from google.adk.agents.callback_context import CallbackContext

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# BLOCKLIST CONFIGURATION
# ============================================================================

# Simplified blocklist for demonstration
BLOCKED_WORDS = [
    "profanity1", "profanity2", "hate-speech",  # Replace with real terms
    "offensive-term", "inappropriate-word"
]

# PII patterns to filter
PII_PATTERNS = {
    'email':  r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
    'snn': r'\b\d{3}-\d{2}-\d{4}\b',
    'credit_card': r'\b\d{4}[-.]?\d{4}[-.]?\d{4}[-.]?\d{4}\b'
}

# ============================================================================
# CALLBACK FUNCTIONS
# ============================================================================

def before_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Called before agent starts processing a request.

    Use Case: Check if agent should even handle this request.

    Returns:
        None: Allow agent to proceed
        Content: Skip agent execution, use returned content as response
    """
    logger.info(f"[AGENT START] Session: {callback_context.invocation_id}")

    # Check if agent is in maintenance mode (app state)
    if callback_context.state.get('app:maintenance_mode', False):
        logging.warning("[AGENT BLOCKED] Maintance mode activate")
        return types.Content(
            parts = [types.Part(text =
            "System is currently under maintenance. Please try again later.")],
            role = "model"
        )

    # Increment request counter
    count = callback_context.state.get('user:request_count', 0)
    callback_context.state['user:request_count'] = count + 1
    return None # Allow agent to proceed

def after_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Called after agent completes processing.

    Use Case: Post-process or validate final output.

    Returns:
        None: Use agent's original output
        Content: Replace agent's output with this
    """
    logger.info(f"[AGENT COMPLETED] Session: {callback_context.invocation_id}")

    # Track successful completions
    callback_context.state['temp:agent_completed'] = True

    # Could add standard disclaimer here
    # return types.Content(
    #     parts=[types.Part(text="\n\n[This is AI-generated content]")]
    # )

    return None # Use original output

def before_model_callback(
    callback_context: CallbackContext,
    llm_request: types._GenerateContentParameters
) -> Optional[types.GenerateContentResponse]:
    """
    Called before sending request to LLM.

    Use Cases:
    1. Guardrails: Block inappropriate requests
    2. Modification: Add safety instructions
    3. Caching: Return cached responses
    4. Logging: Track LLM usage

    Returns:
        None: Allow LLM call to proceed
        LlmResponse: Skip LLM call, use this response instead
    """
    # Extract user input
    user_text = ""
    for content in llm_request.contents:
        for part in content.parts:
            if part.text:
                user_text += part.text

    logger.info(f"[LLM REQUEST] Length: {len(user_text)} chars")

    # GUARDRAIL: Check for blocked words
    for word in BLOCKED_WORDS:
        if word.lower() in user_text.lower():
            logger.warning(f"[LLM BLOCKED] Found blocked word: {word}")

            # Track blocked requests
            blocked_count = callback_context.state.get('user:blocked_requests', 0)
            callback_context.state['user:blocked_requests'] = blocked_count + 1

            # Return error response (skip LLM call)
            return types.GenerateContentResponse(
                candidates=[
                    types.Candidate(
                        content=types.Content(
                            parts=[types.Part(
                                text="I cannot process this request as it contains inappropriate content. Please rephrase respectfully."
                            )],
                            role="model"
                        )
                    )
                ]
            )

    # MODIFICATION: Add safety instruction
    safety_instruction = "\n\nIMPORTANT: Do not generate harmful, biased, or inappropriate content. If the request is unclear, ask for clarification."

    # Modify system instruction
    if llm_request.config and llm_request.config.system_instruction:
        llm_request.config.system_instruction += safety_instruction

    # Track LLM calls
    llm_count = callback_context.state.get('user:llm_calls', 0)
    callback_context.state['user:llm_calls'] = llm_count + 1

    return None  # Allow LLM call with modifications


def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    """
    Called after receiving response from LLM.

    Use Cases:
    1. Filtering: Remove PII or sensitive data
    2. Formatting: Standardize output format
    3. Logging: Track response quality

    Returns:
        None: Use original LLM response
        LlmResponse: Replace with modified response
    """
    # Extract response text
    response_text = ""
    if llm_response.content and llm_response.content.parts:
        for part in llm_response.content.parts:
            if part.text:
                response_text += part.text

    logger.info(f"[LLM RESPONSE] Length: {len(response_text)} chars")

    # FILTERIONG: Remove PII patterns
    filtered_text = response_text
    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, filtered_text)
        if matches:
            logger.warning(f"[FILTERED] Found {len(matches)} {pii_type} instances")
            filtered_text = re.sub(pattern, f'[{pii_type.upper()}_REDACTED]', filtered_text)
    
    # If we filtered anything, return modified response
    if filtered_text != response_text:
        # Create modified content
        modified_content = types.Content(
            parts=[types.Part(text=filtered_text)],
            role=llm_response.content.role if llm_response.content else "model"
        )
        
        # Return modified LlmResponse
        return llm_response.model_copy(update={"content": modified_content})

    return None  # Use original response

def before_tool_callback(
    callback_context: CallbackContext,
    tool_name: str,
    args: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Called before executing a tool.

    Use Cases:
    1. Validation: Check arguments are valid
    2. Authorization: Check user permissions
    3. Rate limiting: Enforce usage limits
    4. Logging: Track tool usage

    Returns:
        None: Allow tool execution
        dict: Skip tool execution, use this result instead
    """
    logger.info(f"[TOOL CALL] {tool_name} with args: {args}")

    # VALIDATION: Check for negative values in generate_text
    if tool_name == 'generate_text':
        word_count = args.get('word_count', 0)
        if word_count <= 0 or word_count > 5000:
            logger.warning(f"[TOOL BLOCKED] Invalid word_count: {word_count}")
            return {
                'status': 'error',
                'message': f'Invalid word_count: {word_count}. Must be between 1 and 5000.'
            }

    # RATE LIMITING: Check tool usage quota
    tool_count = callback_context.state.get(f'user:tool_{tool_name}_count', 0)
    if tool_count >= 100:  # Example limit
        logger.warning(f"[TOOL BLOCKED] Rate limit exceeded for {tool_name}")
        return {
            'status': 'error',
            'message': f'Rate limit exceeded for {tool_name}. Please try again later.'
        }

    # Track tool usage
    callback_context.state[f'user:tool_{tool_name}_count'] = tool_count + 1
    callback_context.state['temp:last_tool'] = tool_name

    return None  # Allow tool execution


def after_tool_callback(
    callback_context: CallbackContext,
    tool_name: str,
    tool_response: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Called after tool execution completes.

    Use Cases:
    1. Logging: Record results
    2. Transformation: Standardize output format
    3. Caching: Store results for future use

    Returns:
        None: Use original tool result
        dict: Replace with modified result
    """
    logger.info(f"[TOOL RESULT] {tool_name}: {tool_response.get('status', 'unknown')}")

    # Store last tool result for debugging
    callback_context.state['temp:last_tool_result'] = str(tool_response)

    # Could standardize all tool responses here
    # if 'status' not in tool_response:
    #     tool_response['status'] = 'success'

    return None  # Use original result
