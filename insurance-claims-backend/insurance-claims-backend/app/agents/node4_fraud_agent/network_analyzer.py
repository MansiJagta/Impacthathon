"""Network analysis for fraud ring detection."""
# app/agents/node4_fraud_agent/network_analyzer.py

import networkx as nx
from typing import Dict, Any, List, Tuple, Optional
from collections import defaultdict
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorCollection
from app.database.mongodb import get_collection
import numpy as np

class NetworkAnalyzer:
    """
    Network analysis for fraud ring detection
    Identifies suspicious connections between:
    - Claimants and providers
    - Claimants and attorneys
    - Providers and other providers
    - Shared contact information
    """
    
    def __init__(self):
        self.graph = nx.Graph()
        self.claims_collection: AsyncIOMotorCollection = get_collection("claims")
        
        # Suspicious thresholds
        self.max_claims_per_provider = 10  # per month
        self.max_claims_per_claimant = 3   # per year
        self.max_shared_entities = 5       # max claimants per provider
        self.time_window_days = 90
        
        # Weights for different connection types
        self.connection_weights = {
            "claimant_provider": 0.3,
            "shared_address": 0.4,
            "shared_phone": 0.4,
            "shared_email": 0.4,
            "shared_attorney": 0.35,
            "temporal_proximity": 0.2
        }
        
        # Cache for network data
        self.network_cache = {}
        self.last_refresh = None
    
    async def analyze(self, claim_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze network connections for fraud indicators
        
        Returns:
            Dict with score and indicators
        """
        indicators = []
        network_score = 0.0
        
        # Refresh network graph periodically
        await self._refresh_network_graph()
        
        # Extract entities from current claim
        current_entities = self._extract_entities(claim_data)
        
        # 1. Check provider connections
        provider_score, provider_indicators = await self._analyze_provider_network(
            current_entities
        )
        network_score += provider_score
        indicators.extend(provider_indicators)
        
        # 2. Check claimant history and connections
        claimant_score, claimant_indicators = await self._analyze_claimant_network(
            current_entities
        )
        network_score += claimant_score
        indicators.extend(claimant_indicators)
        
        # 3. Check for fraud rings (dense subgraphs)
        ring_score, ring_indicators = self._detect_fraud_rings(current_entities)
        network_score += ring_score
        indicators.extend(ring_indicators)
        
        # 4. Check shared attributes
        shared_score, shared_indicators = self._check_shared_attributes(current_entities)
        network_score += shared_score
        indicators.extend(shared_indicators)
        
        # 5. Check temporal patterns
        temporal_score, temporal_indicators = await self._analyze_temporal_patterns(
            current_entities
        )
        network_score += temporal_score
        indicators.extend(temporal_indicators)
        
        return {
            "score": min(network_score, 0.3),
            "indicators": indicators
        }
    
    def _extract_entities(self, claim_data: Dict) -> Dict:
        """Extract all entities from a claim"""
        return {
            "claim_id": claim_data.get("claim_id"),
            "claimant_name": claim_data.get("claimant_name"),
            "claimant_id": claim_data.get("claimant_id"),
            "provider_name": claim_data.get("provider_name"),
            "provider_id": claim_data.get("provider_id"),
            "attorney_name": claim_data.get("attorney_name"),
            "attorney_id": claim_data.get("attorney_id"),
            "phone": claim_data.get("claimant_phone", claim_data.get("phone")),
            "email": claim_data.get("claimant_email", claim_data.get("email")),
            "address": claim_data.get("claimant_address", claim_data.get("address")),
            "incident_date": claim_data.get("incident_date"),
            "submission_date": claim_data.get("submission_date")
        }
    
    async def _refresh_network_graph(self):
        """Refresh the network graph with recent claims"""
        now = datetime.now()
        
        # Refresh if cache is older than 1 hour
        if (self.last_refresh and 
            (now - self.last_refresh).seconds < 3600):
            return
        
        print("🔄 Refreshing network graph...")
        
        # Clear existing graph
        self.graph.clear()
        
        # Get claims from last 90 days
        lookback_date = now - timedelta(days=self.time_window_days)
        
        cursor = self.claims_collection.find({
            "submission_date": {"$gte": lookback_date.isoformat()}
        }).limit(1000)
        
        recent_claims = await cursor.to_list(length=1000)
        
        # Build graph
        for claim in recent_claims:
            self._add_claim_to_graph(claim)
        
        self.last_refresh = now
        print(f"✅ Network graph built with {self.graph.number_of_nodes()} nodes")
    
    def _add_claim_to_graph(self, claim: Dict):
        """Add a claim and its entities to the graph"""
        claim_id = claim.get("claim_id")
        claimant = claim.get("claimant_name")
        provider = claim.get("provider_name")
        attorney = claim.get("attorney_name")
        phone = claim.get("claimant_phone", claim.get("phone"))
        email = claim.get("claimant_email", claim.get("email"))
        address = claim.get("claimant_address", claim.get("address"))
        
        # Add nodes
        if claimant:
            self.graph.add_node(claimant, type="claimant", claims=[claim_id])
        
        if provider:
            self.graph.add_node(provider, type="provider", claims=[claim_id])
        
        if attorney:
            self.graph.add_node(attorney, type="attorney", claims=[claim_id])
        
        if phone:
            self.graph.add_node(phone, type="phone")
        
        if email:
            self.graph.add_node(email, type="email")
        
        if address:
            self.graph.add_node(address, type="address")
        
        # Add edges
        if claimant and provider:
            self.graph.add_edge(claimant, provider, type="claimant_provider", claim_id=claim_id)
        
        if claimant and attorney:
            self.graph.add_edge(claimant, attorney, type="claimant_attorney", claim_id=claim_id)
        
        if claimant and phone:
            self.graph.add_edge(claimant, phone, type="has_phone", claim_id=claim_id)
        
        if claimant and email:
            self.graph.add_edge(claimant, email, type="has_email", claim_id=claim_id)
        
        if claimant and address:
            self.graph.add_edge(claimant, address, type="has_address", claim_id=claim_id)
    
    async def _analyze_provider_network(self, entities: Dict) -> Tuple[float, List[Dict]]:
        """Analyze provider for suspicious patterns"""
        indicators = []
        score = 0.0
        
        provider_name = entities.get("provider_name")
        if not provider_name or provider_name not in self.graph:
            return 0.0, []
        
        # Get all claims connected to this provider
        provider_node = self.graph.nodes[provider_name]
        connected_claims = provider_node.get("claims", [])
        claim_count = len(connected_claims)
        
        # Check claim volume
        if claim_count > self.max_claims_per_provider:
            score += 0.2
            indicators.append({
                "type": "HIGH_VOLUME_PROVIDER",
                "severity": "HIGH",
                "details": f"Provider has {claim_count} claims in last {self.time_window_days} days",
                "confidence": 0.9,
                "score_impact": 0.2,
                "claim_count": claim_count
            })
        
        # Get connected claimants
        neighbors = list(self.graph.neighbors(provider_name))
        claimants = [n for n in neighbors if self.graph.nodes[n].get("type") == "claimant"]
        
        # Check if provider works with many claimants
        if len(claimants) > self.max_shared_entities:
            score += 0.15
            indicators.append({
                "type": "PROVIDER_NETWORK",
                "severity": "HIGH",
                "details": f"Provider connected to {len(claimants)} different claimants",
                "confidence": 0.85,
                "score_impact": 0.15,
                "claimant_count": len(claimants)
            })
        
        # Check for known fraudulent providers (mock)
        if provider_name in ["Quick Fix Garage", "Questionable Clinic", "Fake Provider"]:
            score += 0.3
            indicators.append({
                "type": "KNOWN_FRAUD_PROVIDER",
                "severity": "CRITICAL",
                "details": f"Provider '{provider_name}' is on fraud watchlist",
                "confidence": 0.95,
                "score_impact": 0.3
            })
        
        return score, indicators
    
    async def _analyze_claimant_network(self, entities: Dict) -> Tuple[float, List[Dict]]:
        """Analyze claimant history and connections"""
        indicators = []
        score = 0.0
        
        claimant_name = entities.get("claimant_name")
        if not claimant_name or claimant_name not in self.graph:
            return 0.0, []
        
        # Get all claims by this claimant
        claimant_node = self.graph.nodes[claimant_name]
        connected_claims = claimant_node.get("claims", [])
        claim_count = len(connected_claims)
        
        # Check claim frequency
        if claim_count > self.max_claims_per_claimant:
            score += 0.2
            indicators.append({
                "type": "FREQUENT_CLAIMANT",
                "severity": "HIGH",
                "details": f"Claimant has {claim_count} claims in last {self.time_window_days} days",
                "confidence": 0.85,
                "score_impact": 0.2,
                "claim_count": claim_count
            })
        
        # Get connected providers
        neighbors = list(self.graph.neighbors(claimant_name))
        providers = [n for n in neighbors if self.graph.nodes[n].get("type") == "provider"]
        
        # Check if claimant switches providers frequently
        if len(providers) > 3:
            score += 0.15
            indicators.append({
                "type": "PROVIDER_SHOPPING",
                "severity": "MEDIUM",
                "details": f"Claimant has used {len(providers)} different providers",
                "confidence": 0.8,
                "score_impact": 0.15,
                "provider_count": len(providers)
            })
        
        # Check for shared attributes with other claimants
        phone = entities.get("phone")
        email = entities.get("email")
        address = entities.get("address")
        
        if phone and phone in self.graph:
            phone_neighbors = list(self.graph.neighbors(phone))
            other_claimants = [n for n in phone_neighbors 
                               if n != claimant_name and self.graph.nodes[n].get("type") == "claimant"]
            
            if other_claimants:
                score += 0.2
                indicators.append({
                    "type": "SHARED_PHONE",
                    "severity": "HIGH",
                    "details": f"Phone number shared with {len(other_claimants)} other claimant(s)",
                    "confidence": 0.9,
                    "score_impact": 0.2,
                    "shared_with": other_claimants
                })
        
        return score, indicators
    
    def _detect_fraud_rings(self, entities: Dict) -> Tuple[float, List[Dict]]:
        """Detect dense subgraphs indicating fraud rings"""
        if self.graph.number_of_nodes() < 10:
            return 0.0, []
        
        indicators = []
        score = 0.0
        
        try:
            # Find communities (potential fraud rings)
            communities = list(nx.community.greedy_modularity_communities(self.graph))
            
            for community in communities:
                if len(community) > 5:  # Minimum ring size
                    # Check if current entities are in this community
                    claimant = entities.get("claimant_name")
                    provider = entities.get("provider_name")
                    
                    in_community = (claimant and claimant in community) or \
                                   (provider and provider in community)
                    
                    if in_community:
                        # Calculate density of this community
                        subgraph = self.graph.subgraph(community)
                        density = nx.density(subgraph)
                        
                        if density > 0.3:  # Densely connected
                            score += 0.2
                            indicators.append({
                                "type": "FRAUD_RING_DETECTED",
                                "severity": "CRITICAL",
                                "details": f"Entities part of dense fraud ring ({len(community)} nodes, density: {density:.2f})",
                                "confidence": 0.8,
                                "score_impact": 0.2,
                                "ring_size": len(community),
                                "density": density
                            })
        except Exception as e:
            print(f"⚠️ Fraud ring detection error: {e}")
        
        return score, indicators
    
    def _check_shared_attributes(self, entities: Dict) -> Tuple[float, List[Dict]]:
        """Check for shared attributes across claims"""
        indicators = []
        score = 0.0
        
        # This would query MongoDB for other claims with same attributes
        # Simplified for now
        
        return score, indicators
    
    async def _analyze_temporal_patterns(self, entities: Dict) -> Tuple[float, List[Dict]]:
        """Analyze temporal patterns in claim submissions"""
        indicators = []
        score = 0.0
        
        claimant_name = entities.get("claimant_name")
        if not claimant_name or claimant_name not in self.graph:
            return 0.0, []
        
        # Get claimant's claims with timestamps
        claimant_node = self.graph.nodes[claimant_name]
        claim_ids = claimant_node.get("claims", [])
        
        if len(claim_ids) < 2:
            return 0.0, []
        
        # Fetch claim timestamps
        timestamps = []
        for claim_id in claim_ids:
            cursor = self.claims_collection.find({"claim_id": claim_id})
            claim = await cursor.to_list(length=1)
            if claim:
                ts = claim[0].get("submission_date")
                if ts:
                    try:
                        timestamps.append(datetime.fromisoformat(ts.replace('Z', '+00:00')))
                    except:
                        pass
        
        if len(timestamps) >= 2:
            timestamps.sort()
            
            # Check for rapid successive claims
            for i in range(1, len(timestamps)):
                days_between = (timestamps[i] - timestamps[i-1]).days
                if days_between < 7:
                    score += 0.15
                    indicators.append({
                        "type": "RAPID_SUCCESSIVE_CLAIMS",
                        "severity": "HIGH",
                        "details": f"Claims filed only {days_between} days apart",
                        "confidence": 0.85,
                        "score_impact": 0.15,
                        "days_apart": days_between
                    })
                    break
        
        return score, indicators