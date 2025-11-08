# 📡 API Reference

## Overview

The Health Analysis API provides RESTful endpoints for prescription safety analysis using AI agents. All endpoints accept JSON payloads and return structured analysis results with criticality levels and clinical recommendations.

## Base URLs

- **Local Development**: `http://localhost:8002`
- **Google Cloud Run**: `https://fastapi-health-[hash]-uc.a.run.app`

## Authentication

Currently, the API operates without authentication for development purposes. Production deployments should implement appropriate healthcare-grade authentication mechanisms.

## Common Request/Response Format

### Request Structure
All analysis endpoints accept the following request format:

```json
{
  "health_data": "string"
}
```

**health_data**: Complete patient information including demographics, medical history, current medications, lab values, and new prescription details.

### Response Structure
```json
{
  "status": "success|error",
  "data": {
    // Agent-specific analysis results
  },
  "message": "Human-readable description"
}
```

## Endpoints

### Health Check Endpoints

#### `GET /`
Basic API status check.

**Response:**
```json
{
  "message": "Health Analysis API is running",
  "status": "ok"
}
```

#### `GET /health`
Comprehensive health check including ADK API connectivity.

**Response:**
```json
{
  "status": "healthy|unhealthy",
  "adk_api_status": "connected|disconnected", 
  "available_agents": ["simple_prescription_agent", "parallel_analyzer_agent", "sequential_analyzer_agent"],
  "error": "string (if status is unhealthy)"
}
```

#### `GET /agents`
List all available analysis agents.

**Response:**
```json
{
  "status": "success",
  "agents": ["simple_prescription_agent", "parallel_analyzer_agent", "sequential_analyzer_agent"],
  "configured_agents": {
    "parallel": "parallel_analyzer_agent",
    "sequential": "sequential_analyzer_agent", 
    "prescription": "simple_prescription_agent"
  }
}
```

### Analysis Endpoints

#### `POST /analyze/simple`
Performs routine safety checks using a single agent for rapid assessment.

**Use Case**: Quick prescription safety screening for high-volume scenarios.

**Request Body:**
```json
{
  "health_data": "Patient: João Silva, Age: 65, Current medications: Metformin 500mg BID, Lisinopril 10mg daily. New prescription: Warfarin 5mg daily. Lab: Creatinine 1.2 mg/dL"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "results_criticality": {
      "overall_criticality": "medium",
      "description": "Overall safety assessment indicates moderate clinical concern requiring enhanced monitoring due to potential interaction between Warfarin and patient's current medications."
    }
  },
  "message": "Simple prescription analysis completed successfully"
}
```

#### `POST /analyze/parallel`
Analyzes prescription safety using specialized parallel agents for drug, dose, and route analysis.

**Use Case**: Detailed multi-dimensional analysis for complex prescriptions.

**Request Body:**
```json
{
  "health_data": "Patient: Maria Santos, Age: 72, Weight: 58kg, Creatinine: 1.8 mg/dL. Current: Digoxin 0.25mg daily, Furosemide 40mg BID. New: Amiodarone 200mg daily, route IV initially then PO."
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "synthesized_results_criticality": {
      "level_drug": "high",
      "level_dose": "medium",
      "level_route": "low", 
      "description": "High-risk drug interaction detected between Amiodarone and Digoxin requiring dose adjustment and enhanced cardiac monitoring. Dosing appropriate for patient weight and renal function. IV to PO route transition is clinically appropriate."
    }
  },
  "message": "Parallel prescription analysis completed successfully"
}
```

#### `POST /analyze/sequential`
Performs comprehensive health analysis using sequential agents for patient profiling, treatment assessment, and health report synthesis.

**Use Case**: Complete health impact assessment for complex patients with multiple comorbidities.

**Request Body:**
```json
{
  "health_data": "Patient: Carlos Oliveira, Age: 68, DM Type 2, CHF, CKD Stage 3. Current medications: Metformin 1000mg BID, Enalapril 20mg BID, Carvedilol 12.5mg BID, Furosemide 40mg daily. New prescription: Insulin glargine 20 units at bedtime. Recent HbA1c: 9.2%, eGFR: 45 mL/min/1.73m²"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "synthesized_health_report": {
      "treatment_duration_criticality": "medium",
      "patient_compliance_criticality": "high",
      "lifestyle_impact_criticality": "medium",
      "monitoring_frequency_criticality": "high",
      "executive_summary": "68-year-old male with multiple comorbidities requiring insulin initiation. Patient profile indicates high diabetes burden with complications affecting kidney and cardiovascular system. Complex medication regimen may impact compliance.",
      "actionable_recommendations": "1) Start insulin glargine with careful glucose monitoring 2) Increase nephrology follow-up frequency 3) Diabetes educator consultation for injection training 4) Consider medication adherence assessment tools 5) Monitor for hypoglycemia especially with kidney disease"
    }
  },
  "message": "Sequential health analysis completed successfully"
}
```

#### `POST /analyze/all`
Executes all three analysis types (simple, parallel, sequential) and returns consolidated results.

**Use Case**: Comprehensive analysis when multiple perspectives are needed for complex clinical decisions.

**Request Body:**
```json
{
  "health_data": "Complete patient data with multiple medications and comorbidities"
}
```

**Response:**
```json
{
  "simple": {
    "status": "success",
    "data": { /* Simple analysis results */ },
    "message": "Simple analysis completed"
  },
  "parallel": {
    "status": "success", 
    "data": { /* Parallel analysis results */ },
    "message": "Parallel analysis completed"
  },
  "sequential": {
    "status": "success",
    "data": { /* Sequential analysis results */ },
    "message": "Sequential analysis completed"
  }
}
```

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "detail": "Invalid request format or missing required fields"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Analysis failed: [specific error message]"
}
```

#### Service Unavailable (ADK API Down)
```json
{
  "detail": "ADK API service unavailable. Please try again later."
}
```

## Rate Limiting

- **Development**: No rate limiting
- **Production**: 100 requests per minute per IP address
- **Burst**: Up to 20 requests in 10 seconds

## Request Examples

### cURL Examples

```bash
# Simple analysis
curl -X POST "http://localhost:8002/analyze/simple" \
  -H "Content-Type: application/json" \
  -d '{"health_data": "Patient data here..."}'

# Parallel analysis  
curl -X POST "http://localhost:8002/analyze/parallel" \
  -H "Content-Type: application/json" \
  -d '{"health_data": "Complex patient data..."}'

# Health check
curl -X GET "http://localhost:8002/health"
```

### Python Examples

```python
import requests

# Configuration
BASE_URL = "http://localhost:8002"

# Simple analysis
def analyze_prescription(health_data: str):
    response = requests.post(
        f"{BASE_URL}/analyze/simple",
        json={"health_data": health_data}
    )
    return response.json()

# Parallel analysis
def analyze_parallel(health_data: str):
    response = requests.post(
        f"{BASE_URL}/analyze/parallel", 
        json={"health_data": health_data}
    )
    return response.json()

# All analyses
def analyze_comprehensive(health_data: str):
    response = requests.post(
        f"{BASE_URL}/analyze/all",
        json={"health_data": health_data}
    )
    return response.json()

# Example usage
patient_data = """
Patient: Ana Silva, Age: 45, Hypertension
Current: Losartan 50mg daily
New: Ibuprofen 600mg TID for arthritis pain
"""

result = analyze_prescription(patient_data)
print(f"Criticality: {result['data']['results_criticality']['overall_criticality']}")
```

### JavaScript Examples

```javascript
// Fetch API example
async function analyzePatient(healthData) {
  try {
    const response = await fetch('http://localhost:8002/analyze/simple', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        health_data: healthData
      })
    });
    
    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Analysis failed:', error);
    throw error;
  }
}

// Axios example  
const axios = require('axios');

async function comprehensiveAnalysis(healthData) {
  try {
    const response = await axios.post('http://localhost:8002/analyze/all', {
      health_data: healthData
    });
    
    return response.data;
  } catch (error) {
    console.error('Analysis error:', error.response?.data);
    throw error;
  }
}
```

## Integration Patterns

### Healthcare Information Systems

```python
# Integration with hospital EHR system
class EHRIntegration:
    def __init__(self, api_base_url: str):
        self.api_url = api_base_url
        
    def analyze_prescription_order(self, patient_id: str, order_id: str):
        # Fetch patient data from EHR
        patient_data = self.get_patient_profile(patient_id)
        prescription = self.get_prescription_order(order_id)
        
        # Format for health analysis API
        health_data = self.format_for_analysis(patient_data, prescription)
        
        # Get AI analysis
        analysis = self.call_health_api(health_data)
        
        # Store results in EHR
        self.store_analysis_results(order_id, analysis)
        
        return analysis
```

### Clinical Decision Support Integration

```python
# CDS hooks integration pattern
def cds_order_select_hook(request):
    """
    Integrate with CDS Hooks for real-time prescription analysis
    """
    patient_data = request.get('context', {}).get('patient')
    orders = request.get('context', {}).get('draftOrders', [])
    
    alerts = []
    
    for order in orders:
        if order.get('resourceType') == 'MedicationRequest':
            health_data = format_cds_data(patient_data, order)
            analysis = analyze_prescription(health_data)
            
            if analysis['data']['results_criticality']['overall_criticality'] == 'high':
                alerts.append({
                    'summary': 'High-risk prescription detected',
                    'detail': analysis['data']['results_criticality']['description'],
                    'indicator': 'warning'
                })
    
    return {'cards': alerts}
```

## Monitoring and Analytics

### Usage Tracking
```python
# Track API usage patterns
usage_metrics = {
    "total_requests": 0,
    "requests_by_endpoint": {},
    "average_response_time": 0,
    "error_rate": 0,
    "criticality_distribution": {
        "low": 0,
        "medium": 0, 
        "high": 0
    }
}
```

### Performance Monitoring
```python
# Monitor response times and success rates
@app.middleware("http")
async def monitor_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Log metrics
    logger.info({
        "endpoint": str(request.url.path),
        "method": request.method,
        "status_code": response.status_code,
        "process_time": process_time
    })
    
    return response
```

## API Versioning

Current API version: **v1.0**

Future versions will maintain backward compatibility with deprecation notices for breaking changes.

```
# Version-specific endpoints (future)
/v1/analyze/simple    # Current
/v2/analyze/simple    # Future enhanced version
```