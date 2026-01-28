---
description: Comprehensive test-driven development - unit, integration, E2E, coverage analysis, and quality checks.
ecc_base_version: "5230892"
last_synced: "2026-01-27"
customizations: "Consolidated: e2e, test-coverage, real-testing, no-stubs into single command"
---

# /tdd - Test-Driven Development

Comprehensive testing command covering the full TDD workflow plus E2E, coverage, and quality validation.

## Usage

```bash
/tdd                    # Interactive TDD workflow (default)
/tdd unit               # Focus on unit tests
/tdd integration        # Integration tests (enforces NO MOCKING)
/tdd e2e                # E2E tests with Playwright
/tdd coverage           # Analyze gaps + generate missing tests
/tdd --full             # Complete: all test types + coverage + no-stubs check
```

## What This Command Does

### Default Mode (Interactive TDD)
1. **Scaffold Interfaces** - Define types/interfaces first
2. **Generate Tests First** - Write failing tests (RED)
3. **Implement Minimal Code** - Write just enough to pass (GREEN)
4. **Refactor** - Improve code while keeping tests green (REFACTOR)
5. **Verify Coverage** - Ensure 80%+ test coverage
6. **No-Stubs Check** - Verify no placeholder content

### Mode: `unit`
Focus on function-level unit tests:
- Happy path scenarios
- Edge cases (empty, null, max values)
- Error conditions
- Boundary values

### Mode: `integration`
Integration tests with **NO MOCKING** policy:
- API endpoints with real services
- Database operations with real DB
- External service calls
- Component integration

**NO MOCKING Policy:**
| Test Tier | Mocking Allowed? | Infrastructure |
|-----------|------------------|----------------|
| Unit | Yes | In-memory, mocked |
| Integration | **NO** | Real Docker services |
| E2E | **NO** | Real infrastructure |

### Mode: `e2e`
End-to-end tests with Playwright:
- Generate test journeys for user flows
- Run tests across browsers (Chrome, Firefox, Safari)
- Capture artifacts (screenshots, videos, traces)
- Page Object Model pattern

### Mode: `coverage`
Analyze and improve test coverage:
1. Run tests with coverage report
2. Identify files below 80% threshold
3. Generate missing tests for uncovered paths
4. Show before/after metrics

### Flag: `--full`
Runs everything:
1. Unit tests
2. Integration tests (NO MOCKING enforced)
3. E2E tests
4. Coverage analysis
5. No-stubs validation

---

## TDD Cycle

```
RED → GREEN → REFACTOR → VERIFY

RED:      Write a failing test
GREEN:    Write minimal code to pass
REFACTOR: Improve code, keep tests passing
VERIFY:   Check coverage + no stubs
```

---

## Example: Unit Test (Default)

```
/tdd I need a function to calculate market liquidity score

Agent (tdd-guide):
## Step 1: Define Interface (SCAFFOLD)
interface MarketData { ... }
function calculateLiquidityScore(market: MarketData): number

## Step 2: Write Failing Test (RED)
describe('calculateLiquidityScore', () => {
  it('should return high score for liquid market', () => { ... })
  it('should return low score for illiquid market', () => { ... })
})

## Step 3: Run Tests - Verify FAIL
npm test → FAIL (Not implemented)

## Step 4: Implement (GREEN)
export function calculateLiquidityScore(market: MarketData): number { ... }

## Step 5: Run Tests - Verify PASS
npm test → PASS (3 tests)

## Step 6: Refactor
Extract constants, improve readability

## Step 7: Coverage Check
Coverage: 100% ✅
```

---

## Example: E2E Test

```
/tdd e2e Test the market search and view flow

Agent (e2e-runner):
## Test Scenario
User Journey: Market Search → View Results → Click Market → View Details

## Generated Test (Page Object Model)
// tests/e2e/markets/search-and-view.spec.ts
test('user can search markets and view details', async ({ page }) => {
  const marketsPage = new MarketsPage(page)
  await marketsPage.goto()
  await marketsPage.searchMarkets('election')
  await expect(marketsPage.marketCards.first()).toBeVisible()
  // ...
})

## Run Tests
npx playwright test → 3 passed (9.1s)

## Artifacts
- Screenshots: artifacts/search-results.png
- HTML Report: playwright-report/index.html
```

---

## Example: Coverage Analysis

```
/tdd coverage

Agent:
## Current Coverage
File           | Stmts | Branch | Funcs | Lines
---------------|-------|--------|-------|------
lib/utils.ts   |  45%  |  30%   |  50%  |  45%  ❌
lib/api.ts     |  82%  |  78%   |  90%  |  82%  ✅

## Generating Missing Tests for lib/utils.ts
- formatCurrency: 3 new tests
- parseDate: 2 new tests
- validateInput: 4 new tests

## After Coverage
lib/utils.ts   |  92%  |  88%   |  95%  |  92%  ✅

Overall: 45% → 87% ✅
```

---

## NO MOCKING Policy (Integration/E2E)

**Why NO MOCKING?**
1. Mocks hide real integration issues
2. Real infrastructure catches actual bugs
3. Production-like testing prevents surprises

**Validation:**
```bash
# These patterns are FORBIDDEN in integration/E2E tests:
grep -r "jest.mock" tests/integration/    # ❌
grep -r "vi.mock" tests/integration/      # ❌
grep -r "@patch" tests/integration/       # ❌ (Python)
```

**Correct Pattern:**
```typescript
// ✅ CORRECT: Real API in integration test
test('api integration', async () => {
  const response = await fetch('http://localhost:3001/api/data');
  expect(response.ok).toBe(true);
});
```

---

## No-Stubs Validation

Automatically checked at end of TDD workflow:

**Forbidden Patterns:**
| Category | Forbidden |
|----------|-----------|
| UI | Lorem ipsum, "Coming soon", "TBD", empty pages |
| Code | `pass` without impl, `// TODO:`, empty functions |
| Errors | `throw new Error("Not implemented")` |

**The Rule:** If a feature isn't ready, don't include it at all.

---

## Coverage Requirements

- **80% minimum** for all code
- **100% required** for:
  - Financial calculations
  - Authentication logic
  - Security-critical code
  - Core business logic

---

## Best Practices

**DO:**
- Write the test FIRST, before any implementation
- Run tests and verify they FAIL before implementing
- Write minimal code to make tests pass
- Use Page Object Model for E2E tests
- Use data-testid attributes for selectors
- Aim for 80%+ coverage

**DON'T:**
- Write implementation before tests
- Mock in integration/E2E tests
- Test implementation details (test behavior)
- Use brittle CSS selectors
- Ignore flaky tests
- Leave placeholder content

---

## Quick Commands

```bash
# Unit tests
npm test
npm test -- --coverage

# E2E tests
npx playwright test
npx playwright test --headed
npx playwright test --debug
npx playwright show-report

# Coverage
npm test -- --coverage
```

---

## Agent Escalation

| Condition | Agent | Purpose |
|-----------|-------|---------|
| Progress review | **intermediate-reviewer** | Milestone validation |
| React/Next.js testing | **ui-engineer** | React 19 testing patterns |
| Flutter testing | **flutter-specialist** | Widget/integration tests |
| NO MOCKING violations | **gold-standards-validator** | Policy enforcement |
| Test infrastructure | **deployment-specialist** | Docker test environment |
| Documentation stubs | **documentation-validator** | Doc completeness |

---

## Related Commands

- `/design` - Plan what to build before TDD
- `/verify` - Run full verification after TDD
- `/code-review` - Review implementation quality
- `/build-fix` - Fix build errors if they occur