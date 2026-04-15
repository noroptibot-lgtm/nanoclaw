# Code Review (Code Reviewer)

## Overview

The Code Review skill provides comprehensive frameworks and best practices for conducting effective code reviews that improve code quality, share knowledge, and maintain high engineering standards. This skill enables reviewers to systematically evaluate code for correctness, security, performance, maintainability, and adherence to best practices. It combines automated static analysis, manual review checklists, and constructive feedback techniques with deep expertise in code quality principles and team collaboration.

## Who Should Use This Skill

- **Code Reviewers** conducting systematic code reviews
- **Senior Engineers** mentoring through code review
- **Tech Leads** maintaining code quality standards
- **Team Leads** establishing review processes
- **Staff Engineers** defining code quality guidelines
- **All Engineers** participating in peer reviews
- **Open Source Maintainers** reviewing contributions
- **Engineering Managers** ensuring review quality

## Purpose and Use Cases

Use this skill when you need to:
- Conduct thorough code reviews
- Establish code review standards
- Review pull requests systematically
- Provide constructive feedback
- Identify code quality issues
- Ensure security best practices
- Evaluate performance implications
- Verify test coverage
- Check for maintainability
- Review API designs
- Evaluate architectural decisions
- Mentor junior developers through reviews

**Keywords that trigger this skill:** code review, pull request, PR review, code quality, review checklist, feedback, refactoring, best practices, code standards, peer review

## What's Included

### Automated Code Review Tools

**Static Analysis:**
- **Linters** - ESLint, Pylint, RuboCop, Checkstyle
- **Type Checkers** - TypeScript, mypy, Flow
- **Security Scanners** - Snyk, SonarQube, Bandit
- **Code Quality** - CodeClimate, SonarQube, Code Factor
- **Complexity Analysis** - Cyclomatic complexity, cognitive complexity
- **Dependency Audit** - npm audit, safety, OWASP Dependency Check
- **Style Checkers** - Prettier, Black, gofmt
- **Test Coverage** - Coverage.py, Istanbul, JaCoCo

**Integration Features:**
```bash
# Run comprehensive code review checks
python scripts/code_reviewer.py review \
  --pr-number 123 \
  --checks lint,security,complexity,coverage \
  --auto-comment

# Generate review report
python scripts/code_reviewer.py analyze \
  --files src/**/*.py \
  --output review-report.html \
  --format html

# Check against style guide
python scripts/code_reviewer.py style-check \
  --guide google-python-style \
  --auto-fix

# Security audit
python scripts/code_reviewer.py security-audit \
  --severity high,critical \
  --report-format json
```

**Automated Review Configuration:**
```yaml
# .code-review.yaml
automated_checks:
  linting:
    enabled: true
    tools:
      - eslint
      - pylint
    fail_on_warnings: false
    auto_fix: true

  type_checking:
    enabled: true
    strict_mode: true

  security:
    enabled: true
    tools:
      - snyk
      - bandit
    severity_threshold: high
    block_on_vulnerabilities: true

  complexity:
    enabled: true
    max_cyclomatic_complexity: 10
    max_cognitive_complexity: 15
    max_function_length: 50
    max_file_length: 500

  test_coverage:
    enabled: true
    minimum_coverage: 80
    fail_below_threshold: true
    exclude_patterns:
      - "**/tests/**"
      - "**/mocks/**"

  performance:
    enabled: true
    checks:
      - n_plus_one_queries
      - inefficient_loops
      - memory_leaks

  dependencies:
    enabled: true
    check_vulnerabilities: true
    check_licenses: true
    check_outdated: true

pr_rules:
  require_approval_count: 2
  require_tests: true
  require_documentation: true
  max_files_changed: 50
  max_lines_changed: 500
  block_keywords:
    - "TODO"
    - "FIXME"
    - "console.log"
    - "debugger"

notifications:
  slack_webhook: ${SLACK_WEBHOOK_URL}
  notify_on:
    - security_issue
    - coverage_drop
    - large_pr
```

### Code Review Checklists

**Comprehensive Review Checklist:**
```markdown
# Code Review Checklist

## Functionality
- [ ] Code implements the stated requirements
- [ ] Edge cases are handled correctly
- [ ] Error handling is appropriate
- [ ] Input validation is implemented
- [ ] Business logic is correct
- [ ] No obvious bugs or logical errors

## Code Quality
- [ ] Code is readable and self-documenting
- [ ] Variable and function names are clear and descriptive
- [ ] Functions are small and focused (single responsibility)
- [ ] Code follows DRY principle (Don't Repeat Yourself)
- [ ] No unnecessary complexity
- [ ] Appropriate use of comments (why, not what)
- [ ] No commented-out code
- [ ] No debug statements (console.log, print, etc.)

## Design & Architecture
- [ ] Code follows established patterns and conventions
- [ ] Appropriate design patterns are used
- [ ] Separation of concerns is maintained
- [ ] Dependencies are properly managed
- [ ] Code is modular and reusable
- [ ] No circular dependencies
- [ ] Appropriate abstraction level
- [ ] Follows SOLID principles

## Performance
- [ ] No obvious performance issues
- [ ] Algorithms are efficient (appropriate time complexity)
- [ ] Database queries are optimized (no N+1 queries)
- [ ] Appropriate use of caching
- [ ] No memory leaks
- [ ] Lazy loading where appropriate
- [ ] Batch operations used for bulk data

## Security
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Input is properly sanitized and validated
- [ ] Sensitive data is encrypted
- [ ] Authentication and authorization are correct
- [ ] No hardcoded secrets or credentials
- [ ] Proper error messages (no sensitive info leaked)
- [ ] CSRF protection where needed
- [ ] Rate limiting implemented for APIs

## Testing
- [ ] Tests are included and pass
- [ ] Test coverage is adequate (>80%)
- [ ] Tests are meaningful and test the right things
- [ ] Edge cases are tested
- [ ] Error conditions are tested
- [ ] Integration tests where appropriate
- [ ] Tests are maintainable and readable
- [ ] No flaky tests

## Documentation
- [ ] Code is self-documenting or has adequate comments
- [ ] Public APIs are documented
- [ ] Complex logic is explained
- [ ] README is updated if needed
- [ ] API documentation is updated
- [ ] Architecture decisions are documented (ADR)
- [ ] Migration guides if breaking changes

## Error Handling
- [ ] Errors are caught and handled appropriately
- [ ] Error messages are clear and actionable
- [ ] Logging is appropriate (level and content)
- [ ] No swallowing of exceptions
- [ ] Graceful degradation where appropriate
- [ ] Retry logic for transient failures

## Database & Data
- [ ] Database migrations are included if needed
- [ ] Indexes are added where appropriate
- [ ] Data validation is implemented
- [ ] Transactions are used correctly
- [ ] Database schema changes are backward compatible
- [ ] No data loss scenarios

## API Design (if applicable)
- [ ] RESTful principles followed
- [ ] Appropriate HTTP methods used
- [ ] Proper status codes returned
- [ ] API versioning considered
- [ ] Request/response formats are consistent
- [ ] Pagination implemented for lists
- [ ] Rate limiting considered

## Frontend (if applicable)
- [ ] UI is responsive
- [ ] Accessibility standards met (WCAG)
- [ ] Browser compatibility considered
- [ ] No console errors or warnings
- [ ] Loading states handled
- [ ] Error states handled
- [ ] Proper use of React/Vue best practices

## DevOps & Deployment
- [ ] CI/CD pipeline passes
- [ ] Deployment strategy is clear
- [ ] Configuration is externalized
- [ ] Secrets are not in code
- [ ] Monitoring and alerting considered
- [ ] Rollback strategy exists

## General
- [ ] PR description is clear and complete
- [ ] Linked to relevant issue/ticket
- [ ] Breaking changes are documented
- [ ] No unrelated changes included
- [ ] Reasonable PR size (not too large)
- [ ] Follows team conventions and style guide
```

**Language-Specific Checklists:**

```python
# Python-Specific Review Checklist

## Python Best Practices
- [ ] Follows PEP 8 style guide
- [ ] Uses type hints (Python 3.6+)
- [ ] Appropriate use of list comprehensions
- [ ] Context managers used for resource management
- [ ] Generators used for large datasets
- [ ] No mutable default arguments
- [ ] Proper exception hierarchy
- [ ] Uses f-strings for formatting (Python 3.6+)
- [ ] No bare except clauses
- [ ] Imports are organized (stdlib, third-party, local)

## Python-Specific Security
- [ ] Uses parameterized queries (no string interpolation in SQL)
- [ ] Pickle only trusted data
- [ ] Validates user input
- [ ] Uses secrets module for cryptography
- [ ] No eval() or exec() on user input

## Python Performance
- [ ] Appropriate data structures (set for membership, dict for lookups)
- [ ] No quadratic algorithms on large data
- [ ] Uses builtin functions (sum, min, max, etc.)
- [ ] Appropriate use of __slots__ for large classes
- [ ] No unnecessary object creation in loops
```

```javascript
# JavaScript/TypeScript Review Checklist

## JavaScript Best Practices
- [ ] Uses const/let instead of var
- [ ] Async/await used appropriately
- [ ] Promises handled correctly (no unhandled rejections)
- [ ] Arrow functions used appropriately
- [ ] Destructuring used where appropriate
- [ ] Spread operator used appropriately
- [ ] No == comparisons (use ===)
- [ ] No implicit type coercion
- [ ] Proper error boundaries (React)

## TypeScript-Specific
- [ ] Proper type annotations
- [ ] No 'any' types (or justified)
- [ ] Interfaces/types are well-defined
- [ ] Generic types used appropriately
- [ ] Enums vs unions considered
- [ ] Strict mode enabled

## JavaScript Security
- [ ] No eval() or Function constructor
- [ ] XSS prevention (sanitize user input)
- [ ] CSRF tokens used
- [ ] Secure cookie settings
- [ ] Content Security Policy considered

## React-Specific
- [ ] Proper use of hooks (rules of hooks)
- [ ] No unnecessary re-renders
- [ ] Keys used in lists
- [ ] Prop types or TypeScript
- [ ] Component composition over inheritance
- [ ] Appropriate state management
```

### Review Feedback Framework

**Feedback Categories:**
```markdown
# Feedback Severity Levels

## 🔴 Critical (Must Fix)
Issues that:
- Break functionality
- Introduce security vulnerabilities
- Cause data loss or corruption
- Violate critical requirements
- Create production incidents

Example: "🔴 SQL injection vulnerability: User input is concatenated directly into query"

## 🟠 Major (Should Fix)
Issues that:
- Significantly impact code quality
- Create maintenance burden
- Poor performance
- Violate important design principles
- Missing critical tests

Example: "🟠 This function has cyclomatic complexity of 25. Consider breaking it into smaller functions."

## 🟡 Minor (Consider Fixing)
Issues that:
- Style inconsistencies
- Minor improvements possible
- Opportunities for simplification
- Better alternatives exist

Example: "🟡 Consider using a list comprehension here for better readability"

## 🟢 Suggestion (Optional)
Ideas that:
- Share knowledge
- Offer alternatives
- Improvements with tradeoffs
- Personal preferences

Example: "🟢 You might also consider using the strategy pattern here, though the current approach works fine"

## 💡 Praise (Positive Feedback)
Highlight:
- Excellent code
- Clever solutions
- Good practices
- Learning opportunities for others

Example: "💡 Nice use of the decorator pattern! This makes the code much more maintainable."

## ❓ Question (Needs Clarification)
When you:
- Don't understand something
- Want to learn the reasoning
- Need more context

Example: "❓ Can you explain why you chose this approach over X?"
```

**Constructive Feedback Examples:**

```markdown
# Bad Feedback vs Good Feedback

## ❌ Bad: "This code is terrible"
✅ Good: "🟠 This function is doing too many things. Consider splitting it into separate functions for parsing, validation, and transformation. This will make it easier to test and maintain."

## ❌ Bad: "You should use X instead"
✅ Good: "🟡 Have you considered using X here? It might simplify this logic and improve readability. Here's an example: [code snippet]"

## ❌ Bad: "Why didn't you add tests?"
✅ Good: "🔴 This change modifies critical payment logic but doesn't include tests. Could you add unit tests covering success case, failure case, and edge cases like zero amounts?"

## ❌ Bad: "This won't scale"
✅ Good: "🟠 This O(n²) algorithm could be problematic with large datasets. For 10,000 items, this could take several seconds. Consider using a hash map lookup instead, which would be O(n). Here's a quick implementation: [code snippet]"

## ❌ Bad: "Not following conventions"
✅ Good: "🟡 Our team convention is to use camelCase for variable names (see style-guide.md). Could you rename user_data to userData for consistency?"

## ❌ Bad: "This is wrong"
✅ Good: "❓ I'm seeing this function returns null in some cases, but the callers don't seem to handle it. Am I missing something, or should we add null checks?"
```

**Review Response Templates:**
```markdown
# General Approval
"""
✅ LGTM! Code looks good.

Key strengths:
- Clear and well-structured code
- Comprehensive test coverage (95%)
- Good error handling
- Clear documentation

Minor suggestions:
- Consider extracting the validation logic to a separate function for reusability
- Could add a comment explaining the retry logic

Great work! 💡
"""

# Approval with Minor Changes
"""
✅ Approving with minor suggestions.

Code is solid overall. A few small things to consider:

🟡 Line 45: Consider using Promise.all() here instead of sequential awaits for better performance
🟡 Line 78: This variable name could be more descriptive
💡 Line 102: Nice pattern! I'll use this approach in my code too.

Feel free to merge as-is or incorporate these suggestions. Up to you!
"""

# Request Changes
"""
🔴 Requesting changes before merge.

Overall approach looks good, but there are a few critical issues:

🔴 Line 34: Security issue - user input needs to be sanitized before database query
🟠 Line 56-89: Missing test coverage for error cases
🟠 Line 112: This query will cause N+1 problem with large datasets

Once these are addressed, this will be ready to go! Let me know if you'd like to discuss any of these.
"""

# Questions and Learning
"""
❓ I have a few questions before reviewing:

1. What's the expected throughput for this endpoint? (affects whether we need caching)
2. Is backward compatibility required for the API change?
3. I see we're using approach X - have we considered approach Y? What were the tradeoffs?

Looking forward to understanding the context better!
"""

# Large PR Feedback
"""
📦 This PR is quite large (752 lines across 23 files). This makes it challenging to review thoroughly.

Suggestions:
1. Could we split this into smaller PRs? Perhaps:
   - PR 1: Database schema changes
   - PR 2: Backend API changes
   - PR 3: Frontend changes

2. If splitting isn't feasible, could you add a detailed description covering:
   - High-level architecture
   - Key changes in each major component
   - Testing strategy

This will help ensure a quality review. Thanks!
"""
```

### Code Review Metrics

**Review Quality Metrics:**
```python
# review_metrics.py
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

@dataclass
class ReviewMetrics:
    """Track code review metrics"""

    # Throughput metrics
    avg_review_time: timedelta
    reviews_per_week: int
    prs_merged_per_week: int

    # Quality metrics
    bugs_found_in_review: int
    bugs_escaped_to_production: int
    review_coverage: float  # % of PRs reviewed

    # Size metrics
    avg_pr_size_lines: int
    avg_pr_size_files: int
    large_pr_percentage: float  # % of PRs > 500 lines

    # Collaboration metrics
    avg_reviewers_per_pr: int
    avg_comments_per_pr: int
    avg_iterations_per_pr: int

    # Author metrics
    avg_time_to_address_comments: timedelta
    pr_approval_rate: float  # % approved on first review

class ReviewAnalyzer:
    """Analyze code review effectiveness"""

    def calculate_metrics(self, reviews: List[dict]) -> ReviewMetrics:
        """Calculate review metrics from review data"""
        # Implementation here
        pass

    def identify_bottlenecks(self, metrics: ReviewMetrics) -> List[str]:
        """Identify review process bottlenecks"""
        issues = []

        if metrics.avg_review_time > timedelta(days=2):
            issues.append("Review time is too long. Target: < 1 day")

        if metrics.large_pr_percentage > 0.3:
            issues.append("Too many large PRs (>30%). Encourage smaller PRs")

        if metrics.avg_iterations_per_pr > 4:
            issues.append("Too many review iterations. Improve PR quality before submission")

        if metrics.bugs_escaped_to_production > 0:
            issues.append(f"{metrics.bugs_escaped_to_production} bugs escaped to production")

        return issues

    def generate_report(self, metrics: ReviewMetrics) -> str:
        """Generate review metrics report"""
        report = f"""
        CODE REVIEW METRICS REPORT
        ==========================

        Throughput:
        -----------
        Average Review Time: {metrics.avg_review_time}
        Reviews per Week: {metrics.reviews_per_week}
        PRs Merged per Week: {metrics.prs_merged_per_week}

        Quality:
        --------
        Bugs Found in Review: {metrics.bugs_found_in_review}
        Bugs Escaped to Production: {metrics.bugs_escaped_to_production}
        Review Coverage: {metrics.review_coverage:.1%}

        PR Size:
        --------
        Average PR Size: {metrics.avg_pr_size_lines} lines, {metrics.avg_pr_size_files} files
        Large PRs (>500 lines): {metrics.large_pr_percentage:.1%}

        Collaboration:
        --------------
        Average Reviewers per PR: {metrics.avg_reviewers_per_pr}
        Average Comments per PR: {metrics.avg_comments_per_pr}
        Average Iterations: {metrics.avg_iterations_per_pr}

        Responsiveness:
        ---------------
        Time to Address Comments: {metrics.avg_time_to_address_comments}
        First-time Approval Rate: {metrics.pr_approval_rate:.1%}
        """
        return report
```

## How It Works

### Code Review Workflow

**Step 1: Pre-Review (Automated)**
```bash
# Run automated checks before manual review
python scripts/code_reviewer.py pre-review \
  --pr-number 123 \
  --checks all

# Output:
# ✅ Linting: PASSED
# ✅ Type checking: PASSED
# ⚠️  Test coverage: 75% (below threshold of 80%)
# ❌ Security: 2 high-severity issues found
# ⚠️  Complexity: 3 functions exceed complexity threshold
```

**Step 2: Manual Review**
```markdown
# Systematic review approach

1. Read PR description and linked issue
2. Understand the context and requirements
3. Review architecture/design first (big picture)
4. Review individual files (details)
5. Check tests
6. Run code locally if complex
7. Provide feedback
8. Summarize in comment
```

**Step 3: Author Response**
```markdown
# Responding to review comments

For each comment:
- ✅ Fixed
- 💬 Question/Discussion
- 📝 Added explanation
- ⏭️  Will address in follow-up PR
```

**Step 4: Re-Review**
```markdown
# Verify changes

1. Check if critical issues addressed
2. Review new changes
3. Approve or request more changes
```

## Best Practices

### For Reviewers

**Do:**
- Review promptly (within 24 hours)
- Be respectful and constructive
- Explain the "why" behind feedback
- Distinguish between requirements and suggestions
- Praise good code
- Ask questions when unclear
- Focus on important issues
- Consider author's experience level
- Approve good-enough code (don't perfect)
- Learn from code you review

**Don't:**
- Nitpick on style (use linters instead)
- Be vague or unclear
- Make it personal
- Block on personal preferences
- Require perfection
- Review when tired or rushed
- Ignore security issues
- Skip testing review
- Forget to approve when ready

### For Authors

**Do:**
- Keep PRs small and focused
- Write clear descriptions
- Add tests
- Run checks before submitting
- Respond to feedback promptly
- Ask clarifying questions
- Explain complex decisions
- Thank reviewers
- Learn from feedback

**Don't:**
- Submit broken code
- Skip tests
- Create huge PRs
- Take feedback personally
- Argue unnecessarily
- Ignore feedback
- Mix unrelated changes
- Commit debug code

## Integration Points

This skill integrates with:
- **Version Control:** GitHub, GitLab, Bitbucket
- **Static Analysis:** SonarQube, CodeClimate, DeepSource
- **Security:** Snyk, WhiteSource, Veracode
- **CI/CD:** GitHub Actions, Jenkins, CircleCI
- **Communication:** Slack, Microsoft Teams
- **Project Management:** Jira, Linear, Asana
- **Documentation:** Confluence, Notion

## Common Challenges and Solutions

### Challenge: Large Pull Requests
**Solution:** Encourage smaller PRs, suggest splitting, review architecture separately, use review tools to filter changes, schedule dedicated time for large reviews

### Challenge: Slow Review Turnaround
**Solution:** Set SLA for reviews (24 hours), rotate reviewers, implement review queues, use automated checks to reduce review load, measure and track metrics

### Challenge: Inconsistent Feedback
**Solution:** Create review guidelines, use checklists, train reviewers, establish severity levels, document team conventions, use linters for style

### Challenge: Defensive Authors
**Solution:** Focus on code not person, explain reasoning, ask questions instead of statements, praise good parts, be empathetic, provide examples

### Challenge: Rubber Stamp Reviews
**Solution:** Require meaningful comments, track quality metrics, pair newer reviewers with experienced ones, review the reviewers, emphasize value of reviews

### Challenge: Review Fatigue
**Solution:** Limit review requests per person, rotate reviewers, automate simple checks, improve PR quality, recognize review contributions, allow focus time
