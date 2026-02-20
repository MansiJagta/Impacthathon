import React from 'react';
import { useNavigate } from "react-router-dom";
import { C } from "../constants/theme";

const RoleCard = ({ title, desc, icon, onClick }) => (
    <div
        onClick={onClick}
        style={{
            background: C.panel,
            border: `1px solid ${C.border}`,
            borderRadius: 16,
            padding: "32px",
            flex: 1,
            cursor: "pointer",
            transition: "all 0.2s ease",
            display: "flex",
            flexDirection: "column",
            gap: 16,
            textAlign: "center"
        }}
        onMouseEnter={(e) => {
            e.currentTarget.style.borderColor = C.accent;
            e.currentTarget.style.background = "#1e293b";
            e.currentTarget.style.transform = "translateY(-4px)";
        }}
        onMouseLeave={(e) => {
            e.currentTarget.style.borderColor = C.border;
            e.currentTarget.style.background = C.panel;
            e.currentTarget.style.transform = "translateY(0)";
        }}
    >
        <div style={{ fontSize: 48 }}>{icon}</div>
        <h3 style={{ color: "#fff", fontSize: 20, fontWeight: 800 }}>{title}</h3>
        <p style={{ color: C.muted, fontSize: 13, lineHeight: 1.5 }}>{desc}</p>
    </div>
);

export default function RoleSelect() {

    const navigate = useNavigate();

    return (
        <div style={{ maxWidth: 1000, margin: "100px auto", padding: "0 24px" }}>
            <div style={{ textAlign: "center", marginBottom: 48 }}>
                <h2 style={{ color: C.text, fontSize: 32, fontWeight: 900, marginBottom: 12 }}>
                    Welcome back, John!
                </h2>
                <p style={{ color: C.muted, fontSize: 16 }}>
                    Select your portal to continue
                </p>
            </div>

            <div style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
                <RoleCard
                    title="Claimer"
                    desc="Submit new claims and track your payout status."
                    icon="🛡️"
                    onClick={() => navigate("/login/claimer")}
                />

                <RoleCard
                    title="Reviewer"
                    desc="Analyze claims with AI assistance and approve/flag docs."
                    icon="🔍"
                    onClick={() => navigate("/login/reviewer")}
                />

                <RoleCard
                    title="Administrator"
                    desc="Access global analytics and system configuration."
                    icon="⚙️"
                    onClick={() => navigate("/login/admin")}
                />
            </div>
        </div>
    );
}
