import { useParams, useNavigate } from "react-router-dom";
<<<<<<< HEAD
import { useState } from "react";
import { C } from "../../constants/theme";
import { GaugeBar } from "../../components/GaugeBar";

const claims = [
    {
        id: "CL-2024-0890",
        type: "Health",
        amount: "₹1,20,000",
        hospital: "Apollo Hospital",
        patient: "Rajesh Kumar",
        dates: "10-15 Feb 2024",
        riskScore: 0.58,
        fraudScore: 0.75,
        policyNumber: "POL-7839201",
        email: "claimer@email.com",
        phone: "+91 98765 43210",
        address: "Chennai, Tamil Nadu, India",
        status: "PENDING_REVIEW",
        aiDecision: "FLAGGED_FOR_REVIEW",
        confidence: 0.42,
        reasoning: [
            { node: "Cross Validation", finding: "All documents consistent", confidence: 0.95 },
            { node: "Policy Coverage", finding: "Covered under Clause 4.2", confidence: 0.97 },
            { node: "Fraud Detection", finding: "Moderate anomaly detected", confidence: 0.75 },
            { node: "Predictive Analysis", finding: "Cost aligns with similar claims", confidence: 0.92 }
        ]
    }
];
=======
import { useState, useEffect } from "react";
import { C } from "../../constants/theme";
import { GaugeBar } from "../../components/GaugeBar";
import api from "../../services/api";
>>>>>>> f930c12 (update project before sync)

export default function ClaimDetailsPage() {
    const { id } = useParams();
    const navigate = useNavigate();
<<<<<<< HEAD
    const [showReasoning, setShowReasoning] = useState(false);
    const [note, setNote] = useState("");

    const claim = claims.find(c => c.id === id);

    if (!claim) {
        return <div style={{ padding: 40 }}>Claim not found.</div>;
    }
=======
    const [claim, setClaim] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showReasoning, setShowReasoning] = useState(false);
    const [note, setNote] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);

    useEffect(() => {
        async function fetchDetails() {
            setLoading(true);
            try {
                const data = await api.getClaimDetails(id);
                setClaim(data);
            } catch (err) {
                console.error("Error fetching claim details:", err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }
        fetchDetails();
    }, [id]);

    const handleAction = async (decision) => {
        setIsSubmitting(true);
        try {
            const userRole = localStorage.getItem("userRole") || "reviewer";
            const userEmail = localStorage.getItem("userEmail") || "reviewer@example.com";

            await api.submitReviewDecision(id, {
                decision,
                note,
                reviewer_name: userRole,
                reviewer_email: userEmail
            });

            alert(`Claim ${decision}ed successfully!`);
            navigate(-1);
        } catch (err) {
            alert(`Failed to save decision: ${err.message}`);
        } finally {
            setIsSubmitting(false);
        }
    };

    if (loading) return <div style={{ padding: 40, color: C.muted }}>Loading claim details...</div>;
    if (error) return <div style={{ padding: 40, color: C.red }}>Error: {error}</div>;
    if (!claim) return <div style={{ padding: 40 }}>Claim not found.</div>;

    const userRole = localStorage.getItem("userRole");
    const isReviewer = userRole === "reviewer" || userRole === "admin";
>>>>>>> f930c12 (update project before sync)

    return (
        <div style={{ padding: 40 }}>

            {/* Back */}
            <button
                onClick={() => navigate(-1)}
                style={{
                    marginBottom: 32,
                    background: C.panel,
                    border: `1px solid ${C.border}`,
                    color: C.text,
                    padding: "10px 16px",
                    borderRadius: 8,
                    cursor: "pointer"
                }}
            >
<<<<<<< HEAD
                ← Back to Review Queue
=======
                ← Back
>>>>>>> f930c12 (update project before sync)
            </button>

            <div style={{
                background: C.panel,
                border: `1px solid ${C.border}`,
                borderRadius: 16,
                padding: 32
            }}>

                {/* Header */}
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 32 }}>
                    <h2 style={{ color: C.text, fontWeight: 800 }}>
<<<<<<< HEAD
                        Full Claim Details – {claim.id}
=======
                        Full Claim Details – {claim.claim_id}
>>>>>>> f930c12 (update project before sync)
                    </h2>

                    <div style={{
                        background: "#6366f111",
                        border: "1px solid #6366f122",
                        padding: "8px 16px",
                        borderRadius: 8,
                        color: "#818cf8",
                        fontWeight: 700
                    }}>
                        STATUS: {claim.status}
                    </div>
                </div>

                {/* Risk Badges */}
                <div style={{ display: "flex", gap: 16, marginBottom: 32 }}>
                    <div style={{
<<<<<<< HEAD
                        background: "#ef444411",
                        border: "1px solid #ef444422",
                        padding: "10px 18px",
                        borderRadius: 8,
                        color: "#f87171",
                        fontWeight: 700
                    }}>
                        Fraud Score: {(claim.fraudScore * 100).toFixed(0)}%
                    </div>

                    <div style={{
                        background: "#eab30811",
                        border: "1px solid #eab30822",
                        padding: "10px 18px",
                        borderRadius: 8,
                        color: "#facc15",
                        fontWeight: 700
                    }}>
                        Risk Score: {(claim.riskScore * 100).toFixed(0)}%
=======
                        background: (claim.fraud_score > 0.6) ? "#ef444411" : "#22c55e11",
                        border: `1px solid ${(claim.fraud_score > 0.6) ? "#ef444422" : "#22c55e22"}`,
                        padding: "10px 18px",
                        borderRadius: 8,
                        color: (claim.fraud_score > 0.6) ? "#f87171" : "#4ade80",
                        fontWeight: 700
                    }}>
                        Fraud Score: {(claim.fraud_score * 100).toFixed(0)}%
                    </div>

                    <div style={{
                        background: (claim.risk_score > 0.6) ? "#eab30811" : "#22c55e11",
                        border: `1px solid ${(claim.risk_score > 0.6) ? "#eab30822" : "#22c55e22"}`,
                        padding: "10px 18px",
                        borderRadius: 8,
                        color: (claim.risk_score > 0.6) ? "#facc15" : "#4ade80",
                        fontWeight: 700
                    }}>
                        Risk Score: {(claim.risk_score * 100).toFixed(0)}%
>>>>>>> f930c12 (update project before sync)
                    </div>
                </div>

                {/* AI Recommendation Panel */}
                <div style={{
                    background: "#1e293b",
                    padding: 20,
                    borderRadius: 12,
                    marginBottom: 32,
                    border: `1px solid ${C.border}`
                }}>
                    <div style={{ color: C.muted, fontSize: 12, marginBottom: 8 }}>
                        AI RECOMMENDATION
                    </div>
                    <div style={{ color: C.text, fontWeight: 800, fontSize: 18 }}>
<<<<<<< HEAD
                        {claim.aiDecision}
                    </div>
                    <div style={{ color: C.muted }}>
                        Confidence: {(claim.confidence * 100).toFixed(0)}%
                    </div>
=======
                        {claim.ai_decision || claim.status}
                    </div>
                    <div style={{ color: C.muted }}>
                        Confidence: {(claim.confidence ? (claim.confidence * 100).toFixed(0) : "N/A")}%
                    </div>
                    {claim.explanation && (
                        <div style={{ marginTop: 12, color: C.text, fontSize: 14, fontStyle: "italic", borderLeft: `3px solid ${C.blue}`, paddingLeft: 12 }}>
                            "{claim.explanation}"
                        </div>
                    )}
>>>>>>> f930c12 (update project before sync)
                </div>

                <div style={{ display: "flex", gap: 60 }}>

                    {/* LEFT */}
                    <div style={{ flex: 1 }}>
                        <Section title="Claimer Information">
<<<<<<< HEAD
                            <Info label="Full Name" value={claim.patient} />
                            <Info label="Email" value={claim.email} />
                            <Info label="Phone" value={claim.phone} />
                            <Info label="Policy Number" value={claim.policyNumber} />
                            <Info label="Address" value={claim.address} />
                        </Section>

                        <Section title="Claim Metadata">
                            <Info label="Type" value={claim.type} />
                            <Info label="Amount" value={claim.amount} />
                            <Info label="Hospital" value={claim.hospital} />
                            <Info label="Treatment Dates" value={claim.dates} />
=======
                            <Info label="Full Name" value={claim.claimer.name} />
                            <Info label="Email" value={claim.claimer.email} />
                            <Info label="Phone" value={claim.claimer.phone || "N/A"} />
                            <Info label="Policy Number" value={claim.policy_number} />
                            <Info label="Address" value={claim.claimer.address || "N/A"} />
                        </Section>

                        <Section title="Claim Metadata">
                            <Info label="Type" value={claim.claim_type} />
                            <Info label="Amount" value={`₹${claim.claim_amount.toLocaleString()}`} />
>>>>>>> f930c12 (update project before sync)
                        </Section>
                    </div>

                    {/* RIGHT */}
                    <div style={{ flex: 1 }}>
                        <Section title="AI Risk Assessment">
<<<<<<< HEAD
                            <GaugeBar label="Risk Score" val={claim.riskScore} />
                            <GaugeBar label="Fraud Score" val={claim.fraudScore} />
                        </Section>

                        <Section title="Uploaded Documents">
                            {["Policy Document", "ID Proof", "Hospital Bill", "Discharge Summary"].map(doc => (
                                <div key={doc} style={{
                                    background: C.border,
                                    padding: "12px",
                                    borderRadius: 8,
                                    marginBottom: 10,
                                    fontWeight: 600
                                }}>
                                    📄 {doc}
                                </div>
                            ))}
=======
                            <GaugeBar label="Risk Score" val={claim.risk_score} />
                            <GaugeBar label="Fraud Score" val={claim.fraud_score} />
                        </Section>

                        <Section title="Uploaded Documents">
                            {claim.documents && claim.documents.length > 0 ? (
                                claim.documents.map((doc, idx) => (
                                    <div key={idx} style={{
                                        background: C.border,
                                        padding: "12px",
                                        borderRadius: 8,
                                        marginBottom: 10,
                                        fontWeight: 600,
                                        display: "flex",
                                        justifyContent: "space-between",
                                        alignItems: "center"
                                    }}>
                                        <span>📄 {doc.split(/[\\/]/).pop()}</span>
                                        <a href={`http://localhost:8000/${doc}`} target="_blank" rel="noreferrer" style={{ color: C.blue, fontSize: 12 }}>View</a>
                                    </div>
                                ))
                            ) : (
                                <div style={{ color: C.muted }}>No documents uploaded.</div>
                            )}
>>>>>>> f930c12 (update project before sync)
                        </Section>
                    </div>
                </div>

                {/* Expandable AI Reasoning */}
                <div style={{ marginTop: 40 }}>
                    <button
                        onClick={() => setShowReasoning(!showReasoning)}
                        style={{
                            background: "transparent",
                            border: "none",
                            color: "#60a5fa",
                            cursor: "pointer",
                            fontWeight: 700
                        }}
                    >
                        {showReasoning ? "Hide AI Reasoning ▲" : "View AI Reasoning ▼"}
                    </button>

                    {showReasoning && (
                        <div style={{
                            marginTop: 16,
                            padding: 20,
                            background: "#0f172a",
                            borderRadius: 12
                        }}>
<<<<<<< HEAD
                            {claim.reasoning.map((r, i) => (
                                <div key={i} style={{ marginBottom: 14 }}>
                                    <div style={{ fontWeight: 700 }}>{r.node}</div>
                                    <div style={{ color: C.muted }}>{r.finding}</div>
                                    <div style={{ color: "#22c55e" }}>
                                        Confidence: {(r.confidence * 100).toFixed(0)}%
                                    </div>
                                </div>
                            ))}
=======
                            {claim.reasoning && claim.reasoning.length > 0 ? (
                                claim.reasoning.map((r, i) => (
                                    <div key={i} style={{ marginBottom: 14 }}>
                                        <div style={{ fontWeight: 700 }}>{r.node}</div>
                                        <div style={{ color: C.muted }}>{r.finding}</div>
                                        <div style={{ color: (r.confidence > 0.7) ? "#22c55e" : "#facc15" }}>
                                            Confidence: {(r.confidence * 100).toFixed(0)}%
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <div style={{ color: C.muted }}>No detailed reasoning available yet.</div>
                            )}
>>>>>>> f930c12 (update project before sync)
                        </div>
                    )}
                </div>

<<<<<<< HEAD
                {/* Reviewer Notes */}
                <div style={{ marginTop: 40 }}>
                    <h4 style={{ color: C.muted }}>Add Review Note</h4>
                    <textarea
                        value={note}
                        onChange={(e) => setNote(e.target.value)}
                        style={{
                            width: "100%",
                            height: 80,
                            background: C.panel,
                            border: `1px solid ${C.border}`,
                            borderRadius: 8,
                            padding: 10,
                            color: C.text
                        }}
                    />
                </div>

                {/* Action Buttons */}
                <div style={{ display: "flex", gap: 16, marginTop: 30 }}>
                    <ActionButton label="Approve" color="#22c55e" />
                    <ActionButton label="Reject" color="#ef4444" />
                    <ActionButton label="Request More Info" color="#facc15" />
                </div>
=======
                {isReviewer && (
                    <>
                        {/* Reviewer Notes */}
                        <div style={{ marginTop: 40 }}>
                            <h4 style={{ color: C.muted }}>Add Review Note</h4>
                            <textarea
                                value={note}
                                onChange={(e) => setNote(e.target.value)}
                                style={{
                                    width: "100%",
                                    height: 80,
                                    background: C.panel,
                                    border: `1px solid ${C.border}`,
                                    borderRadius: 8,
                                    padding: 10,
                                    color: C.text
                                }}
                            />
                        </div>

                        {/* Action Buttons */}
                        <div style={{ display: "flex", gap: 16, marginTop: 30 }}>
                            <ActionButton
                                label="Approve"
                                color="#22c55e"
                                onClick={() => handleAction("approve")}
                                disabled={isSubmitting}
                            />
                            <ActionButton
                                label="Reject"
                                color="#ef4444"
                                onClick={() => handleAction("reject")}
                                disabled={isSubmitting}
                            />
                            <ActionButton
                                label="Request More Info"
                                color="#facc15"
                                onClick={() => handleAction("request_more_info")}
                                disabled={isSubmitting}
                            />
                        </div>
                    </>
                )}
>>>>>>> f930c12 (update project before sync)

            </div>
        </div>
    );
}

function Section({ title, children }) {
    return (
        <div style={{ marginBottom: 40 }}>
            <h4 style={{
                color: C.muted,
                fontSize: 11,
                fontWeight: 800,
                textTransform: "uppercase",
                letterSpacing: 1,
                marginBottom: 16
            }}>
                {title}
            </h4>
            {children}
        </div>
    );
}

function Info({ label, value }) {
    return (
        <div style={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: 18
        }}>
            <span style={{ color: C.muted }}>{label}</span>
            <span style={{ color: C.text, fontWeight: 700 }}>{value}</span>
        </div>
    );
}

<<<<<<< HEAD
function ActionButton({ label, color }) {
    return (
        <button style={{
            background: color + "22",
            border: `1px solid ${color}`,
            color,
            padding: "10px 18px",
            borderRadius: 8,
            fontWeight: 700,
            cursor: "pointer"
        }}>
=======
function ActionButton({ label, color, onClick, disabled }) {
    return (
        <button
            onClick={onClick}
            disabled={disabled}
            style={{
                background: color + "22",
                border: `1px solid ${color}`,
                color,
                padding: "10px 18px",
                borderRadius: 8,
                fontWeight: 700,
                cursor: disabled ? "not-allowed" : "pointer",
                opacity: disabled ? 0.7 : 1
            }}
        >
>>>>>>> f930c12 (update project before sync)
            {label}
        </button>
    );
}
<<<<<<< HEAD
=======

>>>>>>> f930c12 (update project before sync)
