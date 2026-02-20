# Frontend-Backend Integration Summary

## Overview
Frontend and Backend are now fully integrated with consistent request/response formats, proper authentication flow, and role-based access control.

---

## Base URL Configuration

**API Endpoint:** `http://127.0.0.1:8000`

Frontend configured in: [frontend/src/services/api.js](frontend/src/services/api.js#L5)

---

## Authentication Flow

### 1. User Registration (Signup)

**Endpoint:** `POST /signup`

**Frontend Call:**
```javascript
authAPI.register(name, email, password, role)
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "role": "claimer"  // Optional: default is "user"
}
```

**Success Response (200):**
```json
{
  "message": "User created successfully"
}
```

**Error Response (400):**
```json
{
  "detail": "Email already registered"
}
```

**Implementation:** [Register.jsx](frontend/src/pages/Register.jsx)

---

### 2. User Login

**Endpoint:** `POST /login`

**Frontend Call:**
```javascript
await authAPI.login(email, password)
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Success Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Token Storage:**
- Stored in `localStorage` as `authToken`
- Used in all subsequent API calls

**Implementation:** [Login.jsx](frontend/src/pages/Login.jsx)

---

### 3. Get Current User Info

**Endpoint:** `GET /me`

**Frontend Call:**
```javascript
authAPI.getCurrentUser()
```

**Headers Required:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Success Response (200):**
```json
{
  "user_id": "65df9c1a2b3c4d5e6f7g8h9i",
  "email": "john@example.com",
  "role": "claimer"
}
```

**Stored in localStorage:**
- `userEmail` → user's email
- `userRole` → user's role
- `userId` → MongoDB ObjectId
- `authToken` → JWT token

**Error Responses:**

Token Missing (401):
```json
{
  "detail": "Not authenticated"
}
```

Invalid Token (401):
```json
{
  "detail": "Invalid token"
}
```

**Implementation:** [api.js](frontend/src/services/api.js#L60-L80)

---

### 4. Logout

**Frontend Call:**
```javascript
authAPI.logout()
```

**Effect:**
- Clears `authToken`, `userEmail`, `userRole`, `userId` from localStorage
- User must re-login to access protected routes

**Implementation:** [api.js](frontend/src/services/api.js#L82-L89)

---

## Role-Based Authentication

### Supported Roles
1. **claimer** - Insurance claimants who can submit and track claims
2. **reviewer** - Internal staff who reviews and processes claims
3. **admin** - System administrators with full access

### Protected Routes

All portal routes are protected by `ProtectedRoute` component:

| Route | Required Role | Component |
|-------|--------------|-----------|
| `/portal/claimer` | `claimer` | ClaimerPortal |
| `/portal/reviewer` | `reviewer` | ReviewerPortal |
| `/portal/admin` | `admin` | AdminPortal |
| `/review-queue` | `reviewer` | ReviewQueue |
| `/claim-details/:id` | `claimer` | ClaimDetailsPage |

**Implementation:** [ProtectedRoute.jsx](frontend/src/components/ProtectedRoute.jsx)

---

## HTTP Headers

### For All Requests
```
Content-Type: application/json
```

### For Protected Requests
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Set by:** `getAuthHeaders()` function in [api.js](frontend/src/services/api.js#L19-26)

---

## Claims API

### Submit Claim (Authenticated)

**Endpoint:** `POST /claims`

**Frontend Call:**
```javascript
claimsAPI.submitClaim(title, description, amount, policyNumber)
```

**Request:**
```json
{
  "title": "Car Insurance Claim",
  "description": "Damage from accident",
  "amount": 5000,
  "policy_number": "POL-123456"
}
```

### Get All Claims (Authenticated)

**Endpoint:** `GET /claims`

**Frontend Call:**
```javascript
claimsAPI.getClaims()
```

Response format depends on user role (backend logic).

### Get Claim by ID

**Endpoint:** `GET /claims/{claimId}`

**Frontend Call:**
```javascript
claimsAPI.getClaimById(claimId)
```

### Update Claim (Reviewer/Admin only)

**Endpoint:** `PATCH /claims/{claimId}`

**Frontend Call:**
```javascript
claimsAPI.updateClaim(claimId, status, remarks)
```

**Request:**
```json
{
  "status": "approved",
  "remarks": "Claim approved after review"
}
```

### Delete Claim (Admin only)

**Endpoint:** `DELETE /claims/{claimId}`

---

## Users API (Admin Only)

### Get All Users

**Endpoint:** `GET /users`

**Frontend Call:**
```javascript
usersAPI.getAllUsers()
```

### Get User by Email

**Endpoint:** `GET /users/{email}`

**Frontend Call:**
```javascript
usersAPI.getUserByEmail(email)
```

### Update User Role

**Endpoint:** `PUT /users/{email}`

**Frontend Call:**
```javascript
usersAPI.updateUserRole(email, newRole)
```

**Request:**
```json
{
  "new_role": "reviewer"
}
```

### Delete User

**Endpoint:** `DELETE /users/{email}`

---

## Error Handling

### Standard Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Error Status Codes

| Code | Meaning | Frontend Action |
|------|---------|-----------------|
| 200 | Success | Proceed |
| 201 | Created | Proceed |
| 400 | Bad Request | Show validation error |
| 401 | Unauthorized | Redirect to login |
| 403 | Forbidden | Show "Access Denied" |
| 422 | Validation Error | Show form errors |
| 500 | Server Error | Show error message |

**Implementation:** Error handling in all API calls via `.catch()` blocks

---

## Complete Authentication Flow

### 1. Registration Flow

```
User fills Register form
↓
POST /signup (name, email, password, role)
↓
POST /login (email, password)
↓
Response: {access_token, token_type}
↓
Store: authToken in localStorage
↓
GET /me
↓
Response: {user_id, email, role}
↓
Store: userEmail, userRole, userId in localStorage
↓
Redirect to /portal/{role}
```

### 2. Login Flow

```
User fills Login form
↓
POST /login (email, password)
↓
Response: {access_token, token_type}
↓
Store: authToken in localStorage
↓
GET /me
↓
Response: {user_id, email, role}
↓
Verify role matches selected role
↓
Store: userEmail, userRole, userId in localStorage
↓
Redirect to /portal/{role}
```

### 3. Protected Route Access

```
User navigates to /portal/{role}
↓
ProtectedRoute checks:
  ├─ Is token present in localStorage?
  │  ├─ No → Redirect to /role-select
  │  └─ Yes → Continue
  └─ Does user role match required role?
     ├─ No → Show "Access Denied"
     └─ Yes → Render component
```

### 4. API Call Flow

```
Frontend calls API endpoint
↓
getAuthHeaders() retrieves token
↓
Request includes: Authorization: Bearer <token>
↓
Backend validates token via get_current_user()
↓
Token valid → Process request
Token invalid → Return 401
↓
Response sent to frontend
```

---

## Files Modified

### Frontend

1. **[api.js](frontend/src/services/api.js)**
   - Changed base URL from `localhost:8000` to `127.0.0.1:8000`
   - Updated `/auth/register` → `/signup`
   - Updated `/auth/login` → `/login`
   - Updated `/auth/me` → `/me`
   - Added `name` parameter to register function
   - Added `getCurrentUser()` call after login
   - Exported `getAuthToken()` for use in ProtectedRoute
   - Updated `getUserInfo()` to include `userId`

2. **[Register.jsx](frontend/src/pages/Register.jsx)**
   - Added `name` state variable
   - Added name input field with validation
   - Updated form validation to check name
   - Updated `handleRegister()` to:
     - Pass name to `authAPI.register()`
     - Call `authAPI.getCurrentUser()` after login
     - Verify role from `/me` response

3. **[Login.jsx](frontend/src/pages/Login.jsx)**
   - Updated `handleLogin()` to:
     - Call `authAPI.login()`
     - Call `authAPI.getCurrentUser()` to get user info
     - Verify role from `/me` response instead of login response

4. **[App.jsx](frontend/src/App.jsx)**
   - Imported `ProtectedRoute` component
   - Wrapped portal routes with `ProtectedRoute`:
     - `/portal/claimer` requires `claimer` role
     - `/portal/reviewer` requires `reviewer` role
     - `/portal/admin` requires `admin` role
     - `/review-queue` requires `reviewer` role
     - `/claim-details/:id` requires `claimer` role

### Backend

1. **[auth_routes.py](backend/app/routes/auth_routes.py)**
   - Added `GET /me` endpoint
   - Returns `{user_id, email, role}` from JWT payload
   - Properly validates token using `get_current_user()` dependency

---

## Token Expiry & Refresh

**Current Behavior:**
- Token expires based on `ACCESS_TOKEN_EXPIRE_MINUTES` (default: 60 minutes)
- When expired, subsequent API calls return `401 Unauthorized`
- Frontend should redirect to login page

**Implementation:**
- All API calls check response status
- If `401` received, catch block shows error
- User can manually navigate to `/role-select` or login page

**Future Enhancement:**
- Implement refresh token mechanism
- Auto-redirect on 401 with token refresh attempt

---

## Testing Checklist

### Authentication
- [ ] User can register with valid credentials
- [ ] Duplicate email registration shows error (400)
- [ ] User can login with valid credentials
- [ ] Invalid credentials show error (401)
- [ ] JWT token stored correctly in localStorage
- [ ] GET /me returns correct user info
- [ ] User can logout (clears all localStorage)

### Authorization
- [ ] Unauthenticated users cannot access /portal/* routes
- [ ] User with wrong role cannot access mismatched portal
- [ ] Admin can access /portal/admin
- [ ] Claimer can access /portal/claimer
- [ ] Reviewer can access /portal/reviewer

### API Integration
- [ ] All API calls include Authorization header
- [ ] Claims API endpoints work with authenticated user
- [ ] Admin can manage users (Users API)
- [ ] 401 responses properly handle token issues
- [ ] 403 responses show access denied message

---

## Environment Variables

### Backend (.env)
```
MONGODB_URI=mongodb://localhost:27017
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Frontend
Base URL hardcoded: `http://127.0.0.1:8000`

*Future: Consider moving to .env via Vite*

---

## Deployment Notes

1. Update `API_BASE_URL` in [api.js](frontend/src/services/api.js) to production URL
2. Ensure CORS is properly configured in backend for frontend domain
3. Change `CORS allow_origins` from `["*"]` to specific domain
4. Use HTTPS for production
5. Store JWT secret key securely (use environment variables)
6. Implement token refresh mechanism for better UX

---

## Version Info

- **Frontend Framework:** React 18 + Vite
- **Backend Framework:** FastAPI
- **Database:** MongoDB
- **Authentication:** JWT (HS256)
- **Integration Date:** 2026-02-20

---

## Support & Troubleshooting

### Common Issues

**1. CORS Error**
- Backend CORS middleware might not be allowing frontend domain
- Check `allow_origins` in [main.py](backend/app/main.py)

**2. 401 Unauthorized**
- Token might be expired
- Check localStorage for `authToken`
- Try logging in again

**3. Token Not Stored**
- Check if localStorage is enabled in browser
- Verify `setAuthToken()` is called after login

**4. Role Mismatch**
- Ensure user's role in database matches selected role
- Check `/me` endpoint response

---

## Related Documentation

- [Authentication Specification](./BACKEND_API_SPEC.md)
- [Database Schema](./DATABASE_SCHEMA.md)
- [Frontend Routes](./FRONTEND_ROUTES.md)

