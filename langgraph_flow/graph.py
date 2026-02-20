from langgraph.graph import StateGraph, END

from langgraph_flow.state import ClaimState

# Import nodes
from nodes.extraction.node import extraction_node
from nodes.cross_validation.node import cross_validation_node


# ============================================================
# Build Graph
# ============================================================

def build_claim_graph():
    """
    Builds and compiles the claim processing LangGraph.
    """

    # 1️⃣ Initialize graph with state schema
    builder = StateGraph(ClaimState)

    # 2️⃣ Register Nodes
    builder.add_node("extraction", extraction_node)
    builder.add_node("validation", cross_validation_node)

    # 3️⃣ Define Flow
    # builder.set_entry_point("extraction")
    # builder.add_edge("extraction", END)
    builder.set_entry_point("extraction")
    builder.add_edge("extraction", "validation")
    builder.add_edge("validation", END)

    # 4️⃣ Compile Graph
    graph = builder.compile()

    return graph


# ============================================================
# Singleton Graph Instance
# ============================================================

claim_graph = build_claim_graph()