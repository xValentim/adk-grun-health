"""
Memory Information Agent

This agent is responsible for gathering and analyzing memory information.
"""

from google.adk.agents import LlmAgent

# from .tools import get_memory_info

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Memory Information Agent
struct_analysis_agent = LlmAgent(
    name="MemoryInfoAgent",
    model=GEMINI_MODEL,
    instruction="""Você é uma IA que vai analisar a estrutura textual de redações.
    
    Fique atento a aspectos como:
    - Coerência e coesão
    - Gramática e ortografia
    - Vocabulário e estilo
    """,
    description="Analisa a estrutura textual de redações.",
    # tools=[get_memory_info],
    output_key="struct_analysis",
)
