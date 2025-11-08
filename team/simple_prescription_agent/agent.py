from google.adk.agents import Agent
# from google.adk.tools import google_search
from datetime import datetime
from pydantic import BaseModel, Field

from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

from dotenv import load_dotenv
import os

load_dotenv()

# ask_vertex_retrieval = VertexAiRagRetrieval(
#     name='retrieve_rag_documentation',
#     description=(
#         'Use this tool to retrieve documentation and reference materials for the question from the RAG corpus,'
#     ),
#     rag_resources=[
#         rag.RagResource(
#             # please fill in your own rag corpus
#             # here is a sample rag corpus for testing purpose
#             # e.g. projects/123/locations/us-central1/ragCorpora/456
#             rag_corpus=os.environ.get("RAG_CORPUS")
#         )
#     ],
#     similarity_top_k=5,
#     vector_distance_threshold=0.6,
# )

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

    Consider these safety aspects with flexibility:
    - Potential drug allergies (only if clearly documented)
    - Drug interactions (focus on major/severe ones only)
    - Dosing appropriateness (allow for clinical judgment)
    - Route suitability (trust physician's choice unless obviously problematic)
    - Basic contraindications (only clear-cut cases)

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

    Provide a supportive, non-critical assessment that acknowledges the physician's expertise while noting any clear safety considerations.
    """,
    # tools=[google_search],
    # tools=[ask_vertex_retrieval],
    output_schema=CriticalityOutput,
    output_key="results_criticality",
)
