# Fullstack Development (Senior Fullstack)

## Overview

The Fullstack Development skill provides comprehensive tools and frameworks for building complete, production-ready web applications with modern technologies. This skill combines React/Next.js frontend development, Node.js backend services, GraphQL APIs, and PostgreSQL databases with industry best practices for architecture, code quality, and development workflows. It enables fullstack engineers to rapidly scaffold projects, maintain high code quality, and build scalable applications.

## Who Should Use This Skill

- **Fullstack Engineers** building complete web applications
- **Senior Software Engineers** architecting and implementing full solutions
- **Tech Leads** establishing project standards and scaffolding
- **Startup Engineers** building MVPs and products from scratch
- **Platform Engineers** creating internal tools and services
- **Application Architects** designing scalable application architectures
- **Engineering Teams** standardizing development workflows and patterns

## Purpose and Use Cases

Use this skill when you need to:
- Scaffold new fullstack projects with best practices
- Build React/Next.js frontend applications
- Create Node.js/Express backend services
- Implement GraphQL APIs
- Set up PostgreSQL databases with Prisma ORM
- Analyze and improve code quality
- Implement architecture patterns (MVC, clean architecture, microservices)
- Set up development workflows and tooling
- Build authentication and authorization systems
- Create RESTful and GraphQL APIs
- Implement real-time features with WebSockets
- Deploy fullstack applications to production

**Keywords that trigger this skill:** fullstack development, React, Next.js, Node.js, GraphQL, REST API, PostgreSQL, Prisma, project scaffolding, code quality, architecture patterns, TypeScript, Express

## What's Included

### Fullstack Scaffolder

**Project Templates:**
- **Next.js + GraphQL + PostgreSQL** - Modern fullstack with tRPC
- **React SPA + Node.js API** - Separate frontend/backend
- **Next.js + REST API** - Server-side rendered with API routes
- **Monorepo Setup** - Turborepo with shared packages
- **Microservices** - Multiple services with shared infrastructure

**Pre-configured Features:**
- TypeScript strict mode
- ESLint + Prettier
- Husky git hooks
- Jest + React Testing Library
- Docker + Docker Compose
- CI/CD templates (GitHub Actions)
- Environment configuration
- Database migrations
- API documentation (Swagger/GraphQL Playground)
- Authentication boilerplate

**Tech Stack Options:**

**Frontend:**
- React 18 with hooks
- Next.js 14 (App Router or Pages Router)
- TailwindCSS or styled-components
- shadcn/ui components
- React Query for data fetching
- Zustand or Redux for state management
- React Hook Form for forms
- Zod for validation

**Backend:**
- Node.js 20+ with TypeScript
- Express.js or Fastify
- GraphQL with Apollo Server or tRPC
- REST API with OpenAPI/Swagger
- Prisma ORM for database
- JWT authentication
- Rate limiting and security middleware
- Logging (Winston, Pino)

**Database:**
- PostgreSQL 16+
- Prisma migrations
- Database seeding
- Connection pooling
- Type-safe queries
- Multi-schema support

**DevOps:**
- Docker containerization
- Docker Compose for local dev
- GitHub Actions CI/CD
- Environment management
- Health checks
- Logging and monitoring

### Project Scaffolder

**Scaffolding Capabilities:**

**Component Generation:**
```bash
# Generate React component with tests
python scripts/project_scaffolder.py component UserProfile \
  --with-tests \
  --with-storybook

# Generate API endpoint
python scripts/project_scaffolder.py endpoint /api/users \
  --method GET,POST \
  --auth required \
  --with-tests

# Generate database model
python scripts/project_scaffolder.py model User \
  --fields email:String,name:String,role:Enum \
  --with-relations
```

**Feature Modules:**
```bash
# Generate complete feature module
python scripts/project_scaffolder.py feature authentication \
  --include-frontend \
  --include-backend \
  --include-database \
  --with-tests

# Generated structure:
# src/features/authentication/
# ├── frontend/
# │   ├── components/
# │   │   ├── LoginForm.tsx
# │   │   └── RegisterForm.tsx
# │   ├── hooks/
# │   │   └── useAuth.ts
# │   └── types.ts
# ├── backend/
# │   ├── routes/
# │   │   └── auth.routes.ts
# │   ├── controllers/
# │   │   └── auth.controller.ts
# │   ├── services/
# │   │   └── auth.service.ts
# │   └── middleware/
# │       └── auth.middleware.ts
# └── database/
#     ├── schema.prisma
#     └── migrations/
```

**Architecture Scaffolding:**
```bash
# Generate clean architecture structure
python scripts/project_scaffolder.py architecture clean \
  --layers domain,application,infrastructure,presentation

# Generate microservice
python scripts/project_scaffolder.py microservice user-service \
  --with-api-gateway \
  --with-database \
  --with-events
```

### Code Quality Analyzer

**Analysis Capabilities:**

**Code Metrics:**
- Cyclomatic complexity
- Code duplication detection
- Lines of code (LOC) analysis
- Test coverage gaps
- Dead code detection
- Import/dependency analysis
- Technical debt estimation

**Quality Checks:**
- TypeScript type coverage
- ESLint violations
- Prettier formatting issues
- Unused exports/imports
- Security vulnerabilities
- Performance anti-patterns
- Accessibility issues
- SEO best practices (Next.js)

**Architecture Analysis:**
- Layer dependency violations
- Circular dependencies
- Module coupling
- Component complexity
- API consistency
- Database query efficiency
- Bundle size analysis

**Automated Fixes:**
- Auto-format code
- Fix ESLint issues
- Update imports
- Remove dead code
- Optimize bundle size
- Add missing TypeScript types
- Generate missing tests

**Quality Reports:**
```bash
# Generate comprehensive quality report
python scripts/code_quality_analyzer.py /path/to/project \
  --output quality-report.html

# Focus on specific areas
python scripts/code_quality_analyzer.py /path/to/project \
  --focus typescript,performance,security \
  --threshold 80
```

## How It Works

### Fullstack Project Scaffolding Workflow

**Step 1: Choose Project Template**
```bash
# Interactive project creation
python scripts/fullstack_scaffolder.py --interactive

# Or specify template directly
python scripts/fullstack_scaffolder.py create my-app \
  --template nextjs-graphql-postgres \
  --package-manager pnpm \
  --styling tailwind
```

**Interactive Prompts:**
```
Welcome to Fullstack Scaffolder!
================================

Project name: my-saas-app
Description: SaaS application with subscription management

Select template:
  1. Next.js + GraphQL + PostgreSQL (recommended for fullstack)
  2. React SPA + Node.js REST API (separate frontend/backend)
  3. Next.js + tRPC + PostgreSQL (type-safe E2E)
  4. Microservices (multiple services)
  5. Custom (manual selection)

Choice: 1

Select features:
  [x] Authentication (JWT + refresh tokens)
  [x] Authorization (role-based access control)
  [x] File uploads (S3 integration)
  [ ] Real-time features (WebSockets)
  [x] Email service (SendGrid)
  [x] Payments (Stripe)
  [x] Admin dashboard
  [x] API documentation
  [x] Docker setup

Database:
  [x] PostgreSQL with Prisma
  [ ] Add Redis for caching
  [x] Database seeding

DevOps:
  [x] GitHub Actions CI/CD
  [x] Docker Compose for local dev
  [x] Environment config (.env)
  [x] Health checks
  [x] Logging setup

Frontend:
  Framework: Next.js 14 (App Router)
  Styling: TailwindCSS
  Components: shadcn/ui
  State: Zustand
  Forms: React Hook Form + Zod

Backend:
  Runtime: Node.js 20
  Framework: Express
  API: GraphQL (Apollo Server)
  ORM: Prisma
  Auth: JWT + refresh tokens

Initializing project...
✓ Created project structure
✓ Installed dependencies (2m 34s)
✓ Set up database
✓ Generated Prisma client
✓ Created example components
✓ Configured CI/CD
✓ Set up Docker

Project created successfully!

Next steps:
  cd my-saas-app
  cp .env.example .env (configure your environment)
  docker-compose up -d (start database)
  pnpm dev (start development server)

Documentation: ./README.md
```

**Step 2: Generated Project Structure**
```
my-saas-app/
├── apps/
│   └── web/                    # Next.js application
│       ├── app/                # App Router
│       │   ├── (auth)/
│       │   │   ├── login/
│       │   │   └── register/
│       │   ├── (dashboard)/
│       │   │   ├── layout.tsx
│       │   │   ├── page.tsx
│       │   │   └── settings/
│       │   ├── api/            # API routes
│       │   │   ├── graphql/
│       │   │   └── webhooks/
│       │   └── layout.tsx
│       ├── components/
│       │   ├── ui/             # shadcn/ui components
│       │   ├── forms/
│       │   └── layouts/
│       ├── lib/
│       │   ├── graphql/        # GraphQL client
│       │   ├── auth/           # Auth utilities
│       │   └── utils/
│       ├── public/
│       ├── styles/
│       ├── .env.example
│       ├── next.config.js
│       ├── tailwind.config.ts
│       └── tsconfig.json
├── packages/
│   ├── database/               # Prisma schema & migrations
│   │   ├── prisma/
│   │   │   ├── schema.prisma
│   │   │   ├── migrations/
│   │   │   └── seed.ts
│   │   └── src/
│   │       ├── client.ts
│   │       └── types.ts
│   ├── api/                    # Backend API
│   │   ├── src/
│   │   │   ├── graphql/
│   │   │   │   ├── schema.ts
│   │   │   │   ├── resolvers/
│   │   │   │   └── context.ts
│   │   │   ├── services/
│   │   │   │   ├── auth.service.ts
│   │   │   │   ├── user.service.ts
│   │   │   │   └── subscription.service.ts
│   │   │   ├── middleware/
│   │   │   │   ├── auth.ts
│   │   │   │   ├── rate-limit.ts
│   │   │   │   └── error-handler.ts
│   │   │   ├── utils/
│   │   │   └── index.ts
│   │   └── tests/
│   ├── shared/                 # Shared types and utils
│   │   ├── src/
│   │   │   ├── types/
│   │   │   ├── constants/
│   │   │   └── utils/
│   │   └── tsconfig.json
│   └── config/                 # Shared config
│       ├── eslint-config/
│       └── typescript-config/
├── docker/
│   ├── Dockerfile.web
│   ├── Dockerfile.api
│   └── nginx.conf
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── deploy.yml
│       └── test.yml
├── docker-compose.yml
├── turbo.json                  # Turborepo config
├── package.json
├── pnpm-workspace.yaml
└── README.md
```

**Step 3: Start Development**
```bash
cd my-saas-app

# Configure environment
cp .env.example .env
# Edit .env with your config

# Start database
docker-compose up -d postgres redis

# Run migrations
pnpm db:migrate

# Seed database
pnpm db:seed

# Start development server
pnpm dev

# Opens:
# - Frontend: http://localhost:3000
# - GraphQL Playground: http://localhost:3000/api/graphql
# - API Docs: http://localhost:3000/api/docs
```

### Code Quality Analysis Workflow

**Step 1: Run Quality Analysis**
```bash
# Comprehensive quality check
python scripts/code_quality_analyzer.py /path/to/project \
  --comprehensive \
  --output quality-report.html

# Quick quality check (critical issues only)
python scripts/code_quality_analyzer.py /path/to/project \
  --quick

# Focus on specific areas
python scripts/code_quality_analyzer.py /path/to/project \
  --focus security,performance \
  --threshold 85
```

**Step 2: Review Quality Report**
```
CODE QUALITY ANALYSIS REPORT
=============================

Project: my-saas-app
Analyzed: 2025-11-13 14:30:00
Files: 247 TypeScript files
Lines of Code: 15,234

OVERALL SCORE: 78/100 (Good, needs improvement)

CATEGORY SCORES
===============

TypeScript Quality: 85/100 (Very Good)
  ✓ Type coverage: 94%
  ✓ Strict mode enabled
  ✗ 23 files with 'any' types
  ✗ 7 files with type assertions

Code Quality: 72/100 (Good)
  ✓ Average complexity: 4.2 (Good)
  ✗ 5 functions exceed complexity threshold (>10)
  ✗ Code duplication: 8.3% (threshold: 5%)
  ✓ Dead code: 2.1% (acceptable)

Test Coverage: 68/100 (Needs Improvement)
  ✗ Overall coverage: 68% (target: 80%)
  ✗ Branch coverage: 62%
  ✓ Unit tests: 89%
  ✗ Integration tests: 45%
  ✗ E2E tests: 12%

Performance: 82/100 (Very Good)
  ✓ Bundle size: 245 KB (good)
  ✓ No heavy dependencies detected
  ✗ 3 unoptimized images
  ✗ 2 components without memoization

Security: 75/100 (Good)
  ✓ No critical vulnerabilities
  ✗ 4 high-severity npm vulnerabilities
  ✗ Environment variables in code (3 instances)
  ✗ Missing rate limiting on 2 endpoints

Architecture: 80/100 (Very Good)
  ✓ Clean separation of concerns
  ✓ No circular dependencies
  ✗ 2 layer boundary violations
  ✗ High coupling in user service

CRITICAL ISSUES (Fix Immediately)
==================================

1. Environment Variable Exposure
   Location: src/lib/config.ts:12
   Issue: API key hardcoded in source
   Evidence:
     const STRIPE_KEY = 'sk_test_xxx'; // NEVER do this
   Impact: Security breach, credential exposure
   Fix: Move to environment variables
   Effort: 15 minutes

2. Missing Input Validation
   Location: src/api/users/create.ts:45
   Issue: User input not validated before database insert
   Evidence:
     await prisma.user.create({ data: req.body });
   Impact: SQL injection risk, data corruption
   Fix: Add Zod schema validation
   Effort: 30 minutes

3. High Cyclomatic Complexity
   Location: src/services/subscription.ts:handlePayment
   Issue: Complexity score of 23 (threshold: 10)
   Impact: Hard to test, maintain, and understand
   Fix: Extract methods, simplify conditionals
   Effort: 2 hours

HIGH PRIORITY ISSUES
====================

4. Missing Test Coverage
   Location: src/api/auth/**
   Issue: Authentication module only 42% covered
   Impact: Critical functionality untested
   Fix: Add unit and integration tests
   Effort: 1 day

5. Code Duplication
   Locations: Multiple files
   Issue: Duplicate validation logic in 7 files
   Evidence:
     src/api/users/create.ts:23
     src/api/users/update.ts:34
     src/api/profiles/update.ts:45
   Impact: Maintenance overhead, inconsistency
   Fix: Extract shared validation utilities
   Effort: 3 hours

6. npm Security Vulnerabilities
   Packages: 4 high-severity vulnerabilities
   - axios@0.21.1 (CVE-2021-3749)
   - lodash@4.17.19 (CVE-2020-8203)
   - minimist@1.2.5 (CVE-2021-44906)
   - node-fetch@2.6.1 (CVE-2022-0235)
   Fix: Run 'pnpm audit fix' and test
   Effort: 1 hour

RECOMMENDATIONS
===============

TypeScript:
  - Replace 'any' types with proper types
  - Enable 'noImplicitAny' in tsconfig
  - Add return types to all functions
  - Remove unnecessary type assertions

Testing:
  - Increase coverage to 80% overall
  - Focus on auth and payment modules
  - Add E2E tests for critical flows
  - Set up coverage gates in CI

Performance:
  - Optimize images with next/image
  - Add React.memo to expensive components
  - Implement code splitting for large pages
  - Add bundle analysis to CI

Security:
  - Update vulnerable dependencies
  - Add rate limiting to all API endpoints
  - Implement input validation with Zod
  - Move all secrets to environment variables
  - Add security headers (helmet.js)

Architecture:
  - Fix layer violations in auth module
  - Reduce coupling in user service
  - Extract shared business logic
  - Document architecture decisions

AUTOMATED FIXES AVAILABLE
==========================

The analyzer can automatically fix 15 issues:

  ✓ Format all files with Prettier
  ✓ Fix ESLint violations (12 auto-fixable)
  ✓ Remove unused imports (34 files)
  ✓ Update npm dependencies
  ✓ Add missing TypeScript types (8 files)

Run with --auto-fix to apply these fixes.

METRICS TRENDS
==============

Compared to last analysis (7 days ago):
  Quality Score: 75 → 78 (+3) ✓ Improving
  Test Coverage: 65% → 68% (+3%) ✓ Improving
  Security Score: 70 → 75 (+5) ✓ Improving
  Technical Debt: 15 days → 12 days (-3) ✓ Improving

Good progress! Keep it up.
```

**Step 3: Apply Automated Fixes**
```bash
# Apply all automated fixes
python scripts/code_quality_analyzer.py /path/to/project \
  --auto-fix

# Apply specific fixes
python scripts/code_quality_analyzer.py /path/to/project \
  --fix formatting,eslint,imports

# Update dependencies
python scripts/code_quality_analyzer.py /path/to/project \
  --update-dependencies \
  --security-only
```

**Step 4: Track Quality Over Time**
```bash
# Generate quality report with history
python scripts/code_quality_analyzer.py /path/to/project \
  --track-history \
  --output quality-dashboard.html

# Export metrics for CI
python scripts/code_quality_analyzer.py /path/to/project \
  --export-metrics metrics.json \
  --fail-threshold 70
```

### Feature Module Scaffolding Workflow

**Example: Adding Subscription Management Feature**

**Step 1: Scaffold Feature Module**
```bash
# Generate complete subscription feature
python scripts/project_scaffolder.py feature subscription \
  --include-frontend \
  --include-backend \
  --include-database \
  --with-tests \
  --with-stripe-integration
```

**Step 2: Generated Structure**
```
src/features/subscription/
├── frontend/
│   ├── components/
│   │   ├── SubscriptionPlan.tsx
│   │   ├── PricingTable.tsx
│   │   ├── CheckoutForm.tsx
│   │   ├── ManageSubscription.tsx
│   │   └── PaymentMethodCard.tsx
│   ├── hooks/
│   │   ├── useSubscription.ts
│   │   ├── useCheckout.ts
│   │   └── usePaymentMethods.ts
│   ├── types/
│   │   └── subscription.types.ts
│   └── __tests__/
│       └── SubscriptionPlan.test.tsx
├── backend/
│   ├── graphql/
│   │   ├── subscription.schema.ts
│   │   └── subscription.resolvers.ts
│   ├── services/
│   │   ├── subscription.service.ts
│   │   ├── stripe.service.ts
│   │   └── billing.service.ts
│   ├── routes/
│   │   └── webhooks.ts (Stripe webhooks)
│   └── __tests__/
│       ├── subscription.service.test.ts
│       └── stripe.service.test.ts
├── database/
│   ├── schema.prisma
│   │   # model Subscription {
│   │   #   id        String   @id @default(cuid())
│   │   #   userId    String
│   │   #   user      User     @relation(...)
│   │   #   planId    String
│   │   #   status    String
│   │   #   ...
│   │   # }
│   └── migrations/
│       └── 001_add_subscription.sql
└── README.md
```

**Step 3: Integrate Feature**
```bash
# Run migrations
pnpm db:migrate

# Generate Prisma client
pnpm db:generate

# Register GraphQL schema
# (automatically imported if using glob imports)

# Add routes to main app
# (automatically registered if using auto-routing)

# Run tests
pnpm test src/features/subscription
```

## Technical Details

### Full Tech Stack

**Frontend Technologies:**
```typescript
// Next.js 14 with App Router
// TypeScript 5+
// React 18
// TailwindCSS 3+
// shadcn/ui components
// React Query for server state
// Zustand for client state
// React Hook Form + Zod for forms
// next-auth for authentication
```

**Backend Technologies:**
```typescript
// Node.js 20+
// TypeScript 5+
// Express.js or Fastify
// GraphQL (Apollo Server) or tRPC
// Prisma ORM
// JWT for authentication
// Winston for logging
// Jest for testing
// Zod for validation
```

**Database:**
```sql
-- PostgreSQL 16+
-- Prisma migrations
-- Connection pooling (PgBouncer)
-- Full-text search
-- JSONB columns for flexible data
-- Row-level security
-- Database triggers and functions
```

**DevOps:**
```yaml
# Docker + Docker Compose
# GitHub Actions CI/CD
# Automated testing
# Automated deployments
# Environment management
# Health checks and monitoring
# Log aggregation
```

### Architecture Patterns

**Clean Architecture:**
```
presentation/     # UI components, pages
├── components/
├── pages/
└── hooks/

application/      # Use cases, business logic
├── usecases/
└── services/

domain/          # Entities, business rules
├── entities/
├── repositories/
└── value-objects/

infrastructure/  # External services, database
├── database/
├── external-services/
└── config/
```

**Feature-Based Architecture:**
```
features/
├── authentication/
│   ├── frontend/    # UI components
│   ├── backend/     # API logic
│   ├── database/    # Schema
│   └── shared/      # Types
├── user-management/
└── subscription/

shared/
├── components/      # Shared UI
├── hooks/          # Shared hooks
├── utils/          # Utilities
└── types/          # Global types
```

### Database Schema Example

```prisma
// schema.prisma

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id            String         @id @default(cuid())
  email         String         @unique
  name          String?
  passwordHash  String
  role          Role           @default(USER)
  subscriptions Subscription[]
  sessions      Session[]
  createdAt     DateTime       @default(now())
  updatedAt     DateTime       @updatedAt

  @@index([email])
  @@map("users")
}

model Subscription {
  id                String   @id @default(cuid())
  userId            String
  user              User     @relation(fields: [userId], references: [id])
  stripeCustomerId  String
  stripeSubscriptionId String @unique
  stripePriceId     String
  status            SubscriptionStatus
  currentPeriodStart DateTime
  currentPeriodEnd   DateTime
  cancelAtPeriodEnd Boolean  @default(false)
  createdAt         DateTime @default(now())
  updatedAt         DateTime @updatedAt

  @@index([userId])
  @@index([stripeSubscriptionId])
  @@map("subscriptions")
}

enum Role {
  USER
  ADMIN
  SUPER_ADMIN
}

enum SubscriptionStatus {
  ACTIVE
  CANCELED
  PAST_DUE
  UNPAID
  INCOMPLETE
}
```

### GraphQL Schema Example

```typescript
// graphql/schema.ts

import { gql } from 'apollo-server-express';

export const typeDefs = gql`
  type User {
    id: ID!
    email: String!
    name: String
    role: Role!
    subscription: Subscription
    createdAt: DateTime!
  }

  type Subscription {
    id: ID!
    status: SubscriptionStatus!
    plan: Plan!
    currentPeriodEnd: DateTime!
    cancelAtPeriodEnd: Boolean!
  }

  type Plan {
    id: ID!
    name: String!
    price: Int!
    interval: BillingInterval!
    features: [String!]!
  }

  enum Role {
    USER
    ADMIN
    SUPER_ADMIN
  }

  enum SubscriptionStatus {
    ACTIVE
    CANCELED
    PAST_DUE
    UNPAID
  }

  enum BillingInterval {
    MONTH
    YEAR
  }

  type Query {
    me: User!
    user(id: ID!): User
    users(limit: Int, offset: Int): [User!]!
    plans: [Plan!]!
  }

  type Mutation {
    updateProfile(input: UpdateProfileInput!): User!
    createSubscription(planId: ID!): Subscription!
    cancelSubscription: Subscription!
    updatePaymentMethod(paymentMethodId: String!): Boolean!
  }

  input UpdateProfileInput {
    name: String
    email: String
  }

  scalar DateTime
`;
```

## Use Cases and Examples

### Building a SaaS Application

**Scenario:** Build a SaaS platform with subscriptions, multi-tenancy, and admin dashboard

**Week 1: Project Setup**
```bash
# Scaffold project
python scripts/fullstack_scaffolder.py create my-saas \
  --template nextjs-graphql-postgres \
  --features auth,rbac,subscriptions,multi-tenant,admin

# Configure environment
cd my-saas
cp .env.example .env
# Edit .env with your credentials

# Start development
docker-compose up -d
pnpm install
pnpm db:migrate
pnpm db:seed
pnpm dev
```

**Week 2: Core Features**
```bash
# Add team management
python scripts/project_scaffolder.py feature teams \
  --with-invitations \
  --with-roles

# Add workspace isolation (multi-tenancy)
python scripts/project_scaffolder.py feature workspace \
  --row-level-security

# Add file uploads
python scripts/project_scaffolder.py feature file-upload \
  --provider s3 \
  --max-size 10mb
```

**Week 3: Business Logic**
```bash
# Add subscription management
python scripts/project_scaffolder.py feature subscription \
  --provider stripe \
  --with-webhooks \
  --with-usage-tracking

# Add email notifications
python scripts/project_scaffolder.py feature notifications \
  --provider sendgrid \
  --templates welcome,subscription-confirmed,payment-failed
```

**Week 4: Admin & Analytics**
```bash
# Add admin dashboard
python scripts/project_scaffolder.py feature admin-dashboard \
  --metrics users,revenue,subscriptions \
  --with-charts

# Add analytics
python scripts/project_scaffolder.py feature analytics \
  --provider mixpanel \
  --track-events pageview,signup,subscription
```

**Week 5-6: Polish & Deploy**
```bash
# Run quality checks
python scripts/code_quality_analyzer.py . \
  --comprehensive \
  --threshold 80

# Fix issues
python scripts/code_quality_analyzer.py . --auto-fix

# Run all tests
pnpm test

# Deploy to production
git push origin main  # Triggers CI/CD
```

### Migrating Legacy Application

**Scenario:** Modernize legacy Express + jQuery app to Next.js + TypeScript

**Step 1: Analysis**
```bash
# Analyze existing codebase
python scripts/code_quality_analyzer.py /path/to/legacy \
  --migration-analysis \
  --target nextjs-typescript

# Output: Migration roadmap with effort estimates
```

**Step 2: Scaffold New Project**
```bash
# Create new Next.js project
python scripts/fullstack_scaffolder.py create app-v2 \
  --template nextjs-rest-postgres \
  --migrate-from /path/to/legacy
```

**Step 3: Incremental Migration**
```bash
# Migrate authentication first
python scripts/project_scaffolder.py migrate auth \
  --from /path/to/legacy/routes/auth \
  --to ./apps/web

# Migrate API endpoints
python scripts/project_scaffolder.py migrate api \
  --from /path/to/legacy/routes/api \
  --to ./packages/api \
  --convert-to graphql

# Migrate database schema
python scripts/project_scaffolder.py migrate database \
  --from /path/to/legacy/schema.sql \
  --to ./packages/database/prisma/schema.prisma
```

## Best Practices

### Project Structure Best Practices

**Do:**
- Use feature-based organization for large apps
- Keep shared code in packages/shared
- Separate frontend and backend concerns
- Use monorepo for related projects
- Maintain consistent naming conventions
- Document architecture decisions
- Use TypeScript for everything

**Don't:**
- Mix frontend and backend logic
- Create deeply nested folder structures (max 3-4 levels)
- Duplicate code across features
- Skip documentation
- Use JavaScript for new code
- Ignore file organization

### Code Quality Best Practices

**Do:**
- Maintain 80%+ test coverage
- Run linters in CI/CD
- Use Prettier for consistent formatting
- Enable TypeScript strict mode
- Review code quality metrics regularly
- Fix security vulnerabilities immediately
- Keep dependencies updated

**Don't:**
- Skip writing tests
- Ignore linter warnings
- Use 'any' type in TypeScript
- Let technical debt accumulate
- Deploy with failing tests
- Ignore security advisories

### API Design Best Practices

**Do:**
- Use consistent naming (camelCase for GraphQL, snake_case for REST)
- Version APIs properly (v1, v2)
- Implement pagination for lists
- Add rate limiting
- Validate all inputs
- Return appropriate status codes
- Document APIs (Swagger/GraphQL schema)
- Use proper error handling

**Don't:**
- Expose internal implementation details
- Skip input validation
- Return stack traces in production
- Use unclear error messages
- Forget about API versioning
- Skip authentication/authorization
- Ignore API performance

### Database Best Practices

**Do:**
- Use migrations for schema changes
- Index frequently queried columns
- Use transactions for related updates
- Implement soft deletes where appropriate
- Use UUIDs for primary keys
- Validate data at application level
- Use connection pooling
- Monitor query performance

**Don't:**
- Modify database schema manually
- Forget to add indexes
- Store sensitive data unencrypted
- Use SELECT * queries
- Skip database backups
- Ignore query performance
- Use cascading deletes carelessly

## Integration Points

This skill integrates with:
- **Frontend:** React, Next.js, TailwindCSS, shadcn/ui
- **Backend:** Node.js, Express, Fastify, tRPC
- **API:** GraphQL (Apollo), REST (OpenAPI)
- **Database:** PostgreSQL, Prisma, Supabase
- **Authentication:** NextAuth.js, JWT, OAuth
- **Payments:** Stripe, PayPal
- **File Storage:** AWS S3, Cloudflare R2
- **Email:** SendGrid, Resend, Mailgun
- **Monitoring:** Sentry, DataDog, New Relic
- **CI/CD:** GitHub Actions, GitLab CI, CircleCI
- **Deployment:** Vercel, AWS, GCP, Azure

## Common Challenges and Solutions

### Challenge: Managing Monorepo Complexity
**Solution:** Use Turborepo for build orchestration, establish clear package boundaries, use shared ESLint/TypeScript configs, document package relationships, keep packages focused and small

### Challenge: TypeScript Configuration Issues
**Solution:** Use shared tsconfig base, enable path aliases (@/), use project references for monorepos, enable strict mode incrementally, document complex types

### Challenge: Database Migration Conflicts
**Solution:** Coordinate schema changes across team, use migration naming conventions, test migrations in staging first, maintain rollback scripts, use database branching tools

### Challenge: API Performance Issues
**Solution:** Implement DataLoader for GraphQL N+1 queries, add database indexes, use Redis caching, enable query logging, implement pagination, optimize bundle size

### Challenge: Test Maintenance Burden
**Solution:** Focus on integration tests over unit tests, use test factories for data setup, mock external services, run tests in parallel, maintain test utilities library

### Challenge: Environment Configuration Complexity
**Solution:** Use .env.example as template, validate environment variables at startup, use type-safe env parsing (Zod), document all variables, use secrets management for production
