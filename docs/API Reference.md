# API Reference

## Overview

This document provides a comprehensive reference for the SLID platform's API endpoints, request/response formats, and error codes. The API is organized by functional areas including authentication, profile management, content management, and social media integration.

## Authentication Endpoints

### POST /sign-in/

Authenticates a user and creates a session.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "redirect": "string" // URL to redirect to
}
```

**Error Codes:**
- 400: Invalid credentials
- 404: User not found

### POST /sign-up/

Creates a new user account.

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "password_confirmation": "string"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "redirect": "/terms-and-conditions/"
}
```

**Error Codes:**
- 400: Validation error (username taken, invalid email format, etc.)

### POST /logout/

Terminates the current user session.

**Response (200 OK):**
```json
{
  "success": true,
  "redirect": "/"
}
```

## Profile Management Endpoints

### GET /profile/{username}/

Retrieves a user profile.

**Path Parameters:**
- username: The username of the profile to retrieve

**Response (200 OK):**
```json
{
  "user_profile": {
    "username": "string",
    "fullName": "string",
    "bio": "string",
    "profilePicture": "url",
    "qr_code": "url",
    "verified": boolean,
    "created_at": "datetime"
  },
  "social_accounts": [
    {
      "platform": "string",
      "is_linked": boolean,
      "last_sync": "datetime"
    }
  ],
  "posts": [
    {
      "id": "integer",
      "content_type": "string",
      "content": "string",
      "media_file": "url",
      "created_at": "datetime"
    }
  ],
  "is_own_profile": boolean,
  "is_connected": boolean
}
```

**Error Codes:**
- 404: Profile not found

### PUT /profile/update/

Updates the current user's profile.

**Request Body:**
```json
{
  "fullName": "string",
  "bio": "string",
  "profilePicture": "file"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "profile": {
    "fullName": "string",
    "bio": "string",
    "profilePicture": "url"
  }
}
```

**Error Codes:**
- 400: Invalid form data
- 401: Unauthorized (not logged in)

### POST /profile/connect/{username}/

Create a connection with another user.

**Path Parameters:**
- username: The username to connect with

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Connection created successfully"
}
```

**Error Codes:**
- 400: Already connected
- 404: User not found

### POST /profile/disconnect/{username}/

Remove a connection with another user.

**Path Parameters:**
- username: The username to disconnect from

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Connection removed successfully"
}
```

**Error Codes:**
- 404: Connection not found

## Content Management Endpoints

### POST /content/create/

Creates a new post.

**Request Body:**
```json
{
  "content_type": "string", // "text", "image", or "video"
  "content": "string",
  "media_file": "file" // Optional, for image/video content
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "post": {
    "id": "integer",
    "content_type": "string",
    "content": "string",
    "media_file": "url",
    "created_at": "datetime"
  }
}
```

**Error Codes:**
- 400: Invalid form data
- 401: Unauthorized (not logged in)

### DELETE /content/delete/{post_id}/

Deletes a post.

**Path Parameters:**
- post_id: The ID of the post to delete

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Post deleted successfully"
}
```

**Error Codes:**
- 403: Forbidden (not post owner)
- 404: Post not found

## Social Media OAuth Endpoints

### GET /oauth/instagram/authorize/

Initiates the Instagram OAuth flow.

**Response:**
Redirects to Instagram for authorization.

### GET /oauth/instagram/callback/

Handles the Instagram OAuth callback.

**Query Parameters:**
- code: Authorization code from Instagram
- state: CSRF protection token

**Response:**
Redirects to the user's profile page after successful connection.

**Error Codes:**
- 400: Invalid authorization request

### GET /oauth/facebook/authorize/

Initiates the Facebook OAuth flow.

**Response:**
Redirects to Facebook for authorization.

### GET /oauth/facebook/callback/

Handles the Facebook OAuth callback.

**Query Parameters:**
- code: Authorization code from Facebook
- state: CSRF protection token

**Response:**
Redirects to the user's profile page after successful connection.

**Error Codes:**
- 400: Invalid authorization request

### POST /oauth/{platform}/disconnect/

Disconnects a social media platform.

**Path Parameters:**
- platform: The platform to disconnect (e.g., "instagram", "facebook")

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Platform disconnected successfully"
}
```

**Error Codes:**
- 404: Platform connection not found

## AI Integration Endpoints

### POST /profile/ai/

Processes a natural language query using the AI assistant.

**Request Body:**
```json
{
  "data": "string" // The natural language query
}
```

**Response (200 OK):**
```json
{
  "message": "string" // AI response
}
```

**Error Codes:**
- 400: No query provided
- 404: User profile not found
- 500: AI processing error

## Common Error Response Format

All error responses follow this standard format:

```json
{
  "error": "string", // Error message
  "code": "integer", // HTTP status code
  "details": {} // Optional additional error details
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse. Clients are limited to:
- 100 requests per minute for authenticated users
- 20 requests per minute for unauthenticated users

Rate limit headers are included in responses:
- X-RateLimit-Limit: Maximum requests per minute
- X-RateLimit-Remaining: Remaining requests in current window
- X-RateLimit-Reset: Time (in seconds) until the rate limit resets 