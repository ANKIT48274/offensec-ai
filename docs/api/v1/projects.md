# Projects API

Base URL: `/api/v1/projects`

## POST /projects

Create a new project.

**Request Body:**
```json
{
  "name": "Internal Network Pentest",
  "description": "Annual internal network assessment"
}
```

**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "p1",
    "name": "Internal Network Pentest",
    "description": "Annual internal network assessment",
    "owner_id": "u1",
    "is_archived": false,
    "created_at": "2026-07-29T00:00:00Z"
  }
}
```

## GET /projects

List all projects for the current user.

**Query Parameters:**
- page (int, default: 1)
- page_size (int, default: 50, max: 100)

## GET /projects/{id}

Get project by ID.

## PATCH /projects/{id}

Update project details.

## DELETE /projects/{id}

Delete a project and all associated assessments.
