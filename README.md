# 🏥 ADK Health Analysis System

**AI-Powered Prescription Safety for Brazil's Public Healthcare System (SUS)**

An intelligent health analysis platform leveraging Google's Agent Development Kit (ADK) to prevent medication errors, reduce adverse drug reactions, and save lives in Brazil's unified healthcare system.

## 🎯 Impact for SUS

> SUS - Sistema Único de Saúde - is Brazil's publicly funded healthcare system, serving over 200 million people nationwide. However, medication errors and adverse drug reactions remain significant challenges, leading to preventable harm and increased healthcare costs.

### The Problem
- **1 in 8 patients** in Brazil's public healthcare network receive interacting drug combinations
- **1 in 25 patients** receive high-risk drug interactions that could lead to serious adverse events
- **24.7 million** Brazilians are served annually through Farmácia Popular alone (85% of municipalities)
- Global medication error costs: **~$42 billion USD annually**

*Source: Longitudinal analysis of 18-month EHR data from Blumenau (SC), Brazil (313,000 patients)*

In an ideal world, every prescription would pass through a pharmacist cross-checking a patient’s full medical record.

**In the real world of Brazil’s SUS—defined by scale, time pressure, and workforce shortages—this critical safety layer often disappears.**

Our platform brings it back: an AI-powered virtual pharmacist that analyzes prescriptions in real time and scales across the entire public network.

### Our Solution Impact

#### **Lives Saved Annually** 🫀
- **Conservative**: ~100-200 lives
- **Base Scenario**: ~200-400 lives  
- **Optimistic**: ~300-600 lives

#### **Adverse Events Prevented** ⚡
- **Conservative**: ~10,000-20,000 events/year
- **Base Scenario**: ~20,000-40,000 events/year
- **Optimistic**: ~30,000-60,000 events/year

#### **Healthcare Professional Time Saved** ⏰
- **500,000+ hours annually** freed up for patient care
- **300-500 FTE capacity** liberated for other critical activities
- **2 minutes saved** per automated prescription analysis

## 🔧 Architecture Overview

Our system deploys three intelligent analysis layers:

<!-- ```mermaid
graph TD
    A[Patient Data + Prescription] --  B[ADK API Server]
    B -- C[Simple Prescription Agent]
    B -- D[Parallel Analyzer Agent]  
    B -- E[Sequential Health Agent]
    
    D -- F[Drug Analysis]
    D -- G[Dose Analysis] 
    D -- H[Route Analysis]

    F -- I[Synthesizer]
    G -- I
    H -- I
    
    E -- J[General Health Assessment]
    J -- K[Treatment Impact Analysis]
    K -- L[Health Report Synthesis]
    
    C -- O[Healthcare Dashboard]
    I -- O
    L -- O
``` -->

```mermaid
graph TB
    subgraph "Client Layer"
        UI[Healthcare Dashboard]
        API_CLIENT[API Clients]
        LLM_CLIENT[LLM Clients]
    end
    
    subgraph "API Gateway Layer"
        FASTAPI[FastAPI Health Server<br/>Port 8002]
    end
    
    subgraph "Protocol Layer"  
        MCP[MCP Server<br/>Port 8001<br/>FastMCP<br/>Agent-as-a-Tool]
    end
    
    subgraph "AI Agent Layer"
        ADK[ADK API Server<br/>Port 8000<br/>Google ADK<br/>]
    end
    
    subgraph "Agent Types"
        SIMPLE[Simple Prescription Agent]
        PARALLEL[Parallel Analyzer Agent] 
        SEQUENTIAL[Sequential Health Agent]
        COMPLIANCE[Compliance Agent]
    end
    
    subgraph "Sub-Agents"
        DRUG[Drug Analysis Agent]
        DOSE[Dose Analysis Agent]
        ROUTE[Route Analysis Agent]
        SYNTH1[Synthesizer Agent]
        
        GENERAL[General Health Agent]
        TREATMENT[Treatment Assessment Agent]
        SYNTH2[Health Report Synthesizer]
    end

    subgraph "Remote-Agents (A2A)"
        SUS_COMPLIANCE[SUS Analysis Agent]
        NHS_COMPLIANCE[NHS Analysis Agent]
    end
    
    UI --> FASTAPI
    API_CLIENT --> FASTAPI
    FASTAPI --> ADK
    LLM_CLIENT --> MCP
    MCP --> ADK
    
    ADK --> SIMPLE
    ADK --> PARALLEL
    ADK --> SEQUENTIAL
    ADK --> COMPLIANCE
    
    PARALLEL --> DRUG
    PARALLEL --> DOSE  
    PARALLEL --> ROUTE
    DRUG --> SYNTH1
    DOSE --> SYNTH1
    ROUTE --> SYNTH1
    
    SEQUENTIAL --> GENERAL
    GENERAL --> TREATMENT
    TREATMENT --> SYNTH2

    COMPLIANCE --> SUS_COMPLIANCE
    COMPLIANCE --> NHS_COMPLIANCE
    
    style ADK fill:#4285f4,stroke:#333,stroke-width:2px,color:#fff
    style MCP fill:#34a853,stroke:#333,stroke-width:2px,color:#fff
    style FASTAPI fill:#ea4335,stroke:#333,stroke-width:2px,color:#fff
    style SUS_COMPLIANCE fill:#fbbc05,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5,color:#000
    style NHS_COMPLIANCE fill:#fbbc05,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5,color:#000
```

## Abstracted Architecture Diagram

In the above diagram, we can see how patient data and prescriptions flow through the ADK API Server to various specialized agents for analysis, culminating in a comprehensive report delivered to the healthcare dashboard. But we additionally have underlying infrastructure components that ensure smooth operation:

- **FastAPI Health API** for RESTful endpoints
- **MCP Server** for protocol communication

So, you can easily access the healthcare data and processing services through a robust and scalable architecture, for LLM Clients and Healthcare Dashboards. Lets look at the details:

![architecture documentation](imgs/full_architecture.png) 

> Each containerized service runs independently, allowing for scalability and maintainability. Note that we have one branch for each cloud run service block in diagram. You can find more details in: `adk-server`, `mcp-server`, and `fastapi` branches.

### Deployment Infrastructure
- **Google Cloud Run** for scalable containerization
- **Docker Compose** for local development and testing
- **Multi-agent architecture** for comprehensive analysis
- **REST API** for healthcare system integration

## 🤖 AI Agent Types

| Agent | Type | Analysis Focus | Output |
|-------|------|----------------|--------|
| **Simple Prescription** | Single Agent | Overall safety assessment | `overall_criticality` (low/medium/high) |
| **Parallel Analyzer** | Parallel Multi-Agent | Drug interactions, dosing, routes | `drug_criticality`, `dose_criticality`, `route_criticality` |
| **Sequential Health** | Sequential Multi-Agent | Comprehensive health impact | Treatment duration, compliance risk, lifestyle impact, monitoring frequency |
| **SUS Compliance** | A2A Remote Agent | Brazilian public health compliance | `overall_compliance`, `severity`, `issues`, `recommendations` |
| **NHS Compliance** | A2A Remote Agent | UK NHS guidelines compliance | `overall_compliance`, `severity`, `issues`, `recommendations` |

### Agent-to-Agent (A2A) Architecture for Critical Patient Routing

Our compliance agents utilize Google ADK's **Agent-to-Agent (A2A)** communication protocol, enabling remote deployment and specialized routing for critical patient scenarios:

#### **Why A2A for Compliance Agents?**
- **Regulatory Separation**: Healthcare compliance requires isolated, jurisdiction-specific analysis
- **Remote Expertise**: Deploy specialized agents in regions with local medical expertise
- **Critical Routing**: Route high-risk patients to appropriate healthcare system protocols
- **Scalable Compliance**: Independent scaling based on healthcare system demand

#### **SUS Compliance Agent** 🇧🇷
- **Purpose**: Validates prescriptions against Brazilian SUS guidelines and protocols
- **Critical Routing**: High-risk patients automatically routed to SUS-specific safety protocols
- **Local Context**: Considers SUS formulary availability and public health constraints
- **Output Schema**: Structured compliance assessment with specific SUS references

#### **NHS Compliance Agent** 🇬🇧  
- **Purpose**: Evaluates adherence to NICE guidelines and British National Formulary (BNF)
- **Critical Routing**: Routes complex cases through UK-specific clinical pathways
- **Guidelines Integration**: Real-time alignment with NHS protocols and best practices
- **Output Schema**: Compliance evaluation with NICE/BNF references and UK-specific recommendations

#### **Why NHS as Second System?**

We chose the **UK's National Health Service (NHS)** as our second compliance agent for three strategic reasons:

1. **Similar Public Healthcare Model**: Like SUS, the NHS is a universal, publicly funded healthcare system serving an entire nation, making it an ideal parallel for validation
2. **Excellent Documentation**: NICE guidelines and the British National Formulary (BNF) are exceptionally well-documented, structured, and publicly available.
3. **Proof of Concept for Global Expansion**: Demonstrates our A2A architecture's ability to support multiple jurisdictions with different regulatory frameworks.

#### **Remote Deployment Benefits**
```mermaid
graph TD
    A[Patient Data] --> B[Primary Analysis]
    B --> C{Risk Level?}
    C -->|High Risk| D[A2A SUS Agent]
    C -->|High Risk| E[A2A NHS Agent]
    C -->|Low/Medium| F[Local Processing]
    
    D --> G[SUS-Specific Routing]
    E --> H[NHS-Specific Routing]
    
    G --> I[Brazilian Healthcare Dashboard]
    H --> J[UK Healthcare Dashboard]
```

This A2A architecture ensures that critical patients receive jurisdiction-appropriate analysis while maintaining system performance and regulatory compliance.

### Clinical Decision Support Features
- **Drug-Drug Interaction (DDI) Detection**
- **Dose Appropriateness Validation**
- **Route Administration Safety**
- **Patient-Specific Risk Assessment**
- **Treatment Duration Analysis**
- **Compliance Risk Evaluation**
- **Healthcare System Compliance (SUS/NHS)**
- **Regulatory Guidelines Validation**
- **Critical Patient Routing via A2A**
- **Jurisdiction-Specific Safety Protocols**

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Google API Key (for ADK)
- Python 3.10+

### Local Deployment
```bash
# Clone repository
git clone https://github.com/xValentim/adk-grun-health
cd adk-grun-health

# Set environment variables
cp .env.example .env
# Edit .env with your GOOGLE_API_KEY

# Deploy all services
docker-compose up --build

# Services will be available at:
# - ADK API Server: http://localhost:8000
# - MCP Server: http://localhost:8001  
# - FastAPI Health API: http://localhost:8002
```

### Cloud Run Deployment
```bash
# Deploy to Google Cloud Run
gcloud run deploy adk-server-health --source . --dockerfile Dockerfile.adk --region europe-west1
gcloud run deploy a2a-server-health --source . --dockerfile Dockerfile.a2a --region europe-west1
gcloud run deploy mcp-server-health --source . --dockerfile Dockerfile.mcp --region europe-west1
gcloud run deploy fastapi-health --source . --dockerfile Dockerfile.api --region europe-west1
```

Or, you can just deploy each service individually as needed using console commands in the Google Cloud Console. We just synchronized deployment using github feature of cloud run deployment, you can find more details in the respective branches: `adk-server`, `feat/a2a-server`, `mcp-server`, and `fastapi`.

After deployment, you should be able to visualize this dashboard:

![dashboard example](imgs/dashboard_example.png)

## 📊 API Usage

### Health Analysis Endpoints

```python
import requests

# Simple prescription analysis
response = requests.post("http://localhost:8002/analyze/simple", 
    json={"health_data": "Patient: João Silva, Age: 65, Prescription: Warfarin 5mg..."})

# Parallel multi-agent analysis  
response = requests.post("http://localhost:8002/analyze/parallel",
    json={"health_data": "Patient data with multiple medications..."})

# Sequential comprehensive analysis
response = requests.post("http://localhost:8002/analyze/sequential", 
    json={"health_data": "Complete patient profile and treatment history..."})

# All analyses at once
response = requests.post("http://localhost:8002/analyze/all",
    json={"health_data": "Patient data for comprehensive assessment..."})
```

## MCP Usage

You can interact with the MCP server for protocol-based communication via LLM clients or other systems that support the MCP protocol. In our case, you can connect to MCP using the following example:

> To run this code, ensure you have `langchain-mcp-adapters` installed in your Python environment.

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

# Your Base MCP URL
BASE_MCP_URL = "https://localhost:8001/mcp" # Adjust as needed

client = MultiServerMCPClient(
    {
        "MyServer": {
            "url": BASE_MCP_URL,
            "transport": "streamable_http",
        }
    }
)
tools = await client.get_tools()
```

If everything is set up correctly, you should be able to see the available tools from the MCP server, like here:

```python
[StructuredTool(name='simple_prescription_analysis', description='Performs routine safety checks on patient prescriptions using a simple agent.\nThis agent provides overall prescription safety assessment with permissive evaluation criteria.\n\nArguments:\n    health_data: str - Patient health data and prescription information in text format.\nOutputs:\n    dict - Dictionary containing overall criticality level (low/medium/high) and description.', args_schema={'properties': {'health_data': {'type': 'string'}}, 'required': ['health_data'], 'type': 'object'}, metadata={'_meta': {'_fastmcp': {'tags': []}}}, response_format='content_and_artifact', coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000001B04F416F80>),
 StructuredTool(name='parallel_prescription_analysis', description='Analyzes prescription safety using parallel agents for drug, dose, and route analysis.\nThree specialist agents work concurrently to evaluate different aspects, then synthesize results.\n\nArguments:\n    health_data: str - Patient health data and prescription information in text format.\nOutputs:\n    dict - Dictionary with individual criticality levels for drug, dose, and route analysis plus synthesis description.', args_schema={'properties': {'health_data': {'type': 'string'}}, 'required': ['health_data'], 'type': 'object'}, metadata={'_meta': {'_fastmcp': {'tags': []}}}, response_format='content_and_artifact', coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000001B04F417910>),
 StructuredTool(name='sequential_health_analysis', description='Performs comprehensive health analysis using sequential agents for general health, treatment impact assessment, and synthesis.\nPipeline analyzes patient profile, evaluates treatment duration and impacts, then consolidates into actionable health report.\n\nArguments:\n    health_data: str - Patient health data and prescription information in text format.\nOutputs:\n    dict - Dictionary with treatment duration criticality, patient compliance risk, lifestyle impact, monitoring frequency, executive summary, and actionable recommendations.', args_schema={'properties': {'health_data': {'type': 'string'}}, 'required': ['health_data'], 'type': 'object'}, metadata={'_meta': {'_fastmcp': {'tags': []}}}, response_format='content_and_artifact', coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000001B04F417010>),
 StructuredTool(name='compliance_health_analysis', description="Analyzes patient health data focusing on compliance-related factors. You will use this agent to route healthcare compliance inquiries.\n\nWhen the user asks about SUS (Sistema Único de Saúde - Brazil), delegate to sus_compliance_client.\nWhen the user asks about NHS (National Health Service - UK), delegate to nhs_compliance_client.\n\nIf unclear, ask which health system they're referring to.\n\nArguments:\n    health_data: str - Patient health data and prescription information in text format.\nOutputs:\n    dict - Dictionary containing compliance analysis results.", args_schema={'properties': {'health_data': {'type': 'string'}}, 'required': ['health_data'], 'type': 'object'}, metadata={'_meta': {'_fastmcp': {'tags': []}}}, response_format='content_and_artifact', coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000001B04F417520>)]
```

## How can I use these tools?

Our system was designed to be easily integrated into existing healthcare applications. You can call the analysis tools directly from your application logic, passing in patient data and prescriptions, and receiving structured analysis results. You can reach the agents in 3 ways:

1. **Via FastAPI Health API**: Call REST endpoints for each analysis type
2. **Via MCP Protocol**: Use MCP clients to call agents as tools
3. **Direct ADK API Calls**: Interact directly with the ADK API server

Lets see cool and fast examples. 

### Example 1: Connect your LLM Client to MCP and call the Parallel Analyzer Agent

In this example, lets use github copilot to call the parallel analysis tool via MCP. In first step, use your MCP URL in VS Code to connect to MCP server and get the tools (Click [here](https://code.visualstudio.com/docs/copilot/customization/mcp-servers) for more details).

After connecting, you can just send a query like:
```txt

data: Subject ID: 0
Admission ID: 169938
Admission Date: 4323585540000
Discharge Date: 4324203900000
Insurance: Medicare
Age: None
Gender: M
Language: None
Marital Status: UNKNOWN (DEFAULT)
Ethnicity: WHITE
Creatinine: 1.1 mg/dL
Hemoglobin: 10.0 g/dL
Potassium: 3.7 mEq/L
Sodium: 142.0 mEq/L
Notes (24h Summary): None
Prescriptions:   
  - Drug: SW, Type: BASE, Dose: 100 ml, Form: None, Route: IV, Start: 2107-01-06 00:00:00, Stop: 2107-01-07 00:00:00
  - Drug: NS, Type: BASE, Dose: 500 ml, Form: None, Route: IV, Start: 2107-01-06 00:00:00, Stop: 2107-01-07 00:00:00
  - Drug: NS, Type: BASE, Dose: 500 ml, Form: None, Route: IV, Start: 2107-01-06 00:00:00, Stop: 2107-01-07 00:00:00
  - Drug: Iso-Osmotic Dextrose, Type: BASE, Dose: 200 ml, Form: None, Route: IV, Start: 2107-01-07 00:00:00, Stop: 2107-01-08 00:00:00
  - Drug: Fat Emulsion 20%, Type: BASE, Dose: 250 ml, Form: None, Route: IV, Start: 2107-01-07 00:00:00, Stop: 2107-01-11 00:00:00
  - Drug: SW, Type: BASE, Dose: 100 ml, Form: None, Route: IV, Start: 2107-01-08 00:00:00, Stop: 2107-01-08 00:00:00
  - Drug: Amino Acids 4.25% W/ Dextrose 5%, Type: BASE, Dose: 1000 ml, Form: None, Route: IV, Start: 2107-01-08 00:00:00, Stop: 2107-01-08 00:00:00
  - Drug: Amino Acids 4.25% W/ Dextrose 5%, Type: BASE, Dose: 1000 ml, Form: None, Route: IV, Start: 2107-01-08 00:00:00, Stop: 2107-01-09 00:00:00
  - Drug: NS, Type: BASE, Dose: 100 ml, Form: None, Route: IV, Start: 2107-01-09 00:00:00, Stop: 2107-01-10 00:00:00
  - Drug: D5W, Type: BASE, Dose: 50 ml, Form: None, Route: IV, Start: 2107-01-09 00:00:00, Stop: 2107-01-09 00:00:00
----------------------------------------


current_prescription: 
    {'drug': 'MethylPREDNISolone Sodium Succ', 
    'drug_type': 'BASE', 
    'dose_val': '1500-2900', 
    'dose_unit': 'mg', 
    'form': None, 
    'route': 'SC', 
    'starttime': '2107-01-10 00:00:00', 
    'stoptime': '2107-01-11 00:00:00'}

---

Please analyze the prescription safety using the Parallel Analyzer Agent and provide the output in few paragraphs.

```

Copilot will process, send the data to MCP server, call the Parallel Analyzer Agent, and return the analysis results directly in your VS Code window. You will se something like this:

![copilot parallel analysis](imgs/output_vs_code.png)
![copilot parallel analysis 2](imgs/output_vs_code_2.png)

### Example 2: Using LangChain MCP Adapter to call Simple Prescription Agent

In this example, we will use the LangChain MCP Adapter to connect to the MCP server and call the Simple Prescription Agent for a quick safety analysis.

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

client = MultiServerMCPClient(
    {
        "MyServer": {
            "url": "<BASE_MCP_URL>", # If you see this from DevPost, Use our deployed MCP URL in the site.
            "transport": "streamable_http",
        }
    }
)
tools = await client.get_tools()
agent = create_react_agent(
    "gpt-4o-mini", 
    tools
)

query = ... # The same example patient data and prescription as above

health_response = await agent.ainvoke(
    {"messages": [{"role": "user", "content": query}]}
)

for message in health_response['messages']:
    message.pretty_print()

```

The agent will process the input, call the Simple Prescription Agent via MCP, and return a structured safety analysis of the prescription.You should see output like this:

```txt
================================== Ai Message ==================================

The analysis of the prescription for MethylPREDNISolone Sodium Succ reveals several safety concerns that must be addressed. 

Firstly, in terms of dosage, the prescribed range of 1500-2900 mg administered subcutaneously (SC) is considered extremely high. This raises immediate flags regarding a potential decimal error or other significant mistakes in the dosing. Such a high dosage poses severe risks for adverse effects and warrants urgent verification by healthcare professionals. The assessment of the dosing reveals a **high criticality level**.

Secondly, the route of administration is also problematic. MethylPREDNISolone Sodium Succ is typically administered either intravenously or intramuscularly, making the subcutaneous route unusual. This necessitates further confirmation regarding its appropriateness for this specific patient scenario, leading to a **medium criticality level** for the route of administration.

From a drug safety perspective, MethylPREDNISolone Sodium Succ does not have any immediate critical safety concerns based on the provided information. There are no known black box warnings or contraindications associated with the drug itself under general circumstances, resulting in a **low criticality level** for the drug.

In summary, while the medication itself does not pose immediate dangers, the high dosage and questionable route of administration highlight significant safety issues that require prompt attention and verification. It is essential for healthcare providers to reassess the prescription to ensure patient safety and therapeutic effectiveness.
```

Also, you will see the structured output artifact with criticality levels (output from the agent-as-a-tool in MCP Server):

```json
{
    "state":{},
    "user_id":"u_test",
    "session_id":"s_e74d8be3",
    "dose_drug_analysis":"The MethylPREDNISolone dose of 1500-2900 mg SC is extremely high and concerning, potentially representing a decimal error or other significant error. This requires immediate verification due to the risk of severe adverse effects.  GRADE: HIGH",
    "route_drug_analysis":"The route of administration is subcutaneous. Subcutaneous administration of MethylPREDNISolone Sodium Succ is not a typical route. It is often administered intravenously or intramuscularly, thus, the subcutaneous route should be verified for appropriateness.\nGRADE: MEDIUM",
    "drug_analysis":"The MethylPREDNISolone Sodium Succ prescription does not raise immediate critical safety concerns. It's important to monitor for potential adverse effects, but there are no black box warnings or immediate contraindications apparent given the information provided. GRADE: LOW\n",
    "synthesized_results_criticality": {
        "level_drug":"LOW",
        "level_dose":"HIGH",
        "level_route":"MEDIUM",
        "description":"The dose of MethylPREDNISolone Sodium Succ is extremely high (1500-2900 mg SC), raising significant safety concerns that require immediate verification. Subcutaneous administration is also not a typical route for this medication and should be verified for appropriateness. The drug itself does not raise immediate concerns apart from these administration issues."
    }
}
```

## 🏗️ Technical Stack

- **AI Framework**: Google Agent Development Kit (ADK)
- **Backend**: FastAPI + Python 3.10
- **Protocol**: Model Context Protocol (MCP) via FastMCP
- **Deployment**: Docker + Google Cloud Run
- **Architecture**: Microservices with health checks and auto-scaling

## 📈 Clinical Evidence Base

Our system builds on evidence-based clinical decision support:
- **60% improvement** in problem identification without time overhead
- **Real EHR data** validation from Brazilian public healthcare
- **Conservative evaluation criteria** prioritizing clinical judgment over rigid algorithms
- **Multi-language support** (Portuguese/English) for diverse healthcare settings

## 🔒 Security & Compliance

- **HIPAA-compatible** architecture design
- **No patient data storage** - analysis only
- **Audit logging** for all clinical decisions
- **Role-based access** controls
- **Encrypted communication** between services

## 📚 Documentation

Detailed technical documentation available in the [`docs/`](docs/) directory:
- [Architecture Details](docs/architecture.md)
- [Agent Development Guide](docs/agents.md)
- [API Reference](docs/api.md)
- [Deployment Guide](docs/deployment.md)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- **Brazilian Public Healthcare System (SUS)** for inspiration and use case validation
- **Google ADK Team** for the agent development framework
- **Blumenau EHR Study** for real-world clinical validation data
- **Healthcare professionals** providing clinical expertise and validation

---

**Making prescription safety intelligent, accessible, and life-saving for millions of Brazilians.**

*Built with ❤️ for Brazil's public healthcare system*
