from typing import Dict, Any

from langgraph_flow.state import ClaimState
from nodes.extraction.ingestion.document_router import DocumentRouter


def extraction_node(state: ClaimState) -> Dict[str, Any]:
    """
    LangGraph extraction node.

    Responsibilities:
    - Read claim_type and documents from state
    - Route documents to correct extractors
    - Return structured extraction output
    - Fail safely (do not break graph)
    """

    claim_type = state.get("claim_type")
    documents = state.get("documents", {})

    if not claim_type:
        raise ValueError("claim_type missing in state")

    router = DocumentRouter()

    try:
        extracted_output = router.route(claim_type, documents)

        return {
            "extracted_entities": extracted_output
        }

    except Exception as e:
        # Fail-safe behavior
        # Do not crash entire graph
        print(f"[ExtractionNode] Error during extraction: {str(e)}")

        return {
            "extracted_entities": None,
            "extraction_error": str(e)
        }