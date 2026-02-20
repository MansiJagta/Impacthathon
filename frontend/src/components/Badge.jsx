import { C } from "../constants/theme";

export function Badge({ status }) {
    const map = {
        Approved: { bg: "#064e3b", color: C.green, dot: C.green, label: "Approved" },
        Pending: { bg: "#451a03", color: C.yellow, dot: C.yellow, label: "Pending" },
        Rejected: { bg: "#450a0a", color: C.red, dot: C.red, label: "Rejected" },
        Flagged: { bg: "#422006", color: "#f97316", dot: "#f97316", label: "Flagged" },
        "Auto-approved": { bg: "#064e3b", color: C.green, dot: C.green, label: "Auto" },
    };
    const s = map[status] || map.Pending;
    return (
        <span style={{
            background: s.bg, color: s.color, borderRadius: 20,
            padding: "2px 10px", fontSize: 11, fontWeight: 700,
            display: "inline-flex", alignItems: "center", gap: 5,
        }}>
            <span style={{ width: 6, height: 6, borderRadius: "50%", background: s.dot, display: "inline-block" }} />
            {s.label}
        </span>
    );
}