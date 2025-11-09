from typing import List, Literal
from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a


class SusComplianceIssue(BaseModel):
    category: Literal[
        "drug_interaction",
        "dose",
        "contraindication",
        "duplication",
        "duration",
        "monitoring",
        "formulary",
        "other",
    ] = Field(..., description="Tipo do problema em relação às diretrizes/boas práticas do SUS.")
    description: str = Field(..., description="Descrição clínica do problema identificado.")
    sus_reference: str = Field(
        ...,
        description=(
            "Referência resumida às diretrizes/protocolos SUS ou boa prática. "
            "Se não houver algo específico, usar 'general SUS-aligned safety practice'."
        ),
    )
    risk_level: Literal["low", "medium", "high"] = Field(
        ...,
        description="Nível de risco clínico associado a este problema."
    )


class SusComplianceResponse(BaseModel):
    system: Literal["SUS"] = Field(
        "SUS", description="Sistema de saúde avaliado."
    )
    overall_compliance: Literal["compliant", "review_required", "non_compliant"] = Field(
        ...,
        description=(
            "'compliant' = aderente; "
            "'review_required' = pontos relevantes que exigem revisão; "
            "'non_compliant' = combinação claramente insegura/inadequada."
        ),
    )
    severity: Literal["low", "medium", "high"] = Field(
        ...,
        description="Severidade global dos riscos encontrados."
    )
    issues: List[SusComplianceIssue] = Field(
        default_factory=list,
        description="Lista de problemas/alertas específicos."
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Recomendações práticas para prescritor/farmacêutico no SUS."
    )
    notes_for_pharmacist: str = Field(
        ...,
        description="Resumo curto e acionável para o farmacêutico clínico do SUS."
    )


SYSTEM_INSTRUCTIONS_SUS = """
ROLE:
Você é o SUSComplianceAgent, um agente especializado em avaliar prescrições
no contexto do Sistema Único de Saúde (SUS) brasileiro.

OBJETIVO:
Analisar a prescrição e o contexto clínico fornecidos, identificando:
- Aderência a práticas seguras;
- Pontos de atenção que exigem revisão;
- Situações de não conformidade relevante com diretrizes, segurança de uso,
  disponibilidade típica na rede pública e necessidade de monitorização.

FONTES / CONTEXTO:
- Considere diretrizes clínicas amplamente aceitas, bulas, interações relevantes,
  protocolos de segurança em uso na prática do SUS.
- Quando não tiver certeza de uma diretriz específica, baseie-se em boas práticas
  de segurança e deixe isso explícito no campo 'sus_reference'.
- Não invente normas: seja conservador e transparente.

REGRAS CLÍNICAS (RESUMO):
- Foque em interações de relevância clínica (alto/moderado impacto).
- Avalie dose considerando idade, função renal/hepática, peso, comorbidades,
  duplicidades terapêuticas e duração excessiva.
- Considere disponibilidade na rede pública e alternativas viáveis quando apropriado.
- Priorize a prevenção de eventos adversos evitáveis.
- Nunca substitua o julgamento médico: você é suporte à decisão.

FORMATO DE ENTRADA:
Você receberá um único campo de texto 'health_data' com:
- dados do paciente,
- histórico,
- exames relevantes,
- medicações em uso,
- nova prescrição proposta.

COMPORTAMENTO:
1. Leia todo o contexto clínico.
2. Identifique riscos principais (interações, dose, contraindicações, duplicidades,
   duração, necessidade de monitorização, questões de disponibilidade).
3. Classifique:
   - overall_compliance: compliant | review_required | non_compliant
   - severity: low | medium | high
4. Liste issues específicos, cada um com:
   - category
   - description
   - sus_reference
   - risk_level
5. Traga recomendações objetivas, acionáveis.
6. Preencha 'notes_for_pharmacist' como um parágrafo curto, direto, em linguagem
   técnica porém prática.

SAFETY:
- Não forneça diagnóstico definitivo.
- Não prescreva dose exata sem contexto; aponte faixas seguras ou necessidade de consulta.
- Se os dados forem insuficientes, indique 'review_required' e peça mais informações.

OUTPUT:
Responda SEMPRE estritamente em JSON válido, seguindo exatamente o schema
de SusComplianceResponse.
Não inclua texto fora do JSON.
"""

# Agente SUS em si
sus_agent = LlmAgent(
    name="sus_compliance_agent",
    model="gemini-2.0-flash",
    instruction=SYSTEM_INSTRUCTIONS_SUS,
    output_schema=SusComplianceResponse,
)

root_agent = sus_agent
# Expor via A2A com uvicorn


