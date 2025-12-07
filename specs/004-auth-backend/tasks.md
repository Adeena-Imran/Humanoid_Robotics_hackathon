---

description: "Tasks for Authentication Backend implementation"
---

# Tasks: Authentication Backend

**Input**: Design documents from `/specs/004-auth-backend/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/auth.yaml

**Tests**: Test tasks are NOT generated unless explicitly requested. The current feature specification does not explicitly request TDD or test generation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/` (as per plan.md)

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Project initialization and basic structure for the authentication backend.

- [x] T001 Create `backend` directory and initialize Node.js project `backend/package.json`
- [x] T002 Install core dependencies: `express`, `prisma`, `bcrypt`, `jsonwebtoken` `backend/package.json`
- [x] T003 [P] Install development dependencies: `typescript`, `@types/node`, `@types/express`, `@types/bcrypt`, `@types/jsonwebtoken`, `ts-node-dev`, `eslint`, `prettier` `backend/package.json`
- [x] T004 [P] Configure TypeScript `backend/tsconfig.json`
- [x] T005 [P] Create basic project directories: `backend/prisma`, `backend/src`, `backend/src/routes`, `backend/src/controllers`, `backend/src/services`, `backend/src/utils`, `backend/tests`
- [x] T006 Create `.env.example` file `backend/.env.example`
- [x] T007 Initialize Prisma: add `DATABASE_URL` and `JWT_SECRET` variables to `.env.example` `backend/.env.example`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Implement Prisma User model in `backend/prisma/schema.prisma`
- [x] T009 [P] Implement password hashing utility functions in `backend/src/utils/hash.ts`
- [x] T010 [P] Implement JWT utility functions (generate, verify) in `backend/src/utils/jwt.ts`
- [x] T011 Setup main Express application logic in `backend/src/app.ts` (middleware, basic error handling)
- [x] T012 Setup server entry point in `backend/src/server.ts` to start the Express app

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - New User Signup (Priority: P1)

**Goal**: Allow new users to create an account by providing their name, email, and password, securely storing their credentials and confirming registration.

**Independent Test**: A new user can successfully register with valid credentials (`POST /api/auth/signup`) and receive a confirmation of their new account without sensitive information being exposed.

### Implementation for User Story 1

- [x] T013 [US1] Implement signup service logic (create user, hash password) in `backend/src/services/auth.service.ts`
- [x] T014 [US1] Implement signup controller logic (handle request, call service, send response) in `backend/src/controllers/auth.controller.ts`
- [x] T015 [US1] Define signup route (`POST /api/auth/signup`) in `backend/src/routes/auth.routes.ts`
- [x] T016 [US1] Integrate signup route into `backend/src/app.ts`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Existing User Login (Priority: P1)

**Goal**: Allow existing users to log in to their account by providing their email and password, verifying credentials and issuing a JWT for authentication.

**Independent Test**: An existing user can successfully log in with correct credentials (`POST /api/auth/login`) and receive a valid JWT. Attempts with incorrect credentials should fail gracefully.

### Implementation for User Story 2

- [x] T017 [US2] Implement login service logic (verify password, generate JWT) in `backend/src/services/auth.service.ts`
- [x] T018 [US2] Implement login controller logic (handle request, call service, send response) in `backend/src/controllers/auth.controller.ts`
- [x] T019 [US2] Define login route (`POST /api/auth/login`) in `backend/src/routes/auth.routes.ts`
- [x] T020 [US2] Integrate login route into `backend/src/app.ts`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Developer Setup (Priority: P2)

**Goal**: Enable a developer to set up the authentication backend locally, including database setup, environment configuration, and running the application.

**Independent Test**: A developer can follow the README steps to get the backend running, connect to the database, and execute migration scripts.

### Implementation for User Story 3

- [x] T021 [US3] Update `backend/package.json` with scripts for `dev`, `start`, `migrate`
- [x] T022 [US3] Create `README.md` with comprehensive setup steps, including `.env` configuration, Prisma migrations, and running the application `backend/README.md`

**Checkpoint**: All user stories should now be independently functional

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and overall quality.

- [x] T023 Implement comprehensive input validation for signup and login requests (e.g., using a validation library) `backend/src/controllers/auth.controller.ts`
- [x] T024 Enhance error handling to return generic, secure messages as per NFR-003 `backend/src/app.ts`, `backend/src/controllers/auth.controller.ts`
- [x] T025 Configure ESLint and Prettier for code quality and formatting `backend/.eslintrc.json`, `backend/.prettierrc`
- [x] T026 Add basic unit tests for utility functions (hash, jwt) `backend/tests/unit/`
- [x] T027 Conduct security review: ensure no sensitive information is logged or exposed inadvertently.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories (focus on documentation/scripts)

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel.
- All Foundational tasks marked [P] can run in parallel (within Phase 2).
- Once Foundational phase completes, User Stories 1, 2, and 3 can be worked on in parallel by different team members, though integration points should be managed.
- Within User Stories, tasks marked [P] can run in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Signup)
   - Developer B: User Story 2 (Login)
   - Developer C: User Story 3 (Developer Setup)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
