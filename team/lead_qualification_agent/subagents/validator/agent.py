"""
Lead Validator Agent

This agent is responsible for validating if a lead has all the necessary information
for qualification.
"""

from google.adk.agents import LlmAgent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Create the validator agent
lead_validator_agent = LlmAgent(
    name="LeadValidatorAgent",
    model=GEMINI_MODEL,
    instruction="""Você é uma IA de Validação de Leads.
    
    Examine as informações do lead fornecidas pelo usuário e determine se estão completas o suficiente para qualificação.
    Um lead completo deve incluir:
    - Informações de contato (nome, email ou telefone)
    - Alguma indicação de interesse ou necessidade
    - Informações da empresa ou contexto, se aplicável
    
    Retorne APENAS 'válido' ou 'inválido' com um único motivo se inválido.
    
    Exemplo de saída válida: 'válido'
    Exemplo de saída inválida: 'inválido: faltam informações de contato'
    """,
    description="Valida informações do lead quanto à completude.",
    output_key="validation_status",
)
