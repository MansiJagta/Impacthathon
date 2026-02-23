import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { C } from "../constants/theme";

export default function Signup() {
    const { role } = useParams();
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [pass, setPass] = useState("");
    const [loading, setLoading] = useState(false);
    const [name, setName] = useState("");
    const handleSignup = async () => {
        if (!name || !email || !pass) {
            alert("Please fill all fields");
            return;
        }

        setLoading(true);

        try {
            const res = await fetch("http://localhost:8000/auth/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name,
                    email,
                    password: pass,
                    role
                }),
            });

            const data = await res.json();

            if (!res.ok) {
                alert(data.detail);
                setLoading(false);
                return;
            }

            alert("Signup successful! Please login.");
            navigate(`/login/${role}`);

        } catch (err) {
            console.error(err);
            alert("Signup failed");
        }

        setLoading(false);
    };

    return (
        <div style={{
            maxWidth: 420,
            margin: "120px auto",
            padding: "40px",
            background: C.panel,
            border: `1px solid ${C.border}`,
            borderRadius: 24,
            textAlign: "center"
        }}>
            <h2 style={{ color: "#fff", fontSize: 28, fontWeight: 900 }}>
                Create {role} Account
            </h2>

            <div style={{ display: "flex", flexDirection: "column", gap: 16, marginTop: 30 }}>
                <input
                    type="text"
                    placeholder="Full Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    style={inputStyle}
                />

                <input
                    type="email"
                    placeholder="Email Address"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    style={inputStyle}
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={pass}
                    onChange={(e) => setPass(e.target.value)}
                    style={inputStyle}
                />

                <button
                    onClick={handleSignup}
                    disabled={loading}
                    style={btnStyle}
                >
                    {loading ? "Creating..." : "Sign Up"}
                </button>
            </div>

            {/* Login Redirect */}
            <div style={{
                marginTop: 30,
                paddingTop: 20,
                borderTop: `1px solid ${C.border}`,
                fontSize: 14,
                color: C.muted
            }}>
                Already have an account?{" "}
                <span
                    onClick={() => navigate(`/login/${role}`)}
                    style={{
                        color: C.accent,
                        fontWeight: 700,
                        cursor: "pointer"
                    }}
                >
                    Login
                </span>
            </div>
        </div>
    );
}

const inputStyle = {
    background: "rgba(255,255,255,0.05)",
    border: "1px solid #333",
    padding: "16px",
    borderRadius: 12,
    color: "#fff",
    fontSize: 14,
    outline: "none"
};

const btnStyle = {
    background: "#22c55e",
    color: "#000",
    border: "none",
    padding: "18px",
    borderRadius: 12,
    fontWeight: 900,
    fontSize: 16,
    cursor: "pointer"
};