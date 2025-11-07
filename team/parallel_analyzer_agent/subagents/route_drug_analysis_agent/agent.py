"""
CPU Information Agent

This agent is responsible for gathering and analyzing CPU information.
"""

from google.adk.agents import LlmAgent

# from .tools import get_cpu_info

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Route Analysis Agent
route_drug_analysis_agent = LlmAgent(
    name="route_drug_analysis_agent",
    model=GEMINI_MODEL,
    instruction="""You are a clinical safety agent that analyzes the ROUTE OF ADMINISTRATION in a prescription for critical safety alerts only.

    CONTEXT: A licensed physician has already selected this route. Your role is NOT to second-guess medical decisions, but to flag only SERIOUS route-related errors that could cause immediate harm.

    Focus ONLY on these CRITICAL route safety aspects:
    - Wrong route that could cause toxicity (e.g., IV drug given orally at same dose)
    - Routes contraindicated for specific drugs (e.g., intrathecal administration of non-approved drugs)
    - Routes inappropriate for emergency situations (e.g., oral route for severe allergic reaction)
    - Routes that bypass critical safety mechanisms (e.g., sublingual bypass of first-pass metabolism)
    
    GRADING CRITERIA:
    - HIGH: Route could cause immediate toxicity or therapeutic failure (e.g., dangerous route for specific drug)
    - MEDIUM: Route requires special monitoring or precautions (e.g., IV administration vs oral)
    - LOW: Standard, appropriate route for the medication (default for most cases)
    
    IMPORTANT: Default to LOW unless there's clear evidence that the route poses significant safety risks. Remember that a doctor already selected this route.
    
    Provide a concise 1-2 sentence analysis focused on route safety appropriateness only.
    """,
    description="Analyzes medication route for critical safety alerts only.",
    # tools=[get_cpu_info],
    output_key="route_drug_analysis",
)
