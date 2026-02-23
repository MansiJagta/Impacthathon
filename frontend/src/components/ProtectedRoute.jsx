import { Navigate, useParams } from "react-router-dom";

export default function ProtectedRoute({ children, requiredRole }) {

    const token = localStorage.getItem("token");

    if (!token) {
        return <Navigate to="/role-select" />;
    }

    try {
        const payload = JSON.parse(
            atob(token.split(".")[1])
        );

        if (requiredRole && payload.role !== requiredRole) {
            return <Navigate to="/role-select" />;
        }

        return children;

    } catch (err) {
        return <Navigate to="/role-select" />;
    }
}