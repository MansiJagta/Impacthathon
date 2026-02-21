import argparse
import json
import os
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_claims import router as claims_router
from app.api.routes_underwriter import router as underwriter_router
from app.core.langgraph_builder import run_claim_workflow


def parse_args():
	parser = argparse.ArgumentParser(
		description="Run insurance claim workflow using LangGraph"
	)
	parser.add_argument(
		"documents",
		nargs="+",
		help="One or more document paths for ingestion",
	)
	parser.add_argument(
		"--claim-id",
		default=None,
		help="Optional claim id. Auto-generated when omitted.",
	)
	return parser.parse_args()


def run_cli():
	load_dotenv()
	args = parse_args()

	claim_id = args.claim_id or f"CLM-{uuid.uuid4().hex[:8].upper()}"
	final_state = run_claim_workflow(claim_id=claim_id, document_paths=args.documents)

	print(json.dumps(final_state, default=str, indent=2))


def create_app() -> FastAPI:
	load_dotenv()
	app = FastAPI(
		title="Intelli Claim API",
		description="FastAPI integration layer for LangGraph insurance claim workflow",
		version="1.0.0",
	)

	allowed_origins = [
		origin.strip()
		for origin in os.getenv(
			"CORS_ORIGINS",
			"http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000",
		).split(",")
		if origin.strip()
	]

	app.add_middleware(
		CORSMiddleware,
		allow_origins=allowed_origins,
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	@app.get("/api/health")
	def health_check():
		return {"status": "ok"}

	app.include_router(claims_router)
	app.include_router(underwriter_router)

	return app


app = create_app()


if __name__ == "__main__":
	run_cli()
