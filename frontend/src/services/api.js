/**
 * API Service - Handles all backend API calls
 */

const API_BASE_URL = "http://127.0.0.1:8000";

// Store token in localStorage
const setAuthToken = (token) => {
  localStorage.setItem("authToken", token);
};

export const getAuthToken = () => {
  return localStorage.getItem("authToken");
};

const clearAuthToken = () => {
  localStorage.removeItem("authToken");
};

const getAuthHeaders = () => {
  const token = getAuthToken();
  return {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
  };
};

// Auth API calls
export const authAPI = {
  // Register user
  register: async (name, email, password, role = "claimer") => {
    const response = await fetch(`${API_BASE_URL}/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password, role }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Registration failed");
    }
    return data;
  },

  // Login user
  login: async (email, password) => {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Login failed");
    }

    // Store token
    setAuthToken(data.access_token);

    return data;
  },

  // Get current user
  getCurrentUser: async () => {
    const response = await fetch(`${API_BASE_URL}/me`, {
      method: "GET",
      headers: getAuthHeaders(),
    });

    const data = await response.json();
    if (!response.ok) {
      clearAuthToken();
      throw new Error(data.detail || "Failed to fetch user");
    }

    // Store user info from /me response
    localStorage.setItem("userEmail", data.email);
    localStorage.setItem("userRole", data.role);
    localStorage.setItem("userId", data.user_id);

    return data;
  },

  // Logout
  logout: () => {
    clearAuthToken();
    localStorage.removeItem("userEmail");
    localStorage.removeItem("userRole");
    localStorage.removeItem("userId");
  },
};

// Claims API calls
export const claimsAPI = {
  // Submit a new claim
  submitClaim: async (title, description, amount, policyNumber = null) => {
    const response = await fetch(`${API_BASE_URL}/claims`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        title,
        description,
        amount,
        policy_number: policyNumber,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Failed to submit claim");
    }
    return data;
  },

  // Get all claims (based on role)
  getClaims: async () => {
    const response = await fetch(`${API_BASE_URL}/claims`, {
      method: "GET",
      headers: getAuthHeaders(),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Failed to fetch claims");
    }
    return data;
  },

  // Get specific claim
  getClaimById: async (claimId) => {
    const response = await fetch(`${API_BASE_URL}/claims/${claimId}`, {
      method: "GET",
      headers: getAuthHeaders(),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Failed to fetch claim");
    }
    return data;
  },

  // Update claim status (reviewer/admin only)
  updateClaim: async (claimId, status, remarks = null) => {
    const response = await fetch(`${API_BASE_URL}/claims/${claimId}`, {
      method: "PATCH",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        status,
        remarks,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Failed to update claim");
    }
    return data;
  },

  // Delete claim (admin only)
  deleteClaim: async (claimId) => {
    const response = await fetch(`${API_BASE_URL}/claims/${claimId}`, {
      method: "DELETE",
      headers: getAuthHeaders(),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Failed to delete claim");
    }
    return data;
  },
};

// Users API calls (admin only)
export const usersAPI = {
  // Get all users
  getAllUsers: async () => {
    const response = await fetch(`${API_BASE_URL}/users`, {
      method: "GET",
      headers: getAuthHeaders(),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Failed to fetch users");
    }
    return data;
  },

  // Get user by email
  getUserByEmail: async (email) => {
    const response = await fetch(`${API_BASE_URL}/users/${email}`, {
      method: "GET",
      headers: getAuthHeaders(),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Failed to fetch user");
    }
    return data;
  },

  // Update user role
  updateUserRole: async (email, newRole) => {
    const response = await fetch(`${API_BASE_URL}/users/${email}`, {
      method: "PUT",
      headers: getAuthHeaders(),
      body: JSON.stringify({ new_role: newRole }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Failed to update user");
    }
    return data;
  },

  // Delete user
  deleteUser: async (email) => {
    const response = await fetch(`${API_BASE_URL}/users/${email}`, {
      method: "DELETE",
      headers: getAuthHeaders(),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Failed to delete user");
    }
    return data;
  },
};

// Utility function to check if user is authenticated
export const isAuthenticated = () => {
  return !!getAuthToken();
};

// Utility function to get user info from localStorage
export const getUserInfo = () => {
  return {
    email: localStorage.getItem("userEmail"),
    role: localStorage.getItem("userRole"),
    userId: localStorage.getItem("userId"),
    token: getAuthToken(),
  };
};
