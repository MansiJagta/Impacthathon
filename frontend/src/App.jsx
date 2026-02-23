import { useState } from "react";
import { C } from "./constants/theme";
import Nav from "./components/Nav";
import Home from "./pages/Home";
import RoleSelect from "./pages/RoleSelect";
import Login from "./pages/Login";
import ClaimerPortal from "./pages/claimer/ClaimerPortal";
import ReviewerPortal from "./pages/reviewer/ReviewerPortal";
import AdminPortal from "./pages/admin/AdminPortal"
import ReviewQueue from "./pages/reviewer/ReviewQueue";
import ClaimDetailsPage from "./pages/claimer/ClaimDetailsPage";
import { Routes, Route } from "react-router-dom";
import Signup from "./pages/Signup";
import ProtectedRoute from "./components/ProtectedRoute";



export default function App() {
  const [screen, setScreen] = useState("landing"); // landing | roleSelect | login | portal
  const [role, setRole] = useState(null);

  const handleLogout = () => {
    setRole(null);
    setScreen("landing");
  };

  return (
    <div style={{
      fontFamily: "'DM Sans', sans-serif",
      background: C.bg,
      minHeight: "100vh",
      color: C.text
    }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700;900&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        ::-webkit-scrollbar { width: 6px; } 
        ::-webkit-scrollbar-thumb { background: ${C.border}; border-radius: 3px; }
        body { margin: 0; }
      `}</style>

      <Nav />

      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/role-select" element={<RoleSelect />} />
          <Route path="/signup/:role" element={<Signup />} />
          <Route path="/login/:role" element={<Login />} />

          {/* 🔐 Protected Portals */}

          <Route
            path="/portal/claimer"
            element={
              <ProtectedRoute requiredRole="claimer">
                <ClaimerPortal />
              </ProtectedRoute>
            }
          />

          <Route
            path="/portal/reviewer"
            element={
              <ProtectedRoute requiredRole="reviewer">
                <ReviewerPortal />
              </ProtectedRoute>
            }
          />

          <Route
            path="/portal/admin"
            element={
              <ProtectedRoute requiredRole="admin">
                <AdminPortal />
              </ProtectedRoute>
            }
          />

          {/* 🔐 Also protect reviewer-only pages */}
          <Route
            path="/review-queue"
            element={
              <ProtectedRoute requiredRole="reviewer">
                <ReviewQueue />
              </ProtectedRoute>
            }
          />

          {/* 🔐 Claimer-specific page */}
          <Route
            path="/claim-details/:id"
            element={
              <ProtectedRoute requiredRole="claimer">
                <ClaimDetailsPage />
              </ProtectedRoute>
            }
          />
        </Routes>
      </main>
    </div>
  );
}