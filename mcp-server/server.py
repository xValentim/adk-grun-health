from fastmcp import FastMCP
import asyncio, platform
from datetime import datetime
import requests
import json
import uuid
import os

# Configuração
BASE_URL = os.getenv("ADK_API_URL", "http://adk-api:8000")
APP_NAME = "lead_qualification_agent"

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
def qualify_lead_without_session(lead_data: str, user_id: str = "u_test") -> dict:
    """
    Qualifica um lead e retorna apenas o essencial.
    Arguments:
        lead_data: str - Dados do lead em formato de texto.
    Outputs:
        dict - Dicionário com validação, score e recomendação.
    """
    
    session_id = f"s_{uuid.uuid4().hex[:8]}"
    APP_NAME = "lead_qualification_agent"
    
    # 1. Criar sessão
    requests.post(
        f"{BASE_URL}/apps/{APP_NAME}/users/{user_id}/sessions/{session_id}",
        json={"state": {}, "user_id": user_id, "session_id": session_id}
    )
    
    # 2. Executar agente
    requests.post(
        f"{BASE_URL}/run",
        json={
            "appName": APP_NAME,
            "userId": user_id,
            "sessionId": session_id,
            "newMessage": {"parts": [{"text": lead_data}], "role": "user"}
        }
    )
    
    # 3. Obter resultado
    response = requests.get(
        f"{BASE_URL}/apps/{APP_NAME}/users/{user_id}/sessions/{session_id}"
    )
    
    # 4. Deletar sessão
    requests.delete(
        f"{BASE_URL}/apps/{APP_NAME}/users/{user_id}/sessions/{session_id}"
    )
    
    state = response.json().get("state", {})
    
    return {
        "validacao": state.get("validation_status", "N/A"),
        "score": state.get("lead_score", "N/A"),
        "recomendacao": state.get("action_recommendation", "N/A")
    }
    
def qualify_essay_without_session(essay_text: str, user_id: str = "u_test") -> dict:
    """
    Qualifica uma redação e retorna apenas o essencial. Essa análise é feita para ajudar um aluno a melhorar sua redação.
    Arguments:
        essay_text: str - Texto da redação a ser analisada.
    Outputs:
        dict - Dicionário com análise de conteúdo, análise estrutural e relatório sintetizado.
    """
    session_id = f"s_{uuid.uuid4().hex[:8]}"
    APP_NAME = "essay_analyzer_agent"
    
    # 1. Criar sessão
    requests.post(
        f"{BASE_URL}/apps/{APP_NAME}/users/{user_id}/sessions/{session_id}",
        json={"state": {}, "user_id": user_id, "session_id": session_id}
    )
    
    # 2. Executar agente
    requests.post(
        f"{BASE_URL}/run",
        json={
            "appName": APP_NAME,
            "userId": user_id,
            "sessionId": session_id,
            "newMessage": {"parts": [{"text": essay_text}], "role": "user"}
        }
    )
    
    # 3. Obter resultado
    response = requests.get(
        f"{BASE_URL}/apps/{APP_NAME}/users/{user_id}/sessions/{session_id}"
    )
    
    # 4. Deletar sessão
    requests.delete(
        f"{BASE_URL}/apps/{APP_NAME}/users/{user_id}/sessions/{session_id}"
    )
    
    state = response.json().get("state", {})
    
    return {
        "content_analysis": state.get("content_analysis", "N/A"),
        "struct_analysis": state.get("struct_analysis", "N/A"),
        "synthesized_report": state.get("synthesized_report", "N/A")
    }
    
def search_agent_without_session(query: str, user_id: str = "u_test") -> dict:
    """
    Executa o agente de busca e retorna apenas o essencial. O LLM pega a query do usuário, usa uma tool de busca no google e retorna os resultados trazendo informações relevantes interpretadas pelo modelo.
    Arguments:
        query: str - Consulta de busca em formato de texto.
    Outputs:
        dict - Dicionário com os resultados da busca.
    """
    session_id = f"s_{uuid.uuid4().hex[:8]}"
    APP_NAME = "search_agent"
    
    # 1. Criar sessão
    requests.post(
        f"{BASE_URL}/apps/{APP_NAME}/users/{user_id}/sessions/{session_id}",
        json={"state": {}, "user_id": user_id, "session_id": session_id}
    )
    
    # 2. Executar agente
    requests.post(
        f"{BASE_URL}/run",
        json={
            "appName": APP_NAME,
            "userId": user_id,
            "sessionId": session_id,
            "newMessage": {"parts": [{"text": query}], "role": "user"}
        }
    )
    
    # 3. Obter resultado
    response = requests.get(
        f"{BASE_URL}/apps/{APP_NAME}/users/{user_id}/sessions/{session_id}"
    )
    
    # 4. Deletar sessão
    requests.delete(
        f"{BASE_URL}/apps/{APP_NAME}/users/{user_id}/sessions/{session_id}"
    )
    
    state = response.json().get("state", {})
    
    return {
        "results_search": state.get("results_search", "N/A")
    }

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

@mcp.tool()
def qualify_lead(lead_data: str) -> dict:
    """
    Qualifica um lead e retorna apenas o essencial.
    Arguments:
        lead_data: str - Dados do lead em formato de texto.
    Outputs:
        dict - Dicionário com validação, score e recomendação.
    """
    return qualify_lead_without_session(lead_data)

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