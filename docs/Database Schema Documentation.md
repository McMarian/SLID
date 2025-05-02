# Database Schema Documentation

## Overview

The SLID platform uses a relational database model with PostgreSQL to store user data, social media connections, and content. This document provides a comprehensive overview of all database models, their fields, relationships, and usage within the application.

## Core Models

### User

Django's built-in User model serves as the foundation for authentication and authorization.

**Fields:**
- `id` (Primary Key): Unique identifier
- `username`: Unique username for login (stored in lowercase)
- `email`: User's email address
- `password`: Securely hashed password (using BCryptSHA256PasswordHasher)
- `date_joined`: Timestamp when the user account was created
- `last_login`: Timestamp of the user's last login

**Relationships:**
- One-to-One with UserProfile
- One-to-Many with SocialMediaAccount
- One-to-Many with Post
- Many-to-Many with itself through Connection

**Usage:**
- Authentication and login
- User identification across the platform
- Base for user-related relationships

### UserProfile

Extends the base User model with additional profile information and settings.

**Fields:**
- `id` (Primary Key): Unique identifier
- `user` (Foreign Key → User): One-to-one relationship with User
- `fullName`: User's full name (optional)
- `bio`: User profile description (optional)
- `profilePicture`: User's profile picture (ImageField, defaults to "default_pp.png")
- `qr_code`: QR code image for sharing profile (ImageField, defaults to "qr_code.png")
- `user_code`: Unique alphanumeric code for identification (unique=True)
- `verified`: Boolean indicating whether the profile is verified
- `created_at`: Timestamp when the profile was created
- `profile_score`: Integer score based on profile completeness (0-100)
- `is_deleted`: Soft deletion flag

**Indexes:**
- `user`: For fast profile lookup
- `profile_score`: For engagement and sorting queries

**Methods:**
- `update_profile_score()`: Calculates and updates the profile completion score
- `__str__()`: Returns the username

**Usage:**
- Storing extended user information
- Profile visibility and sharing
- Computing profile completeness metrics

### SocialMediaAccount

Unifies the representation of various social media platform connections.

**Fields:**
- `id` (Primary Key): Unique identifier
- `user` (Foreign Key → User): User who owns this account connection
- `platform`: Platform type (choices: facebook, instagram, youtube, linkedin, google, x, tiktok)
- `token`: OAuth access token for authentication
- `token_type`: Type of token (usually "bearer")
- `expires`: Token expiration timestamp
- `data`: JSONField storing platform-specific data
- `last_sync`: Timestamp of the last data synchronization
- `is_linked`: Boolean flag indicating if the account is currently connected

**Indexes:**
- `(user, platform)`: Combined index for user-platform lookups
- `platform`: For platform-specific queries

**Meta:**
- `unique_together`: (user, platform) to ensure only one connection per platform per user

**Usage:**
- OAuth integration with social platforms
- Storing platform-specific data
- Managing user's cross-platform presence

### Connection

Represents relationships between users on the platform.

**Fields:**
- `id` (Primary Key): Unique identifier
- `user` (Foreign Key → User): User initiating the connection
- `connected_user` (Foreign Key → User): User receiving the connection
- `created_at`: Timestamp when the connection was established
- `is_deleted`: Soft deletion flag for removing connections without deleting data

**Meta:**
- `unique_together`: (user, connected_user) to prevent duplicate connections

**Indexes:**
- `(user, connected_user)`: For efficient lookup of user connections

**Usage:**
- Building the social graph within the platform
- Determining content visibility and feed population
- Supporting connection management features

### TermsAndConditions

Tracks user acceptance of the platform's terms and conditions.

**Fields:**
- `id` (Primary Key): Unique identifier
- `user` (Foreign Key → User): User who has accepted the terms
- `accepted`: Boolean flag indicating acceptance
- `date_accepted`: Timestamp when terms were accepted

**Usage:**
- Legal compliance tracking
- User onboarding flow management
- Access control based on terms acceptance

### Post

Stores user-generated content across different media types.

**Fields:**
- `id` (Primary Key): Unique identifier
- `user` (Foreign Key → User): User who created the post
- `content_type`: Type of content (choices: image, video, text)
- `content`: Text content, descriptions, or HTML for embedded media
- `media_file`: FileField for image or video uploads (optional)
- `metadata`: JSONField for analytics or engagement data
- `created_at`: Timestamp when the post was created
- `updated_at`: Timestamp when the post was last updated
- `is_deleted`: Soft deletion flag

**Indexes:**
- `(user, content_type)`: For filtering user posts by type
- `created_at`: For chronological sorting

**Usage:**
- Storing user-generated content
- Content feed generation
- Analytics and engagement tracking

### AuditLog

Records user actions for security monitoring and analytics.

**Fields:**
- `id` (Primary Key): Unique identifier
- `user` (Foreign Key → User): User who performed the action
- `action`: Type of action (choices: login, update_profile, post, connect)
- `timestamp`: When the action occurred
- `metadata`: JSONField with additional contextual information

**Indexes:**
- `(user, action)`: For filtering user actions by type
- `timestamp`: For chronological sorting

**Usage:**
- Security monitoring and auditing
- User activity analysis
- Debugging and support

## Database Relationships Diagram

```
+-------------+       +---------------+       +--------------------+
|    User     |<----->| UserProfile   |       | TermsAndConditions |
+-------------+       +---------------+       +--------------------+
    ^    ^                                          ^
    |    |                                          |
    |    |                                          |
    |    v                                          |
    |  +----------------+                           |
    |  | Connection     |                           |
    |  +----------------+                           |
    |                                               |
    v                                               |
+-------------------+                               |
| SocialMediaAccount|<------------------------------+
+-------------------+
    ^
    |
    |
    v
+-------------+       +-------------+
|    Post     |<----->|  AuditLog   |
+-------------+       +-------------+
```

## Database Indexing Strategy

SLID implements a strategic indexing approach to optimize query performance:

1. **Primary Keys**: All models have an auto-incrementing primary key (`id`)
2. **Foreign Key Indexes**: All foreign key fields are indexed
3. **Composite Indexes**: Where queries frequently filter by multiple columns
4. **Sorting Indexes**: Fields frequently used for ordering (e.g., `created_at`)
5. **Lookup Indexes**: Fields frequently used in WHERE clauses (e.g., `username`)

## Soft Deletion Implementation

Several models use a `is_deleted` boolean field rather than physical deletion:

1. **UserProfile**: User accounts are soft-deleted to preserve data integrity
2. **Post**: Content is marked as deleted but retained for record-keeping
3. **Connection**: Relationships can be removed while maintaining history

This approach preserves data for analytics and potential recovery while maintaining privacy.

## Performance Considerations

1. **Denormalization**: The `SocialMediaAccount.data` JSONField stores platform-specific data to reduce the need for multiple tables per platform
2. **Profile Score Caching**: The `profile_score` field pre-computes completeness metrics
3. **Strategic Indexing**: Indexes are placed on frequently queried fields
4. **Soft Deletion**: Maintains data integrity while allowing "deletion" from a user perspective

## Data Model Evolution

The SLID data model follows these principles for future evolution:

1. **Backward Compatibility**: New fields should be nullable or have defaults
2. **Migration Planning**: Schema changes require careful migration planning
3. **Performance Analysis**: New models and relationships should be analyzed for performance impact
4. **Data Integrity**: Referential integrity should be maintained

## Future Extensions

Planned database schema extensions include:

1. **Analytics Models**: More detailed tracking of user engagement
2. **Content Categorization**: Advanced tagging and categorization of user content
3. **Notification System**: Models to support a comprehensive notification framework
4. **Enhanced Privacy Controls**: More granular privacy settings storage
5. **Access Control Lists**: Refined permissions beyond the current model
