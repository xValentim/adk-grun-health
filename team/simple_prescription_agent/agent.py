from google.adk.agents import Agent
# from google.adk.tools import google_search
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, Any

from dotenv import load_dotenv
import os

# RAG dependencies (usando SDKs nativos, sem LangChain)
import google.generativeai as genai
from pinecone import Pinecone

load_dotenv()

# Initialize Pinecone RAG (lazy initialization)
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
INDEX_NAME = "health-rag"

_pc = None
_index = None
_genai_configured = False

def _initialize_rag():
    """Initialize RAG components if not already done"""
    global _pc, _index, _genai_configured

    if _pc is None:
        _pc = Pinecone(api_key=PINECONE_API_KEY)
        _index = _pc.Index(INDEX_NAME)

    if not _genai_configured:
        genai.configure(api_key=GOOGLE_API_KEY)
        _genai_configured = True

async def query_medical_knowledge(
    query: str,
    top_k: int = 3,
    min_score: float = 0.7
) -> Dict[str, Any]:
    """
    Query the RENAME 2024 medical knowledge base for relevant information.

    Use this tool when you need authoritative information about:
    - Drug interactions and contraindications
    - Medication dosage guidelines
    - Administration routes and best practices
    - Clinical safety protocols from RENAME 2024

    Args:
        query: The medical question or topic to search for. Be specific.
        top_k: Number of relevant chunks to retrieve (default: 3, max: 10).
        min_score: Minimum similarity score threshold (0.0 to 1.0, default: 0.7).

    Returns:
        A dictionary containing relevant information chunks with sources and metadata.
    """
    try:
        # Initialize if needed
        _initialize_rag()

        # Validate inputs
        top_k = min(max(1, top_k), 10)
        min_score = max(0.0, min(1.0, min_score))

        # Generate embedding using native Google GenAI SDK (sem LangChain)
        embedding_result = genai.embed_content(
            model="models/gemini-embedding-001",
            content=query,
            task_type="retrieval_query"
        )
        query_embedding = embedding_result['embedding']

        # Search in Pinecone using native SDK (sem LangChain)
        results = _index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

        # Filter by minimum score and format results
        filtered_results = []
        for match in results['matches']:
            if match['score'] >= min_score:
                filtered_results.append({
                    'text': match['metadata']['text'],
                    'page': match['metadata'].get('page', 'unknown'),
                    'source': match['metadata'].get('source', 'RENAME 2024'),
                    'relevance_score': round(match['score'], 3)
                })

        if not filtered_results:
            return {
                'status': 'no_results',
                'message': f'No relevant information found for query: "{query}"',
                'query': query,
                'count': 0,
                'results': []
            }

        return {
            'status': 'success',
            'query': query,
            'count': len(filtered_results),
            'results': filtered_results,
            'note': 'Information from RENAME 2024 (Relação Nacional de Medicamentos Essenciais)'
        }

    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error querying knowledge base: {str(e)}',
            'query': query,
            'count': 0,
            'results': []
        }

class CriticalityOutput(BaseModel):
    level: str = Field(..., description="Level of criticality: low, medium, high.")
    description: str = Field(..., description="Description of the criticality assessment. Include key factors influencing the decision.") #

root_agent = Agent(
    name="simple_prescription_agent",
    model="gemini-2.0-flash",
    description="Clinical prescription safety agent for routine safety checks",
    instruction="""
    You are a clinical prescription safety agent that performs routine safety checks on patient prescriptions.

    CONTEXT: You are reviewing prescriptions written by licensed physicians. Your role is to perform a gentle safety review, understanding that medical professionals have already made informed clinical decisions based on their expertise and patient knowledge.

    AVAILABLE TOOLS:
    - query_medical_knowledge: Use this to consult RENAME 2024 (Brazil's National Essential Medicines List) for authoritative information about drug interactions, dosages, routes, and contraindications. Query when you need specific clinical guidance.

    Consider these safety aspects with flexibility:
    - Potential drug allergies (only if clearly documented)
    - Drug interactions (focus on major/severe ones only) - consult RENAME 2024 if unsure
    - Dosing appropriateness (allow for clinical judgment) - verify against RENAME 2024 when needed
    - Route suitability (trust physician's choice unless obviously problematic)
    - Basic contraindications (only clear-cut cases) - check RENAME 2024 for guidance

    GRADING CRITERIA (be generous and permissive):
    - HIGH: Only for truly dangerous situations that any reasonable physician would flag (e.g., documented severe allergy to prescribed drug, extreme overdose)
    - MEDIUM: For situations that might benefit from extra attention but are likely within acceptable clinical practice
    - LOW: For routine, standard prescriptions - this should be the most common grade

    IMPORTANT PRINCIPLES:
    - Default to LOW for most prescriptions - physicians are competent professionals
    - Give benefit of the doubt to clinical decisions
    - Remember that you don't have full patient context that the prescribing physician had
    - Focus on obvious safety issues, not minor clinical preferences
    - Trust that physicians considered patient-specific factors you may not see
    - Use the RENAME 2024 knowledge base to support your assessment when dealing with unfamiliar medications

    Provide a supportive, non-critical assessment that acknowledges the physician's expertise while noting any clear safety considerations.
    """,
    # tools=[query_medical_knowledge],
    output_schema=CriticalityOutput,
    output_key="results_criticality",
)
