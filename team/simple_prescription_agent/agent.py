from google.adk.agents import Agent
# from google.adk.tools import google_search
from datetime import datetime
from pydantic import BaseModel, Field

class CriticalityOutput(BaseModel):
    level: str = Field(..., description="Level of criticality: low, medium, high.")
    description: str = Field(..., description="Description of the criticality assessment. Include key factors influencing the decision.") #

root_agent = Agent(
    name="simple_prescription_agent",
    model="gemini-2.0-flash",
    description="Agente de prescrição médica",
    instruction="""
    You are a medical prescription agent that analyzes patient data and prescribes medications based on the provided information. You must assess the criticality of the patient's condition before making any prescriptions.
    Use the following tool to determine the criticality level:
    - Criticality: Determines the criticality level of the patient's condition (low, medium, high). 
    """,
    # tools=[google_search],
    output_schema=CriticalityOutput,
    output_key="results_search",
)
