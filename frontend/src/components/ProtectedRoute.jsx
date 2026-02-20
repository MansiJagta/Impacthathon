import { Navigate } from "react-router-dom";
import { getAuthToken, getUserInfo } from "../services/api";

/**
 * ProtectedRoute - Ensures only authenticated users can access certain routes
 */
export default function ProtectedRoute({ component: Component, requiredRole = null }) {
  const token = getAuthToken();
  const userInfo = getUserInfo();

  if (!token) {
    // User not authenticated, redirect to role selection
    return <Navigate to="/role-select" replace />;
  }

  if (requiredRole && userInfo.role !== requiredRole) {
    // User authenticated but doesn't have required role
    return (
      <div style={{ padding: 40, textAlign: "center", marginTop: 100 }}>
        <h2 style={{ color: "#fff" }}>Access Denied</h2>
        <p style={{ color: "#888" }}>
          You don't have permission to access this page.
        </p>
        <p style={{ color: "#888", fontSize: 12 }}>
          Your role: <strong>{userInfo.role}</strong> | Required: <strong>{requiredRole}</strong>
        </p>
        <button
          onClick={() => (window.location.href = "/role-select")}
          style={{
            marginTop: 20,
            padding: "10px 20px",
            background: "#fbbf24",
            border: "none",
            borderRadius: 8,
            cursor: "pointer",
            fontWeight: "bold"
          }}
        >
          Go Back
        </button>
      </div>
    );
  }

  return <Component />;
}
