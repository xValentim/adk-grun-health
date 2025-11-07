"""
System Monitor Root Agent

This module defines the root agent for the system monitoring application.
It uses a parallel agent for system information gathering and a sequential
pipeline for the overall flow.
"""

from google.adk.agents import ParallelAgent, SequentialAgent

from .subagents.drug_analysis_agent import drug_analysis_agent
from .subagents.dose_drug_analysis_agent import dose_drug_analysis_agent
from .subagents.route_drug_analysis_agent import route_drug_analysis_agent

from .subagents.synthesizer_agent import drug_report_synthesizer

# --- 1. Create Parallel Agent to gather information concurrently ---
individual_drug_analysis_agent = ParallelAgent(
    name="individual_drug_analyzer",
    sub_agents=[drug_analysis_agent, 
                dose_drug_analysis_agent,
                route_drug_analysis_agent],
)

# --- 2. Create Sequential Pipeline to gather info in parallel, then synthesize ---
root_agent = SequentialAgent(
    name="drug_monitor_agent",
    sub_agents=[individual_drug_analysis_agent, 
                drug_report_synthesizer],
)
