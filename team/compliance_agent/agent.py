from google.adk.agents import LlmAgent


from .subagents.sus.agent import root_agent as sus_compliance_agent
from .subagents.nhs.agent import root_agent as nhs_compliance_agent

root_agent = LlmAgent(
    name="compliance_agent",
    model="gemini-2.0-flash",
    description="Agente de conformidade que encaminha solicitações para agentes específicos do SUS e do NHS.",
    instruction="""
    You are a healthcare compliance routing agent.

    When the user asks about SUS (Sistema Único de Saúde - Brazil), delegate to sus_compliance_client.
    When the user asks about NHS (National Health Service - UK), delegate to nhs_compliance_client.

    If unclear, ask which health system they're referring to.
    """,
    sub_agents=[
        sus_compliance_agent,
        nhs_compliance_agent,
    ],
)

