<<<<<<< HEAD
import { C } from "../../constants/theme";
import { Badge } from "../../components/Badge";

export default function ClaimerHistory() {
    const claims = [
        { id: "CL-2024-0891", type: "Motor", amount: "₹75,000", status: "Auto-approved – Low risk", date: "18 Feb 2024", badge: "Approved" },
        { id: "CL-2024-0890", type: "Health", amount: "₹1,20,000", status: "Under review by underwriter", date: "17 Feb 2024", badge: "Pending" },
        { id: "CL-2024-0889", type: "Property", amount: "₹5,00,000", status: "Policy exclusion – Flood damage not covered", date: "15 Feb 2024", badge: "Rejected" },
        { id: "CL-2024-0888", type: "Motor", amount: "₹12,500", status: "Auto-approved – Minor claim", date: "14 Feb 2024", badge: "Approved" },
        { id: "CL-2024-0887", type: "Health", amount: "₹45,000", status: "Approved after manual review", date: "12 Feb 2024", badge: "Approved" },
    ];
=======
import { useState, useEffect } from "react";
import { C } from "../../constants/theme";
import { Badge } from "../../components/Badge";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";

export default function ClaimerHistory() {
    const navigate = useNavigate();
    const [claims, setClaims] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState("");
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchHistory() {
            setLoading(true);
            try {
                const userEmail = localStorage.getItem("userEmail") || "demo@example.com";
                const response = await api.listClaims({ claimer_email: userEmail, search });
                setClaims(response.claims || []);
            } catch (err) {
                console.error("History fetch error:", err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }
        fetchHistory();
    }, [search]);

    const formatDate = (dateStr) => {
        if (!dateStr) return "N/A";
        return new Date(dateStr).toLocaleDateString("en-IN", {
            day: "numeric",
            month: "short",
            year: "numeric"
        });
    };

    const stats = claims.reduce((acc, c) => {
        acc.total++;
        if (c.badge === "Approved") acc.approved++;
        if (c.badge === "Pending" || c.badge === "Flagged") acc.pending++;
        if (c.badge === "Rejected") acc.rejected++;
        return acc;
    }, { total: 0, approved: 0, pending: 0, rejected: 0 });
>>>>>>> f930c12 (update project before sync)

    return (
        <div>
            <div style={{
                background: C.panel,
                border: `1px solid ${C.border}`,
                borderRadius: 12,
                padding: "16px 24px",
                display: "flex",
                alignItems: "center",
                gap: 16,
                marginBottom: 32
            }}>
                <span style={{ fontSize: 20 }}>🔍</span>
                <input
                    type="text"
                    placeholder="Search by claim ID or type..."
<<<<<<< HEAD
=======
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
>>>>>>> f930c12 (update project before sync)
                    style={{
                        flex: 1,
                        background: "transparent",
                        border: "none",
                        color: C.text,
                        outline: "none",
                        fontSize: 14
                    }}
                />
            </div>

            <div style={{
                background: C.panel,
                border: `1px solid ${C.border}`,
                borderRadius: 12,
                overflow: "hidden"
            }}>
                <div style={{ padding: "20px 24px", borderBottom: `1px solid ${C.border}`, background: "rgba(255,255,255,0.02)" }}>
                    <h3 style={{ color: C.muted, fontSize: 12, fontWeight: 800, textTransform: "uppercase", letterSpacing: 1 }}>
<<<<<<< HEAD
                        All My Claims (5 Results)
                    </h3>
                </div>
                <div style={{ display: "flex", flexDirection: "column" }}>
                    {claims.map((c, i) => (
                        <div key={i} style={{
                            padding: "24px",
                            borderBottom: i === claims.length - 1 ? "none" : `1px solid ${C.border}`,
                            display: "flex",
                            flexDirection: "column",
                            gap: 12
                        }}>
                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                                <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
                                    <span style={{ color: C.accent, fontWeight: 800, fontSize: 14 }}>{c.id}</span>
                                    <span style={{ background: C.dim, color: C.text, padding: "4px 12px", borderRadius: 4, fontSize: 11, fontWeight: 700 }}>{c.type}</span>
                                    <span style={{ color: C.text, fontWeight: 800, fontSize: 16 }}>{c.amount}</span>
                                </div>
                                <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
                                    <Badge status={c.badge} />
                                    <span style={{ color: C.muted, fontSize: 12 }}>{c.date}</span>
                                </div>
                            </div>
                            <p style={{ color: C.muted, fontSize: 13 }}>{c.status}</p>
                        </div>
                    ))}
                </div>
            </div>

            <div style={{ marginTop: 24, textAlign: "center", color: C.muted, fontSize: 12 }}>
                Summary: 24 Total • 18 Approved • 3 Pending • 3 Rejected
            </div>
        </div>
    );
}
=======
                        All My Claims ({claims.length} Results)
                    </h3>
                </div>
                <div style={{ display: "flex", flexDirection: "column" }}>
                    {loading ? (
                        <div style={{ padding: 40, textAlign: "center", color: C.muted }}>Loading history...</div>
                    ) : claims.length === 0 ? (
                        <div style={{ padding: 40, textAlign: "center", color: C.muted }}>No claims found.</div>
                    ) : (
                        claims.map((c, i) => (
                            <div
                                key={i}
                                onClick={() => navigate(`/claim-details/${c.claim_id}`)}
                                style={{
                                    padding: "24px",
                                    borderBottom: i === claims.length - 1 ? "none" : `1px solid ${C.border}`,
                                    display: "flex",
                                    flexDirection: "column",
                                    gap: 12,
                                    cursor: "pointer",
                                    transition: "background 0.2s ease"
                                }}
                                onMouseEnter={(e) => e.currentTarget.style.background = "rgba(255,255,255,0.02)"}
                                onMouseLeave={(e) => e.currentTarget.style.background = "transparent"}
                            >
                                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                                    <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
                                        <span style={{ color: C.accent, fontWeight: 800, fontSize: 14 }}>{c.claim_id}</span>
                                        <span style={{ background: C.dim, color: C.text, padding: "4px 12px", borderRadius: 4, fontSize: 11, fontWeight: 700 }}>{c.claim_type}</span>
                                        <span style={{ color: C.text, fontWeight: 800, fontSize: 16 }}>₹{c.claim_amount.toLocaleString()}</span>
                                    </div>
                                    <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
                                        <Badge status={c.badge} />
                                        <span style={{ color: C.muted, fontSize: 12 }}>{formatDate(c.created_at)}</span>
                                    </div>
                                </div>
                                <p style={{ color: C.muted, fontSize: 13 }}>{c.summary}</p>
                            </div>
                        ))
                    )}
                </div>
            </div>

            {!loading && (
                <div style={{ marginTop: 24, textAlign: "center", color: C.muted, fontSize: 12 }}>
                    Summary: {stats.total} Total • {stats.approved} Approved • {stats.pending} Pending • {stats.rejected} Rejected
                </div>
            )}
        </div>
    );
}

>>>>>>> f930c12 (update project before sync)
