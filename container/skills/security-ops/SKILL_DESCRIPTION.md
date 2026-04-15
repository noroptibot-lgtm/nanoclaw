# Security Operations (Senior SecOps)

## Overview

The Security Operations skill provides comprehensive tools and frameworks for application security, vulnerability management, compliance, and secure development practices. This skill enables security teams to proactively identify, assess, and remediate security vulnerabilities while ensuring compliance with industry standards and regulations. It combines automated security scanning, vulnerability assessment, and compliance checking with best practices for secure development and operations.

## Who Should Use This Skill

- **Security Operations Engineers** managing security infrastructure and incident response
- **Application Security Engineers** focusing on secure code and vulnerability management
- **DevSecOps Engineers** integrating security into CI/CD pipelines
- **Security Analysts** conducting security assessments and audits
- **Compliance Officers** ensuring regulatory and standards compliance
- **Platform Security Teams** securing infrastructure and cloud environments
- **Security Architects** designing secure systems and processes

## Purpose and Use Cases

Use this skill when you need to:
- Conduct automated security scans of applications and infrastructure
- Assess and prioritize security vulnerabilities
- Verify compliance with security standards (OWASP, CIS, PCI-DSS, SOC2, HIPAA)
- Implement security controls and safeguards
- Automate security testing in CI/CD pipelines
- Monitor security posture and track remediation
- Generate security audit reports
- Respond to security vulnerabilities and incidents
- Establish secure development practices
- Conduct security code reviews

**Keywords that trigger this skill:** security scanning, vulnerability assessment, compliance checking, security audit, penetration testing, threat modeling, security controls, OWASP, security automation, vulnerability management, security monitoring

## What's Included

### Security Scanner

**Automated Application Security Testing:**
- Static Application Security Testing (SAST)
- Dynamic Application Security Testing (DAST)
- Software Composition Analysis (SCA)
- Container and image scanning
- Infrastructure as Code (IaC) security scanning
- API security testing
- Secret detection and credential scanning
- License compliance checking

**Scanning Capabilities:**
- Multi-language support (JavaScript, TypeScript, Python, Go, Java, etc.)
- Framework-specific security checks
- Dependency vulnerability scanning
- Configuration security analysis
- Cloud resource security scanning
- Database security assessment
- Network security validation

**Output Formats:**
- JSON for CI/CD integration
- HTML reports for stakeholders
- SARIF for developer tools
- CSV for tracking and metrics
- PDF for compliance documentation

### Vulnerability Assessor

**Vulnerability Analysis:**
- CVE database integration
- Severity scoring (CVSS v3.1)
- Exploitability assessment
- Attack vector analysis
- Business impact evaluation
- Remediation effort estimation
- Risk prioritization matrix

**Assessment Features:**
- Automated vulnerability triaging
- False positive detection
- Vulnerability correlation across systems
- Trend analysis and metrics
- SLA tracking for remediation
- Vulnerability lifecycle management
- Retest validation

**Prioritization Framework:**
```
Critical: CVSS 9.0-10.0, Active exploits, High business impact
High: CVSS 7.0-8.9, Public exploits, Medium business impact
Medium: CVSS 4.0-6.9, Theoretical exploits, Low business impact
Low: CVSS 0.1-3.9, No known exploits, Minimal business impact
```

**Risk Scoring Formula:**
```
Risk Score = (CVSS Score × Exploitability × Asset Value × Exposure) / Remediation Effort
```

### Compliance Checker

**Compliance Frameworks:**
- **OWASP Top 10** - Web application security risks
- **CIS Benchmarks** - Infrastructure hardening standards
- **PCI-DSS** - Payment card industry standards
- **SOC 2** - Service organization controls
- **HIPAA** - Healthcare data protection
- **GDPR** - Data privacy regulations
- **NIST Cybersecurity Framework** - Security best practices
- **ISO 27001** - Information security management

**Compliance Checks:**
- Authentication and authorization controls
- Encryption requirements (data at rest and in transit)
- Access control policies
- Audit logging and monitoring
- Data retention and privacy
- Incident response procedures
- Business continuity planning
- Vendor risk management

**Compliance Reporting:**
- Gap analysis against standards
- Control effectiveness assessment
- Evidence collection and documentation
- Audit-ready compliance reports
- Remediation roadmap generation
- Continuous compliance monitoring
- Exception and risk acceptance tracking

## How It Works

### Security Scanner Workflow

**Step 1: Configure Scanning**
```bash
# Initialize security scanner configuration
python scripts/security_scanner.py --init

# Configure scan types and targets
{
  "scan_types": ["sast", "sca", "secrets"],
  "targets": ["src/**/*.js", "src/**/*.py"],
  "exclude": ["node_modules", "test/**"],
  "severity_threshold": "medium",
  "fail_on": ["critical", "high"]
}
```

**Step 2: Run Security Scan**
```bash
# Full security scan
python scripts/security_scanner.py /path/to/project

# Specific scan types
python scripts/security_scanner.py /path/to/project --scan-type sast,sca

# Quick scan (critical/high only)
python scripts/security_scanner.py /path/to/project --quick

# CI/CD integration mode
python scripts/security_scanner.py /path/to/project --ci --format json
```

**Step 3: Review Scan Results**
```
SECURITY SCAN RESULTS
=====================

Summary:
--------
Total Issues: 47
Critical: 2
High: 8
Medium: 23
Low: 14

Critical Issues:
----------------
[CRITICAL] SQL Injection vulnerability in user authentication
  File: src/auth/login.js:45
  CWE: CWE-89
  CVSS: 9.8
  Description: User input not sanitized before SQL query execution
  Recommendation: Use parameterized queries or ORM

[CRITICAL] Hardcoded AWS credentials in source code
  File: src/config/aws.js:12
  CWE: CWE-798
  CVSS: 9.1
  Description: AWS access key and secret exposed in code
  Recommendation: Use environment variables or secrets manager

High Priority Issues:
---------------------
[HIGH] Cross-Site Scripting (XSS) vulnerability
  File: src/components/UserProfile.jsx:78
  CWE: CWE-79
  CVSS: 7.4
  Description: User input rendered without sanitization
  Recommendation: Use React's built-in XSS protection or sanitize input

[HIGH] Outdated dependency with known vulnerability
  Package: lodash@4.17.15
  CVE: CVE-2020-8203
  CVSS: 7.4
  Description: Prototype pollution vulnerability
  Recommendation: Update to lodash@4.17.21 or higher
```

**Step 4: Export and Track**
```bash
# Generate HTML report
python scripts/security_scanner.py /path/to/project --output html

# Export for tracking
python scripts/security_scanner.py /path/to/project --output json > scan-results.json

# Compare with baseline
python scripts/security_scanner.py /path/to/project --compare baseline.json
```

### Vulnerability Assessment Workflow

**Step 1: Import Scan Results**
```bash
# Assess vulnerabilities from scan
python scripts/vulnerability_assessor.py scan-results.json

# Assess from multiple sources
python scripts/vulnerability_assessor.py scan-results.json --import-sarif,--import-nessus
```

**Step 2: Analyze and Prioritize**
```bash
# Full assessment with business context
python scripts/vulnerability_assessor.py scan-results.json \
  --asset-value high \
  --exposure internet-facing \
  --business-impact critical

# Generate risk matrix
python scripts/vulnerability_assessor.py scan-results.json --risk-matrix
```

**Step 3: Review Assessment**
```
VULNERABILITY ASSESSMENT
========================

Risk Distribution:
------------------
Critical Risk: 3 vulnerabilities
High Risk: 12 vulnerabilities
Medium Risk: 18 vulnerabilities
Low Risk: 14 vulnerabilities

Top 5 Priorities:
-----------------
1. SQL Injection (auth module) - Risk Score: 950
   CVSS: 9.8 | Exploitability: High | Asset Value: Critical
   Remediation: 2 hours | SLA: 24 hours
   Business Impact: Customer data breach, regulatory fines

2. Remote Code Execution (API endpoint) - Risk Score: 920
   CVSS: 9.6 | Exploitability: High | Asset Value: Critical
   Remediation: 4 hours | SLA: 24 hours
   Business Impact: Complete system compromise

3. Authentication Bypass - Risk Score: 875
   CVSS: 9.1 | Exploitability: Medium | Asset Value: Critical
   Remediation: 8 hours | SLA: 48 hours
   Business Impact: Unauthorized access to all accounts

Remediation Roadmap:
--------------------
Week 1: Critical risk items (3 vulnerabilities)
Week 2-3: High risk items (12 vulnerabilities)
Month 2: Medium risk items (18 vulnerabilities)
Quarterly: Low risk items (14 vulnerabilities)

SLA Tracking:
-------------
Overdue: 0
Due Today: 2
Due This Week: 8
On Track: 37
```

**Step 4: Track Remediation**
```bash
# Update vulnerability status
python scripts/vulnerability_assessor.py --update-status vuln-001 fixed

# Verify fix
python scripts/vulnerability_assessor.py --retest vuln-001

# Generate metrics report
python scripts/vulnerability_assessor.py --metrics monthly
```

### Compliance Checking Workflow

**Step 1: Select Compliance Framework**
```bash
# Check OWASP Top 10 compliance
python scripts/compliance_checker.py /path/to/project --framework owasp-top-10

# Check multiple frameworks
python scripts/compliance_checker.py /path/to/project \
  --framework owasp-top-10,cis-docker,pci-dss

# Custom compliance requirements
python scripts/compliance_checker.py /path/to/project --custom requirements.yaml
```

**Step 2: Run Compliance Check**
```bash
# Full compliance audit
python scripts/compliance_checker.py /path/to/project \
  --framework soc2 \
  --evidence-output ./compliance-evidence/

# Continuous compliance monitoring
python scripts/compliance_checker.py /path/to/project \
  --framework pci-dss \
  --watch \
  --alert-on-violations
```

**Step 3: Review Compliance Report**
```
COMPLIANCE REPORT: SOC 2
========================

Overall Compliance: 87% (78/90 controls)

Control Categories:
-------------------
CC6.1 - Logical Access: 92% (11/12 controls)
CC6.6 - Encryption: 83% (5/6 controls)
CC7.2 - System Monitoring: 75% (9/12 controls)
CC8.1 - Change Management: 95% (19/20 controls)

Non-Compliant Controls:
-----------------------
[FAILED] CC6.1.4 - Multi-factor authentication
  Requirement: MFA required for all user accounts
  Status: MFA only enabled for admin accounts
  Gap: 65% of user accounts without MFA
  Remediation: Enable MFA for all users, enforce at login
  Priority: High

[FAILED] CC6.6.2 - Encryption at rest
  Requirement: All sensitive data encrypted at rest
  Status: Database encryption enabled, file storage not encrypted
  Gap: S3 buckets lack server-side encryption
  Remediation: Enable S3 default encryption, migrate existing data
  Priority: Critical

[FAILED] CC7.2.3 - Security event logging
  Requirement: Comprehensive security event logging
  Status: Application logs exist, no centralized SIEM
  Gap: No correlation or alerting on security events
  Remediation: Implement SIEM solution, configure alerts
  Priority: High

Remediation Plan:
-----------------
Immediate (1-2 weeks):
- Enable S3 encryption (CC6.6.2)
- Configure SIEM alerts (CC7.2.3)

Short-term (1 month):
- Roll out MFA to all users (CC6.1.4)
- Implement audit log retention (CC7.2.5)

Medium-term (1-3 months):
- Enhance monitoring coverage (CC7.2.1)
- Implement automated backups (CC6.7.1)

Evidence Collected:
-------------------
- IAM policy documents
- Encryption configuration screenshots
- Log retention policies
- Access control matrices
- Incident response procedures
```

**Step 4: Export Compliance Documentation**
```bash
# Generate audit report
python scripts/compliance_checker.py /path/to/project \
  --framework soc2 \
  --output pdf \
  --include-evidence

# Export gap analysis
python scripts/compliance_checker.py /path/to/project \
  --framework iso-27001 \
  --gap-analysis \
  --output csv
```

## Technical Details

### Security Scanner Capabilities

**SAST (Static Analysis):**
- Control flow analysis
- Data flow analysis
- Taint tracking
- Pattern matching for security issues
- Custom rule definitions
- False positive reduction

**SCA (Software Composition):**
- Dependency tree analysis
- Transitive dependency scanning
- CVE database lookups
- License compliance checking
- End-of-life detection
- Patch availability identification

**Secret Detection:**
- API keys and tokens
- Database credentials
- Private keys and certificates
- Cloud provider credentials
- OAuth tokens
- Custom secret patterns

**Container Scanning:**
- Base image vulnerabilities
- Layer-by-layer analysis
- Malware detection
- Configuration issues
- Compliance violations
- Registry integration

### Vulnerability Assessment Metrics

**CVSS Scoring Components:**
```
Base Score:
- Attack Vector (Network/Adjacent/Local/Physical)
- Attack Complexity (Low/High)
- Privileges Required (None/Low/High)
- User Interaction (None/Required)
- Scope (Unchanged/Changed)
- Impact (Confidentiality/Integrity/Availability)

Temporal Score:
- Exploit Code Maturity
- Remediation Level
- Report Confidence

Environmental Score:
- Modified Base Metrics
- Confidentiality/Integrity/Availability Requirements
```

**Risk Calculation:**
```python
def calculate_risk_score(vuln):
    cvss = vuln.cvss_score
    exploitability = {
        'active': 1.0,
        'public': 0.8,
        'theoretical': 0.5,
        'none': 0.2
    }[vuln.exploit_status]

    asset_value = {
        'critical': 1.0,
        'high': 0.75,
        'medium': 0.5,
        'low': 0.25
    }[vuln.asset_value]

    exposure = {
        'internet': 1.0,
        'internal': 0.6,
        'isolated': 0.3
    }[vuln.network_exposure]

    effort = {
        'hours': 10,
        'days': 5,
        'weeks': 2,
        'months': 1
    }[vuln.remediation_effort]

    risk = (cvss * exploitability * asset_value * exposure) / effort
    return risk
```

### Compliance Framework Mappings

**OWASP Top 10 Coverage:**
- A01: Broken Access Control
- A02: Cryptographic Failures
- A03: Injection
- A04: Insecure Design
- A05: Security Misconfiguration
- A06: Vulnerable and Outdated Components
- A07: Identification and Authentication Failures
- A08: Software and Data Integrity Failures
- A09: Security Logging and Monitoring Failures
- A10: Server-Side Request Forgery

**PCI-DSS Requirements:**
- Requirement 1: Firewall configuration
- Requirement 2: Default passwords changed
- Requirement 3: Cardholder data protection
- Requirement 4: Encryption in transit
- Requirement 6: Secure systems and applications
- Requirement 8: Access control
- Requirement 10: Logging and monitoring
- Requirement 11: Security testing

## Use Cases and Examples

### Integrating Security Scanning into CI/CD

**Scenario:** Automated security checks in GitHub Actions

```yaml
name: Security Scan

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  security-scan:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Run Security Scanner
        run: |
          python scripts/security_scanner.py . \
            --ci \
            --format sarif \
            --output results.sarif \
            --fail-on critical,high

      - name: Upload Results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: results.sarif

      - name: Assess Vulnerabilities
        if: failure()
        run: |
          python scripts/vulnerability_assessor.py results.sarif \
            --format markdown > security-report.md

      - name: Comment on PR
        if: failure() && github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('security-report.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            });
```

**Benefits:**
- Automatic security checks on every PR
- Block merges with critical/high vulnerabilities
- Security visibility in GitHub Security tab
- Automated reporting to developers

### Monthly Security Audit and Compliance Check

**Scenario:** Quarterly SOC 2 compliance audit preparation

```bash
# Week 1: Comprehensive security scan
python scripts/security_scanner.py /path/to/production \
  --full-scan \
  --output json > q3-security-scan.json

# Week 2: Vulnerability assessment and prioritization
python scripts/vulnerability_assessor.py q3-security-scan.json \
  --asset-value high \
  --exposure internet-facing \
  --output json > q3-vulnerability-assessment.json

# Week 3: Compliance check
python scripts/compliance_checker.py /path/to/production \
  --framework soc2 \
  --evidence-output ./q3-compliance-evidence/ \
  --output pdf > q3-compliance-report.pdf

# Week 4: Remediation and documentation
python scripts/vulnerability_assessor.py q3-vulnerability-assessment.json \
  --remediation-roadmap \
  --output markdown > q3-remediation-plan.md

# Generate executive summary
python scripts/generate_security_summary.py \
  --scan q3-security-scan.json \
  --assessment q3-vulnerability-assessment.json \
  --compliance q3-compliance-report.pdf \
  --output executive-summary.pdf
```

**Deliverables:**
- Comprehensive security scan results
- Prioritized vulnerability remediation roadmap
- SOC 2 compliance status report with evidence
- Executive summary for leadership
- Quarterly trend analysis

### Responding to a Critical Vulnerability

**Scenario:** Zero-day vulnerability discovered in production dependency

**Step 1: Immediate Assessment**
```bash
# Scan for affected systems
python scripts/security_scanner.py /path/to/all/projects \
  --scan-type sca \
  --package log4j \
  --version "2.0-2.14.1" \
  --output json > log4j-affected-systems.json

# Assess risk and impact
python scripts/vulnerability_assessor.py log4j-affected-systems.json \
  --cve CVE-2021-44228 \
  --asset-value critical \
  --urgent \
  --output markdown > log4j-assessment.md
```

**Assessment Output:**
```
URGENT VULNERABILITY ASSESSMENT: CVE-2021-44228 (Log4Shell)
============================================================

Affected Systems: 23 applications
CVSS Score: 10.0 (Critical)
Exploit Status: Active exploitation in the wild
Attack Vector: Network, unauthenticated

Business Impact:
- Remote Code Execution possible
- Complete system compromise
- Customer data at risk
- Regulatory reporting required

Affected Applications:
1. customer-api (Production, Internet-facing)
   Package: log4j-core@2.14.0
   Exposure: High - Public API
   Priority: P0 - Fix immediately

2. analytics-service (Production, Internal)
   Package: log4j-core@2.12.1
   Exposure: Medium - Internal network
   Priority: P0 - Fix within 24h

... (21 more applications)

Recommended Actions:
1. IMMEDIATE: Implement WAF rules to block exploitation
2. IMMEDIATE: Enable security monitoring for IOCs
3. URGENT: Update to log4j@2.17.0 in all affected apps
4. URGENT: Conduct forensic analysis for compromise
5. Follow-up: Implement dependency scanning in CI/CD
```

**Step 2: Implement Emergency Mitigations**
```bash
# Update WAF rules
aws waf update-rule --rule-id log4shell-block --predicates ...

# Deploy monitoring alerts
python scripts/deploy_security_monitoring.py \
  --ioc log4shell-indicators.json \
  --alert-severity critical

# Emergency patching
for app in $(cat affected-apps.txt); do
  cd $app
  # Update dependency
  npm update log4j-core@2.17.0
  # Run security scan to verify
  python scripts/security_scanner.py . --quick --verify-fix CVE-2021-44228
  # Deploy to production
  ./deploy.sh --emergency
done
```

**Step 3: Post-Incident Analysis**
```bash
# Verify remediation
python scripts/vulnerability_assessor.py \
  --retest CVE-2021-44228 \
  --verify-all-systems

# Generate incident report
python scripts/generate_incident_report.py \
  --cve CVE-2021-44228 \
  --assessment log4j-assessment.md \
  --actions remediation-log.json \
  --output log4shell-incident-report.pdf
```

## Best Practices

### Security Scanning Best Practices

**Do:**
- Scan early and often in development lifecycle
- Integrate scanning into CI/CD pipelines
- Scan all code, including third-party dependencies
- Use multiple scanning techniques (SAST, DAST, SCA)
- Tune scanners to reduce false positives
- Maintain baseline scans for comparison
- Scan infrastructure as code and containers
- Keep scanner rules and CVE databases updated

**Don't:**
- Rely solely on automated scanning
- Ignore low severity findings completely
- Scan only before major releases
- Skip validation of scanner findings
- Treat all findings equally without context
- Forget to scan transitive dependencies
- Ignore licensing and compliance issues

### Vulnerability Management Best Practices

**Do:**
- Prioritize based on risk, not just CVSS score
- Consider business context and asset value
- Track vulnerabilities through full lifecycle
- Set and enforce remediation SLAs
- Verify fixes with rescans
- Document accepted risks with justification
- Trend and report metrics regularly
- Maintain vulnerability playbooks

**Don't:**
- Fix vulnerabilities without understanding impact
- Accept all scanner findings without validation
- Let vulnerabilities languish without tracking
- Miss SLAs without escalation
- Deploy fixes without testing
- Accept risks without proper approval
- Ignore patterns in recurring vulnerabilities

### Compliance Best Practices

**Do:**
- Automate compliance checking where possible
- Collect and preserve evidence continuously
- Map controls to actual implementations
- Conduct regular self-assessments
- Document exceptions with risk acceptance
- Keep compliance documentation current
- Involve stakeholders early
- Use compliance as a security improvement driver

**Don't:**
- Wait until audit time to check compliance
- Treat compliance as checkbox exercise
- Implement controls without understanding purpose
- Accept findings without remediation plans
- Forget to maintain evidence trail
- Ignore control effectiveness testing
- Assume past compliance means current compliance

### Secure Development Practices

**Do:**
- Implement security requirements in design phase
- Use secure coding standards and guidelines
- Conduct security code reviews
- Perform threat modeling for new features
- Use security champions in dev teams
- Provide security training regularly
- Build security into definition of done
- Maintain security documentation

**Don't:**
- Add security as afterthought
- Skip security review for "small" changes
- Trust user input without validation
- Store secrets in code or repositories
- Disable security features for convenience
- Ignore security in dependencies
- Deploy without security testing

## Integration Points

This skill integrates with:
- **CI/CD Platforms:** GitHub Actions, GitLab CI, Jenkins, CircleCI, Azure DevOps
- **Security Tools:** Snyk, SonarQube, Checkmarx, Veracode, OWASP ZAP
- **Vulnerability Databases:** NVD, CVE, GitHub Advisory Database
- **Issue Tracking:** Jira, Linear, GitHub Issues (for vulnerability tracking)
- **SIEM/Monitoring:** Splunk, ELK Stack, Datadog, New Relic
- **Cloud Security:** AWS Security Hub, Azure Security Center, GCP Security Command Center
- **Container Security:** Docker Scout, Trivy, Aqua Security, Snyk Container
- **Compliance:** Vanta, Drata, Secureframe, OneTrust

## Common Challenges and Solutions

### Challenge: High False Positive Rate
**Solution:** Tune scanner configurations, create suppression rules for validated false positives, use contextual analysis, implement manual validation workflow for medium/low findings, continuously improve detection rules based on feedback

### Challenge: Overwhelming Number of Vulnerabilities
**Solution:** Focus on risk-based prioritization, address critical/high items first, batch fix similar issues, accept risk on low-impact items with proper approval, improve prevention through secure coding practices, implement progressive remediation

### Challenge: Slow Scan Times Blocking CI/CD
**Solution:** Use incremental scanning, scan only changed code/dependencies, run full scans asynchronously, cache scan results, optimize scanner configuration, consider parallel scanning, use faster scanners for CI checks

### Challenge: Compliance Framework Complexity
**Solution:** Start with automated checks, use control mapping tools, break down into manageable workstreams, assign control owners, document interpretations, leverage frameworks from similar organizations, engage compliance experts

### Challenge: Developer Resistance to Security
**Solution:** Provide security training, make security tools developer-friendly, integrate into existing workflows, show value not just requirements, celebrate security wins, use security champions model, automate where possible

### Challenge: Keeping Up with New Vulnerabilities
**Solution:** Automate dependency updates, subscribe to security advisories, implement continuous monitoring, maintain vulnerability database subscriptions, use automated alerting, prioritize based on exploitability, establish rapid response procedures
