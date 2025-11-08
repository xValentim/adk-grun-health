from fastmcp import FastMCP
import asyncio, platform
from datetime import datetime
import requests
import json
import uuid
import os

# Configuração
BASE_URL = os.getenv("ADK_API_URL", "http://localhost:8000")
APP_NAME = "lead_qualification_agent"

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Nomes dos agentes disponíveis
AGENTS = {
    "parallel": "parallel_analyzer_agent",
    "sequential": "sequential_analyzer_agent", 
    "prescription": "simple_prescription_agent"
}

def run_agent(agent_name: str, input_data: str, user_id: str = "u_test") -> dict:
    """
    Executa um agente e retorna o estado completo.
    Cria e deleta a sessão automaticamente.
    """
    session_id = f"s_{uuid.uuid4().hex[:8]}"
    
    # 1. Criar sessão
    requests.post(
        f"{BASE_URL}/apps/{agent_name}/users/{user_id}/sessions/{session_id}",
        json={"state": {}, "user_id": user_id, "session_id": session_id}
    )
    
    # 2. Executar agente
    requests.post(
        f"{BASE_URL}/run",
        json={
            "appName": agent_name,
            "userId": user_id,
            "sessionId": session_id,
            "newMessage": {"parts": [{"text": input_data}], "role": "user"}
        }
    )
    
    # 3. Obter resultado
    response = requests.get(
        f"{BASE_URL}/apps/{agent_name}/users/{user_id}/sessions/{session_id}"
    )
    
    # 4. Deletar sessão
    requests.delete(
        f"{BASE_URL}/apps/{agent_name}/users/{user_id}/sessions/{session_id}"
    )
    
    return response.json().get("state", {})


def get_all_sessions(agent_name: str, user_id: str = "u_test") -> list:
    """Obtém todas as sessões de um usuário para um agente específico."""
    response = requests.get(
        f"{BASE_URL}/apps/{agent_name}/users/{user_id}/sessions"
    )
    return response.json()
    
mcp = FastMCP(name="MyServer")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

@mcp.tool()
def pizza_salami_price() -> str:
    """Returns that Pizza Salami at Bella Vista costs 10€."""
    return "Pizza Salami at Bella Vista costs 10€."

@mcp.tool()
def current_year() -> int:
    """Returns the current year."""
    return datetime.now().year

@mcp.tool()
def greet(name: str) -> str:
    """Greets a person with their name."""
    return f"Hello, {name}!"

def get_all_apps():
    """
    Recupera a lista de todos os aplicativos disponíveis na API ADK.
    
    Returns:
        list - Lista de aplicativos.
    """
    response = requests.get(f"{BASE_URL}/list-apps")
    return response.json()

@mcp.tool()
def simple_prescription_analysis(health_data: str) -> dict:
    """
    Performs routine safety checks on patient prescriptions using a simple agent.
    This agent provides overall prescription safety assessment with permissive evaluation criteria.
    
    Arguments:
        health_data: str - Patient health data and prescription information in text format.
    Outputs:
        dict - Dictionary containing overall criticality level (low/medium/high) and description.
    """
    return run_agent("simple_prescription_agent", health_data)

@mcp.tool()
def parallel_prescription_analysis(health_data: str) -> dict:
    """
    Analyzes prescription safety using parallel agents for drug, dose, and route analysis.
    Three specialist agents work concurrently to evaluate different aspects, then synthesize results.
    
    Arguments:
        health_data: str - Patient health data and prescription information in text format.
    Outputs:
        dict - Dictionary with individual criticality levels for drug, dose, and route analysis plus synthesis description.
    """
    return run_agent("parallel_analyzer_agent", health_data)

@mcp.tool()
def sequential_health_analysis(health_data: str) -> dict:
    """
    Performs comprehensive health analysis using sequential agents for general health, treatment impact assessment, and synthesis.
    Pipeline analyzes patient profile, evaluates treatment duration and impacts, then consolidates into actionable health report.
    
    Arguments:
        health_data: str - Patient health data and prescription information in text format.
    Outputs:
        dict - Dictionary with treatment duration criticality, patient compliance risk, lifestyle impact, monitoring frequency, executive summary, and actionable recommendations.
    """
    return run_agent("sequential_analyzer_agent", health_data)

@mcp.tool()
def qualify_essay(essay_text: str) -> dict:
    """
    Qualifica uma redação e retorna apenas o essencial. Essa análise é feita para ajudar um aluno a melhorar sua redação.
    Arguments:
        essay_text: str - Texto da redação a ser analisada.
    Outputs:
        dict - Dicionário com análise de conteúdo, análise estrutural e relatório sintetizado.
    """
    return qualify_essay_without_session(essay_text)    

@mcp.tool()
def search_agent(query: str) -> dict:
    """
    Executa o agente de busca e retorna apenas o essencial. O LLM pega a query do usuário, usa uma tool de busca no google e retorna os resultados trazendo informações relevantes interpretadas pelo modelo.
    Arguments:
        query: str - Consulta de busca em formato de texto.
    Outputs:
        dict - Dicionário com os resultados da busca.
    """
    return search_agent_without_session(query)

if __name__ == "__main__":
    # Start an HTTP server on port 8001
    mcp.run(transport="http", host="0.0.0.0", port=8001, path="/mcp")