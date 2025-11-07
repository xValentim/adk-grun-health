"""
Essay Report Synthesizer Agent

This agent is responsible for synthesizing information from other agents
to create a comprehensive essay report.
"""

from google.adk.agents import LlmAgent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

from pydantic import BaseModel, Field

class IndividualCriticalityOutput(BaseModel):
    level_drug: str = Field(..., description="Level of criticality about drug: low, medium, high.",
                            example=["low", "medium", "high"])
    level_dose: str = Field(..., description="Level of criticality about dose: low, medium, high.",
                            example=["low", "medium", "high"])
    level_route: str = Field(..., description="Level of criticality about route: low, medium, high.",
                            example=["low", "medium", "high"])
    description: str = Field(..., description="Description of the criticality assessment. Include key factors influencing the decision.")

# System Report Synthesizer Agent
drug_report_synthesizer = LlmAgent(
    name="drug_report_synthesizer",
    model=GEMINI_MODEL,
    instruction="""You are an agent that analyzes the *drug* report and results from other analysis agents.

    The aspects to consider include:
    - Drug: {drug_analysis}
    - Dose: {dose_drug_analysis}
    - Route: {route_drug_analysis}
    
    You must to analyse and extract criticality level for each aspect. Grade in low, medium, high.
    
    PS.: All the prescription was made a doctor. In this case, you just need to judge if have possible criticality issues (you don't need to judge if the prescription is good or bad, just if have possible issues and dont be very rigorous).
    
    Finally, synthesize a comprehensive report summarizing the findings from all analyses.
    """,
    description="Sintetiza um relatório abrangente de redação.",
    output_schema=IndividualCriticalityOutput,
    output_key="synthesized_results_criticality",
)
