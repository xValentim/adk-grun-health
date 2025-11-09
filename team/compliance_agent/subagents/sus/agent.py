from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

# SUS_A2A_AGENT_CARD_URL = os.getenv(
#     "SUS_A2A_AGENT_CARD_URL",
#     "http://127.0.0.1:9001/.well-known/agent-card.json",
# )


sus_compliance_client= RemoteA2aAgent(
    name="sus_compliance_client",
    description="Client agent que encaminha análise para o SUSComplianceAgent remoto via A2A.",
    agent_card=(
        f"http://localhost:8080/a2a/sus{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)

root_agent = sus_compliance_client