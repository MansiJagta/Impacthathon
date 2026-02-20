import { useState } from "react";
import { C } from "../constants/theme";
import { useParams, useNavigate } from "react-router-dom";
import { authAPI } from "../services/api";

export default function Register() {
  const { role } = useParams();
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [pass, setPass] = useState("");
  const [confirmPass, setConfirmPass] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [validationErrors, setValidationErrors] = useState({});

  const roleMap = {
    claimer: {
      title: "Create Claimer Account",
      desc: "Join IntelliClaim to manage your insurance claims",
      icon: "🛡️",
      primaryBtn: "Create Account",
      portalPath: "/portal/claimer",
      altText: "Already have an account?",
      altLink: "Sign in instead",
    },
    reviewer: {
      title: "Create Reviewer Account",
      desc: "Join the claims review team",
      icon: "🔍",
      primaryBtn: "Create Account",
      portalPath: "/portal/reviewer",
      altText: "Already have an account?",
      altLink: "Sign in instead",
    },
    admin: {
      title: "Create Admin Account",
      desc: "Set up your administrator account",
      icon: "⚙️",
      primaryBtn: "Create Account",
      portalPath: "/portal/admin",
      altText: "Already have an account?",
      altLink: "Sign in instead",
    },
  };

  const config = roleMap[role];

  if (!config) {
    return <div style={{ padding: 40 }}>Invalid role.</div>;
  }

  const validateForm = () => {
    const errors = {};

    if (!name.trim()) {
      errors.name = "Full name is required";
    }

    if (!email.trim()) {
      errors.email = "Email is required";
    } else if (!email.includes("@")) {
      errors.email = "Please enter a valid email address";
    }

    if (!pass) {
      errors.password = "Password is required";
    } else if (pass.length < 8) {
      errors.password = "Password must be at least 8 characters";
    }

    if (!confirmPass) {
      errors.confirmPass = "Please confirm your password";
    } else if (pass !== confirmPass) {
      errors.confirmPass = "Passwords do not match";
    }

    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleRegister = async () => {
    setError("");

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      // Register user
      await authAPI.register(name, email, pass, role);

      // Auto-login after successful registration
      await authAPI.login(email, pass);

      // Get current user info from /me endpoint
      const userInfo = await authAPI.getCurrentUser();

      if (userInfo.role !== role) {
        setError(
          `User role (${userInfo.role}) does not match selected role (${role})`
        );
        return;
      }

      // Navigate to portal
      navigate(config.portalPath);
    } catch (err) {
      setError(err.message || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field) => {
    if (validationErrors[field]) {
      setValidationErrors({
        ...validationErrors,
        [field]: "",
      });
    }
  };

  return (
    <div
      style={{
        maxWidth: 420,
        margin: "80px auto",
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

      {/* Registration Form */}
      <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
        {/* Name Field */}
        <div style={{ textAlign: "left" }}>
          <input
            type="text"
            placeholder="Full Name"
            value={name}
            onChange={(e) => {
              setName(e.target.value);
              handleInputChange("name");
            }}
            disabled={loading}
            style={{
              ...inputStyle,
              borderColor: validationErrors.name ? "#ef4444" : "#333",
            }}
          />
          {validationErrors.name && (
            <p style={{ color: "#fca5a5", fontSize: 12, marginTop: 4 }}>
              {validationErrors.name}
            </p>
          )}
        </div>

        {/* Email Field */}
        <div style={{ textAlign: "left" }}>
          <input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              handleInputChange("email");
            }}
            disabled={loading}
            style={{
              ...inputStyle,
              borderColor: validationErrors.email ? "#ef4444" : "#333",
            }}
          />
          {validationErrors.email && (
            <p style={{ color: "#fca5a5", fontSize: 12, marginTop: 4 }}>
              {validationErrors.email}
            </p>
          )}
        </div>

        {/* Password Field */}
        <div style={{ textAlign: "left" }}>
          <input
            type="password"
            placeholder="Password (min 8 characters)"
            value={pass}
            onChange={(e) => {
              setPass(e.target.value);
              handleInputChange("password");
            }}
            disabled={loading}
            style={{
              ...inputStyle,
              borderColor: validationErrors.password
                ? "#ef4444"
                : "#333",
            }}
          />
          {validationErrors.password && (
            <p style={{ color: "#fca5a5", fontSize: 12, marginTop: 4 }}>
              {validationErrors.password}
            </p>
          )}
        </div>

        {/* Confirm Password Field */}
        <div style={{ textAlign: "left" }}>
          <input
            type="password"
            placeholder="Confirm Password"
            value={confirmPass}
            onChange={(e) => {
              setConfirmPass(e.target.value);
              handleInputChange("confirmPass");
            }}
            disabled={loading}
            style={{
              ...inputStyle,
              borderColor: validationErrors.confirmPass
                ? "#ef4444"
                : "#333",
            }}
          />
          {validationErrors.confirmPass && (
            <p style={{ color: "#fca5a5", fontSize: 12, marginTop: 4 }}>
              {validationErrors.confirmPass}
            </p>
          )}
        </div>

        {/* Submit Button */}
        <button
          onClick={handleRegister}
          disabled={loading}
          style={{
            ...primaryBtnStyle,
            background: C.accent,
            opacity: loading ? 0.7 : 1,
            marginTop: 8,
          }}
        >
          {loading ? "Creating account..." : config.primaryBtn}
        </button>
      </div>

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
          onClick={() => navigate(`/login/${role}`)}
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
  width: "100%",
  background: "rgba(255,255,255,0.05)",
  border: "1px solid #333",
  padding: "16px",
  borderRadius: 12,
  color: "#fff",
  fontSize: 14,
  outline: "none",
  transition: "border-color 0.2s ease",
};

const primaryBtnStyle = {
  border: "none",
  padding: "18px",
  borderRadius: 12,
  fontWeight: 900,
  fontSize: 16,
  cursor: "pointer",
  boxShadow: "0 10px 20px rgba(0,0,0,0.3)",
  width: "100%",
};
