---
description: Verify tests use real infrastructure. NO MOCKING policy for integration and E2E tests.
---

# /real-testing - Real Infrastructure Testing

Verify that integration and E2E tests use real services, not mocks.

## NO MOCKING Policy

| Test Tier | Mocking Policy | Infrastructure |
|-----------|---------------|----------------|
| **Tier 1: Unit** | ✅ ALLOWED | In-memory, mocked |
| **Tier 2: Integration** | ❌ NO MOCKING | Real Docker services |
| **Tier 3: E2E** | ❌ NO MOCKING | Real infrastructure |

## Why NO MOCKING?

1. Mocks hide real integration issues
2. Real infrastructure catches actual bugs
3. Production-like testing prevents surprises
4. Better confidence in deployments

## Validation Checklist

Check for mock usage in integration/E2E tests:

```bash
# Python - find mocking in integration tests
grep -r "@patch" tests/integration/
grep -r "Mock(" tests/integration/
grep -r "MagicMock" tests/e2e/

# JavaScript - find mocking in integration tests
grep -r "jest.mock" tests/integration/
grep -r "vi.mock" tests/integration/
```

## Correct Patterns

```python
# ✅ CORRECT: Real database in integration test
@pytest.mark.requires_docker
def test_database_integration():
    conn = get_real_database_connection()
    result = conn.execute("SELECT 1")
    assert result is not None
```

```typescript
// ✅ CORRECT: Real API in integration test
test('api integration', async () => {
  const response = await fetch('http://localhost:3001/api/data');
  expect(response.ok).toBe(true);
});
```

## Execution

When running /real-testing:

1. Scan integration and E2E test files
2. Identify any mock usage
3. Flag violations of NO MOCKING policy
4. Suggest refactoring to use real services
5. Verify Docker test infrastructure exists

## Agent Escalation

This command automatically escalates to specialized agents when:

| Condition | Agent | Purpose |
|-----------|-------|---------|
| Testing policy violations | **gold-standards-validator** | Enforce NO MOCKING policy |
| Infrastructure setup | **deployment-specialist** | Docker test environment configuration |
| Test refactoring needed | **tdd-guide** | Convert mocked tests to real infrastructure |

### Escalation Triggers
- **gold-standards-validator**: Use for comprehensive testing policy audit
- **deployment-specialist**: Use to set up Docker test infrastructure
- **tdd-guide**: Use to refactor tests to use real services
