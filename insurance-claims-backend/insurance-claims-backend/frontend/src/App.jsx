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
          <Route path="/login/:role" element={<Login />} />
          <Route path="/portal/claimer" element={<ClaimerPortal />} />
          <Route path="/portal/reviewer" element={<ReviewerPortal />} />
          <Route path="/portal/admin" element={<AdminPortal />} />
          <Route path="/review-queue" element={<ReviewQueue />} />
          <Route path="/claim-details/:id" element={<ClaimDetailsPage />} />
          <Route path="/login/:role" element={<Login />} />
        </Routes>
      </main>
    </div>
  );
}