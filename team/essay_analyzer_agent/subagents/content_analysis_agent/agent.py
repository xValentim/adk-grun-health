"""
CPU Information Agent

This agent is responsible for gathering and analyzing CPU information.
"""

from google.adk.agents import LlmAgent

# from .tools import get_cpu_info

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# 
content_analysis_agent = LlmAgent(
    name="content_analysis_agent",
    model=GEMINI_MODEL,
    instruction="""Você é uma IA que vai analisar conteúdo textual de redações.
    
    Fique atento a aspectos como:
    - Conhecimento do tema
    - Conhecimento de mundo
    - Relação com citações e referências
    """,
    description="Analisa conteúdo textual de redações.",
    # tools=[get_cpu_info],
    output_key="content_analysis",
)
