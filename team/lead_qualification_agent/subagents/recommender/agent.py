"""
Action Recommender Agent

This agent is responsible for recommending appropriate next actions
based on the lead validation and scoring results.
"""

from google.adk.agents import LlmAgent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Create the recommender agent
action_recommender_agent = LlmAgent(
    name="ActionRecommenderAgent",
    model=GEMINI_MODEL,
    instruction="""Você é uma IA de Recomendação de Ações.
    
    Com base nas informações e pontuação do lead:
    
    - Para leads inválidos: Sugira quais informações adicionais são necessárias
    - Para leads com pontuação 1-3: Sugira ações de nutrição (conteúdo educacional, etc.)
    - Para leads com pontuação 4-7: Sugira ações de qualificação (chamada de descoberta, avaliação de necessidades)
    - Para leads com pontuação 8-10: Sugira ações de vendas (demonstração, proposta, etc.)
    
    Formate sua resposta como uma recomendação completa para a equipe de vendas.
    
    Pontuação do Lead:
    {lead_score}

    Status de Validação do Lead:
    {validation_status}
    """,
    description="Recomenda próximas ações baseadas na qualificação do lead.",
    output_key="action_recommendation",
)
