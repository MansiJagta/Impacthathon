import React from 'react';
import { useNavigate } from "react-router-dom";
import { C } from "../constants/theme";

const RoleCard = ({ title, desc, icon, onLogin, onRegister }) => (
    <div
        style={{
            background: C.panel,
            border: `1px solid ${C.border}`,
            borderRadius: 16,
            padding: "32px",
            flex: 1,
            display: "flex",
            flexDirection: "column",
            gap: 16,
            textAlign: "center"
        }}
    >
        <div style={{ fontSize: 48 }}>{icon}</div>
        <h3 style={{ color: "#fff", fontSize: 20, fontWeight: 800 }}>{title}</h3>
        <p style={{ color: C.muted, fontSize: 13, lineHeight: 1.5 }}>{desc}</p>

        <div style={{ display: "flex", gap: 12, flexDirection: "column", marginTop: "auto" }}>
            <button
                onClick={onLogin}
                style={{
                    background: C.accent,
                    border: "none",
                    padding: "12px",
                    borderRadius: 12,
                    fontWeight: 700,
                    fontSize: 14,
                    cursor: "pointer",
                    color: "#000",
                    transition: "all 0.2s ease",
                }}
                onMouseEnter={(e) => {
                    e.currentTarget.style.opacity = "0.8";
                    e.currentTarget.style.transform = "scale(1.02)";
                }}
                onMouseLeave={(e) => {
                    e.currentTarget.style.opacity = "1";
                    e.currentTarget.style.transform = "scale(1)";
                }}
            >
                Sign In
            </button>
            <button
                onClick={onRegister}
                style={{
                    background: "transparent",
                    border: `1px solid ${C.accent}`,
                    padding: "12px",
                    borderRadius: 12,
                    fontWeight: 700,
                    fontSize: 14,
                    cursor: "pointer",
                    color: C.accent,
                    transition: "all 0.2s ease",
                }}
                onMouseEnter={(e) => {
                    e.currentTarget.style.background = `${C.accent}20`;
                    e.currentTarget.style.transform = "scale(1.02)";
                }}
                onMouseLeave={(e) => {
                    e.currentTarget.style.background = "transparent";
                    e.currentTarget.style.transform = "scale(1)";
                }}
            >
                Create Account
            </button>
        </div>
    </div>
);

export default function RoleSelect() {

    const navigate = useNavigate();

    return (
        <div style={{ maxWidth: 1000, margin: "100px auto", padding: "0 24px" }}>
            <div style={{ textAlign: "center", marginBottom: 48 }}>
                <h2 style={{ color: C.text, fontSize: 32, fontWeight: 900, marginBottom: 12 }}>
                    Welcome to IntelliClaim
                </h2>
                <p style={{ color: C.muted, fontSize: 16 }}>
                    Select your role to continue
                </p>
            </div>

            <div style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
                <RoleCard
                    title="Claimer"
                    desc="Submit new claims and track your payout status."
                    icon="🛡️"
                    onLogin={() => navigate("/login/claimer")}
                    onRegister={() => navigate("/register/claimer")}
                />

                <RoleCard
                    title="Reviewer"
                    desc="Analyze claims with AI assistance and approve/flag docs."
                    icon="🔍"
                    onLogin={() => navigate("/login/reviewer")}
                    onRegister={() => navigate("/register/reviewer")}
                />

                <RoleCard
                    title="Administrator"
                    desc="Access global analytics and system configuration."
                    icon="⚙️"
                    onLogin={() => navigate("/login/admin")}
                    onRegister={() => navigate("/register/admin")}
                />
            </div>
        </div>
    );
}

