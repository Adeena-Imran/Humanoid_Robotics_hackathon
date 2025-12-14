# Feature Specification: Authentication Backend

**Feature Branch**: `004-auth-backend`
**Created**: 2025-12-07
**Status**: Draft
**Input**: User description: "Create a simple authentication backend for the humanoid_roboti
cs_book project. Goal: A small Node.js + Express + Prisma + PostgreSQL API that supports: - 
User signup - User login - JWT access tokens (1h expiry) - Password hashing with bcrypt NO e
mail verification, NO refresh tokens, NO rate limiting. Keep it simple. Tech stack: - Node.j
s + Express - Prisma ORM - PostgreSQL (or SQLite for dev) - bcrypt for hashing - jsonwebtoke
n for JWT Features: 1) POST /api/auth/signup body: { name, email, password } - Validate inpu
ts - Hash password with bcrypt (salt rounds = 12) - Store user in DB - Return: { id, name, e
mail } 2) POST /api/auth/login body: { email, password } - Validate inputs - Check password 
with bcrypt - Return JWT token valid for 1h: { token } Database schema (Prisma): User: - id 
(uuid, PK) - name (string) - email (unique) - passwordHash (string) - createdAt (datetime) .
env.example: DATABASE_URL= JWT_SECRET= PORT=4000 BCRYPT_SALT=12 Deliverables: - prisma/schem
a.prisma - src/app.ts - src/server.ts - src/routes/auth.routes.ts - src/controllers/auth.con
troller.ts - src/services/auth.service.ts - src/utils/hash.ts - src/utils/jwt.ts - package.j
son with scripts: dev, start, migrate - README with setup steps Security: - Never log passwo
rds - Use bcrypt hashing - Use environment variables for secrets - Use safe error messages (
"Invalid credentials") This should be a minimal, simple authentication module suitable for b
eginners. Produce the full feature specification JSON and tasks.md."

## User Scenarios & Testing

### User Story 1 - New User Signup (Priority: P1)

A new user wants to create an account by providing their name, email, and password. The syst
em should securely store their credentials and confirm successful registration.

**Why this priority**: Essential for new users to access authenticated features.

**Independent Test**: A new user can successfully register with valid credentials and receiv
e a confirmation of their new account without sensitive information being exposed.

**Acceptance Scenarios**:

1.  **Given** the signup endpoint `POST /api/auth/signup` is available, **When** a user send
s a request with valid `name`, `email`, and `password`, **Then** the system creates a new us
er record in the database, hashes the password using bcrypt, and returns the new user's `id`
, `name`, and `email`.
2.  **Given** the signup endpoint `POST /api/auth/signup` is available, **When** a user atte
mpts to register with an `email` that already exists, **Then** the system returns an error i
ndicating the email is taken, without exposing internal errors.
3.  **Given** the signup endpoint `POST /api/auth/signup` is available, **When** a user send
s a request with invalid input (e.g., missing `email`, weak `password`), **Then** the system
 returns a validation error.

---

### User Story 2 - Existing User Login (Priority: P1)

An existing user wants to log in to their account by providing their email and password. The
 system should verify their credentials and issue a JSON Web Token (JWT) for authentication.

**Why this priority**: Allows existing users to authenticate and access protected resources.

**Independent Test**: An existing user can successfully log in with correct credentials and 
receive a valid JWT. Attempts with incorrect credentials should fail gracefully.

**Acceptance Scenarios**:

1.  **Given** the login endpoint `POST /api/auth/login` is available, **When** a user sends 
a request with a valid `email` and `password`, **Then** the system verifies the credentials,
 generates a JWT token valid for 1 hour, and returns the token.
2.  **Given** the login endpoint `POST /api/auth/login` is available, **When** a user sends 
a request with an incorrect `email` or `password`, **Then** the system returns a generic "In
valid credentials" error.
3.  **Given** the login endpoint `POST /api/auth/login` is available, **When** a user sends 
a request with invalid input (e.g., missing `email`), **Then** the system returns a validati
on error.

---

### User Story 3 - Developer Setup (Priority: P2)

A developer wants to set up the authentication backend locally, including database setup, en
vironment configuration, and running the application.

**Why this priority**: Facilitates development and deployment of the backend service.       

**Independent Test**: A developer can follow the README steps to get the backend running, co
nnect to the database, and execute migration scripts.

**Acceptance Scenarios**:

1.  **Given** the project repository, **When** a developer follows the setup instructions in
 the `README.md`, **Then** they can successfully set up the database (PostgreSQL/SQLite), co
nfigure environment variables, run database migrations, and start the backend server.       

---

### Edge Cases

-   **What happens when** a database connection fails during signup or login? The system sho
uld return an appropriate server error without exposing database details.
-   **How does the system handle** malformed JWTs provided by a client? The system should re
ject them gracefully.
-   **What if** `bcrypt` hashing or `jsonwebtoken` operations fail? The system should handle
 these errors and return generic server errors.

## Requirements

### Functional Requirements

-   **FR-001**: The system MUST provide an endpoint for user signup (`POST /api/auth/signup`
).
-   **FR-002**: The signup endpoint MUST validate `name`, `email`, and `password` inputs.   
-   **FR-003**: The system MUST hash user passwords using `bcrypt` (salt rounds = 12) before
 storing them.
-   **FR-004**: The system MUST store new user data (`id`, `name`, `email`, `passwordHash`, 
`createdAt`) in a PostgreSQL (or SQLite for dev) database via Prisma ORM.
-   **FR-005**: The signup endpoint MUST return the new user's `id`, `name`, and `email` upo
n successful registration.
-   **FR-006**: The system MUST provide an endpoint for user login (`POST /api/auth/login`).
-   **FR-007**: The login endpoint MUST validate `email` and `password` inputs.
-   **FR-008**: The system MUST verify user passwords against stored hashes using `bcrypt` d
uring login.
-   **FR-009**: Upon successful login, the system MUST generate a JWT access token valid for
 1 hour.
-   **FR-010**: The login endpoint MUST return the generated JWT token upon successful authe
ntication.
-   **FR-011**: The system MUST NOT implement email verification.
-   **FR-012**: The system MUST NOT implement refresh tokens.
-   **FR-013**: The system MUST NOT implement rate limiting.

### Non-Functional Requirements (Implicit from Description)

-   **NFR-001 (Security)**: Passwords MUST be hashed using `bcrypt` and NEVER stored in plai
ntext or logged.
-   **NFR-002 (Security)**: Sensitive information (e.g., database connection strings, JWT se
crets) MUST be stored as environment variables.
-   **NFR-003 (Security)**: Error messages for authentication failures MUST be generic (e.g.
, "Invalid credentials") to avoid leaking information.
-   **NFR-004 (Maintainability)**: The codebase SHOULD be modular and follow a clear archite
cture (e.g., routes, controllers, services, utils).
-   **NFR-005 (Usability)**: A `README.md` file MUST be provided with clear setup and usage 
instructions.

### Key Entities

-   **User**: Represents an authenticated user in the system.
    *   **Fields**:
        *   `id`: `String` (UUID, primary key, `@id`, `@default(uuid())`)
        *   `name`: `String`
        *   `email`: `String` (unique, `@unique`)
        *   `passwordHash`: `String`
        *   `createdAt`: `DateTime` (`@default(now())`)

## Success Criteria

### Measurable Outcomes

-   **SC-001**: New users can successfully sign up (`POST /api/auth/signup`) and their `id`,
 `name`, and `email` are returned within 500ms.
-   **SC-002**: Existing users can successfully log in (`POST /api/auth/login`) and receive 
a valid JWT token within 500ms.
-   **SC-003**: Attempts to sign up with a duplicate email address are rejected with an appr
opriate error message within 200ms.
-   **SC-004**: Attempts to log in with invalid credentials receive a "Invalid credentials" 
error message within 200ms.
-   **SC-005**: A developer can follow the `README.md` instructions and have the authenticat
ion backend fully operational (database migrations complete, server running, API endpoints a
ccessible) within 10 minutes on a fresh setup.
-   **SC-006**: The generated JWT tokens are correctly signed and expire after 1 hour.      
-   **SC-007**: No sensitive information (e.g., raw passwords, database errors) is exposed i
n API responses or logs during error scenarios.