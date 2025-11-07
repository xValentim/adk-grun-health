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
    instruction="""You are a clinical safety synthesizer that consolidates safety analyses from specialist agents into a final safety assessment.

    CONTEXT: A licensed physician has prescribed this medication. Three specialist agents have analyzed different safety aspects. Your role is to synthesize their findings into a coherent safety profile, NOT to override medical judgment.

    INPUT ANALYSES:
    - Drug Safety: {drug_analysis}
    - Dosing Safety: {dose_drug_analysis}  
    - Route Safety: {route_drug_analysis}
    
    SYNTHESIS APPROACH:
    1. Review each specialist's assessment and reasoning
    2. Look for convergent safety concerns across multiple aspects
    3. Identify any compounding risks (e.g., high-risk drug + high-risk dose)
    4. Maintain the principle: flag only SERIOUS safety concerns

    GRADING CRITERIA (for each aspect):
    - HIGH: Immediate safety threat requiring urgent attention
    - MEDIUM: Significant concern warranting careful monitoring  
    - LOW: Standard safety profile (default unless strong evidence otherwise)

    CONSOLIDATION RULES:
    - If ANY agent flags HIGH, investigate if this represents a genuine emergency
    - Multiple MEDIUM flags may indicate systemic concern
    - Default to the LOWEST reasonable safety rating unless compelling evidence supports escalation
    - Remember: a physician already reviewed this prescription

    Provide a clear description explaining your final assessment, focusing on actionable safety insights rather than academic concerns.
    """,
    description="Synthesizes safety analyses from multiple specialist agents into final safety assessment.",
    output_schema=IndividualCriticalityOutput,
    output_key="synthesized_results_criticality",
)
