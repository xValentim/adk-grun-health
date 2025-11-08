"""
Health Report Synthesizer Agent

This agent is responsible for synthesizing the general health analysis
and treatment impact assessment into a comprehensive, unified health report.
"""

"""
Health Report Synthesizer Agent

This agent is responsible for synthesizing the general health analysis
and treatment impact assessment into a comprehensive, unified health report.
"""

from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field

class SynthesizedHealthReport(BaseModel):
    # Criticality alerts for variables not mapped by other agents
    treatment_duration_criticality: str = Field(..., description="Criticality level for treatment duration: low, medium, high",
                                                example=["low", "medium", "high"])
    patient_compliance_criticality: str = Field(..., description="Criticality level for patient compliance risk: low, medium, high",
                                                example=["low", "medium", "high"])
    lifestyle_impact_criticality: str = Field(..., description="Criticality level for lifestyle/quality of life impact: low, medium, high",
                                                example=["low", "medium", "high"])
    monitoring_frequency_criticality: str = Field(..., description="Criticality level for required monitoring frequency: low, medium, high",
                                                example=["low", "medium", "high"])

    # Summary and actionable insights
    executive_summary: str = Field(..., description="Concise summary of patient status, treatment plan, and key considerations")
    actionable_recommendations: str = Field(..., description="Clear, actionable recommendations for healthcare providers and patient care")

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Create the synthesizer agent
synthesizer_health_report_agent = LlmAgent(
    name="synthesizer_health_report_agent",
    model=GEMINI_MODEL,
    instruction="""You are a health report synthesizer agent that consolidates multiple analyses into a simplified, actionable health report.

    You will receive two key analyses:
    1. General Health Report - comprehensive patient overview
    2. Treatment Impact Assessment - duration and impact analysis

    Your role is to synthesize these and assess criticality for NEW variables not covered by other agents:

    CRITICALITY ASSESSMENTS (grade as low, medium, high):
    - Treatment Duration: How critical is the length/complexity of treatment timeline
    - Patient Compliance: Risk level for patient adherence to treatment plan
    - Lifestyle Impact: How severely treatment affects patient's daily life/activities  
    - Monitoring Frequency: How critical is the required monitoring schedule

    GRADING CRITERIA:
    - HIGH: Requires immediate attention or poses significant risk
    - MEDIUM: Needs careful monitoring but manageable
    - LOW: Standard/routine level requiring normal care

    EXECUTIVE SUMMARY:
    Provide a clear, concise summary covering:
    - Patient key demographics and condition
    - Treatment overview and expected timeline
    - Main risk factors and considerations
    - Overall prognosis and outlook

    ACTIONABLE RECOMMENDATIONS:
    Provide specific, practical recommendations for:
    - Healthcare provider actions and monitoring
    - Patient education and compliance strategies
    - Follow-up scheduling and care coordination
    - Risk mitigation strategies

    Keep assessments realistic and avoid over-flagging. Default to lower criticality unless clear evidence supports higher levels.

    General Health Analysis:
    {general_health_report}

    Treatment Impact Assessment:
    {treatment_impact_assessment}
    """,
    description="Synthesizes health analyses into simplified report with criticality alerts and actionable insights.",
    output_schema=SynthesizedHealthReport,
    output_key="synthesized_health_report",
)
