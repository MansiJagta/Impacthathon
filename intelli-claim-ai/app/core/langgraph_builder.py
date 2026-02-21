import os
from typing import Any

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph
from langsmith import traceable

from app.core.state_schema import ClaimGraphState
from app.nodes.node1_extraction.extractor import extract_documents
from app.nodes.node2_cross_validation.validator import cross_validate
from app.nodes.node3_policy_coverage.policy_agent import (
	extract_claim_context,
	verify_policy_coverage,
)
from app.nodes.node3_policy_coverage.policy_fetcher import fetch_policy
from app.nodes.node4_fraud_detection.fraud_agent import fraud_detection
from app.nodes.node5_predictive.predictive_agent import predictive_analysis
from app.nodes.node6_explanation.explanation_generator import generate_explanation
from app.nodes.node7_decision.decision_agent import make_claim_decision
from app.nodes.node8_subrogation.subrogation_agent import analyze_subrogation
from app.services.hitl_service import store_high_risk_claim


os.environ.setdefault("LANGSMITH_PROJECT", "insurance-claim-ai")


@traceable(name="node1_document_ingestion")
def node1_document_ingestion(state: ClaimGraphState, config: RunnableConfig | None = None):
	document_paths = ((config or {}).get("configurable") or {}).get("document_paths")
	if not document_paths:
		raise ValueError("No document paths supplied. Pass config.configurable.document_paths")
	return {"node1_output": extract_documents(document_paths)}


@traceable(name="node2_cross_validation")
def node2_cross_validation(state: ClaimGraphState):
	return {"node2_output": cross_validate(state["node1_output"])}


@traceable(name="node3_policy_coverage")
def node3_policy_coverage(state: ClaimGraphState):
	return {"node3_output": verify_policy_coverage(state["node1_output"])}


@traceable(name="node4_fraud_detection")
def node4_fraud_detection(state: ClaimGraphState):
	context = extract_claim_context(state["node1_output"])
	policy_number = context.get("policy_number")
	policy = fetch_policy(policy_number) if policy_number else {}
	return {"node4_output": fraud_detection(state["node1_output"], policy or {})}


@traceable(name="node5_predictive")
def node5_predictive(state: ClaimGraphState):
	return {
		"node5_output": predictive_analysis(
			state["node1_output"],
			state["node2_output"],
			state["node3_output"],
			state["node4_output"],
		)
	}


@traceable(name="node6_explanation")
def node6_explanation(state: ClaimGraphState):
	return {
		"node6_output": generate_explanation(
			state["node2_output"],
			state["node3_output"],
			state["node4_output"],
		)
	}


@traceable(name="node8_subrogation")
def node8_subrogation(state: ClaimGraphState):
	return {"node8_output": analyze_subrogation(state["node1_output"])}


@traceable(name="node7_decision")
def node7_decision(state: ClaimGraphState):
	return {
		"node7_output": make_claim_decision(
			state["node3_output"],
			state["node4_output"],
		)
	}


def route_after_node7(state: ClaimGraphState) -> str:
	if state["node7_output"].get("human_review_required"):
		return "hitl_storage"
	return "automated_final_decision"


@traceable(name="hitl_storage")
def hitl_storage(state: ClaimGraphState):
	store_high_risk_claim(
		claim_id=state["claim_id"],
		node1_output=state["node1_output"],
		node2_output=state["node2_output"],
		node3_output=state["node3_output"],
		node4_output=state["node4_output"],
		explanation_output=state["node6_output"],
	)
	return {}


@traceable(name="automated_final_decision")
def automated_final_decision(state: ClaimGraphState):
	return {}


@traceable(name="build_claim_workflow")
def build_claim_workflow():
	graph = StateGraph(ClaimGraphState)

	graph.add_node("node1_document_ingestion", node1_document_ingestion)
	graph.add_node("node2_cross_validation", node2_cross_validation)
	graph.add_node("node3_policy_coverage", node3_policy_coverage)
	graph.add_node("node4_fraud_detection", node4_fraud_detection)
	graph.add_node("node5_predictive", node5_predictive)
	graph.add_node("node6_explanation", node6_explanation)
	graph.add_node("node8_subrogation", node8_subrogation)
	graph.add_node("node7_decision", node7_decision)
	graph.add_node("hitl_storage", hitl_storage)
	graph.add_node("automated_final_decision", automated_final_decision)

	graph.add_edge(START, "node1_document_ingestion")
	graph.add_edge("node1_document_ingestion", "node2_cross_validation")
	graph.add_edge("node2_cross_validation", "node3_policy_coverage")
	graph.add_edge("node3_policy_coverage", "node4_fraud_detection")
	graph.add_edge("node4_fraud_detection", "node5_predictive")
	graph.add_edge("node5_predictive", "node6_explanation")
	graph.add_edge("node6_explanation", "node8_subrogation")
	graph.add_edge("node8_subrogation", "node7_decision")

	graph.add_conditional_edges(
		"node7_decision",
		route_after_node7,
		{
			"hitl_storage": "hitl_storage",
			"automated_final_decision": "automated_final_decision",
		},
	)

	graph.add_edge("hitl_storage", END)
	graph.add_edge("automated_final_decision", END)

	return graph.compile()


@traceable(name="run_claim_workflow")
def run_claim_workflow(claim_id: str, document_paths: list[str]):
	app = build_claim_workflow()

	initial_state: ClaimGraphState = {
		"claim_id": claim_id,
		"node1_output": {},
		"node2_output": {},
		"node3_output": {},
		"node4_output": {},
		"node5_output": {},
		"node6_output": {},
		"node7_output": {},
		"node8_output": {},
	}

	return app.invoke(
		initial_state,
		config={"configurable": {"document_paths": document_paths}},
	)
