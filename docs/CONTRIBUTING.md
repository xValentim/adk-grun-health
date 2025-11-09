# 🤝 Contributing Guide

## Welcome Contributors

Thank you for your interest in contributing to the ADK Health Analysis System! This project aims to improve prescription safety in Brazil's public healthcare system (SUS), and every contribution helps save lives.

## Code of Conduct

This project is dedicated to providing a harassment-free experience for everyone. We are committed to:

- **Patient Safety First**: All contributions must prioritize patient safety and clinical accuracy
- **Evidence-Based Approach**: Changes should be grounded in clinical evidence and best practices
- **Inclusive Healthcare**: Solutions must be accessible to diverse populations and healthcare settings
- **Respectful Collaboration**: Maintain professional, respectful communication in all interactions

## Getting Started

### Prerequisites

- **Python 3.10+**
- **Docker & Docker Compose**
- **Git** with basic knowledge of branching/merging
- **Google API Key** for ADK development
- **Basic understanding** of healthcare terminology (helpful but not required)

### Development Setup

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/your-username/adk-grun-health.git
cd adk-grun-health

# Set up development environment
cp .env.example .env
# Add your GOOGLE_API_KEY to .env

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Start development services
docker-compose up --build

# Verify setup
curl http://localhost:8002/health
```

## Contribution Types

### 🤖 AI Agent Development

**Clinical Agent Improvements**
- Enhance prompt engineering for better clinical accuracy
- Add new clinical decision rules based on evidence
- Improve agent response schemas for healthcare integration
- Add support for new medication classes or conditions

**Example: Adding a new drug interaction check**
```python
# team/parallel_analyzer_agent/subagents/drug_analysis_agent/agent.py

# Add to system instructions
additional_instructions = """
WARFARIN INTERACTIONS:
- Amiodarone: Major interaction, reduce warfarin dose by 25-50%
- NSAIDs: Increased bleeding risk, consider gastroprotection
- Antibiotics: Variable INR effects, increase monitoring frequency
"""
```

### 🏗️ Architecture & Infrastructure

**System Improvements**
- Optimize Docker containers for faster startup
- Enhance API error handling and recovery
- Add new deployment targets (Kubernetes, AWS, etc.)
- Improve monitoring and observability

**Example: Adding new health check**
```python
# api-server/main.py
@app.get("/health/detailed")
async def detailed_health_check():
    """Enhanced health check with agent-specific status"""
    agent_status = {}
    
    for agent_name in AGENTS.keys():
        try:
            # Test agent availability
            test_result = run_agent(agent_name, "test query")
            agent_status[agent_name] = "healthy"
        except Exception as e:
            agent_status[agent_name] = f"error: {str(e)}"
    
    return {
        "overall_status": "healthy",
        "agent_status": agent_status,
        "timestamp": datetime.utcnow()
    }
```

### 📚 Documentation

**Documentation Needs**
- Clinical validation studies and evidence
- Integration guides for EHR systems
- Deployment tutorials for different cloud providers
- API usage examples for various programming languages

### 🧪 Testing & Quality Assurance

**Testing Improvements**
- Clinical scenario test cases
- Performance benchmarking
- Integration testing with mock EHR systems
- Security and compliance validation

**Example: Clinical test case**
```python
# tests/test_clinical_scenarios.py
def test_high_risk_warfarin_interaction():
    """Test detection of major warfarin-amiodarone interaction"""
    
    patient_data = """
    Patient: Maria Silva, Age: 72, Weight: 65kg
    Current medications: Warfarin 5mg daily (INR 2.1 last week)
    New prescription: Amiodarone 200mg daily for atrial fibrillation
    Recent labs: INR 2.1, Creatinine 1.0 mg/dL
    """
    
    result = run_agent("parallel_analyzer_agent", patient_data)
    
    # Should detect high-risk drug interaction
    assert result["synthesized_results_criticality"]["level_drug"] == "high"
    assert "warfarin" in result["synthesized_results_criticality"]["description"].lower()
    assert "amiodarone" in result["synthesized_results_criticality"]["description"].lower()
```

## Development Workflow

### Branching Strategy

```
main
├── develop (integration branch)
├── feature/agent-improvements
├── feature/api-enhancements  
├── hotfix/critical-clinical-fix
└── docs/update-deployment-guide
```

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow coding standards (see below)
   - Add tests for new functionality
   - Update documentation as needed

3. **Test thoroughly**
   ```bash
   # Run local tests
   pytest tests/
   
   # Test with real scenarios
   docker-compose up
   # Test your changes with clinical scenarios
   ```

4. **Commit with descriptive messages**
   ```bash
   git commit -m "feat(agents): improve warfarin interaction detection
   
   - Add comprehensive warfarin-amiodarone interaction logic
   - Include dose adjustment recommendations  
   - Update clinical evidence references
   - Add test cases for major DDI scenarios"
   ```

5. **Submit pull request**
   - Provide clear description of changes
   - Include clinical rationale for agent modifications
   - Reference any relevant medical literature
   - Add screenshots for UI changes

## Coding Standards

### Python Code Style

```python
# Use type hints
def analyze_prescription(
    patient_data: str, 
    agent_type: str = "simple"
) -> Dict[str, Any]:
    """
    Analyze prescription safety using specified agent.
    
    Args:
        patient_data: Complete patient and prescription information
        agent_type: Type of analysis agent to use
        
    Returns:
        Dictionary containing analysis results and criticality levels
        
    Raises:
        AnalysisError: If agent execution fails
        ValidationError: If input data is invalid
    """
    
# Use descriptive variable names
def calculate_pediatric_dose(weight_kg: float, adult_dose_mg: float) -> float:
    """Calculate pediatric dose using body weight formula"""
    if weight_kg <= 0:
        raise ValueError("Weight must be positive")
        
    # Clark's rule for pediatric dosing
    pediatric_dose = (weight_kg / 70) * adult_dose_mg
    return round(pediatric_dose, 2)
```

### Agent Development Standards

```python
# Clear, clinical system instructions
system_instructions = """
You are a clinical pharmacist specializing in medication safety 
for Brazil's public healthcare system (SUS). 

CLINICAL CONTEXT:
- Patients may have limited healthcare access
- Focus on preventable adverse events with high impact
- Consider medication availability in public formulary
- Respect resource constraints in public healthcare

EVALUATION APPROACH:
- Conservative but clinically appropriate assessment
- Avoid over-alerting on theoretical interactions
- Prioritize actionable recommendations
- Include monitoring guidance when appropriate

OUTPUT FORMAT:
- Structured JSON with required fields
- Clear, jargon-free descriptions for healthcare providers
- Specific criticality levels (low/medium/high)
"""
```

### API Development Standards

```python
# Comprehensive error handling
@app.post("/analyze/simple")
async def simple_analysis(request: HealthDataRequest):
    try:
        # Validate input
        if not request.health_data.strip():
            raise HTTPException(
                status_code=400, 
                detail="Health data cannot be empty"
            )
        
        # Perform analysis
        result = run_agent("simple_prescription_agent", request.health_data)
        
        # Validate output
        validate_agent_output(result, "simple")
        
        return AnalysisResponse(
            status="success",
            data=result,
            message="Analysis completed successfully"
        )
        
    except ValidationError as e:
        logger.error("Validation error", error=str(e))
        raise HTTPException(status_code=422, detail=str(e))
        
    except Exception as e:
        logger.error("Analysis error", error=str(e))
        raise HTTPException(
            status_code=500, 
            detail="Analysis service temporarily unavailable"
        )
```

## Testing Guidelines

### Test Categories

1. **Unit Tests**: Individual functions and methods
2. **Integration Tests**: Service-to-service communication
3. **Clinical Tests**: Medical accuracy and safety
4. **Performance Tests**: Response times and throughput
5. **Security Tests**: Input validation and error handling

### Clinical Test Requirements

All agent changes must include clinical validation:

```python
# Required clinical test structure
clinical_scenarios = [
    {
        "name": "High-risk elderly polypharmacy",
        "patient_data": "Patient: 78y male, DM, HTN, CHF...",
        "expected_criticality": "high", 
        "rationale": "Multiple DDIs with narrow therapeutic index drugs",
        "evidence": "DOI: 10.1xxx/journal.reference"
    },
    {
        "name": "Pregnancy category X medication",
        "patient_data": "Patient: 28y female, pregnant (32 weeks)...",
        "expected_criticality": "high",
        "rationale": "Teratogenic medication in pregnancy",
        "evidence": "FDA Pregnancy Categories, WHO guidelines"
    }
]
```

## Clinical Evidence Requirements

### For Agent Modifications

When modifying clinical decision logic:

1. **Provide evidence**: Include references to peer-reviewed studies
2. **Brazilian context**: Consider local guidelines and formularies
3. **SUS applicability**: Ensure recommendations fit public healthcare constraints
4. **Expert review**: Get input from Brazilian healthcare professionals when possible

### Evidence Documentation Format

```markdown
## Clinical Evidence for [Feature Name]

### Background
Brief clinical context and problem statement.

### Evidence Base
- **Study 1**: [Citation] - Key findings relevant to implementation
- **Brazilian Data**: [Local studies] - Population-specific evidence  
- **Guidelines**: [Professional society recommendations]

### Implementation Rationale
How the evidence translates to specific agent behavior.

### Monitoring & Safety
Post-implementation monitoring plan and safety considerations.
```

## Deployment and Release

### Pre-Release Checklist

- [ ] All tests pass (unit, integration, clinical)
- [ ] Performance benchmarks meet requirements
- [ ] Security review completed
- [ ] Documentation updated
- [ ] Clinical evidence documented
- [ ] Breaking changes communicated

### Release Process

1. **Feature Freeze**: Stop adding features for release
2. **Testing Phase**: Comprehensive testing including clinical scenarios
3. **Documentation**: Update all relevant documentation
4. **Staging Deployment**: Deploy to staging environment
5. **Clinical Review**: Healthcare professional validation
6. **Production Deployment**: Phased rollout with monitoring
7. **Post-Release**: Monitor metrics and gather feedback

## Getting Help

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Email**: [maintainer-email] for security issues or sensitive topics

### Issue Templates

**Bug Report Template**
```markdown
## Bug Description
Clear description of the issue

## Clinical Impact
How does this affect patient safety or clinical accuracy?

## Reproduction Steps
1. Step one
2. Step two
3. Expected vs actual behavior

## Environment
- Deployment type (local/cloud)
- Agent types affected
- Error logs (if applicable)
```

**Feature Request Template**
```markdown
## Clinical Need
What clinical problem does this address?

## Proposed Solution
Detailed description of the proposed feature

## Evidence Base
Supporting clinical evidence or guidelines

## Implementation Considerations
Technical and clinical considerations for implementation
```

## Recognition

Contributors will be recognized in:
- **README.md** contributor list
- **CHANGELOG.md** for significant contributions
- **Academic publications** when applicable (with consent)

## Legal and Compliance

- All contributions must be original work or properly attributed
- Medical advice disclaimers must be maintained
- Patient privacy considerations must be respected
- Code must be compatible with project license (MIT)

Thank you for contributing to healthcare technology that saves lives! 🏥❤️