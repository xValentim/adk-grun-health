from google.adk.agents import Agent
from google.adk.tools import google_search
from datetime import datetime

root_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    description="Agente de busca",
    instruction="""
    Você é um agente que utiliza ferramentas para responder às perguntas do usuário:
    - google_search
    """,
    tools=[google_search],
    output_key="results_search",
)
