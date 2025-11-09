from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
import uuid
import os
from typing import Dict, Any

# Configuration
BASE_URL = os.getenv("ADK_API_URL", "http://localhost:8000")

app = FastAPI(
    title="Health Analysis API",
    description="API for health prescription analysis using ADK agents",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Available agent names
AGENTS = {
    "parallel": "parallel_analyzer_agent",
    "sequential": "sequential_analyzer_agent", 
    "prescription": "simple_prescription_agent"
}

class HealthDataRequest(BaseModel):
    health_data: str

class AnalysisResponse(BaseModel):
    status: str
    data: Dict[Any, Any]
    message: str = ""

def run_agent(agent_name: str, input_data: str, user_id: str = "api_user") -> dict:
    """
    Executes an agent and returns the complete state.
    Creates and deletes the session automatically.
    """
    session_id = f"s_{uuid.uuid4().hex[:8]}"
    
    try:
        # 1. Create session
        requests.post(
            f"{BASE_URL}/apps/{agent_name}/users/{user_id}/sessions/{session_id}",
            json={"state": {}, "user_id": user_id, "session_id": session_id}
        )
        
        # 2. Execute agent
        requests.post(
            f"{BASE_URL}/run",
            json={
                "appName": agent_name,
                "userId": user_id,
                "sessionId": session_id,
                "newMessage": {"parts": [{"text": input_data}], "role": "user"}
            }
        )
        
        # 3. Get result
        response = requests.get(
            f"{BASE_URL}/apps/{agent_name}/users/{user_id}/sessions/{session_id}"
        )
        
        # 4. Delete session
        requests.delete(
            f"{BASE_URL}/apps/{agent_name}/users/{user_id}/sessions/{session_id}"
        )
        
        return response.json().get("state", {})
    
    except Exception as e:
        # Try to delete session in case of error
        try:
            requests.delete(
                f"{BASE_URL}/apps/{agent_name}/users/{user_id}/sessions/{session_id}"
            )
        except:
            pass
        raise e

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Health Analysis API is running", "status": "ok"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        # Test connection with ADK API
        response = requests.get(f"{BASE_URL}/list-apps", timeout=5)
        apps = response.json()
        return {
            "status": "healthy",
            "adk_api_status": "connected",
            "available_agents": apps
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "adk_api_status": "disconnected",
            "error": str(e)
        }

@app.get("/agents")
async def get_available_agents():
    """List all available agents"""
    try:
        response = requests.get(f"{BASE_URL}/list-apps")
        apps = response.json()
        return {
            "status": "success",
            "agents": apps,
            "configured_agents": AGENTS
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching agents: {str(e)}")

@app.post("/analyze/simple", response_model=AnalysisResponse)
async def simple_prescription_analysis(request: HealthDataRequest):
    """
    Performs routine safety checks on patient prescriptions using a simple agent.
    This agent provides overall prescription safety assessment with permissive evaluation criteria.
    """
    try:
        result = run_agent("simple_prescription_agent", request.health_data)
        return AnalysisResponse(
            status="success",
            data=result,
            message="Simple prescription analysis completed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze/parallel", response_model=AnalysisResponse)
async def parallel_prescription_analysis(request: HealthDataRequest):
    """
    Analyzes prescription safety using parallel agents for drug, dose, and route analysis.
    Three specialist agents work concurrently to evaluate different aspects, then synthesize results.
    """
    try:
        result = run_agent("parallel_analyzer_agent", request.health_data)
        return AnalysisResponse(
            status="success",
            data=result,
            message="Parallel prescription analysis completed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze/sequential", response_model=AnalysisResponse)
async def sequential_health_analysis(request: HealthDataRequest):
    """
    Performs comprehensive health analysis using sequential agents for general health, 
    treatment impact assessment, and synthesis. Pipeline analyzes patient profile, 
    evaluates treatment duration and impacts, then consolidates into actionable health report.
    """
    try:
        result = run_agent("sequential_analyzer_agent", request.health_data)
        return AnalysisResponse(
            status="success",
            data=result,
            message="Sequential health analysis completed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze/all", response_model=Dict[str, AnalysisResponse])
async def comprehensive_analysis(request: HealthDataRequest):
    """
    Executes all three analyses (simple, parallel, and sequential) and returns consolidated results.
    """
    results = {}
    
    # Simple analysis
    try:
        simple_result = run_agent("simple_prescription_agent", request.health_data)
        results["simple"] = AnalysisResponse(
            status="success",
            data=simple_result,
            message="Simple analysis completed"
        )
    except Exception as e:
        results["simple"] = AnalysisResponse(
            status="error",
            data={},
            message=f"Simple analysis failed: {str(e)}"
        )
    
    # Parallel analysis
    try:
        parallel_result = run_agent("parallel_analyzer_agent", request.health_data)
        results["parallel"] = AnalysisResponse(
            status="success",
            data=parallel_result,
            message="Parallel analysis completed"
        )
    except Exception as e:
        results["parallel"] = AnalysisResponse(
            status="error",
            data={},
            message=f"Parallel analysis failed: {str(e)}"
        )
    
    # Sequential analysis
    try:
        sequential_result = run_agent("sequential_analyzer_agent", request.health_data)
        results["sequential"] = AnalysisResponse(
            status="success",
            data=sequential_result,
            message="Sequential analysis completed"
        )
    except Exception as e:
        results["sequential"] = AnalysisResponse(
            status="error",
            data={},
            message=f"Sequential analysis failed: {str(e)}"
        )
    
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)