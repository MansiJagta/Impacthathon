import { C } from "../../constants/theme";
import { GaugeBar } from "../../components/GaugeBar";
import { useNavigate } from "react-router-dom";

const FRAUD_THRESHOLD = 0.6;

// 🔥 Sample Claims Data
const claims = [
    {
        id: "CL-2024-0890",
        type: "Health",
        amount: "₹1,20,000",
        hospital: "Apollo Hospital",
        patient: "Rajesh Kumar",
        dates: "10-15 Feb 2024",
        submittedBy: "John (claimer@email.com)",
        riskScore: 0.58,
        fraudScore: 0.75,
        status: "Pending"
    },
    {
        id: "CL-2024-0911",
        type: "Health",
        amount: "₹45,000",
        hospital: "Fortis",
        patient: "Amit Sharma",
        dates: "01-03 Feb 2024",
        submittedBy: "Rita (rita@email.com)",
        riskScore: 0.30,
        fraudScore: 0.22,
        status: "Pending"
    },
    {
        id: "CL-2024-0922",
        type: "Motor",
        amount: "₹2,80,000",
        hospital: "N/A",
        patient: "Vikram Singh",
        dates: "12 Feb 2024",
        submittedBy: "Arun (arun@email.com)",
        riskScore: 0.80,
        fraudScore: 0.82,
        status: "Pending"
    }
];

export default function ReviewQueue() {
    const navigate = useNavigate();

    // 🔥 Filter only high fraud claims
    const highFraudClaims = claims
        .filter(claim => claim.fraudScore >= FRAUD_THRESHOLD)
        .sort((a, b) => b.fraudScore - a.fraudScore); // highest first

    return (
        <div>

            {/* If no high fraud claims */}
            {highFraudClaims.length === 0 && (
                <div style={{
                    background: C.panel,
                    border: `1px solid ${C.border}`,
                    padding: 40,
                    borderRadius: 16,
                    textAlign: "center",
                    color: C.muted
                }}>
                    No high-risk claims for manual review.
                </div>
            )}

            {highFraudClaims.map((claim) => (
                <div
                    key={claim.id}
                    style={{
                        background: C.panel,
                        border: `1px solid ${C.border}`,
                        borderRadius: 16,
                        padding: 32,
                        marginBottom: 40
                    }}
                >

                    {/* Header */}
                    <div style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        marginBottom: 32
                    }}>
                        <h2 style={{
                            color: C.text,
                            fontSize: 20,
                            fontWeight: 800
                        }}>
                            Claim {claim.id}
                        </h2>

                        <span style={{
                            background: "#713f12",
                            color: C.yellow,
                            padding: "4px 12px",
                            borderRadius: 20,
                            fontSize: 11,
                            fontWeight: 800
                        }}>
                            ⚠ High Fraud Risk
                        </span>
                    </div>

                    {/* Layout */}
                    <div style={{ display: "flex", gap: 48 }}>

                        {/* LEFT: Claim Details */}
                        <div style={{ flex: 1 }}>
                            <h4 style={{
                                color: C.muted,
                                fontSize: 11,
                                fontWeight: 800,
                                textTransform: "uppercase",
                                letterSpacing: 1,
                                marginBottom: 24,
                                paddingBottom: 12,
                                borderBottom: `1px solid ${C.border}`
                            }}>
                                Claim Details
                            </h4>

                            {[
                                { label: "Type", value: claim.type },
                                { label: "Amount", value: claim.amount },
                                { label: "Hospital", value: claim.hospital },
                                { label: "Patient", value: claim.patient },
                                { label: "Dates", value: claim.dates },
                                { label: "Submitted by", value: claim.submittedBy },
                            ].map((item, i) => (
                                <div
                                    key={i}
                                    style={{
                                        display: "flex",
                                        justifyContent: "space-between",
                                        marginBottom: 20
                                    }}
                                >
                                    <span style={{ color: C.muted, fontSize: 13 }}>
                                        {item.label}
                                    </span>
                                    <span style={{ color: C.text, fontSize: 13, fontWeight: 700 }}>
                                        {item.value}
                                    </span>
                                </div>
                            ))}

                            <textarea
                                placeholder="Add notes (optional)…"
                                style={{
                                    width: "100%",
                                    background: C.bg,
                                    border: `1px solid ${C.border}`,
                                    color: C.text,
                                    borderRadius: 8,
                                    padding: "10px",
                                    fontSize: 12,
                                    resize: "vertical",
                                    minHeight: 70,
                                    outline: "none",
                                    boxSizing: "border-box",
                                    marginTop: 20
                                }}
                            />
                        </div>

                        {/* RIGHT: AI Analysis */}
                        <div style={{ flex: 1 }}>
                            <h4 style={{
                                color: C.muted,
                                fontSize: 11,
                                fontWeight: 800,
                                textTransform: "uppercase",
                                letterSpacing: 1,
                                marginBottom: 24,
                                paddingBottom: 12,
                                borderBottom: `1px solid ${C.border}`
                            }}>
                                AI Analysis
                            </h4>

                            <div style={{ marginBottom: 24 }}>
                                <GaugeBar label="Risk Score" val={claim.riskScore} />
                                <GaugeBar label="Fraud Score" val={claim.fraudScore} />
                            </div>

                            <div style={{
                                background: "#ef444411",
                                border: "1px solid #ef444422",
                                padding: "12px",
                                borderRadius: 8,
                                color: "#f87171",
                                fontSize: 12
                            }}>
                                ⚠ This claim exceeded fraud threshold ({FRAUD_THRESHOLD})
                            </div>
                        </div>
                    </div>

                    {/* Decision Buttons */}
                    <div style={{
                        marginTop: 40,
                        paddingTop: 40,
                        borderTop: `1px solid ${C.border}`,
                        display: "flex",
                        gap: 16
                    }}>
                        <button style={{
                            flex: 1,
                            background: C.green,
                            color: "#fff",
                            border: "none",
                            padding: "16px",
                            borderRadius: 8,
                            fontWeight: 800,
                            cursor: "pointer"
                        }}>
                            Approve Claim
                        </button>

                        <button style={{
                            flex: 1,
                            background: C.red,
                            color: "#fff",
                            border: "none",
                            padding: "16px",
                            borderRadius: 8,
                            fontWeight: 800,
                            cursor: "pointer"
                        }}>
                            Reject & Flag
                        </button>

                        <button
                            onClick={() => navigate(`/claim-details/${claim.id}`)}
                            style={{
                                flex: 1,
                                background: C.panel,
                                color: C.text,
                                border: `1px solid ${C.border}`,
                                padding: "16px",
                                borderRadius: 8,
                                fontWeight: 800,
                                cursor: "pointer"
                            }}
                        >
                            Request More Info
                        </button>
                    </div>

                </div>
            ))}
        </div>
    );
}
