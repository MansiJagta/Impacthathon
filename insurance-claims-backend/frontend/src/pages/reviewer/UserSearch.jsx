import { C } from "../../constants/theme";
import { Badge } from "../../components/Badge";

const UserStat = ({ label, value }) => (
    <div style={{ flex: 1, textAlign: "center" }}>
        <div style={{ color: C.blue, fontSize: 24, fontWeight: 900, marginBottom: 4 }}>{value}</div>
        <div style={{ color: C.muted, fontSize: 11, fontWeight: 700, textTransform: "uppercase", letterSpacing: 0.5 }}>{label}</div>
    </div>
);

export default function UserSearch() {
    const results = [
        { id: "CL-2024-0890", type: "Health", amount: "₹1,20,000", status: "Approved manually", badge: "Approved", date: "18 Feb" },
        { id: "CL-2024-0885", type: "Health", amount: "₹25,000", status: "Auto-approved", badge: "Approved", date: "15 Feb" },
        { id: "CL-2024-0872", type: "Motor", amount: "₹12,500", status: "Auto-approved", badge: "Approved", date: "10 Feb" },
    ];

    return (
        <div>
            <div style={{ display: "flex", gap: 12, marginBottom: 32 }}>
                <input
                    type="text"
                    defaultValue="John"
                    style={{
                        flex: 1,
                        background: C.panel,
                        border: `1px solid ${C.border}`,
                        padding: "16px 24px",
                        borderRadius: 8,
                        color: C.text,
                        fontSize: 16,
                        outline: "none"
                    }}
                />
                <button style={{
                    background: "#a855f7",
                    color: "#fff",
                    border: "none",
                    padding: "0 32px",
                    borderRadius: 8,
                    fontWeight: 800,
                    cursor: "pointer"
                }}>Search</button>
            </div>

            <p style={{ color: C.muted, fontSize: 12, marginBottom: 24 }}>Results for "John" (3 claims)</p>

            <div style={{
                background: C.panel,
                border: `1px solid ${C.border}`,
                borderRadius: 16,
                overflow: "hidden",
                marginBottom: 32
            }}>
                <div style={{ display: "flex", flexDirection: "column" }}>
                    {results.map((c, i) => (
                        <div key={i} style={{
                            padding: "24px",
                            borderBottom: i === results.length - 1 ? "none" : `1px solid ${C.border}`
                        }}>
                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
                                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                                    <span style={{ color: C.accent, fontWeight: 800, fontSize: 14 }}>{c.id}</span>
                                    <span style={{ background: C.dim, color: C.text, padding: "4px 10px", borderRadius: 4, fontSize: 11, fontWeight: 700 }}>{c.type}</span>
                                    <span style={{ color: C.text, fontWeight: 800, fontSize: 16 }}>{c.amount}</span>
                                </div>
                                <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
                                    <Badge status={c.badge} />
                                    <span style={{ color: C.muted, fontSize: 12 }}>{c.date}</span>
                                </div>
                            </div>
                            <p style={{ color: C.muted, fontSize: 12 }}>{c.status}</p>
                        </div>
                    ))}
                </div>
            </div>

            <div style={{
                background: C.panel,
                border: `1px solid ${C.border}`,
                borderRadius: 16,
                padding: "24px 24px"
            }}>
                <h4 style={{ color: C.muted, fontSize: 11, fontWeight: 800, textTransform: "uppercase", letterSpacing: 1, marginBottom: 25 }}>
                    User Stats
                </h4>
                <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <UserStat label="Total Claims" value="12" />
                    <UserStat label="Approval Rate" value="83%" />
                    <UserStat label="Avg Amount" value="₹58k" />
                    <UserStat label="Last Claim" value="18 Feb" />
                </div>
            </div>
        </div>
    );
}
