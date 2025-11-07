"""
Essay Report Synthesizer Agent

This agent is responsible for synthesizing information from other agents
to create a comprehensive essay report.
"""

from google.adk.agents import LlmAgent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# System Report Synthesizer Agent
essay_report_synthesizer = LlmAgent(
    name="essay_report_synthesizer",
    model=GEMINI_MODEL,
    instruction="""Você é uma IA que cria um relatório abrangente de redação com base nas análises fornecidas por outros agentes.
    
    Use as seguintes informações coletadas:
    - Content analysis: {content_analysis}
    - Structure analysis: {struct_analysis}

    Crie um relatório detalhado que inclua:

    1. Um resumo executivo no topo com o status geral da redação
    2. Seções para cada componente com suas respectivas informações
    3. Recomendações com base em quaisquer métricas preocupantes

    Use a formatação markdown para tornar o relatório legível e profissional.
    Destaque quaisquer valores preocupantes e forneça recomendações práticas.
    """,
    description="Sintetiza um relatório abrangente de redação.",
    output_key="synthesized_report"
)
