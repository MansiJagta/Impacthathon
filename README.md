uvicorn app.main:app --reload

example request json : 

{
  "claim_type": "health",
  "health_documents": {
    "claim_form": {
      "filename": "health_claim_form.pdf",
      "content_type": "application/pdf",
      "file_path": "C:/Users/Asus/Desktop/sample_docs/health_claim_form.pdf",
      "base64_content": null
    },
    "id_proof": {
      "filename": "aadhaar.jpg",
      "content_type": "image/jpeg",
      "file_path": "C:/Users/Asus/Desktop/InsureAI/data/health/id_proof/aadhar/Adhar_1.jpg",
      "base64_content": null
    },
    "discharge_summary": {
      "filename": "discharge_summary.pdf",
      "content_type": "application/pdf",
      "file_path": "C:/Users/Asus/Desktop/sample_docs/discharge_summary.pdf",
      "base64_content": null
    },
    "hospital_bills": {
      "filename": "hospital_bill.pdf",
      "content_type": "application/pdf",
      "file_path": "C:/Users/Asus/Desktop/sample_docs/hospital_bill.pdf",
      "base64_content": null
    },
    "medical_prescriptions": {
      "filename": "prescription.pdf",
      "content_type": "application/pdf",
      "file_path": "C:/Users/Asus/Desktop/sample_docs/prescription.pdf",
      "base64_content": null
    }
  },
  "motor_documents": null,
  "death_documents": null,
  "policy_number": "HLT-2024-0001",
  "claim_id": "CLM-H-001"
}

validation result : 

{
  "checks": [
    {
      "check_name": "name_match_check",
      "score": 0.7,
      "confidence": 0.92,
      "status": "fail",
      "message": "Name mismatch between ID Proof and Claim Form",
      "metadata": {
        "claim_form_name": "Rahul Sharma",
        "id_proof_name": "Rohit Sharma"
      }
    },
    {
      "check_name": "required_docs_check",
      "score": 0.0,
      "confidence": 1.0,
      "status": "pass",
      "message": "All required documents present"
    }
  ],
  "total_risk_score": 0.52,
  "risk_category": "medium",
  "recommended_action": "manual_review"
}