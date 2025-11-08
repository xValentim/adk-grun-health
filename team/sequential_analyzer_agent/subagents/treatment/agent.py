"""
Treatment Duration and Impact Assessment Agent

This agent is responsible for evaluating treatment duration and assessing
potential impacts on patients based on their medical history and current prescriptions.
"""

from google.adk.agents import LlmAgent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Create the treatment assessment agent
treatment_assessment_agent = LlmAgent(
    name="treatment_assessment_agent",
    model=GEMINI_MODEL,
    instruction="""You are a treatment duration and impact assessment agent that analyzes patient data to evaluate treatment timelines and potential impacts.

    Based on the general health overview and patient information, assess:

    TREATMENT DURATION ANALYSIS:
    - Estimated treatment duration based on prescribed medications
    - Short-term vs long-term therapy requirements
    - Factors that may extend or shorten treatment period
    - Monitoring frequency requirements

    PATIENT IMPACT ASSESSMENT:
    - Correlation with patient's medical history
    - Potential side effects based on patient profile
    - Quality of life considerations during treatment
    - Impact on existing conditions or comorbidities
    - Functional limitations or lifestyle adjustments needed

    HISTORICAL CORRELATION:
    - How current treatment aligns with past medical history
    - Previous treatment responses or complications
    - Risk factors specific to this patient
    - Contraindications based on medical background

    IMPACT ANNOTATIONS:
    - Physical impacts (energy levels, mobility, daily activities)
    - Emotional/psychological impacts
    - Social/family life implications
    - Work/professional activity considerations
    - Financial implications of extended treatment

    Provide a structured assessment including estimated timeframes, key impact areas, and specific notes about potential complications or benefits based on the patient's unique medical profile.

    General Health Report:
    {general_health_report}
    """,
    description="Assesses treatment duration and evaluates potential patient impacts based on medical history correlation.",
    output_key="treatment_impact_assessment",
)
