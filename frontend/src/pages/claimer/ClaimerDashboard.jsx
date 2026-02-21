<<<<<<< HEAD
import { C } from "../../constants/theme";
import { Badge } from "../../components/Badge";
=======
import { useState, useEffect } from "react";
import { C } from "../../constants/theme";
import { Badge } from "../../components/Badge";
import api from "../../services/api";
>>>>>>> f930c12 (update project before sync)

const StatCard = ({ label, value, color }) => (
    <div style={{
        background: C.panel,
        border: `1px solid ${C.border}`,
        borderRadius: 12,
        padding: "24px",
        flex: 1,
        textAlign: "center"
    }}>
        <div style={{ color: color, fontSize: 32, fontWeight: 800, marginBottom: 8 }}>{value}</div>
        <div style={{ color: C.muted, fontSize: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: 1 }}>{label}</div>
    </div>
);

export default function ClaimerDashboard({ onNew, onHistory }) {
<<<<<<< HEAD
    const recentClaims = [
        { id: "CL-2024-0891", type: "Motor", amount: "₹75,000", status: "Auto-approved", date: "2m ago", badge: "Approved" },
        { id: "CL-2024-0890", type: "Health", amount: "₹1,20,000", status: "Under review by underwriter", date: "1h ago", badge: "Pending" },
        { id: "CL-2024-0889", type: "Property", amount: "₹5,00,000", status: "Documents flagged as suspicious", date: "3h ago", badge: "Flagged" },
    ];
=======
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchDashboard() {
            setLoading(true);
            try {
                const userEmail = localStorage.getItem("userEmail") || "demo@example.com";
                const dashboardData = await api.getClaimerDashboard(userEmail);
                setData(dashboardData);
            } catch (err) {
                console.error("Dashboard fetch error:", err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }
        fetchDashboard();
    }, []);

    if (loading) return <div style={{ color: C.muted, padding: 40 }}>Loading dashboard analytics...</div>;
    if (error) return <div style={{ color: C.red, padding: 40 }}>Error: {error}</div>;

    const { stats, recent_claims } = data || { stats: { total: 0, approved: 0, pending: 0, flagged: 0 }, recent_claims: [] };

    const formatDate = (dateStr) => {
        if (!dateStr) return "";
        const date = new Date(dateStr);
        const now = new Date();
        const diffMs = now - date;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMins / 60);
        const diffDays = Math.floor(diffHours / 24);

        if (diffMins < 60) return `${diffMins}m ago`;
        if (diffHours < 24) return `${diffHours}h ago`;
        return `${diffDays}d ago`;
    };
>>>>>>> f930c12 (update project before sync)

    return (
        <div>
            <div style={{ display: "flex", gap: 20, marginBottom: 32 }}>
<<<<<<< HEAD
                <StatCard label="Total" value="12" color={C.blue} />
                <StatCard label="Approved" value="8" color={C.green} />
                <StatCard label="Pending" value="2" color={C.yellow} />
                <StatCard label="Flagged" value="2" color={C.red} />
=======
                <StatCard label="Total" value={stats.total} color={C.blue} />
                <StatCard label="Approved" value={stats.approved} color={C.green} />
                <StatCard label="Pending" value={stats.pending} color={C.yellow} />
                <StatCard label="Flagged" value={stats.flagged} color={C.red} />
>>>>>>> f930c12 (update project before sync)
            </div>

            <div style={{ display: "flex", gap: 16, marginBottom: 40 }}>
                <button
                    onClick={onNew}
                    style={{
                        background: C.blue,
                        color: "#fff",
                        border: "none",
                        padding: "12px 24px",
                        borderRadius: 8,
                        fontWeight: 700,
                        cursor: "pointer",
                        display: "flex",
                        alignItems: "center",
                        gap: 8
                    }}
                >
                    📄 New Claim →
                </button>
                <button
                    onClick={onHistory}
                    style={{
                        background: "transparent",
                        color: C.text,
                        border: `1px solid ${C.border}`,
                        padding: "12px 24px",
                        borderRadius: 8,
                        fontWeight: 700,
                        cursor: "pointer",
                        display: "flex",
                        alignItems: "center",
                        gap: 8
                    }}
                    onMouseEnter={(e) => e.target.style.background = C.panel}
                    onMouseLeave={(e) => e.target.style.background = "transparent"}
                >
                    📜 My History →
                </button>
            </div>

            <div style={{
                background: C.panel,
                border: `1px solid ${C.border}`,
                borderRadius: 12,
                overflow: "hidden"
            }}>
                <div style={{ padding: "20px 24px", borderBottom: `1px solid ${C.border}`, background: "rgba(255,255,255,0.02)" }}>
                    <h3 style={{ color: C.muted, fontSize: 12, fontWeight: 800, textTransform: "uppercase", letterSpacing: 1 }}>
                        My Recent Claims
                    </h3>
                </div>
                <table style={{ width: "100%", borderCollapse: "collapse" }}>
                    <tbody>
<<<<<<< HEAD
                        {recentClaims.map((c, i) => (
                            <tr key={i} style={{ borderBottom: i === recentClaims.length - 1 ? "none" : `1px solid ${C.border}` }}>
                                <td style={{ padding: "20px 24px", color: C.accent, fontWeight: 700, fontSize: 13 }}>{c.id}</td>
                                <td style={{ padding: "20px 24px" }}>
                                    <span style={{ background: C.dim, color: C.text, padding: "4px 12px", borderRadius: 4, fontSize: 11, fontWeight: 700 }}>{c.type}</span>
                                </td>
                                <td style={{ padding: "20px 24px", color: C.text, fontWeight: 800 }}>{c.amount}</td>
                                <td style={{ padding: "20px 24px", color: C.muted, fontSize: 12 }}>{c.status}</td>
                                <td style={{ padding: "20px 24px" }}><Badge status={c.badge} /></td>
                                <td style={{ padding: "20px 24px", color: C.muted, fontSize: 11, textAlign: "right" }}>{c.date}</td>
                            </tr>
                        ))}
=======
                        {recent_claims.length === 0 ? (
                            <tr>
                                <td colSpan="6" style={{ padding: "40px", textAlign: "center", color: C.muted }}>
                                    No claims found.
                                </td>
                            </tr>
                        ) : (
                            recent_claims.map((c, i) => (
                                <tr key={i} style={{ borderBottom: i === recent_claims.length - 1 ? "none" : `1px solid ${C.border}` }}>
                                    <td style={{ padding: "20px 24px", color: C.accent, fontWeight: 700, fontSize: 13 }}>{c.claim_id}</td>
                                    <td style={{ padding: "20px 24px" }}>
                                        <span style={{ background: C.dim, color: C.text, padding: "4px 12px", borderRadius: 4, fontSize: 11, fontWeight: 700 }}>{c.claim_type}</span>
                                    </td>
                                    <td style={{ padding: "20px 24px", color: C.text, fontWeight: 800 }}>₹{c.claim_amount.toLocaleString()}</td>
                                    <td style={{ padding: "20px 24px", color: C.muted, fontSize: 12 }}>{c.summary}</td>
                                    <td style={{ padding: "20px 24px" }}><Badge status={c.badge} /></td>
                                    <td style={{ padding: "20px 24px", color: C.muted, fontSize: 11, textAlign: "right" }}>{formatDate(c.created_at)}</td>
                                </tr>
                            ))
                        )}
>>>>>>> f930c12 (update project before sync)
                    </tbody>
                </table>
            </div>
        </div>
    );
}
<<<<<<< HEAD
=======

>>>>>>> f930c12 (update project before sync)
