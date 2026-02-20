import { useState } from "react";
import { C } from "../../constants/theme";

export default function NewClaimForm() {
    const [type, setType] = useState("Health");

    const types = [
        { id: "Health", icon: "🏥" },
        { id: "Motor", icon: "🚗" },
        { id: "Property", icon: "🏠" },
    ];

    return (
        <div>
            <div style={{ marginBottom: 40 }}>
                <p style={{ color: C.muted, fontSize: 11, fontWeight: 800, textTransform: "uppercase", marginBottom: 16 }}>
                    Step 1: Select Insurance Type
                </p>
                <div style={{ display: "flex", gap: 12 }}>
                    {types.map(t => (
                        <button
                            key={t.id}
                            onClick={() => setType(t.id)}
                            style={{
                                background: type === t.id ? C.blue + "22" : C.panel,
                                color: type === t.id ? C.blue : C.muted,
                                border: `1px solid ${type === t.id ? C.blue : C.border}`,
                                padding: "12px 24px",
                                borderRadius: 8,
                                cursor: "pointer",
                                fontWeight: 700,
                                display: "flex",
                                alignItems: "center",
                                gap: 8,
                                flex: 1
                            }}
                        >
                            <span>{t.icon}</span> {t.id}
                        </button>
                    ))}
                </div>
            </div>

            <div style={{ display: "flex", gap: 40 }}>
                <div style={{ flex: 1.5 }}>
                    <h3 style={{ color: C.text, display: "flex", alignItems: "center", gap: 12, marginBottom: 24, fontSize: 18 }}>
                        <span>{types.find(t => t.id === type).icon}</span> {type.toUpperCase()} INSURANCE CLAIM FORM
                    </h3>
                    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                        {["Policy Number", "Patient Name", "Hospital Name", "Admission Date", "Discharge Date", "Claim Amount (₹)"].map(field => (
                            <div key={field}>
                                <label style={{ display: "block", color: C.muted, fontSize: 11, fontWeight: 800, marginBottom: 8, textTransform: "uppercase" }}>{field}</label>
                                <input
                                    type="text"
                                    placeholder={field}
                                    style={{
                                        width: "100%",
                                        background: C.panel,
                                        border: `1px solid ${C.border}`,
                                        padding: "12px",
                                        borderRadius: 6,
                                        color: C.text,
                                        outline: "none"
                                    }}
                                />
                            </div>
                        ))}
                    </div>
                </div>

                <div style={{ flex: 1 }}>
                    <h3 style={{ color: C.text, display: "flex", alignItems: "center", gap: 12, marginBottom: 24, fontSize: 18 }}>
                        <span>📎</span> Required Documents
                    </h3>
                    <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                        {[
                            { name: "Policy Document", icon: "📄", status: "Uploaded", color: C.green },
                            { name: "Patient ID Proof", icon: "🆔", status: "Uploaded", color: C.green },
                            { name: "Hospital Bill", icon: "🏥", status: "Pending", color: C.yellow },
                            { name: "Discharge Summary", icon: "📄", status: "Pending", color: C.yellow },
                        ].map((doc, i) => (
                            <div key={i} style={{
                                background: C.panel,
                                padding: "16px",
                                borderRadius: 8,
                                border: `1px solid ${C.border}`,
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center"
                            }}>
                                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                                    <span style={{
                                        background: doc.name.includes("ID") ? "#a855f7" : C.text,
                                        color: "#000",
                                        width: 24,
                                        height: 24,
                                        borderRadius: 4,
                                        display: "flex",
                                        alignItems: "center",
                                        justifyContent: "center",
                                        fontSize: 12
                                    }}>{doc.icon}</span>
                                    <span style={{ color: C.text, fontSize: 13, fontWeight: 700 }}>{doc.name}</span>
                                </div>
                                <div style={{ color: doc.color, fontSize: 11, fontWeight: 800 }}>
                                    {doc.status === "Uploaded" ? "✓ Uploaded" : "⏳ Pending"}
                                </div>
                            </div>
                        ))}
                    </div>

                    <div style={{ display: "flex", gap: 16, marginTop: 32 }}>
                        <button style={{
                            flex: 1,
                            background: C.blue,
                            color: "#fff",
                            border: "none",
                            padding: "16px",
                            borderRadius: 8,
                            fontWeight: 800,
                            cursor: "pointer"
                        }}>Submit Claim</button>
                        <button style={{
                            flex: 1,
                            background: C.panel,
                            color: C.text,
                            border: `1px solid ${C.border}`,
                            padding: "16px",
                            borderRadius: 8,
                            fontWeight: 800,
                            cursor: "pointer"
                        }}>Save Draft</button>
                    </div>
                </div>
            </div>
        </div>
    );
}
