from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas.request_schema import ClaimRequest
from schemas.response_schema import ClaimProcessingResponse

from langgraph_flow.graph import claim_graph
from langgraph_flow.state import ClaimState


app = FastAPI(title="Claims Extraction Engine")


# ------------------------------------------------------------
# CORS (optional but useful for frontend testing)
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------------------------------------
# Health Check Endpoint
# ------------------------------------------------------------
@app.get("/")
def health_check():
    return {"status": "Extraction service running"}


# ------------------------------------------------------------
# Main Claim Processing Endpoint
# ------------------------------------------------------------
@app.post("/process-claim", response_model=ClaimProcessingResponse)
async def process_claim(request: ClaimRequest):

    # --------------------------------------------------------
    # Convert request → Graph State
    # --------------------------------------------------------

    # Extract correct document block
    documents = None

    if request.claim_type == "health":
        documents = (
            request.health_documents.model_dump()
            if request.health_documents
            else {}
        )

    elif request.claim_type == "motor":
        documents = (
            request.motor_documents.model_dump()
            if request.motor_documents
            else {}
        )

    elif request.claim_type == "death":
        documents = (
            request.death_documents.model_dump()
            if request.death_documents
            else {}
        )

    # Initial Graph State
    initial_state: ClaimState = {
        "claim_type": request.claim_type,
        "request_data": request.model_dump(),
        "documents": documents,
        "extracted_entities": None,
        "validation_results": None,
        "total_risk_score": None,
    }

    # --------------------------------------------------------
    # Invoke LangGraph
    # --------------------------------------------------------

    final_state = claim_graph.invoke(initial_state)

    # --------------------------------------------------------
    # Build API Response
    # --------------------------------------------------------

    return ClaimProcessingResponse(
        claim_type=request.claim_type,
        extracted_data=final_state.get("extracted_entities"),
        validation_result=final_state.get("validation_results"),
        status="processed"
    )