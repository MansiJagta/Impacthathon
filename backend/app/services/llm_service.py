import json
import os
import requests
from typing import Any, Dict, List

class LLMService:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = "gemma3:4b"  # Found on user's system

    def _call_ollama(self, prompt: str, system_prompt: str = "") -> str:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "format": "json"
        }
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            res_text = response.json().get("response", "")
            print(f"DEBUG: Ollama Raw Response: {res_text[:200]}")
            return res_text
        except Exception as e:
            print(f"Ollama Call Error: {e}")
            return ""

    def extract_structured_data(self, text: str, document_type: str) -> Dict[str, Any]:
        """
        Extract structured information from OCR text using local Ollama.
        """
        system_prompt = "You are an expert insurance claim adjuster. Your task is to extract structured data from OCR text and return ONLY a valid JSON object."
        
        prompt = f"""
        Extract the following information from the provided OCR text of a {document_type} document.
        Return the data in a valid JSON format with these exact keys:
        - claimer_name (Full name of the person)
        - claimer_email
        - claimer_phone
        - claimer_address
        - policy_number
        - amount (Numerical value only)
        - date (DD/MM/YYYY)
        - summary (Brief description of content)

        OCR Text:
        {text[:2000]}
        """

        raw_response = self._call_ollama(prompt, system_prompt)
        try:
            return json.loads(raw_response)
        except Exception as e:
            print(f"Ollama JSON Parse Error: {e}\nRaw: {raw_response}")
            return {}

    def analyze_claim_context(self, documents_context: str) -> Dict[str, Any]:
        """
        Perform qualitative analysis on the entire claim context using Ollama.
        """
        system_prompt = "You are an insurance fraud expert. Analyze sequences of documents and return results in JSON format."
        
        prompt = f"""
        Analyze the following insurance claim document context for fraud and risk.
        Look for inconsistencies in names, dates, amounts, or missing critical info.
        Return a JSON object with:
        - risk_level (LOW, MEDIUM, HIGH, CRITICAL)
        - fraud_indicators (list of strings)
        - reasoning (detailed explanation)
        - extraction_confidence (0.0 to 1.0)

        Claim Context:
        {documents_context[:4000]}
        """

        raw_response = self._call_ollama(prompt, system_prompt)
        try:
            return json.loads(raw_response)
        except Exception as e:
            print(f"Ollama Analysis Parse Error: {e}")
            return {
                "risk_level": "UNKNOWN",
                "fraud_indicators": ["Local AI Error"],
                "reasoning": f"Error parsing Ollama response: {e}",
                "extraction_confidence": 0.5
            }

llm_service = LLMService()
