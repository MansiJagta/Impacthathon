import { C } from "../../constants/theme";
import { Badge } from "../../components/Badge";

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
    const recentClaims = [
        { id: "CL-2024-0891", type: "Motor", amount: "₹75,000", status: "Auto-approved", date: "2m ago", badge: "Approved" },
        { id: "CL-2024-0890", type: "Health", amount: "₹1,20,000", status: "Under review by underwriter", date: "1h ago", badge: "Pending" },
        { id: "CL-2024-0889", type: "Property", amount: "₹5,00,000", status: "Documents flagged as suspicious", date: "3h ago", badge: "Flagged" },
    ];

    return (
        <div>
            <div style={{ display: "flex", gap: 20, marginBottom: 32 }}>
                <StatCard label="Total" value="12" color={C.blue} />
                <StatCard label="Approved" value="8" color={C.green} />
                <StatCard label="Pending" value="2" color={C.yellow} />
                <StatCard label="Flagged" value="2" color={C.red} />
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
                    </tbody>
                </table>
            </div>
        </div>
    );
}
