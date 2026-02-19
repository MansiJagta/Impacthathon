import { C } from "../constants/theme";
import { useNavigate } from "react-router-dom";


const FeatureCard = ({ title, desc, icon }) => (
    <div style={{
        background: C.panel,
        border: `1px solid ${C.border}`,
        borderRadius: 24,
        padding: "40px",
        flex: 1,
        minWidth: 280,
        display: "flex",
        flexDirection: "column",
        gap: 20,
        transition: "all 0.3s ease",
        cursor: "default"
    }}
        onMouseEnter={(e) => {
            e.currentTarget.style.transform = "translateY(-8px)";
            e.currentTarget.style.borderColor = C.accent;
            e.currentTarget.style.boxShadow = `0 12px 30px ${C.accent}11`;
        }}
        onMouseLeave={(e) => {
            e.currentTarget.style.transform = "translateY(0)";
            e.currentTarget.style.borderColor = C.border;
            e.currentTarget.style.boxShadow = "none";
        }}
    >
        <div style={{
            fontSize: 40,
            background: `${C.accent}11`,
            width: 80,
            height: 80,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            borderRadius: 20,
            marginBottom: 10
        }}>{icon}</div>
        <h3 style={{ color: C.text, fontSize: 24, fontWeight: 800 }}>{title}</h3>
        <p style={{ color: C.muted, fontSize: 16, lineHeight: 1.6 }}>{desc}</p>
    </div>
);

const DetailSection = ({ title, text, color = C.accent }) => (
    <div style={{ flex: 1, minWidth: 300 }}>
        <h3 style={{ color: C.text, fontSize: 32, fontWeight: 900, marginBottom: 24, display: "flex", alignItems: "center", gap: 12 }}>
            <span style={{ width: 4, height: 32, background: color, borderRadius: 2 }}></span>
            {title}
        </h3>
        <p style={{ color: C.muted, fontSize: 18, lineHeight: 1.8 }}>{text}</p>
    </div>
);

export default function Home({ onGetStarted }) {
    const navigate = useNavigate();

    return (
        <div style={{ background: C.bg, minHeight: "100vh" }}>
            {/* Hero Section */}
            <section style={{
                padding: "160px 24px 100px",
                textAlign: "left",
                maxWidth: 1200,
                margin: "0 auto",
                display: "flex",
                flexDirection: "column",
                gap: 32
            }}>
                <div style={{
                    display: "inline-flex",
                    alignItems: "center",
                    gap: 8,
                    background: `${C.accent}22`,
                    border: `1px solid ${C.accent}44`,
                    padding: "8px 20px",
                    borderRadius: 30,
                    color: C.accent,
                    fontSize: 13,
                    fontWeight: 800,
                    textTransform: "uppercase",
                    letterSpacing: 1.5,
                    alignSelf: "flex-start"
                }}>
                    🛡️ AI-Powered Insurance Validation
                </div>

                <h1 style={{
                    color: "#fff",
                    fontSize: 84,
                    fontWeight: 900,
                    lineHeight: 1,
                    maxWidth: 900,
                    letterSpacing: -2
                }}>
                    Process Claims in <br />
                    <span style={{ color: C.accent }}>Minutes, Not Months</span>
                </h1>

                <p style={{
                    color: C.muted,
                    fontSize: 22,
                    maxWidth: 650,
                    lineHeight: 1.6,
                    fontWeight: 500
                }}>
                    Intelligent automation with fraud detection, policy validation & instant approvals for trusted insurance providers.
                </p>

                <div style={{ display: "flex", gap: 20, marginTop: 20 }}>
                    <button
                        onClick={() => navigate("/role-select")}
                        style={{
                            background: C.accent,
                            color: "#000",
                            border: "none",
                            padding: "20px 48px",
                            borderRadius: 12,
                            fontSize: 20,
                            fontWeight: 900,
                            cursor: "pointer",
                            boxShadow: `0 10px 30px ${C.accent}44`,
                            transition: "all 0.2s"
                        }}
                        onMouseEnter={(e) => e.currentTarget.style.transform = "scale(1.02)"}
                        onMouseLeave={(e) => e.currentTarget.style.transform = "scale(1)"}
                    >
                        Get Started →
                    </button>
                    <button style={{
                        background: "rgba(255,255,255,0.05)",
                        color: "#fff",
                        border: `1px solid ${C.border}`,
                        padding: "20px 40px",
                        borderRadius: 12,
                        fontSize: 20,
                        fontWeight: 700,
                        cursor: "pointer",
                        transition: "all 0.2s"
                    }}
                        onMouseEnter={(e) => e.currentTarget.style.background = "rgba(255,255,255,0.1)"}
                        onMouseLeave={(e) => e.currentTarget.style.background = "rgba(255,255,255,0.05)"}
                    >
                        Watch Demo
                    </button>
                </div>
            </section>

            {/* Feature Cards Section */}
            <section style={{ padding: "120px 24px", borderTop: `1px solid ${C.border}`, borderBottom: `1px solid ${C.border}`, background: "rgba(0,0,0,0.2)" }}>
                <div
                    style={{
                        maxWidth: 1200,
                        margin: "0 auto",
                        display: "grid",
                        gridTemplateColumns: "repeat(4, 1fr)",
                        gap: 32,
                    }}
                >
                    <FeatureCard
                        title="Claims Processing"
                        desc="Resolve most claims automatically, in real time, freeing claims handlers to manage complex and sensitive claims faster."
                        icon="🏥"
                    />
                    <FeatureCard
                        title="Fraud Detection"
                        desc="Automatically identify anomalies and unusual patterns. Ensure handlers have the time and insights to intercept fraud."
                        icon="🔍"
                    />
                    <FeatureCard
                        title="Policy Validation"
                        desc="Instantly verify coverage details and policy limits against current database to ensure accurate processing."
                        icon="🛡️"
                    />
                    <FeatureCard
                        title="Instant Approvals"
                        desc="Low-risk claims are approved instantly, providing immediate satisfaction and reducing manual backlog."
                        icon="⚡"
                    />
                </div>
            </section>

            {/* Industries Section */}
            <section style={{ padding: "100px 24px" }}>
                <div style={{ maxWidth: 1200, margin: "0 auto", textAlign: "center" }}>
                    <h2 style={{ color: "#fff", fontSize: 40, fontWeight: 900, marginBottom: 60, letterSpacing: -1 }}>Supported Industries</h2>
                    <div style={{ display: "flex", justifyContent: "space-between", gap: 32, flexWrap: "wrap" }}>
                        {["Health & Life", "Motor & Auto", "Home & Property"].map(industry => (
                            <div key={industry} style={{
                                flex: 1,
                                padding: "40px 24px",
                                background: C.panel,
                                border: `1px solid ${C.border}`,
                                borderRadius: 20,
                                fontWeight: 800,
                                color: "#fff",
                                fontSize: 18,
                                minWidth: 200,
                                transition: "all 0.3s ease"
                            }}
                                onMouseEnter={(e) => e.currentTarget.style.borderColor = C.accent}
                                onMouseLeave={(e) => e.currentTarget.style.borderColor = C.border}
                            >
                                {industry}
                            </div>
                        ))}
                    </div>
                </div>
            </section>
        </div>
    );
}
