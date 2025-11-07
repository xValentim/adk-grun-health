"""
Lead Scorer Agent

This agent is responsible for scoring a lead's qualification level
based on various criteria.
"""

from google.adk.agents import LlmAgent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Create the scorer agent
lead_scorer_agent = LlmAgent(
    name="LeadScorerAgent",
    model=GEMINI_MODEL,
    instruction="""Você é uma IA de Pontuação de Leads.
    
    Analise as informações do lead e atribua uma pontuação de qualificação de 1-10 baseada em:
    - Necessidade expressa (urgência/clareza do problema)
    - Autoridade para tomada de decisão
    - Indicadores de orçamento
    - Indicadores de cronograma
    
    Retorne APENAS uma pontuação numérica e UMA frase de justificativa.
    
    Exemplo de saída: '8: Tomador de decisão com orçamento claro e necessidade imediata'
    Exemplo de saída: '3: Interesse vago sem cronograma ou orçamento mencionado'
    """,
    description="Pontua leads qualificados em uma escala de 1-10.",
    output_key="lead_score",
)
