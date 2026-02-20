import { useState } from "react";
import { C } from "../../constants/theme";
import ClaimerDashboard from "./ClaimerDashboard";
import NewClaimForm from "./NewClaimForm";
import ClaimerHistory from "./ClaimerHistory";

export default function ClaimerPortal() {
    const [sub, setSub] = useState("dashboard");

    const tabs = [
        { id: "dashboard", label: "📋 Dashboard" },
        { id: "newclaim", label: "📄 New Claim" },
        { id: "history", label: "📜 History" },
    ];

    return (
        <div style={{ minHeight: "calc(100vh - 56px)", background: C.bg }}>
            <div style={{ background: C.panel, borderBottom: `1px solid ${C.border}`, padding: "0 28px", display: "flex", gap: 4 }}>
                {tabs.map(t => (
                    <button key={t.id} onClick={() => setSub(t.id)} style={{
                        background: sub === t.id ? C.blue + "22" : "transparent",
                        color: sub === t.id ? C.blue : C.muted,
                        border: "none", borderBottom: sub === t.id ? `2px solid ${C.blue}` : "2px solid transparent",
                        padding: "14px 18px", cursor: "pointer", fontSize: 13, fontWeight: 600,
                    }}>{t.label}</button>
                ))}
            </div>

            <div style={{ padding: "32px 28px", maxWidth: 900, margin: "0 auto" }}>
                {sub === "dashboard" && <ClaimerDashboard onNew={() => setSub("newclaim")} onHistory={() => setSub("history")} />}
                {sub === "newclaim" && <NewClaimForm />}
                {sub === "history" && <ClaimerHistory />}
            </div>
        </div>
    );
}