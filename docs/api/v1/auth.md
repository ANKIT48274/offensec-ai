# Authentication API

Base URL: `/api/v1/auth`

## POST /register

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "offensec_user",
  "password": "securePassword123"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "abc123",
    "email": "user@example.com",
    "username": "offensec_user",
    "is_active": true,
    "created_at": "2026-07-29T00:00:00Z"
  }
}
```

## POST /login

Authenticate and receive JWT tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer",
    "expires_in": 3600
  }
}
```

## GET /me

Get current authenticated user information.

**Headers:**
- Authorization: Bearer <access_token>

**Response (200):**
```json
{
  "success": true,
  "data": {
    "id": "abc123",
    "email": "user@example.com",
    "username": "offensec_user"
  }
}
```
