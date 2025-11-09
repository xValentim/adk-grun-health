from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

# SUS_A2A_AGENT_CARD_URL = os.getenv(
#     "SUS_A2A_AGENT_CARD_URL",
#     "http://127.0.0.1:9001/.well-known/agent-card.json",
# )


nhs_compliance_client= RemoteA2aAgent(
    name="nhs_compliance_client",
    description="Client agent que encaminha análise para o NHSComplianceAgent remoto via A2A.",
    agent_card=(
        f"https://a2a-server-health-894271896157.europe-west1.run.app/a2a/nhs{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)

root_agent = nhs_compliance_client