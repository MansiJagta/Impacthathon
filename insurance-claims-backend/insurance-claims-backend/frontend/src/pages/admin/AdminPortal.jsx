import { useState } from "react";
import { C } from "../../constants/theme";
import AdminDashboard from "../../components/AdminDashboard";
import UserActivity from "../../components/UserActivity";
import ReviewerHistory from "../reviewer/ReviewerHistory";

export default function AdminPortal() {

    const [activeTab, setActiveTab] = useState("dashboard");

    const tabs = [
        { id: "dashboard", label: "Dashboard" },
        { id: "claims", label: "All Claims" },
        { id: "users", label: "User Activity" }
    ];

    return (
        <div style={{ padding: 40, display: "flex", flexDirection: "column", gap: 32 }}>

            {/* Tabs */}
            <div style={{ display: "flex", gap: 24, borderBottom: `1px solid ${C.border}`, paddingBottom: 16 }}>
                {tabs.map(tab => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        style={{
                            background: "transparent",
                            border: "none",
                            color: activeTab === tab.id ? C.accent : C.muted,
                            fontWeight: 800,
                            fontSize: 14,
                            cursor: "pointer",
                            borderBottom: activeTab === tab.id ? `2px solid ${C.accent}` : "none",
                            paddingBottom: 6
                        }}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>

            {/* Content */}
            {activeTab === "dashboard" && <AdminDashboard />}
            {activeTab === "claims" && <ReviewerHistory />}
            {activeTab === "users" && <UserActivity />}

        </div>
    );
}
