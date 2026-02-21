import { useState, useRef } from "react";
import { C } from "../constants/theme";

export default function FileUploader({ label, icon, onFilesChange, files = [] }) {
    const fileInputRef = useRef(null);
    const [isDragging, setIsDragging] = useState(false);

    const handleFileSelect = (e) => {
        const newFiles = Array.from(e.target.files);
        onFilesChange([...files, ...newFiles]);
    };

    const removeFile = (index) => {
        const updatedFiles = files.filter((_, i) => i !== index);
        onFilesChange(updatedFiles);
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        const newFiles = Array.from(e.dataTransfer.files);
        onFilesChange([...files, ...newFiles]);
    };

    return (
        <div style={{ marginBottom: 12 }}>
            <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                style={{
                    background: C.panel,
                    padding: "16px",
                    borderRadius: 8,
                    border: `1px dashed ${isDragging ? C.blue : C.border}`,
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    transition: "all 0.2s ease"
                }}
            >
                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                    <span style={{
                        background: icon === "🆔" ? "#a855f7" : C.text,
                        color: "#000",
                        width: 24,
                        height: 24,
                        borderRadius: 4,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        fontSize: 12
                    }}>{icon}</span>
                    <span style={{ color: C.text, fontSize: 13, fontWeight: 700 }}>{label}</span>
                </div>

                <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                    <div style={{ color: files.length > 0 ? C.green : C.yellow, fontSize: 11, fontWeight: 800 }}>
                        {files.length > 0 ? `✓ ${files.length} File(s)` : "⏳ Pending"}
                    </div>
                    <button
                        onClick={() => fileInputRef.current.click()}
                        style={{
                            background: C.blue,
                            color: "#fff",
                            border: "none",
                            padding: "6px 12px",
                            borderRadius: 4,
                            fontSize: 11,
                            fontWeight: 700,
                            cursor: "pointer"
                        }}
                    >
                        Upload
                    </button>
                    <input
                        type="file"
                        multiple
                        ref={fileInputRef}
                        onChange={handleFileSelect}
                        style={{ display: "none" }}
                    />
                </div>
            </div>

            {files.length > 0 && (
                <div style={{ marginTop: 8, display: "flex", flexDirection: "column", gap: 4 }}>
                    {files.map((file, i) => (
                        <div key={i} style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                            background: C.panel + "88",
                            padding: "6px 12px",
                            borderRadius: 6,
                            fontSize: 11,
                            color: C.muted,
                            border: `1px solid ${C.border}`
                        }}>
                            <span style={{ maxWidth: "80%", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                                {file.name}
                            </span>
                            <button
                                onClick={() => removeFile(i)}
                                style={{
                                    background: "transparent",
                                    border: "none",
                                    color: C.red,
                                    cursor: "pointer",
                                    fontSize: 14,
                                    padding: 0
                                }}
                            >
                                ×
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
