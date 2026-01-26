# Code Review

Comprehensive security and quality review supporting multiple modes:
- **Default**: Review uncommitted local changes
- **PR Mode**: Review a GitHub pull request
- **Issue Fix Mode**: Analyze and fix a GitHub issue

## Usage

```bash
/code-review              # Review local uncommitted changes
/code-review #123         # Review GitHub PR #123
/code-review fix #42      # Analyze and fix GitHub issue #42
/code-review https://github.com/owner/repo/pull/123  # Review PR by URL
```

---

## Mode 1: Local Changes (Default)

Review uncommitted changes in the working directory.

### Process

1. Get changed files: `git diff --name-only HEAD`

2. For each changed file, check for:

**Security Issues (CRITICAL):**
- Hardcoded credentials, API keys, tokens
- SQL injection vulnerabilities
- XSS vulnerabilities
- Missing input validation
- Insecure dependencies
- Path traversal risks

**Code Quality (HIGH):**
- Functions > 50 lines
- Files > 800 lines
- Nesting depth > 4 levels
- Missing error handling
- console.log statements
- TODO/FIXME comments
- Missing JSDoc for public APIs

**Best Practices (MEDIUM):**
- Mutation patterns (use immutable instead)
- Emoji usage in code/comments
- Missing tests for new code
- Accessibility issues (a11y)

3. Generate report with:
   - Severity: CRITICAL, HIGH, MEDIUM, LOW
   - File location and line numbers
   - Issue description
   - Suggested fix

4. Block commit if CRITICAL or HIGH issues found

Never approve code with security vulnerabilities!

---

## Mode 2: GitHub PR Review

When run with a PR number or URL: `/code-review #123`

### Process

1. **Fetch PR Details**
   ```bash
   gh pr view 123 --json title,body,author,files,additions,deletions
   gh pr diff 123
   ```

2. **Parallel Analysis**
   - Code quality check (apply local review standards)
   - Security scan (escalate to security-auditor)
   - Standards compliance (escalate to gold-standards-validator)

3. **Review Categories**
   - **Architecture**: Design decisions, patterns used
   - **Security**: Vulnerability scan of changed code
   - **Testing**: Adequate test coverage for changes
   - **Documentation**: Updated docs for new features

4. **Generate Review Summary**
   ```markdown
   ## PR Review: #123 - [Title]

   ### Overview
   - Files changed: X
   - Lines: +Y / -Z

   ### Findings
   | Severity | Count | Category |
   |----------|-------|----------|
   | Critical | 0     | Security |
   | High     | 2     | Quality  |

   ### Recommendation
   [ ] Approve  [ ] Request Changes  [ ] Comment
   ```

5. **Optional: Post to GitHub**
   ```bash
   gh pr review 123 --comment --body "Review summary..."
   ```

---

## Mode 3: GitHub Issue Fix

When run with fix keyword: `/code-review fix #42`

### Process

1. **Fetch Issue Details**
   ```bash
   gh issue view 42 --json title,body,labels,comments
   ```

2. **Requirements Analysis**
   - Parse issue description for requirements
   - Identify affected files from context
   - Determine scope (bug fix, feature, refactor)

3. **Plan Fix** (Internal /plan invocation)
   - Design implementation approach
   - Identify test requirements
   - Estimate change scope

4. **Implement with TDD** (Internal /tdd invocation)
   - Write failing tests first
   - Implement minimal fix
   - Verify tests pass

5. **Verification**
   - Run full test suite
   - Check for regressions
   - Validate fix addresses issue

6. **Create PR**
   ```bash
   git checkout -b fix/issue-42-description
   git add .
   git commit -m "fix: [description]

   Fixes #42"
   gh pr create --title "Fix: [Issue Title]" --body "..."
   ```

---

## Agent Escalation

This command automatically escalates to specialized agents when:

| Condition | Agent | Purpose |
|-----------|-------|---------|
| Pattern compliance needed | **gold-standards-validator** | SDK patterns, coding standards enforcement |
| Complex codebase audit | **gold-standards-validator** | Full repository compliance scan |
| Security-critical code | **security-auditor** | Deep vulnerability analysis, OWASP Top 10 |
| PR from GitHub | **gh-manager** | GitHub API integration, PR management |
| Issue resolution (fix mode) | **requirements-analyst** | Issue analysis, requirement extraction |

### Escalation Triggers
- **gold-standards-validator**: Use for SDK compliance, import patterns, node development standards
- **security-auditor**: Use for auth, payments, PII handling, or external API integrations
- **gh-manager**: Use for GitHub PR/issue operations requiring API access
- **requirements-analyst**: Use for complex issue analysis requiring requirement breakdown
