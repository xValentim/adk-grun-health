"""
Sequential Agent with a Minimal Callback

This example demonstrates a lead qualification pipeline with a minimal
before_agent_callback that only initializes state once at the beginning.
"""

from google.adk.agents import SequentialAgent

from .subagents.general import general_health_agent
from .subagents.treatment import treatment_assessment_agent

# Import the subagents
from .subagents.synthesizer import synthesizer_health_report_agent

# Create the sequential agent with minimal callback
root_agent = SequentialAgent(
    name="holistic_qualification_agent",
    sub_agents=[general_health_agent, 
                treatment_assessment_agent, 
                synthesizer_health_report_agent],
    description="Pipeline that analyzes general health, assesses treatment impact, and synthesizes a comprehensive health report.",
)
