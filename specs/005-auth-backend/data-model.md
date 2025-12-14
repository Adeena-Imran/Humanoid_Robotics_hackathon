# Data Model for Authentication Backend

## Entity: User

Represents an authenticated user in the system.

**Fields**:

*   `id`: `String` (UUID, primary key, `@id`, `@default(uuid())`)
    *   **Description**: Unique identifier for the user.
*   `name`: `String`
    *   **Description**: User's display name.
*   `email`: `String` (unique, `@unique`)
    *   **Description**: User's email address, must be unique across all users.
*   `passwordHash`: `String`
    *   **Description**: Hashed password using bcrypt. Never stored in plaintext.
*   `createdAt`: `DateTime` (`@default(now())`)
    *   **Description**: Timestamp of when the user account was created.

**Relationships**: (None for this feature)

**Validation Rules (Implicit from Feature Spec)**:

*   `name`, `email`, `password` (for signup) must be present and valid (e.g., `email` must be a valid email format, `password` should meet certain strength requirements - though not explicitly detailed, assumed as basic validation).
*   `email` must be unique during signup.