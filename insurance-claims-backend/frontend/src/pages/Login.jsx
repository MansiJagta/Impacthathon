import { useState } from "react";
import { C } from "../constants/theme";
import { useParams, useNavigate } from "react-router-dom";

export default function Login() {

    const { role } = useParams();
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [pass, setPass] = useState("");

    const roleMap = {
        claimer: {
            title: "Customer Login",
            desc: "Access your claims and policy details",
            icon: "🛡️",
            primaryBtn: "Login to Portal",
            portalPath: "/portal/claimer",
            altText: "New to IntelliClaim?",
            altLink: "Create an account"
        },
        reviewer: {
            title: "Reviewer SSO",
            desc: "Internal Claims Processing Environment",
            icon: "🔍",
            primaryBtn: "Sign in with Okta",
            portalPath: "/portal/reviewer",
            altText: "Issues with SSO?",
            altLink: "Contact IT Support"
        },
        admin: {
            title: "Admin Terminal",
            desc: "Secure System Administration & Analytics",
            icon: "⚙️",
            primaryBtn: "Authorize with Key",
            portalPath: "/portal/admin",
            altText: "Security Notice:",
            altLink: "MFA Required for all sessions"
        }
    };

    const config = roleMap[role];

    if (!config) {
        return <div style={{ padding: 40 }}>Invalid role.</div>;
    }

    const handleLogin = () => {
        // Later you can add real authentication here
        localStorage.setItem("userRole", role);
        navigate(config.portalPath);
    };

    return (
        <div style={{
            maxWidth: 420,
            margin: "120px auto",
            padding: "40px",
            background: C.panel,
            border: `1px solid ${C.border}`,
            borderRadius: 24,
            boxShadow: "0 20px 50px rgba(0,0,0,0.3)",
            textAlign: "center"
        }}>

            {/* Back Button */}
            <button
                onClick={() => navigate("/role-select")}
                style={{
                    background: "transparent",
                    border: "none",
                    color: C.muted,
                    fontSize: 12,
                    fontWeight: 700,
                    cursor: "pointer",
                    marginBottom: 32
                }}
            >
                ← Back to Selection
            </button>

            <div style={{ fontSize: 64, marginBottom: 20 }}>
                {config.icon}
            </div>

            <h2 style={{ color: "#fff", fontSize: 28, fontWeight: 900, marginBottom: 8 }}>
                {config.title}
            </h2>

            <p style={{ color: C.muted, fontSize: 14, marginBottom: 40 }}>
                {config.desc}
            </p>

            {role === "claimer" ? (
                <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                    <input
                        type="email"
                        placeholder="Email Address"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        style={{
                            background: "rgba(255,255,255,0.05)",
                            border: `1px solid ${C.border}`,
                            padding: "16px",
                            borderRadius: 12,
                            color: "#fff",
                            fontSize: 14,
                            outline: "none"
                        }}
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        value={pass}
                        onChange={(e) => setPass(e.target.value)}
                        style={{
                            background: "rgba(255,255,255,0.05)",
                            border: `1px solid ${C.border}`,
                            padding: "16px",
                            borderRadius: 12,
                            color: "#fff",
                            fontSize: 14,
                            outline: "none"
                        }}
                    />

                    <button
                        onClick={handleLogin}
                        style={{
                            background: C.accent,
                            color: "#000",
                            border: "none",
                            padding: "18px",
                            borderRadius: 12,
                            fontWeight: 900,
                            fontSize: 16,
                            cursor: "pointer",
                            marginTop: 8,
                            boxShadow: `0 10px 20px ${C.accent}44`
                        }}
                    >
                        {config.primaryBtn}
                    </button>
                </div>
            ) : (
                <button
                    onClick={handleLogin}
                    style={{
                        background: role === "admin" ? C.text : "#a855f7",
                        color: "#000",
                        border: "none",
                        padding: "18px",
                        borderRadius: 12,
                        fontWeight: 900,
                        fontSize: 16,
                        cursor: "pointer",
                        boxShadow: "0 10px 30px rgba(168,85,247,0.3)"
                    }}
                >
                    {config.primaryBtn}
                </button>
            )}

            <div style={{ marginTop: 40, paddingTop: 20, borderTop: `1px solid ${C.border}` }}>
                <span style={{ color: C.muted, fontSize: 13 }}>{config.altText} </span>
                <span style={{ color: C.accent, fontSize: 13, fontWeight: 700 }}>
                    {config.altLink}
                </span>
            </div>

        </div>
    );
}
