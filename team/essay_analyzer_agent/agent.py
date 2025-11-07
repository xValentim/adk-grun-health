"""
System Monitor Root Agent

This module defines the root agent for the system monitoring application.
It uses a parallel agent for system information gathering and a sequential
pipeline for the overall flow.
"""

from google.adk.agents import ParallelAgent, SequentialAgent

from .subagents.content_analysis_agent import content_analysis_agent
from .subagents.struct_analysis_agent import struct_analysis_agent
from .subagents.synthesizer_agent import essay_report_synthesizer

# --- 1. Create Parallel Agent to gather information concurrently ---
individual_analysis_agent = ParallelAgent(
    name="essay_analyzer",
    sub_agents=[content_analysis_agent, 
                struct_analysis_agent],
)

# --- 2. Create Sequential Pipeline to gather info in parallel, then synthesize ---
root_agent = SequentialAgent(
    name="essay_monitor_agent",
    sub_agents=[individual_analysis_agent, essay_report_synthesizer],
)
