<<<<<<< HEAD
import { C } from "../../constants/theme";
import { GaugeBar } from "../../components/GaugeBar";
import { useNavigate } from "react-router-dom";

const FRAUD_THRESHOLD = 0.6;

// 🔥 Sample Claims Data
const claims = [
    {
        id: "CL-2024-0890",
        type: "Health",
        amount: "₹1,20,000",
        hospital: "Apollo Hospital",
        patient: "Rajesh Kumar",
        dates: "10-15 Feb 2024",
        submittedBy: "John (claimer@email.com)",
        riskScore: 0.58,
        fraudScore: 0.75,
        status: "Pending"
    },
    {
        id: "CL-2024-0911",
        type: "Health",
        amount: "₹45,000",
        hospital: "Fortis",
        patient: "Amit Sharma",
        dates: "01-03 Feb 2024",
        submittedBy: "Rita (rita@email.com)",
        riskScore: 0.30,
        fraudScore: 0.22,
        status: "Pending"
    },
    {
        id: "CL-2024-0922",
        type: "Motor",
        amount: "₹2,80,000",
        hospital: "N/A",
        patient: "Vikram Singh",
        dates: "12 Feb 2024",
        submittedBy: "Arun (arun@email.com)",
        riskScore: 0.80,
        fraudScore: 0.82,
        status: "Pending"
    }
];

export default function ReviewQueue() {
    const navigate = useNavigate();

    // 🔥 Filter only high fraud claims
    const highFraudClaims = claims
        .filter(claim => claim.fraudScore >= FRAUD_THRESHOLD)
        .sort((a, b) => b.fraudScore - a.fraudScore); // highest first
=======
import { useState, useEffect } from "react";
import { C } from "../../constants/theme";
import { GaugeBar } from "../../components/GaugeBar";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";

const FRAUD_THRESHOLD = 0.6;

export default function ReviewQueue() {
    const navigate = useNavigate();
    const [claims, setClaims] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [notes, setNotes] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(null); // claimId being submitted

    useEffect(() => {
        async function fetchQueue() {
            setLoading(true);
            try {
                const response = await api.getReviewerQueue(FRAUD_THRESHOLD);
                setClaims(response.claims || []);
            } catch (err) {
                console.error("Queue fetch error:", err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }
        fetchQueue();
    }, []);

    const handleAction = async (claimId, decision) => {
        setIsSubmitting(claimId);
        try {
            const userRole = localStorage.getItem("userRole") || "reviewer";
            const userEmail = localStorage.getItem("userEmail") || "reviewer@example.com";

            await api.submitReviewDecision(claimId, {
                decision,
                note: notes[claimId] || "",
                reviewer_name: userRole,
                reviewer_email: userEmail
            });

            alert(`Claim ${decision}ed successfully!`);
            setClaims(prev => prev.filter(c => c.claim_id !== claimId));
        } catch (err) {
            alert(`Failed to save decision: ${err.message}`);
        } finally {
            setIsSubmitting(null);
        }
    };

    const handleNoteChange = (claimId, val) => {
        setNotes(prev => ({ ...prev, [claimId]: val }));
    };

    if (loading) return <div style={{ padding: 40, color: C.muted }}>Loading reviewer queue...</div>;
    if (error) return <div style={{ padding: 40, color: C.red }}>Error: {error}</div>;
>>>>>>> f930c12 (update project before sync)

    return (
        <div>

            {/* If no high fraud claims */}
<<<<<<< HEAD
            {highFraudClaims.length === 0 && (
=======
            {claims.length === 0 && (
>>>>>>> f930c12 (update project before sync)
                <div style={{
                    background: C.panel,
                    border: `1px solid ${C.border}`,
                    padding: 40,
                    borderRadius: 16,
                    textAlign: "center",
                    color: C.muted
                }}>
                    No high-risk claims for manual review.
                </div>
            )}

<<<<<<< HEAD
            {highFraudClaims.map((claim) => (
                <div
                    key={claim.id}
=======
            {claims.map((claim) => (
                <div
                    key={claim.claim_id}
>>>>>>> f930c12 (update project before sync)
                    style={{
                        background: C.panel,
                        border: `1px solid ${C.border}`,
                        borderRadius: 16,
                        padding: 32,
                        marginBottom: 40
                    }}
                >

                    {/* Header */}
                    <div style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        marginBottom: 32
                    }}>
                        <h2 style={{
                            color: C.text,
                            fontSize: 20,
                            fontWeight: 800
                        }}>
<<<<<<< HEAD
                            Claim {claim.id}
                        </h2>

                        <span style={{
                            background: "#713f12",
                            color: C.yellow,
=======
                            Claim {claim.claim_id}
                        </h2>

                        <span style={{
                            background: claim.fraud_score >= FRAUD_THRESHOLD ? "#713f12" : "#14532d",
                            color: claim.fraud_score >= FRAUD_THRESHOLD ? C.yellow : C.green,
>>>>>>> f930c12 (update project before sync)
                            padding: "4px 12px",
                            borderRadius: 20,
                            fontSize: 11,
                            fontWeight: 800
                        }}>
<<<<<<< HEAD
                            ⚠ High Fraud Risk
=======
                            {claim.fraud_score >= FRAUD_THRESHOLD ? "⚠ High Fraud Risk" : "✓ Verification Required"}
>>>>>>> f930c12 (update project before sync)
                        </span>
                    </div>

                    {/* Layout */}
                    <div style={{ display: "flex", gap: 48 }}>

                        {/* LEFT: Claim Details */}
                        <div style={{ flex: 1 }}>
                            <h4 style={{
                                color: C.muted,
                                fontSize: 11,
                                fontWeight: 800,
                                textTransform: "uppercase",
                                letterSpacing: 1,
                                marginBottom: 24,
                                paddingBottom: 12,
                                borderBottom: `1px solid ${C.border}`
                            }}>
                                Claim Details
                            </h4>

                            {[
<<<<<<< HEAD
                                { label: "Type", value: claim.type },
                                { label: "Amount", value: claim.amount },
                                { label: "Hospital", value: claim.hospital },
                                { label: "Patient", value: claim.patient },
                                { label: "Dates", value: claim.dates },
                                { label: "Submitted by", value: claim.submittedBy },
=======
                                { label: "Type", value: claim.claim_type },
                                { label: "Amount", value: `₹${claim.claim_amount.toLocaleString()}` },
                                { label: "Created", value: new Date(claim.created_at).toLocaleDateString() },
                                { label: "Summary", value: claim.summary },
>>>>>>> f930c12 (update project before sync)
                            ].map((item, i) => (
                                <div
                                    key={i}
                                    style={{
                                        display: "flex",
                                        justifyContent: "space-between",
                                        marginBottom: 20
                                    }}
                                >
                                    <span style={{ color: C.muted, fontSize: 13 }}>
                                        {item.label}
                                    </span>
                                    <span style={{ color: C.text, fontSize: 13, fontWeight: 700 }}>
                                        {item.value}
                                    </span>
                                </div>
                            ))}

                            <textarea
                                placeholder="Add notes (optional)…"
<<<<<<< HEAD
=======
                                value={notes[claim.claim_id] || ""}
                                onChange={(e) => handleNoteChange(claim.claim_id, e.target.value)}
>>>>>>> f930c12 (update project before sync)
                                style={{
                                    width: "100%",
                                    background: C.bg,
                                    border: `1px solid ${C.border}`,
                                    color: C.text,
                                    borderRadius: 8,
                                    padding: "10px",
                                    fontSize: 12,
                                    resize: "vertical",
                                    minHeight: 70,
                                    outline: "none",
                                    boxSizing: "border-box",
                                    marginTop: 20
                                }}
                            />
                        </div>

                        {/* RIGHT: AI Analysis */}
                        <div style={{ flex: 1 }}>
                            <h4 style={{
                                color: C.muted,
                                fontSize: 11,
                                fontWeight: 800,
                                textTransform: "uppercase",
                                letterSpacing: 1,
                                marginBottom: 24,
                                paddingBottom: 12,
                                borderBottom: `1px solid ${C.border}`
                            }}>
                                AI Analysis
                            </h4>

                            <div style={{ marginBottom: 24 }}>
<<<<<<< HEAD
                                <GaugeBar label="Risk Score" val={claim.riskScore} />
                                <GaugeBar label="Fraud Score" val={claim.fraudScore} />
                            </div>

                            <div style={{
                                background: "#ef444411",
                                border: "1px solid #ef444422",
                                padding: "12px",
                                borderRadius: 8,
                                color: "#f87171",
                                fontSize: 12
                            }}>
                                ⚠ This claim exceeded fraud threshold ({FRAUD_THRESHOLD})
                            </div>
=======
                                <GaugeBar label="Risk Score" val={claim.risk_score} />
                                <GaugeBar label="Fraud Score" val={claim.fraud_score} />
                            </div>

                            {claim.fraud_score >= FRAUD_THRESHOLD && (
                                <div style={{
                                    background: "#ef444411",
                                    border: "1px solid #ef444422",
                                    padding: "12px",
                                    borderRadius: 8,
                                    color: "#f87171",
                                    fontSize: 12
                                }}>
                                    ⚠ This claim exceeded fraud threshold ({FRAUD_THRESHOLD})
                                </div>
                            )}
>>>>>>> f930c12 (update project before sync)
                        </div>
                    </div>

                    {/* Decision Buttons */}
                    <div style={{
                        marginTop: 40,
                        paddingTop: 40,
                        borderTop: `1px solid ${C.border}`,
                        display: "flex",
                        gap: 16
                    }}>
<<<<<<< HEAD
                        <button style={{
                            flex: 1,
                            background: C.green,
                            color: "#fff",
                            border: "none",
                            padding: "16px",
                            borderRadius: 8,
                            fontWeight: 800,
                            cursor: "pointer"
                        }}>
                            Approve Claim
                        </button>

                        <button style={{
                            flex: 1,
                            background: C.red,
                            color: "#fff",
                            border: "none",
                            padding: "16px",
                            borderRadius: 8,
                            fontWeight: 800,
                            cursor: "pointer"
                        }}>
=======
                        <button
                            onClick={() => handleAction(claim.claim_id, "approve")}
                            disabled={isSubmitting === claim.claim_id}
                            style={{
                                flex: 2,
                                background: C.green,
                                color: "#fff",
                                border: "none",
                                padding: "16px",
                                borderRadius: 8,
                                fontWeight: 800,
                                cursor: isSubmitting === claim.claim_id ? "not-allowed" : "pointer",
                                opacity: isSubmitting === claim.claim_id ? 0.7 : 1
                            }}
                        >
                            Approve Claim
                        </button>

                        <button
                            onClick={() => handleAction(claim.claim_id, "reject")}
                            disabled={isSubmitting === claim.claim_id}
                            style={{
                                flex: 2,
                                background: C.red,
                                color: "#fff",
                                border: "none",
                                padding: "16px",
                                borderRadius: 8,
                                fontWeight: 800,
                                cursor: isSubmitting === claim.claim_id ? "not-allowed" : "pointer",
                                opacity: isSubmitting === claim.claim_id ? 0.7 : 1
                            }}
                        >
>>>>>>> f930c12 (update project before sync)
                            Reject & Flag
                        </button>

                        <button
<<<<<<< HEAD
                            onClick={() => navigate(`/claim-details/${claim.id}`)}
=======
                            onClick={() => navigate(`/claim-details/${claim.claim_id}`)}
>>>>>>> f930c12 (update project before sync)
                            style={{
                                flex: 1,
                                background: C.panel,
                                color: C.text,
                                border: `1px solid ${C.border}`,
                                padding: "16px",
                                borderRadius: 8,
                                fontWeight: 800,
                                cursor: "pointer"
                            }}
                        >
<<<<<<< HEAD
                            Request More Info
=======
                            Full Details →
>>>>>>> f930c12 (update project before sync)
                        </button>
                    </div>

                </div>
            ))}
        </div>
    );
}
<<<<<<< HEAD
=======

>>>>>>> f930c12 (update project before sync)
