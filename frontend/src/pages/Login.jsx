import { useState } from "react";
import { C } from "../constants/theme";
import { useParams, useNavigate } from "react-router-dom";
import { authAPI } from "../services/api";

export default function Login() {
    const { role } = useParams();
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [pass, setPass] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const roleMap = {
        claimer: {
            title: "Customer Login",
            desc: "Access your claims and policy details",
            icon: "🛡️",
            primaryBtn: "Login to Portal",
            portalPath: "/portal/claimer",
            altText: "New to IntelliClaim?",
            altLink: "Create an account",
        },
        reviewer: {
            title: "Reviewer SSO",
            desc: "Internal Claims Processing Environment",
            icon: "🔍",
            primaryBtn: "Sign in with Okta",
            portalPath: "/portal/reviewer",
            altText: "Issues with SSO?",
            altLink: "Contact IT Support",
        },
        admin: {
            title: "Admin Terminal",
            desc: "Secure System Administration & Analytics",
            icon: "⚙️",
            primaryBtn: "Authorize with Key",
            portalPath: "/portal/admin",
            altText: "Security Notice:",
            altLink: "MFA Required for all sessions",
        },
    };

    const config = roleMap[role];

    if (!config) {
        return <div style={{ padding: 40 }}>Invalid role.</div>;
    }

    const handleLogin = async () => {
        if (!email || !pass) {
            setError("Please enter email and password");
            return;
        }

        setLoading(true);
        setError("");

        try {
            // Login to get token
            await authAPI.login(email, pass);

            // Get current user info from /me endpoint
            const userInfo = await authAPI.getCurrentUser();

            if (userInfo.role !== role) {
                setError(
                    `User role (${userInfo.role}) does not match selected role (${role})`
                );
                return;
            }

            navigate(config.portalPath);
        } catch (err) {
            setError(err.message || "Login failed. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div
            style={{
                maxWidth: 420,
                margin: "120px auto",
                padding: "40px",
                background: C.panel,
                border: `1px solid ${C.border}`,
                borderRadius: 24,
                boxShadow: "0 20px 50px rgba(0,0,0,0.3)",
                textAlign: "center",
            }}
        >
            {/* Back Button */}
            <button
                onClick={() => navigate("/role-select")}
                style={{
                    background: "transparent",
                    border: "none",
                    color: C.muted,
                    cursor: "pointer",
                    marginBottom: 20,
                }}
            >
                ← Back
            </button>

            <h2 style={{ marginBottom: 8 }}>
                {config.icon} {config.title}
            </h2>
            <p style={{ color: C.muted, marginBottom: 24 }}>{config.desc}</p>

            {/* Error Message */}
            {error && (
                <div
                    style={{
                        background: "rgba(239, 68, 68, 0.1)",
                        border: "1px solid #ef4444",
                        borderRadius: 12,
                        padding: 12,
                        marginBottom: 20,
                        color: "#fca5a5",
                        fontSize: 14,
                    }}
                >
                    {error}
                </div>
            )}

            {/* Claimer Login Form */}
            {role === "claimer" ? (
                <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                    <input
                        type="email"
                        placeholder="Email Address"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        disabled={loading}
                        style={inputStyle}
                    />

                    <input
                        type="password"
                        placeholder="Password"
                        value={pass}
                        onChange={(e) => setPass(e.target.value)}
                        disabled={loading}
                        style={inputStyle}
                    />

                    <button
                        onClick={handleLogin}
                        disabled={loading}
                        style={{
                            ...primaryBtnStyle,
                            background: C.accent,
                            opacity: loading ? 0.7 : 1,
                        }}
                    >
                        {loading ? "Logging in..." : config.primaryBtn}
                    </button>
                </div>
            ) : (
                <button
                    onClick={handleLogin}
                    disabled={loading}
                    style={{
                        ...primaryBtnStyle,
                        background: role === "admin" ? C.text : "#a855f7",
                        opacity: loading ? 0.7 : 1,
                    }}
                >
                    {loading ? "Signing in..." : config.primaryBtn}
                </button>
            )}

            {/* Footer */}
            <div
                style={{
                    marginTop: 40,
                    paddingTop: 20,
                    borderTop: `1px solid ${C.border}`,
                }}
            >
                <span style={{ color: C.muted, fontSize: 13 }}>
                    {config.altText}{" "}
                </span>
                <span
                    style={{
                        color: C.accent,
                        fontSize: 13,
                        fontWeight: 700,
                        cursor: "pointer",
                    }}
                >
                    {config.altLink}
                </span>
            </div>
        </div>
    );
}

/* Reusable Styles */
const inputStyle = {
    background: "rgba(255,255,255,0.05)",
    border: "1px solid #333",
    padding: "16px",
    borderRadius: 12,
    color: "#fff",
    fontSize: 14,
    outline: "none",
};

const primaryBtnStyle = {
    border: "none",
    padding: "18px",
    borderRadius: 12,
    fontWeight: 900,
    fontSize: 16,
    cursor: "pointer",
    boxShadow: "0 10px 20px rgba(0,0,0,0.3)",
};