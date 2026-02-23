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

    const handleLogin = async () => {
        try {
            const res = await fetch("http://localhost:8000/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email,
                    password: pass,
                    role
                })
            });

            const data = await res.json();

            if (!res.ok) {
                alert(data.detail);
                return;
            }

            localStorage.setItem("token", data.access_token);

            // decode JWT payload
            const payload = JSON.parse(
                atob(data.access_token.split(".")[1])
            );

            // If role mismatch, block login
            if (payload.role !== role) {
                alert(`You are registered as ${payload.role}. Please login via correct portal.`);
                return;
            }

            localStorage.setItem("userEmail", payload.sub);

            // Navigate based on REAL backend role
            navigate(`/portal/${payload.role}`);

        } catch (err) {
            console.error(err);
            alert("Login failed");
        }
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
                {role.toUpperCase()} Login
            </h2>

            <p style={{ color: C.muted, fontSize: 14, marginBottom: 40 }}>
                Enter your credentials to continue
            </p>

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
                    Login
                </button>

            </div>

            <div style={{
                marginTop: 40,
                paddingTop: 20,
                borderTop: `1px solid ${C.border}`,
                fontSize: 13
            }}>
                <span style={{ color: C.muted }}>
                    {config.altText}{" "}
                </span>

                {role === "claimer" ? (
                    <span
                        onClick={() => navigate(`/signup/${role}`)}
                        style={{
                            color: C.accent,
                            fontWeight: 700,
                            cursor: "pointer"
                        }}
                    >
                        {config.altLink}
                    </span>
                ) : (
                    <span style={{ color: C.accent, fontWeight: 700 }}>
                        {config.altLink}
                    </span>
                )}
            </div>

        </div>
    );
}
