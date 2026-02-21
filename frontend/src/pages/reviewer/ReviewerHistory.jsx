<<<<<<< HEAD
import { C } from "../../constants/theme";
import { Badge } from "../../components/Badge";

export default function ReviewerHistory() {
    const claims = [
        { id: "CL-2024-0890", name: "John", type: "Health", amount: "₹1,20,000", reviewer: "Sarah", status: "Approved – Valid docs, out-of-network emergency covered", badge: "Approved", date: "18 Feb" },
        { id: "CL-2024-0889", name: "Priya", type: "Property", amount: "₹5,00,000", reviewer: "Sarah", status: "Rejected – Flood not covered, exclusion clause 7.3", badge: "Rejected", date: "17 Feb" },
        { id: "CL-2024-0886", name: "Amit", type: "Motor", amount: "₹95,000", reviewer: "Mike", status: "Approved – All docs valid, within limit", badge: "Approved", date: "16 Feb" },
        { id: "CL-2024-0885", name: "John", type: "Health", amount: "₹25,000", reviewer: "Sarah", status: "Auto-approved (system)", badge: "Approved", date: "15 Feb" },
    ];
=======
import { useState, useEffect } from "react";
import { C } from "../../constants/theme";
import { Badge } from "../../components/Badge";
import api from "../../services/api";

export default function ReviewerHistory() {
    const [claims, setClaims] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchHistory() {
            setLoading(true);
            try {
                // For "All Processed Claims", we list all claims but maybe filter by processed status if API allows
                const response = await api.listClaims({});
                setClaims(response.claims || []);
            } catch (err) {
                console.error("Error fetching history:", err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }
        fetchHistory();
    }, []);

    if (loading) return <div style={{ color: C.muted, padding: 24 }}>Loading history...</div>;
    if (error) return <div style={{ color: C.red, padding: 24 }}>Error: {error}</div>;
>>>>>>> f930c12 (update project before sync)

    return (
        <div style={{ background: C.panel, border: `1px solid ${C.border}`, borderRadius: 16, overflow: "hidden" }}>
            <div style={{ padding: "24px", borderBottom: `1px solid ${C.border}`, background: "rgba(255,255,255,0.02)" }}>
                <h3 style={{ color: C.muted, fontSize: 13, fontWeight: 800, textTransform: "uppercase", letterSpacing: 1 }}>
<<<<<<< HEAD
                    All Processed Claims (347 Total)
                </h3>
            </div>
            <div style={{ display: "flex", flexDirection: "column" }}>
                {claims.map((c, i) => (
=======
                    All Processed Claims ({claims.length} Total)
                </h3>
            </div>
            <div style={{ display: "flex", flexDirection: "column" }}>
                {claims.length > 0 ? claims.map((c, i) => (
>>>>>>> f930c12 (update project before sync)
                    <div key={i} style={{
                        padding: "24px",
                        borderBottom: i === claims.length - 1 ? "none" : `1px solid ${C.border}`,
                        display: "flex",
                        flexDirection: "column",
                        gap: 12
                    }}>
                        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
<<<<<<< HEAD
                                <span style={{ color: C.accent, fontWeight: 800, fontSize: 14 }}>{c.id}</span>
                                <span style={{ background: C.dim, color: C.text, padding: "4px 10px", borderRadius: 4, fontSize: 11, fontWeight: 700 }}>{c.name}</span>
                                <span style={{ background: C.dim, color: C.text, padding: "4px 10px", borderRadius: 4, fontSize: 11, fontWeight: 700 }}>{c.type}</span>
                                <span style={{ color: C.text, fontWeight: 800, fontSize: 16 }}>{c.amount}</span>
                            </div>
                            <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
                                <Badge status={c.badge} />
                                <span style={{ color: C.muted, fontSize: 12 }}>{c.date}</span>
                            </div>
                        </div>
                        <p style={{ color: C.muted, fontSize: 13 }}>
                            Reviewed by: <span style={{ color: "#a855f7", fontWeight: 600 }}>{c.reviewer}</span> · {c.status}
                        </p>
                    </div>
                ))}
=======
                                <span style={{ color: C.accent, fontWeight: 800, fontSize: 14 }}>{c.claim_id}</span>
                                <span style={{ background: C.dim, color: C.text, padding: "4px 10px", borderRadius: 4, fontSize: 11, fontWeight: 700 }}>{c.claimer.name}</span>
                                <span style={{ background: C.dim, color: C.text, padding: "4px 10px", borderRadius: 4, fontSize: 11, fontWeight: 700 }}>{c.claim_type}</span>
                                <span style={{ color: C.text, fontWeight: 800, fontSize: 16 }}>₹{c.claim_amount.toLocaleString() || 0}</span>
                            </div>
                            <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
                                <Badge status={c.status} />
                                <span style={{ color: C.muted, fontSize: 12 }}>{new Date(c.created_at).toLocaleDateString()}</span>
                            </div>
                        </div>
                        <p style={{ color: C.muted, fontSize: 13 }}>
                            AI Recommendation: <span style={{ color: "#a855f7", fontWeight: 600 }}>{c.ai_decision || 'N/A'}</span> · {c.summary}
                        </p>
                    </div>
                )) : (
                    <div style={{ padding: 40, textAlign: "center", color: C.muted }}>No claims found.</div>
                )}
>>>>>>> f930c12 (update project before sync)
            </div>
        </div>
    );
}
