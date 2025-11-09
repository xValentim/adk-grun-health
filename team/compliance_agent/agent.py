from google.adk.agents import LlmAgent


from .subagents.sus.agent import root_agent as sus_compliance_agent
from .subagents.nhs.agent import root_agent as nhs_compliance_agent

root_agent = LlmAgent(
    name="compliance_agent",
    description="Agente de conformidade que encaminha solicitações para agentes específicos do SUS e do NHS.",
    sub_agents=[
        sus_compliance_agent,
        nhs_compliance_agent,
    ],
)

