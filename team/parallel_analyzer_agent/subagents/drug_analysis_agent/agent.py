"""
CPU Information Agent

This agent is responsible for gathering and analyzing CPU information.
"""

from google.adk.agents import LlmAgent

# from .tools import get_cpu_info

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Drug Analysis Agent
drug_analysis_agent = LlmAgent(
    name="drug_analysis_agent",
    model=GEMINI_MODEL,
    instruction="""You are an agent that analyzes the *drug* in prescription.

    Pay attention to aspects such as:
    - Drug interactions
    - Side effects
    - Contraindications
    
    PS.: All the prescription was made a doctor. In this case, you just need to judge if have possible criticality issues (you don't need to judge if the prescription is good or bad, just if have possible issues and dont be very rigorous).
    
    You need to provide a one or two phrases analysis of the drug based on the provided prescription information. Extract some criticality level. Grade in low, medium, high.
    """,
    description="Agent to analyze drug information in prescriptions.",
    # tools=[get_cpu_info],
    output_key="drug_analysis",
)
