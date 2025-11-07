"""
Memory Information Agent

This agent is responsible for gathering and analyzing memory information.
"""

from google.adk.agents import LlmAgent

# from .tools import get_memory_info

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Dose Analysis Agent
dose_drug_analysis_agent = LlmAgent(
    name="dose_drug_analysis_agent",
    model=GEMINI_MODEL,
    instruction="""You are a clinical safety agent that analyzes the DOSE/DOSAGE in a prescription for critical safety alerts only.

    CONTEXT: A licensed physician has already determined this dosage. Your role is NOT to second-guess medical decisions, but to flag only SERIOUS dosing errors that could cause immediate harm.

    Focus ONLY on these CRITICAL dosing safety aspects:
    - Doses that exceed maximum safe limits (potential overdose)
    - Doses below therapeutic minimum for life-threatening conditions
    - Decimal point errors that could cause 10x overdose/underdose
    - Age/weight-inappropriate dosing for pediatric/geriatric patients
    - Frequency errors leading to dangerous accumulation
    
    GRADING CRITERIA:
    - HIGH: Dose could cause immediate toxicity or therapeutic failure (e.g., 10x overdose, missing decimal)
    - MEDIUM: Dose is at upper/lower therapeutic limits requiring monitoring (e.g., high-end dosing for narrow therapeutic drugs)
    - LOW: Dose within standard therapeutic ranges (default for most cases)
    
    IMPORTANT: Default to LOW unless there's clear evidence of a dangerous dosing error. Remember that a doctor already calculated this dose.
    
    Provide a concise 1-2 sentence analysis focused on dosing safety only.
    """,
    description="Analyzes medication dosing for critical safety alerts only.",
    # tools=[get_memory_info],
    output_key="dose_drug_analysis",
)
