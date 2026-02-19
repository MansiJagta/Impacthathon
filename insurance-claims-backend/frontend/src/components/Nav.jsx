import { C } from "../constants/theme";
import { useNavigate } from "react-router-dom";

export default function Nav() {

    const navigate = useNavigate();
    const role = localStorage.getItem("userRole");

    const handleLogout = () => {
        localStorage.removeItem("userRole");
        navigate("/");
    };

    return (
        <nav style={{
            background: C.panel,
            borderBottom: `1px solid ${C.border}`,
            padding: "12px 28px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            position: "sticky",
            top: 0,
            zIndex: 100
        }}>

            {/* Logo */}
            <div
                onClick={() => navigate("/")}
                style={{
                    color: C.text,
                    fontWeight: 700,
                    fontSize: 18,
                    letterSpacing: 1,
                    cursor: "pointer"
                }}
            >
                IntelliClaim
            </div>

            {/* Right Side */}
            <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
                {role ? (
                    <div style={{ display: "flex", alignItems: "center", gap: 12 }}>

                        {/* Role Badge */}
                        <div style={{
                            background: "#a855f722",
                            color: "#a855f7",
                            padding: "4px 12px",
                            borderRadius: 20,
                            fontSize: 12,
                            fontWeight: 700,
                            display: "flex",
                            alignItems: "center",
                            gap: 6
                        }}>
                            👤 {role.charAt(0).toUpperCase() + role.slice(1)}
                        </div>

                        {/* Logout */}
                        <button
                            onClick={handleLogout}
                            style={{
                                background: "transparent",
                                border: `1px solid ${C.border}`,
                                color: C.text,
                                padding: "4px 12px",
                                borderRadius: 4,
                                cursor: "pointer",
                                fontSize: 12
                            }}
                        >
                            Logout
                        </button>

                    </div>
                ) : (
                    <div style={{ display: "flex", gap: 20 }}>

                        <button
                            onClick={() => navigate("/role-select")}
                            style={{
                                background: "transparent",
                                color: C.text,
                                border: "none",
                                fontSize: 16,
                                fontWeight: 600,
                                cursor: "pointer"
                            }}
                        >
                            Login
                        </button>

                        <button
                            onClick={() => navigate("/role-select")}
                            style={{
                                background: C.accent,
                                color: "#000",
                                border: "none",
                                padding: "8px 16px",
                                borderRadius: 6,
                                fontSize: 16,
                                fontWeight: 800,
                                cursor: "pointer",
                                boxShadow: `0 4px 12px ${C.accent}44`
                            }}
                        >
                            Get Started
                        </button>

                    </div>
                )}
            </div>
        </nav>
    );
}
