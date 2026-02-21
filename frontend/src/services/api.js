const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

/**
 * API service for interacting with the intelli-claim-ai backend.
 */
const api = {
    /**
     * Submit a new claim with supporting documents.
     * @param {FormData} formData - Multipart form data containing files and claim info.
     */
    async submitClaim(formData) {
        const response = await fetch(`${BASE_URL}/claims/submit-upload`, {
            method: 'POST',
            body: formData,
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to submit claim');
        }
        return response.json();
    },

    /**
     * Get claimer dashboard stats and recent claims.
     * @param {string} email - Claimer's email.
     */
    async getClaimerDashboard(email) {
        const response = await fetch(`${BASE_URL}/claims/dashboard/${encodeURIComponent(email)}`);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to fetch dashboard');
        }
        return response.json();
    },

    /**
     * Get full details for a specific claim.
     * @param {string} claimId - The unique claim ID.
     */
    async getClaimDetails(claimId) {
        const response = await fetch(`${BASE_URL}/claims/${claimId}`);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to fetch claim details');
        }
        return response.json();
    },

    /**
     * List claims with optional filtering.
     * @param {Object} params - Query parameters (claimer_email, status, claim_type, etc.)
     */
    async listClaims(params = {}) {
        const query = new URLSearchParams(params).toString();
        const response = await fetch(`${BASE_URL}/claims?${query}`);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to fetch claims');
        }
        return response.json();
    },

    /**
     * Get reviewer queue (pending/flagged claims).
     * @param {number} threshold - Fraud score threshold.
     */
    async getReviewerQueue(threshold = 0.6) {
        const response = await fetch(`${BASE_URL}/reviewer/queue?fraud_threshold=${threshold}`);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to fetch reviewer queue');
        }
        return response.json();
    },

    /**
     * Submit a reviewer decision.
     * @param {string} claimId 
     * @param {Object} decision - { decision: 'approve'|'reject'|'request_more_info', note, reviewer_name, reviewer_email }
     */
    async submitReviewDecision(claimId, decision) {
        const response = await fetch(`${BASE_URL}/reviewer/claims/${claimId}/decision`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(decision),
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to submit decision');
        }
        return response.json();
    },

    /**
     * Get admin dashboard metrics.
     */
    async getAdminDashboard() {
        const response = await fetch(`${BASE_URL}/admin/dashboard`);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to fetch admin dashboard');
        }
        return response.json();
    },

    /**
     * Get user activity for admin.
     */
    async getUserActivity() {
        const response = await fetch(`${BASE_URL}/admin/users/activity`);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to fetch user activity');
        }
        return response.json();
    }
};

export default api;
