from typing import List, Literal
from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent
# from google.adk.a2a.utils.agent_to_a2a import to_a2a


class NhsComplianceIssue(BaseModel):
    category: Literal[
        "drug_interaction",
        "dose",
        "contraindication",
        "duplication",
        "duration",
        "monitoring",
        "formulary",
        "renal_adjustment",
        "hepatic_adjustment",
        "other",
    ] = Field(..., description="Tipo do problema em relação às boas práticas/guidelines NHS.")
    description: str = Field(
        ...,
        description="Descrição clínica clara do problema identificado no contexto NHS."
    )
    nhs_reference: str = Field(
        ...,
        description=(
            "Referência resumida (ex: NICE guideline, BNF, local formulary) ou "
            "'NHS best practice' quando não houver guideline específica."
        ),
    )
    risk_level: Literal["low", "medium", "high"] = Field(
        ...,
        description="Nível de risco clínico associado ao problema."
    )


class NhsComplianceResponse(BaseModel):
    system: Literal["NHS"] = Field(
        "NHS", description="Sistema de saúde avaliado."
    )
    overall_compliance: Literal["compliant", "review_required", "non_compliant"] = Field(
        ...,
        description=(
            "'compliant' = alinhado às boas práticas/guidelines NHS; "
            "'review_required' = pontos relevantes que exigem revisão; "
            "'non_compliant' = combinação claramente insegura ou contra guidelines."
        ),
    )
    severity: Literal["low", "medium", "high"] = Field(
        ...,
        description="Severidade global dos riscos encontrados."
    )
    issues: List[NhsComplianceIssue] = Field(
        default_factory=list,
        description="Lista de problemas/alertas específicos."
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description=(
            "Recomendações práticas para o prescritor/farmacêutico no contexto NHS "
            "(ajustes, alternativas, monitorização, etc.)."
        ),
    )
    notes_for_pharmacist: str = Field(
        ...,
        description="Resumo curto e acionável para o pharmacist no NHS."
    )


SYSTEM_INSTRUCTIONS_NHS = """
ROLE:
Você é o NHSComplianceAgent, um agente especializado em avaliar prescrições
no contexto do National Health Service (NHS) do Reino Unido.

OBJETIVO:
Identificar riscos e verificar alinhamento com:
- NICE guidelines;
- British National Formulary (BNF);
- protocolos locais comuns no NHS;
- boas práticas de segurança em uso de medicamentos no UK.

ORIENTAÇÕES:
- Considere interações clinicamente relevantes, não alertas triviais.
- Avalie dose, frequência, duração e necessidade de ajuste em insuficiência renal/hepática.
- Verifique contraindicações, duplicidades terapêuticas e necessidade de monitorização.
- Considere disponibilidade típica no NHS / formulary quando relevante.
- Seja transparente quando a conclusão se basear em "best practice" e não guideline específica.
- Não substitua o julgamento clínico. Você é suporte à decisão.

COMPORTAMENTO:
1. Leia todo o 'health_data' (contexto + prescrição).
2. Classifique:
   - overall_compliance: compliant | review_required | non_compliant
   - severity: low | medium | high
3. Liste issues com:
   - category
   - description
   - nhs_reference (NICE/BNF/best practice)
   - risk_level
4. Traga recomendações objetivas, acionáveis.
5. Preencha 'notes_for_pharmacist' em linguagem direta, técnica e prática.
6. Se os dados forem insuficientes, use 'review_required' e peça mais informação.

SAFETY:
- Não forneça diagnóstico definitivo.
- Não prescreva dose exata sem contexto; sugira faixas/checagens.
- Seja conservador em caso de dúvida.

OUTPUT:
Responda SEMPRE estritamente em JSON válido no formato de NhsComplianceResponse.
Não inclua texto fora do JSON.
"""


nhs_agent = LlmAgent(
    name="nhs_compliance_agent",
    model="gemini-2.0-flash",
    instruction=SYSTEM_INSTRUCTIONS_NHS,
    output_schema=NhsComplianceResponse,
)

root_agent = nhs_agent

# Expor via A2A com uvicorn (comentado para usar adk api_server --a2a)
from google.adk.a2a.utils.agent_to_a2a import to_a2a
app_nhs = to_a2a(root_agent, agent_card="./compliance_agents/nhs/agent-card.json")