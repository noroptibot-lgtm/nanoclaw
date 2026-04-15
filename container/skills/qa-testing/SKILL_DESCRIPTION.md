# QA and Testing (Senior QA)

## Overview

The QA and Testing skill provides comprehensive tools and frameworks for quality assurance, test automation, and testing strategies for modern web applications. This skill enables QA engineers to design robust test strategies, implement automated testing pipelines, analyze test coverage, and ensure software quality across unit, integration, and end-to-end testing. It combines test suite generation, coverage analysis, and E2E testing with industry best practices for React, Next.js, and Node.js applications.

## Who Should Use This Skill

- **QA Engineers** implementing comprehensive testing strategies
- **Test Automation Engineers** building automated testing frameworks
- **SDET (Software Development Engineers in Test)** bridging development and testing
- **Quality Assurance Leads** establishing testing standards and practices
- **Senior QA** designing test architectures and strategies
- **DevOps Engineers** integrating testing into CI/CD pipelines
- **Fullstack Engineers** implementing testing for their applications
- **Engineering Managers** ensuring quality standards across teams

## Purpose and Use Cases

Use this skill when you need to:
- Design comprehensive test strategies
- Generate test suites for components, APIs, and features
- Implement test automation frameworks
- Analyze and improve test coverage
- Set up end-to-end testing with Playwright or Cypress
- Create API testing suites
- Implement visual regression testing
- Build performance and load testing
- Generate test data and fixtures
- Integrate testing into CI/CD pipelines
- Analyze test metrics and quality trends
- Perform exploratory testing

**Keywords that trigger this skill:** testing, QA, test automation, test coverage, unit tests, integration tests, E2E testing, Playwright, Cypress, Jest, test suite, test strategy, quality assurance, test data

## What's Included

### Test Suite Generator

**Automated Test Generation:**
- Unit test generation for React components
- Integration test generation for API endpoints
- Service test generation for business logic
- Database test generation for data access layer
- Hook test generation for custom React hooks
- Utility function test generation
- Test data factory generation

**Testing Frameworks:**
- **Jest** - Unit and integration testing
- **React Testing Library** - Component testing
- **Vitest** - Fast unit testing (Vite-powered)
- **Supertest** - API integration testing
- **MSW (Mock Service Worker)** - API mocking
- **Testing Library** - DOM testing utilities

**Test Generation Features:**
```bash
# Generate component tests
python scripts/test_suite_generator.py component UserProfile \
  --with-props \
  --with-events \
  --with-hooks

# Generate API tests
python scripts/test_suite_generator.py api /api/users \
  --methods GET,POST,PUT,DELETE \
  --auth-required \
  --with-validation

# Generate service tests
python scripts/test_suite_generator.py service UserService \
  --mock-database \
  --with-errors

# Generate E2E tests
python scripts/test_suite_generator.py e2e user-registration \
  --happy-path \
  --error-scenarios \
  --accessibility
```

**Generated Test Structure:**
```typescript
// UserProfile.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  // Setup and teardown
  beforeEach(() => {
    // Mock setup
  });

  describe('rendering', () => {
    it('renders user information correctly', () => {
      // Test implementation
    });

    it('displays loading state while fetching data', () => {
      // Test implementation
    });
  });

  describe('user interactions', () => {
    it('handles edit button click', async () => {
      // Test implementation
    });

    it('validates form input', async () => {
      // Test implementation
    });
  });

  describe('error handling', () => {
    it('displays error message on failed update', async () => {
      // Test implementation
    });
  });

  describe('accessibility', () => {
    it('has no accessibility violations', async () => {
      // Test implementation
    });
  });
});
```

### Coverage Analyzer

**Coverage Analysis:**
- Line coverage percentage
- Branch coverage percentage
- Function coverage percentage
- Statement coverage percentage
- Uncovered lines identification
- Coverage gaps by file/directory
- Coverage trend analysis
- Critical path coverage

**Coverage Reports:**
```bash
# Generate coverage report
python scripts/coverage_analyzer.py /path/to/project \
  --threshold 80 \
  --output coverage-report.html

# Analyze coverage gaps
python scripts/coverage_analyzer.py /path/to/project \
  --find-gaps \
  --prioritize critical

# Compare coverage over time
python scripts/coverage_analyzer.py /path/to/project \
  --compare-with baseline.json \
  --trend-analysis
```

**Coverage Metrics:**
```
COVERAGE ANALYSIS
=================

Overall Coverage: 76% (Target: 80%)
-----------------------------------

By Type:
  Unit Tests:        89% ✓
  Integration Tests: 72% ✗
  E2E Tests:         45% ✗

By Category:
  Statements: 78%
  Branches:   72%
  Functions:  81%
  Lines:      76%

Critical Gaps:
--------------
1. Authentication module: 54% (HIGH PRIORITY)
2. Payment processing: 62% (HIGH PRIORITY)
3. User registration flow: 68% (MEDIUM PRIORITY)
4. Admin dashboard: 43% (MEDIUM PRIORITY)

Files Needing Tests:
--------------------
  src/lib/payment.ts           (0% coverage)
  src/services/subscription.ts (34% coverage)
  src/components/Checkout.tsx  (45% coverage)
  src/api/webhooks.ts          (52% coverage)

Recommendations:
----------------
  Add integration tests for payment flow
  Add E2E tests for registration
  Add unit tests for payment utilities
  Add API tests for webhook handlers

Estimated Effort to 80%: 3-4 days
```

**Automated Coverage Improvements:**
- Identify untested code paths
- Generate missing test stubs
- Suggest test cases for uncovered branches
- Create test data for edge cases
- Generate mock configurations

### E2E Test Scaffolder

**E2E Testing Frameworks:**
- **Playwright** - Modern E2E testing (recommended)
- **Cypress** - Developer-friendly E2E testing
- **Puppeteer** - Headless browser automation
- **WebDriverIO** - Cross-browser testing

**E2E Test Features:**
```bash
# Set up Playwright
python scripts/e2e_test_scaffolder.py init \
  --framework playwright \
  --browsers chromium,firefox,webkit

# Generate E2E test suite
python scripts/e2e_test_scaffolder.py generate user-flows \
  --scenarios registration,login,checkout \
  --with-screenshots \
  --with-videos

# Generate visual regression tests
python scripts/e2e_test_scaffolder.py visual \
  --pages home,product,checkout \
  --viewports desktop,tablet,mobile

# Generate accessibility tests
python scripts/e2e_test_scaffolder.py accessibility \
  --standard wcag2.1-aa \
  --all-pages
```

**Generated E2E Test:**
```typescript
// tests/e2e/user-registration.spec.ts
import { test, expect } from '@playwright/test';

test.describe('User Registration Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/register');
  });

  test('successful registration with valid data', async ({ page }) => {
    // Fill registration form
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.fill('[name="confirmPassword"]', 'SecurePass123!');
    await page.check('[name="terms"]');

    // Submit form
    await page.click('button[type="submit"]');

    // Assert success
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('.welcome-message')).toContainText('Welcome');
  });

  test('shows validation errors for invalid email', async ({ page }) => {
    await page.fill('[name="email"]', 'invalid-email');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error-message')).toContainText(
      'Please enter a valid email'
    );
  });

  test('shows error for weak password', async ({ page }) => {
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', '123');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error-message')).toContainText(
      'Password must be at least 8 characters'
    );
  });

  test('handles server errors gracefully', async ({ page }) => {
    // Mock server error
    await page.route('**/api/register', (route) =>
      route.fulfill({
        status: 500,
        body: JSON.stringify({ error: 'Server error' }),
      })
    );

    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error-message')).toContainText(
      'Something went wrong'
    );
  });

  test('meets accessibility standards', async ({ page }) => {
    const accessibilityScanResults = await page.evaluate(() => {
      // Run axe-core accessibility checks
      return (window as any).axe.run();
    });

    expect(accessibilityScanResults.violations).toHaveLength(0);
  });
});
```

## How It Works

### Test Suite Generation Workflow

**Step 1: Analyze Codebase**
```bash
# Analyze project to find untested code
python scripts/test_suite_generator.py analyze /path/to/project \
  --output test-analysis.json
```

**Analysis Output:**
```
CODE ANALYSIS FOR TESTING
==========================

Total Files: 342
Files with Tests: 198 (58%)
Files without Tests: 144 (42%)

Priority Files Needing Tests:
------------------------------
[HIGH] src/lib/payment.ts (0 tests)
  - 8 functions, 245 lines
  - Critical: Payment processing
  - Complexity: High

[HIGH] src/services/auth.ts (0 tests)
  - 12 functions, 389 lines
  - Critical: Authentication
  - Complexity: Medium

[MEDIUM] src/components/Checkout.tsx (0 tests)
  - Complex component, 456 lines
  - User interaction heavy
  - Complexity: High

[MEDIUM] src/api/webhooks.ts (2 tests, 34% coverage)
  - 6 functions, 198 lines
  - Needs more test coverage
  - Complexity: Medium

Components Needing Tests: 45
API Endpoints Needing Tests: 23
Services Needing Tests: 12
Utils Needing Tests: 8
```

**Step 2: Generate Test Suites**
```bash
# Generate tests for specific file
python scripts/test_suite_generator.py generate \
  --file src/lib/payment.ts \
  --output src/lib/__tests__/payment.test.ts

# Generate tests for entire directory
python scripts/test_suite_generator.py generate \
  --directory src/components \
  --recursive

# Generate tests for untested files
python scripts/test_suite_generator.py generate \
  --untested-only \
  --priority high,medium
```

**Step 3: Review and Customize**
```typescript
// Generated test (src/lib/__tests__/payment.test.ts)
import { processPayment, validateCard, calculateTotal } from '../payment';

describe('Payment Processing', () => {
  describe('processPayment', () => {
    it('successfully processes valid payment', async () => {
      const payment = {
        amount: 100,
        currency: 'USD',
        paymentMethod: 'card',
        cardToken: 'tok_visa',
      };

      const result = await processPayment(payment);

      expect(result.success).toBe(true);
      expect(result.transactionId).toBeDefined();
    });

    it('rejects payment with invalid card', async () => {
      const payment = {
        amount: 100,
        currency: 'USD',
        paymentMethod: 'card',
        cardToken: 'invalid_token',
      };

      await expect(processPayment(payment)).rejects.toThrow('Invalid card');
    });

    it('handles network errors', async () => {
      // Mock network failure
      jest.spyOn(global, 'fetch').mockRejectedValueOnce(
        new Error('Network error')
      );

      const payment = {
        amount: 100,
        currency: 'USD',
        paymentMethod: 'card',
        cardToken: 'tok_visa',
      };

      await expect(processPayment(payment)).rejects.toThrow('Network error');
    });
  });

  describe('validateCard', () => {
    // Generated tests for validateCard
  });

  describe('calculateTotal', () => {
    // Generated tests for calculateTotal
  });
});
```

**Step 4: Run Tests and Measure Coverage**
```bash
# Run generated tests
npm test

# Generate coverage report
python scripts/coverage_analyzer.py /path/to/project \
  --include-new-tests \
  --output updated-coverage.html
```

### Coverage Analysis Workflow

**Step 1: Run Coverage Analysis**
```bash
# Comprehensive coverage analysis
python scripts/coverage_analyzer.py /path/to/project \
  --comprehensive \
  --threshold 80 \
  --output coverage-dashboard.html

# Focus on specific modules
python scripts/coverage_analyzer.py /path/to/project \
  --modules auth,payment,subscription \
  --detailed
```

**Step 2: Review Coverage Report**
```
DETAILED COVERAGE ANALYSIS
===========================

Project: my-saas-app
Date: 2025-11-13
Overall Coverage: 76.3%

Coverage by Module:
-------------------
authentication/     89.2% ✓ (Target: 80%)
user-management/    84.5% ✓ (Target: 80%)
payment/            62.1% ✗ (Target: 80%)
subscription/       71.4% ✗ (Target: 80%)
admin/              45.3% ✗ (Target: 80%)
api/                78.9% ✗ (Target: 80%)
utils/              91.2% ✓ (Target: 80%)

Critical Uncovered Paths:
--------------------------
1. Payment Error Handling (payment.ts:156-178)
   Risk: High - Payment failures not tested
   Lines: 23 uncovered
   Branches: 8 uncovered
   Impact: Critical business logic

2. Subscription Cancellation (subscription.ts:234-256)
   Risk: High - Refund logic not tested
   Lines: 23 uncovered
   Branches: 6 uncovered
   Impact: Financial risk

3. Admin User Creation (admin.ts:89-112)
   Risk: Medium - Privilege escalation not tested
   Lines: 24 uncovered
   Branches: 5 uncovered
   Impact: Security risk

4. Webhook Signature Verification (webhooks.ts:45-67)
   Risk: High - Security validation not tested
   Lines: 23 uncovered
   Branches: 4 uncovered
   Impact: Security risk

Recommended Actions:
--------------------
Priority 1: Add payment error handling tests (Est: 4 hours)
Priority 2: Add subscription cancellation tests (Est: 3 hours)
Priority 3: Add webhook security tests (Est: 2 hours)
Priority 4: Add admin function tests (Est: 3 hours)

Test Generation Suggestions:
-----------------------------
✓ 23 test cases generated for payment module
✓ 15 test cases generated for subscription module
✓ 12 test cases generated for webhook module
✓ 8 test cases generated for admin module

Total Effort to 80%: 12-15 hours
```

**Step 3: Generate Missing Tests**
```bash
# Auto-generate tests for uncovered code
python scripts/test_suite_generator.py \
  --from-coverage-report coverage-dashboard.html \
  --priority critical,high \
  --output-directory src/__tests__/generated/
```

**Step 4: Track Coverage Over Time**
```bash
# Track coverage trends
python scripts/coverage_analyzer.py /path/to/project \
  --track-history \
  --compare-with baseline.json \
  --output coverage-trends.html
```

### E2E Testing Workflow

**Step 1: Initialize E2E Testing**
```bash
# Set up Playwright
python scripts/e2e_test_scaffolder.py init \
  --framework playwright \
  --browsers chromium,firefox,webkit \
  --config playwright.config.ts

# Install dependencies
npm install -D @playwright/test
npx playwright install
```

**Step 2: Generate E2E Test Suites**
```bash
# Generate tests for critical user flows
python scripts/e2e_test_scaffolder.py generate \
  --flows "user-registration,login,checkout,subscription" \
  --with-screenshots \
  --with-videos

# Generate visual regression tests
python scripts/e2e_test_scaffolder.py visual \
  --pages home,product,pricing,checkout \
  --viewports "1920x1080,1366x768,768x1024,375x667"

# Generate accessibility tests
python scripts/e2e_test_scaffolder.py accessibility \
  --standard wcag2.1-aa \
  --pages all
```

**Step 3: Run E2E Tests**
```bash
# Run all E2E tests
npx playwright test

# Run specific test suite
npx playwright test user-registration

# Run in headed mode for debugging
npx playwright test --headed --debug

# Run with UI mode
npx playwright test --ui

# Run on specific browser
npx playwright test --project=chromium
```

**Step 4: Review E2E Test Results**
```
PLAYWRIGHT TEST RESULTS
========================

Total Tests: 48
Passed: 43 (90%)
Failed: 3 (6%)
Skipped: 2 (4%)

Failed Tests:
-------------
1. user-registration.spec.ts:45
   "handles server errors gracefully"
   Error: Timeout waiting for error message
   Screenshot: test-results/user-registration-failed.png
   Video: test-results/user-registration-failed.webm

2. checkout.spec.ts:89
   "processes payment successfully"
   Error: Payment button not clickable
   Screenshot: test-results/checkout-failed.png

3. subscription.spec.ts:123
   "upgrades subscription plan"
   Error: Plan selection not updating
   Screenshot: test-results/subscription-failed.png

Visual Regression:
------------------
✓ Homepage: No changes detected
✗ Product Page: 2 visual differences detected
  - Header layout shifted 5px
  - Button color changed
✓ Checkout Page: No changes detected

Accessibility:
--------------
✓ Homepage: No violations (WCAG 2.1 AA)
✗ Product Page: 2 violations
  - Missing alt text on product image
  - Insufficient color contrast on price
✓ Checkout Page: No violations (WCAG 2.1 AA)

Performance:
------------
Homepage: 1.2s (Good)
Product Page: 2.4s (Needs improvement)
Checkout Page: 1.8s (Good)

Test Duration: 4m 32s
```

## Technical Details

### Testing Pyramid

```
        /\
       /  \      E2E Tests (10%)
      /____\     - User flows
     /      \    - Integration across systems
    /________\
   /          \  Integration Tests (30%)
  /____________\ - API endpoints
 /              \- Service interactions
/________________\
    Unit Tests (60%)
    - Functions
    - Components
    - Business logic
```

### Jest Configuration

```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.test.ts?(x)'],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.tsx',
    '!src/types/**/*',
  ],
  coverageThresholds: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
};
```

### Playwright Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results.json' }],
    ['junit', { outputFile: 'test-results.xml' }],
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 13'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### Test Data Factories

```typescript
// tests/factories/user.factory.ts
import { faker } from '@faker-js/faker';

export const createUser = (overrides = {}) => ({
  id: faker.string.uuid(),
  email: faker.internet.email(),
  name: faker.person.fullName(),
  role: 'user',
  createdAt: faker.date.past(),
  ...overrides,
});

export const createUsers = (count: number) =>
  Array.from({ length: count }, () => createUser());

// Usage in tests
import { createUser } from '@/tests/factories/user.factory';

test('displays user profile', () => {
  const user = createUser({ name: 'John Doe' });
  render(<UserProfile user={user} />);
  expect(screen.getByText('John Doe')).toBeInTheDocument();
});
```

## Use Cases and Examples

### Testing Authentication Flow

**Scenario:** Comprehensive testing of authentication module

**Unit Tests:**
```typescript
// src/services/__tests__/auth.service.test.ts
describe('AuthService', () => {
  describe('login', () => {
    it('returns token for valid credentials', async () => {
      const result = await authService.login('user@example.com', 'password');
      expect(result).toHaveProperty('token');
      expect(result).toHaveProperty('refreshToken');
    });

    it('throws error for invalid credentials', async () => {
      await expect(
        authService.login('user@example.com', 'wrong')
      ).rejects.toThrow('Invalid credentials');
    });
  });
});
```

**Integration Tests:**
```typescript
// src/api/__tests__/auth.api.test.ts
describe('POST /api/auth/login', () => {
  it('returns 200 with valid credentials', async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({ email: 'user@example.com', password: 'password' });

    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('token');
  });

  it('returns 401 with invalid credentials', async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({ email: 'user@example.com', password: 'wrong' });

    expect(response.status).toBe(401);
  });
});
```

**E2E Tests:**
```typescript
// tests/e2e/auth.spec.ts
test('user can login successfully', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'user@example.com');
  await page.fill('[name="password"]', 'password');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('/dashboard');
});
```

### Performance Testing with Playwright

```typescript
// tests/e2e/performance.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Performance Tests', () => {
  test('homepage loads within 2 seconds', async ({ page }) => {
    const startTime = Date.now();
    await page.goto('/');
    const loadTime = Date.now() - startTime;

    expect(loadTime).toBeLessThan(2000);
  });

  test('measures Core Web Vitals', async ({ page }) => {
    await page.goto('/');

    const webVitals = await page.evaluate(() => {
      return new Promise((resolve) => {
        new PerformanceObserver((list) => {
          const entries = list.getEntries();
          resolve({
            LCP: entries.find((e) => e.entryType === 'largest-contentful-paint'),
            FID: entries.find((e) => e.entryType === 'first-input'),
            CLS: entries.find((e) => e.entryType === 'layout-shift'),
          });
        }).observe({ entryTypes: ['paint', 'first-input', 'layout-shift'] });
      });
    });

    expect(webVitals.LCP).toBeLessThan(2500); // Good LCP
  });
});
```

## Best Practices

### Test Writing Best Practices

**Do:**
- Follow Arrange-Act-Assert (AAA) pattern
- Write descriptive test names
- Test one thing per test
- Use factories for test data
- Mock external dependencies
- Clean up after tests
- Test edge cases and error scenarios
- Keep tests independent

**Don't:**
- Test implementation details
- Write flaky tests
- Share state between tests
- Over-mock (test doubles should be minimal)
- Skip cleanup
- Test library code
- Ignore failing tests

### Coverage Best Practices

**Do:**
- Aim for 80%+ coverage
- Focus on critical paths first
- Test edge cases and error handling
- Track coverage trends
- Set coverage thresholds in CI
- Review coverage reports regularly

**Don't:**
- Chase 100% coverage
- Write tests just for coverage
- Ignore coverage gaps in critical code
- Test getters/setters only
- Skip integration tests

### E2E Testing Best Practices

**Do:**
- Test critical user flows
- Use data-testid attributes
- Run tests in CI/CD
- Capture screenshots and videos on failure
- Test across browsers
- Implement retry logic
- Use page object pattern
- Test accessibility

**Don't:**
- Test everything with E2E (use unit/integration tests)
- Use brittle selectors (CSS classes, deep selectors)
- Hardcode delays (use waitFor)
- Skip mobile testing
- Ignore visual regressions

## Integration Points

This skill integrates with:
- **Testing Frameworks:** Jest, Vitest, Mocha, Playwright, Cypress
- **Testing Libraries:** React Testing Library, Testing Library, Supertest
- **Coverage Tools:** Istanbul, c8, NYC
- **CI/CD:** GitHub Actions, GitLab CI, Jenkins, CircleCI
- **Monitoring:** Sentry, DataDog, New Relic (error tracking)
- **Code Quality:** SonarQube, CodeClimate
- **Visual Testing:** Percy, Chromatic, BackstopJS
- **Performance:** Lighthouse, WebPageTest

## Common Challenges and Solutions

### Challenge: Flaky E2E Tests
**Solution:** Use proper wait conditions, avoid fixed timeouts, use retry logic, mock external services, ensure test data isolation, run tests in parallel carefully, use unique test data identifiers

### Challenge: Slow Test Suite
**Solution:** Run tests in parallel, use test sharding, optimize test setup/teardown, use test fixtures, mock expensive operations, profile test execution, skip E2E for unit-testable code

### Challenge: Low Test Coverage
**Solution:** Set coverage thresholds in CI, use coverage analyzer to find gaps, generate missing tests automatically, prioritize critical paths, make testing part of definition of done

### Challenge: Maintaining Test Data
**Solution:** Use test data factories, implement database seeding, use in-memory databases for unit tests, clean up test data after runs, use test data generation tools

### Challenge: Testing Async Code
**Solution:** Use async/await, use waitFor utilities, mock timers, test loading and error states, ensure proper cleanup, avoid race conditions

### Challenge: Integration Test Complexity
**Solution:** Use test containers for databases, implement test fixtures, use API mocking (MSW), separate integration and E2E tests, keep tests focused and isolated
