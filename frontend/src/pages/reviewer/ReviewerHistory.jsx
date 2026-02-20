import { C } from "../../constants/theme";
import { Badge } from "../../components/Badge";

export default function ReviewerHistory() {
    const claims = [
        { id: "CL-2024-0890", name: "John", type: "Health", amount: "₹1,20,000", reviewer: "Sarah", status: "Approved – Valid docs, out-of-network emergency covered", badge: "Approved", date: "18 Feb" },
        { id: "CL-2024-0889", name: "Priya", type: "Property", amount: "₹5,00,000", reviewer: "Sarah", status: "Rejected – Flood not covered, exclusion clause 7.3", badge: "Rejected", date: "17 Feb" },
        { id: "CL-2024-0886", name: "Amit", type: "Motor", amount: "₹95,000", reviewer: "Mike", status: "Approved – All docs valid, within limit", badge: "Approved", date: "16 Feb" },
        { id: "CL-2024-0885", name: "John", type: "Health", amount: "₹25,000", reviewer: "Sarah", status: "Auto-approved (system)", badge: "Approved", date: "15 Feb" },
    ];

    return (
        <div style={{ background: C.panel, border: `1px solid ${C.border}`, borderRadius: 16, overflow: "hidden" }}>
            <div style={{ padding: "24px", borderBottom: `1px solid ${C.border}`, background: "rgba(255,255,255,0.02)" }}>
                <h3 style={{ color: C.muted, fontSize: 13, fontWeight: 800, textTransform: "uppercase", letterSpacing: 1 }}>
                    All Processed Claims (347 Total)
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
                            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
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
            </div>
        </div>
    );
}
