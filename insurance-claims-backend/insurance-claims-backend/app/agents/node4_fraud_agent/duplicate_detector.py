# """Duplicate document detection using hashing and vector search."""
# # app/agents/node4_fraud_agent/duplicate_detector.py

# import hashlib
# import json
# from typing import Dict, Any, List, Optional, Tuple
# from datetime import datetime, timedelta
# from motor.motor_asyncio import AsyncIOMotorCollection
# from app.database.mongodb import get_collection
# import numpy as np

# class DuplicateDetector:
#     """
#     Detects duplicate documents and claims using:
#     1. SHA-256 hashing for exact duplicates
#     2. Fuzzy matching for near-duplicates
#     3. MongoDB queries for cross-claim comparison
#     """
    
#     def __init__(self):
#         self.claims_collection: AsyncIOMotorCollection = get_collection("claims")
#         self.hash_cache = {}  # Cache for faster lookups
#         self.similarity_threshold = 0.85  # 85% similarity threshold
        
#         # Document fingerprint fields
#         self.fingerprint_fields = ['type', 'filename', 'content_preview', 'metadata']
        
#         # Time window for duplicate checking (90 days)
#         self.lookback_days = 90
    
#     async def detect(self, claim_data: Dict[str, Any]) -> Dict[str, Any]:
#         """
#         Detect duplicate documents across all claims
        
#         Returns:
#             Dict with score and indicators
#         """
#         claim_id = claim_data.get("claim_id")
#         documents = claim_data.get("documents", [])
        
#         if not documents:
#             return {"score": 0.0, "indicators": []}
        
#         indicators = []
#         duplicate_score = 0.0
        
#         # Check each document for duplicates
#         for idx, doc in enumerate(documents):
#             # 1. Check for exact duplicates using hash
#             exact_result = await self._check_exact_duplicate(doc, claim_id)
            
#             if exact_result["is_duplicate"]:
#                 duplicate_score += 0.3
#                 indicators.append({
#                     "type": "EXACT_DUPLICATE",
#                     "severity": "CRITICAL",
#                     "details": exact_result["details"],
#                     "confidence": 1.0,
#                     "score_impact": 0.3,
#                     "document_index": idx,
#                     "matched_claim": exact_result.get("matched_claim")
#                 })
#                 continue  # Skip further checks if exact duplicate found
            
#             # 2. Check for near-duplicates using content similarity
#             near_result = await self._check_near_duplicate(doc, claim_id)
            
#             if near_result["is_duplicate"]:
#                 duplicate_score += 0.2
#                 indicators.append({
#                     "type": "NEAR_DUPLICATE",
#                     "severity": "HIGH",
#                     "details": near_result["details"],
#                     "confidence": near_result["similarity"],
#                     "score_impact": 0.2,
#                     "document_index": idx,
#                     "similarity": near_result.get("similarity"),
#                     "matched_claim": near_result.get("matched_claim")
#                 })
            
#             # 3. Check for duplicate document pairs within same claim
#             if idx < len(documents) - 1:
#                 internal_result = self._check_internal_duplicates(documents, idx)
#                 if internal_result["is_duplicate"]:
#                     duplicate_score += 0.15
#                     indicators.append({
#                         "type": "INTERNAL_DUPLICATE",
#                         "severity": "MEDIUM",
#                         "details": internal_result["details"],
#                         "confidence": 0.95,
#                         "score_impact": 0.15,
#                         "document_indices": [idx, internal_result["matched_index"]]
#                     })
        
#         return {
#             "score": min(duplicate_score, 0.4),
#             "indicators": indicators
#         }
    
#     def _generate_document_hash(self, document: Dict) -> str:
#         """
#         Generate SHA-256 hash of document content
#         Used for exact duplicate detection
#         """
#         # Create a fingerprint from key fields
#         fingerprint_parts = []
        
#         # Add document type
#         fingerprint_parts.append(document.get("type", "unknown"))
        
#         # Add filename (if exists)
#         if "filename" in document:
#             fingerprint_parts.append(document["filename"])
        
#         # Add content preview (first 1000 chars)
#         if "content" in document:
#             fingerprint_parts.append(document["content"][:1000])
#         elif "content_preview" in document:
#             fingerprint_parts.append(document["content_preview"])
        
#         # Add metadata
#         if "metadata" in document:
#             fingerprint_parts.append(json.dumps(document["metadata"], sort_keys=True))
        
#         # Create fingerprint string
#         fingerprint = "|".join(str(p) for p in fingerprint_parts)
        
#         # Generate SHA-256 hash
#         return hashlib.sha256(fingerprint.encode()).hexdigest()
    
#     def _generate_content_fingerprint(self, document: Dict) -> str:
#         """
#         Generate a lighter fingerprint for content comparison
#         Used for near-duplicate detection
#         """
#         content = document.get("content", "")
#         if not content:
#             return ""
        
#         # Create chunks for similarity comparison
#         # Use first 500 chars, last 500 chars, and a sample from middle
#         content_len = len(content)
#         fingerprints = []
        
#         # Beginning
#         fingerprints.append(content[:500])
        
#         # Middle (if content is long enough)
#         if content_len > 1000:
#             mid = content_len // 2
#             fingerprints.append(content[mid:mid+500])
        
#         # End
#         if content_len > 500:
#             fingerprints.append(content[-500:])
        
#         # Join and hash
#         combined = "|".join(fingerprints)
#         return hashlib.md5(combined.encode()).hexdigest()
    
#     async def _check_exact_duplicate(self, document: Dict, current_claim_id: str) -> Dict:
#         """
#         Check if exact document hash exists in other claims
#         """
#         doc_hash = self._generate_document_hash(document)
        
#         # Check cache first
#         if doc_hash in self.hash_cache:
#             return {
#                 "is_duplicate": True,
#                 "details": f"Document matches claim {self.hash_cache[doc_hash]}",
#                 "matched_claim": self.hash_cache[doc_hash]
#             }
        
#         try:
#             # Calculate lookback date
#             lookback_date = datetime.now() - timedelta(days=self.lookback_days)
            
#             # Query MongoDB for duplicate hash
#             cursor = self.claims_collection.find({
#                 "documents.hash": doc_hash,
#                 "claim_id": {"$ne": current_claim_id},
#                 "submission_date": {"$gte": lookback_date.isoformat()}
#             }).limit(1)
            
#             duplicate = await cursor.to_list(length=1)
            
#             if duplicate:
#                 matched_claim = duplicate[0].get("claim_id")
#                 # Cache the result
#                 self.hash_cache[doc_hash] = matched_claim
                
#                 return {
#                     "is_duplicate": True,
#                     "details": f"Document matches claim {matched_claim}",
#                     "matched_claim": matched_claim
#                 }
            
#             return {"is_duplicate": False, "details": ""}
            
#         except Exception as e:
#             print(f"⚠️ Duplicate check failed: {e}")
#             return {"is_duplicate": False, "details": ""}
    
#     async def _check_near_duplicate(self, document: Dict, current_claim_id: str) -> Dict:
#         """
#         Check for near-duplicate documents using content similarity
#         """
#         content = document.get("content", "")
#         if not content or len(content) < 100:
#             return {"is_duplicate": False, "details": ""}
        
#         content_fp = self._generate_content_fingerprint(document)
        
#         try:
#             # Look for similar content fingerprints
#             lookback_date = datetime.now() - timedelta(days=self.lookback_days)
            
#             cursor = self.claims_collection.find({
#                 "documents.content_fingerprint": {"$regex": f"^{content_fp[:10]}"},
#                 "claim_id": {"$ne": current_claim_id},
#                 "submission_date": {"$gte": lookback_date.isoformat()}
#             }).limit(5)
            
#             similar_claims = await cursor.to_list(length=5)
            
#             for claim in similar_claims:
#                 for doc in claim.get("documents", []):
#                     if doc.get("content_fingerprint") == content_fp:
#                         return {
#                             "is_duplicate": True,
#                             "details": f"Similar document found in claim {claim.get('claim_id')}",
#                             "similarity": 0.95,
#                             "matched_claim": claim.get("claim_id")
#                         }
            
#             return {"is_duplicate": False, "details": ""}
            
#         except Exception as e:
#             print(f"⚠️ Near-duplicate check failed: {e}")
#             return {"is_duplicate": False, "details": ""}
    
#     def _check_internal_duplicates(self, documents: List, current_idx: int) -> Dict:
#         """
#         Check for duplicate documents within the same claim
#         """
#         current_doc = documents[current_idx]
#         current_hash = self._generate_document_hash(current_doc)
        
#         for i in range(current_idx + 1, len(documents)):
#             other_hash = self._generate_document_hash(documents[i])
            
#             if current_hash == other_hash:
#                 return {
#                     "is_duplicate": True,
#                     "details": f"Duplicate documents within same claim (documents {current_idx} and {i})",
#                     "matched_index": i
#                 }
        
#         return {"is_duplicate": False, "details": ""}








"""Duplicate document detection using hashing and vector search."""
# app/agents/node4_fraud_agent/duplicate_detector.py

import hashlib
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorCollection
from app.database.mongodb import get_collection

class DuplicateDetector:
    """
    Detects duplicate documents and claims using hashing
    """
    
    def __init__(self):
        self.claims_collection = get_collection("claims")
        self.hash_cache = {}
        self.similarity_threshold = 0.85
        self.fingerprint_fields = ['type', 'filename', 'content_preview', 'metadata']
        self.lookback_days = 90
        
        if self.claims_collection is None:
            print("⚠️ DuplicateDetector: MongoDB not available - will use cache only")
    
    async def detect(self, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect duplicate documents"""
        claim_id = claim_data.get("claim_id")
        documents = claim_data.get("documents", [])
        
        if not documents:
            return {"score": 0.0, "indicators": []}
        
        indicators = []
        duplicate_score = 0.0
        
        for idx, doc in enumerate(documents):
            # Check cache for exact duplicates
            doc_hash = self._generate_document_hash(doc)
            
            if doc_hash in self.hash_cache:
                duplicate_score += 0.3
                indicators.append({
                    "type": "EXACT_DUPLICATE",
                    "severity": "CRITICAL",
                    "details": f"Document matches previously seen document",
                    "confidence": 1.0,
                    "score_impact": 0.3
                })
                continue
            
            # Add to cache
            self.hash_cache[doc_hash] = claim_id
            
            # Check internal duplicates within same claim
            if idx < len(documents) - 1:
                for j in range(idx + 1, len(documents)):
                    other_hash = self._generate_document_hash(documents[j])
                    if doc_hash == other_hash:
                        duplicate_score += 0.15
                        indicators.append({
                            "type": "INTERNAL_DUPLICATE",
                            "severity": "MEDIUM",
                            "details": f"Duplicate documents within same claim (docs {idx} and {j})",
                            "confidence": 0.95,
                            "score_impact": 0.15
                        })
        
        return {
            "score": min(duplicate_score, 0.4),
            "indicators": indicators
        }
    
    def _generate_document_hash(self, document: Dict) -> str:
        """Generate SHA-256 hash of document content"""
        fingerprint_parts = []
        
        fingerprint_parts.append(document.get("type", "unknown"))
        
        if "filename" in document:
            fingerprint_parts.append(document["filename"])
        
        if "content" in document:
            fingerprint_parts.append(document["content"][:500])
        
        fingerprint = "|".join(str(p) for p in fingerprint_parts)
        return hashlib.sha256(fingerprint.encode()).hexdigest()