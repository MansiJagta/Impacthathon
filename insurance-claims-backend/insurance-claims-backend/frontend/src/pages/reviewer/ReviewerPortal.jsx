import { useState } from "react";
import { C } from "../../constants/theme";
import ReviewQueue from "./ReviewQueue";
import ReviewerHistory from "./ReviewerHistory";
import UserSearch from "./UserSearch";

export default function ReviewerPortal() {
    const [sub, setSub] = useState("queue");
    const tabs = [
        { id: "queue", label: "⚡ Review Queue" },
        { id: "history", label: "📋 All Claims" },
        { id: "search", label: "🔍 User Search" },
    ];

    return (
        <div style={{ minHeight: "calc(100vh - 56px)", background: C.bg }}>
            <div style={{
                background: C.panel, borderBottom: `1px solid ${C.border}`,
                padding: "0 28px", display: "flex", gap: 4,
            }}>
                {tabs.map(t => (
                    <button key={t.id} onClick={() => setSub(t.id)} style={{
                        background: sub === t.id ? "#a855f722" : "transparent",
                        color: sub === t.id ? "#a855f7" : C.muted,
                        border: "none", borderBottom: sub === t.id ? "2px solid #a855f7" : "2px solid transparent",
                        padding: "14px 18px", cursor: "pointer", fontSize: 13, fontWeight: 600,
                    }}>{t.label}</button>
                ))}
            </div>
            <div style={{ padding: "32px 28px", maxWidth: 960, margin: "0 auto" }}>
                {sub === "queue" && <ReviewQueue />}
                {sub === "history" && <ReviewerHistory />}
                {sub === "search" && <UserSearch />}
            </div>
        </div>
    );
}