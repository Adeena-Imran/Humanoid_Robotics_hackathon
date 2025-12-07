# Authentication Backend

This is a simple authentication backend for the `humanoid_robotics_book` project, built with Node.js, Express, Prisma, and PostgreSQL. It provides user signup, login, and JWT access tokens.

## Features

- User signup (`POST /api/auth/signup`)
- User login (`POST /api/auth/login`)
- JWT access tokens (1h expiry)
- Password hashing with bcrypt (salt rounds = 12)

## Technologies

- Node.js + Express
- Prisma ORM
- PostgreSQL (or SQLite for development)
- bcrypt for password hashing
- jsonwebtoken for JWTs
- TypeScript

## Setup Instructions

Follow these steps to get the authentication backend running locally.

### Prerequisites

- Node.js (v20 or higher recommended)
- npm or yarn
- PostgreSQL database (or Docker for easy setup)

### 1. Clone the repository

```bash
# Assuming you are in the root of the humanoid_robotics_book project
git clone <repository-url>
cd backend # Navigate into the backend directory
```

### 2. Install Dependencies

Navigate to the `backend` directory and install the project dependencies:

```bash
npm install
# or
yarn install
```

### 3. Environment Configuration

Create a `.env` file in the `backend` directory by copying the `.env.example` file:

```bash
cp .env.example .env
```

Edit the `.env` file and update the following variables:

-   `DATABASE_URL`: Your PostgreSQL connection string. Example: `postgresql://user:password@localhost:5432/mydb?schema=public`
-   `JWT_SECRET`: A strong, random string for signing JWTs.
-   `PORT`: The port on which the server will run (default: `4000`).

Example `.env` file:
```
DATABASE_URL="postgresql://myuser:mypassword@localhost:5432/authdb?schema=public"
JWT_SECRET="YOUR_SUPER_SECRET_KEY_HERE_REPLACE_ME_WITH_A_STRONG_RANDOM_STRING"
PORT=4000
```

### 4. Database Setup and Migrations (Prisma)

Ensure your PostgreSQL database is running and accessible via the `DATABASE_URL` you provided in `.env`.

Run Prisma migrations to create the database schema:

```bash
npx prisma migrate dev --name init
```

This command will apply the schema defined in `prisma/schema.prisma` to your database.

### 5. Run the Application

#### Development Mode (with hot-reloading)

```bash
npm run dev
# or
yarn dev
```

The server will start on the configured `PORT` (default: 4000).

#### Production Mode (build and start)

First, build the TypeScript project:

```bash
npm run build
# or
yarn build
```

Then, start the server:

```bash
npm start
# or
yarn start
```

### API Endpoints

-   **Signup**: `POST /api/auth/signup`
    -   **Request Body**: `{ "name": "string", "email": "string", "password": "string" }`
    -   **Response**: `{ "id": "uuid", "name": "string", "email": "string" }`
-   **Login**: `POST /api/auth/login`
    -   **Request Body**: `{ "email": "string", "password": "string" }`
    -   **Response**: `{ "token": "string" }`

---
