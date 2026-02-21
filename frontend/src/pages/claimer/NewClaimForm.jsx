<<<<<<< HEAD
import { useState } from "react";
import { C } from "../../constants/theme";

export default function NewClaimForm() {
    const [type, setType] = useState("Health");

    const types = [
        { id: "Health", icon: "🏥" },
        { id: "Motor", icon: "🚗" },
        { id: "Property", icon: "🏠" },
    ];

=======
import { useState, useEffect, useRef } from "react";
import { C } from "../../constants/theme";
import FileUploader from "../../components/FileUploader";
import api from "../../services/api";
import { useNavigate } from "react-router-dom";

export default function NewClaimForm() {
    const navigate = useNavigate();
    const [type, setType] = useState("Motor");
    const [formData, setFormData] = useState({});
    const [documents, setDocuments] = useState({
        policy: [],
        id_proof: [],
        bill: [],
        summary: [],
        other: []
    });
    const [isSubmitting, setIsSubmitting] = useState(false);
    const commentRef = useRef(null);

    // Keyboard shortcut handler
    useEffect(() => {
        const handleKeyDown = (e) => {
            if (e.ctrlKey && e.altKey && e.key.toLowerCase() === 'm') {
                e.preventDefault();
                commentRef.current?.focus();
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, []);

    const types = [
        { id: "Motor", icon: "🚗" },
        { id: "Health", icon: "🏥" },
        { id: "Property", icon: "🏠" },
    ];

    const insuranceConfig = {
        Motor: {
            fields: ["Policy Number", "Vehicle Number", "Accident Date", "Garage Name", "Claim Amount (₹)"],
            docs: [
                { id: "policy", name: "Policy Document", icon: "📄" },
                { id: "id_proof", name: "Driving License", icon: "🆔" },
                { id: "bill", name: "Repair Estimate", icon: "🛠️" },
                { id: "summary", name: "Accident Images", icon: "📸" },
            ]
        },
        Health: {
            fields: ["Policy Number", "Patient Name", "Hospital Name", "Admission Date", "Discharge Date", "Claim Amount (₹)"],
            docs: [
                { id: "policy", name: "Policy Document", icon: "📄" },
                { id: "id_proof", name: "Patient ID Proof", icon: "🆔" },
                { id: "bill", name: "Hospital Bill", icon: "🏥" },
                { id: "summary", name: "Discharge Summary", icon: "📄" },
            ]
        },
        Property: {
            fields: ["Policy Number", "Property Address", "Damage Date", "Estimated Loss (₹)"],
            docs: [
                { id: "policy", name: "Policy Document", icon: "📄" },
                { id: "id_proof", name: "Property Ownership Proof", icon: "🏠" },
                { id: "bill", name: "Damage Assessment", icon: "📊" },
                { id: "summary", name: "Photos of Damage", icon: "📸" },
            ]
        }
    };

    const handleFieldChange = (field, value) => {
        setFormData(prev => ({ ...prev, [field]: value }));
    };

    const handleFilesChange = (docId, files) => {
        setDocuments(prev => ({ ...prev, [docId]: files }));
    };

    const handleSubmit = async () => {
        if (Object.values(documents).flat().length === 0) {
            alert("Please upload at least one document.");
            return;
        }

        setIsSubmitting(true);
        try {
            const userEmail = localStorage.getItem("userEmail") || "demo@example.com";
            const data = new FormData();
            data.append("claim_type", type);
            data.append("claimer_email", userEmail);

            // Map form data fields
            Object.entries(formData).forEach(([key, value]) => {
                data.append(key, value);
            });

            // Append all files with their document types if possible
            // The backend expects 'files' as a list of UploadFile
            Object.values(documents).flat().forEach(file => {
                data.append("files", file);
            });

            const result = await api.submitClaim(data);
            alert("Claim submitted successfully! ID: " + result.claim_id);
            navigate("/portal/claimer/history"); // Redirect to history after success
        } catch (error) {
            console.error("Submission error:", error);
            alert("Failed to submit claim: " + error.message);
        } finally {
            setIsSubmitting(false);
        }
    };

    const currentConfig = insuranceConfig[type];

>>>>>>> f930c12 (update project before sync)
    return (
        <div>
            <div style={{ marginBottom: 40 }}>
                <p style={{ color: C.muted, fontSize: 11, fontWeight: 800, textTransform: "uppercase", marginBottom: 16 }}>
<<<<<<< HEAD
                    Step 1: Select Insurance Type
=======
                    Step 1: SELECT INSURANCE TYPE
>>>>>>> f930c12 (update project before sync)
                </p>
                <div style={{ display: "flex", gap: 12 }}>
                    {types.map(t => (
                        <button
                            key={t.id}
<<<<<<< HEAD
                            onClick={() => setType(t.id)}
=======
                            onClick={() => {
                                setType(t.id);
                                setFormData({});
                                setDocuments({
                                    policy: [],
                                    id_proof: [],
                                    bill: [],
                                    summary: [],
                                    other: []
                                });
                            }}
>>>>>>> f930c12 (update project before sync)
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
<<<<<<< HEAD
                                flex: 1
=======
                                flex: 1,
                                transition: "all 0.2s ease"
>>>>>>> f930c12 (update project before sync)
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
<<<<<<< HEAD
                        {["Policy Number", "Patient Name", "Hospital Name", "Admission Date", "Discharge Date", "Claim Amount (₹)"].map(field => (
=======
                        {currentConfig.fields.map(field => (
>>>>>>> f930c12 (update project before sync)
                            <div key={field}>
                                <label style={{ display: "block", color: C.muted, fontSize: 11, fontWeight: 800, marginBottom: 8, textTransform: "uppercase" }}>{field}</label>
                                <input
                                    type="text"
                                    placeholder={field}
<<<<<<< HEAD
=======
                                    value={formData[field] || ""}
                                    onChange={(e) => handleFieldChange(field, e.target.value)}
>>>>>>> f930c12 (update project before sync)
                                    style={{
                                        width: "100%",
                                        background: C.panel,
                                        border: `1px solid ${C.border}`,
                                        padding: "12px",
                                        borderRadius: 6,
                                        color: C.text,
<<<<<<< HEAD
                                        outline: "none"
=======
                                        outline: "none",
                                        boxSizing: "border-box"
>>>>>>> f930c12 (update project before sync)
                                    }}
                                />
                            </div>
                        ))}
<<<<<<< HEAD
=======

                        <div>
                            <label style={{ display: "block", color: C.muted, fontSize: 11, fontWeight: 800, marginBottom: 8, textTransform: "uppercase" }}>
                                Comments (Press Ctrl+Alt+M to focus)
                            </label>
                            <textarea
                                ref={commentRef}
                                placeholder="Add any additional details or notes here..."
                                value={formData.comments || ""}
                                onChange={(e) => handleFieldChange("comments", e.target.value)}
                                style={{
                                    width: "100%",
                                    background: C.panel,
                                    border: `1px solid ${C.border}`,
                                    padding: "12px",
                                    borderRadius: 6,
                                    color: C.text,
                                    outline: "none",
                                    boxSizing: "border-box",
                                    minHeight: "100px",
                                    resize: "vertical"
                                }}
                            />
                        </div>
>>>>>>> f930c12 (update project before sync)
                    </div>
                </div>

                <div style={{ flex: 1 }}>
                    <h3 style={{ color: C.text, display: "flex", alignItems: "center", gap: 12, marginBottom: 24, fontSize: 18 }}>
                        <span>📎</span> Required Documents
                    </h3>
<<<<<<< HEAD
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
=======
                    <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                        {currentConfig.docs.map((doc) => (
                            <FileUploader
                                key={doc.id}
                                label={doc.name}
                                icon={doc.icon}
                                files={documents[doc.id]}
                                onFilesChange={(files) => handleFilesChange(doc.id, files)}
                            />
                        ))}
                        <FileUploader
                            label="Additional Documents"
                            icon="📂"
                            files={documents.other}
                            onFilesChange={(files) => handleFilesChange("other", files)}
                        />
                    </div>

                    <div style={{ display: "flex", gap: 16, marginTop: 32 }}>
                        <button
                            disabled={isSubmitting}
                            onClick={handleSubmit}
                            style={{
                                flex: 1,
                                background: C.blue,
                                color: "#fff",
                                border: "none",
                                padding: "16px",
                                borderRadius: 8,
                                fontWeight: 800,
                                cursor: isSubmitting ? "not-allowed" : "pointer",
                                opacity: isSubmitting ? 0.7 : 1
                            }}
                        >
                            {isSubmitting ? "Submitting..." : "Submit Claim"}
                        </button>
>>>>>>> f930c12 (update project before sync)
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
