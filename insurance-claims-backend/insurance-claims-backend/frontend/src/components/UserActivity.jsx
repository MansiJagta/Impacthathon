import { C } from "../constants/theme";

export default function UserActivity() {

    return (
        <div style={{ background: C.panel, border: `1px solid ${C.border}`, borderRadius: 16, overflow: "hidden" }}>
            <div style={{ padding: "24px", borderBottom: `1px solid ${C.border}`, background: "rgba(255,255,255,0.02)" }}>
                <h3 style={{ color: C.muted, fontSize: 13, fontWeight: 800, textTransform: "uppercase", letterSpacing: 1 }}>
                    User Activity Overview
                </h3>
            </div>

            <div style={{ overflowX: "auto" }}>
                <table style={{ width: "100%", borderCollapse: "collapse" }}>
                    <thead>
                        <tr style={{ textAlign: "left" }}>
                            <th style={thStyle}>User</th>
                            <th style={thStyle}>Role</th>
                            <th style={thStyle}>Claims</th>
                            <th style={thStyle}>Approval %</th>
                            <th style={thStyle}>Last Active</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style={{ borderBottom: `1px solid ${C.border}` }}>
                            <td style={tdStyle}>John Doe</td>
                            <td style={tdStyle}>👤 Claimer</td>
                            <td style={tdStyle}>24</td>
                            <td style={{ ...tdStyle, color: C.green, fontWeight: 800 }}>83%</td>
                            <td style={{ ...tdStyle, color: C.muted }}>2m ago</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
}

const thStyle = {
    padding: "12px 24px",
    color: "#64748b",
    fontSize: 11,
    fontWeight: 800,
    textTransform: "uppercase",
};

const tdStyle = {
    padding: "20px 24px",
    color: "#fff",
    fontSize: 13,
    fontWeight: 600
};
