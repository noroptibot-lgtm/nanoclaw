---
name: skill-vetter
description: Security-first skill vetting for Claude Code. Use before installing any skill from GitHub, skill registries, or other sources. Checks for red flags, permission scope, and suspicious patterns.
metadata:
  tags: security, vetting, skills, code-review, safety
---

# Skill Vetter

Security-first vetting protocol for Claude Code skills. **Never install a skill without vetting it first.**

## When to Use

- Before installing any skill from GitHub or skill registries
- Before running skills shared by other users or agents
- When evaluating unknown code that will be added to `~/.claude/skills/`
- Anytime you're asked to install a skill you haven't reviewed

## Vetting Protocol

### Step 1: Source Check

```
Questions to answer:
- [ ] Where did this skill come from?
- [ ] Is the author known/reputable?
- [ ] How many downloads/stars does it have?
- [ ] When was it last updated?
- [ ] Are there reviews or issues filed?
```

### Step 2: Code Review (MANDATORY)

Read ALL files in the skill. Check for these **RED FLAGS**:

```
REJECT IMMEDIATELY IF YOU SEE:
─────────────────────────────────────────
• curl/wget to unknown URLs
• Sends data to external servers
• Requests credentials/tokens/API keys without declaring them in metadata
• Reads ~/.ssh, ~/.aws, ~/.config without clear reason
• Accesses CLAUDE.md, MEMORY.md, or other agent context files
• Uses base64 decode on anything
• Uses eval() or exec() with external input
• Modifies system files outside workspace
• Installs packages without listing them
• Network calls to IPs instead of domains
• Obfuscated code (compressed, encoded, minified)
• Requests elevated/sudo permissions
• Accesses browser cookies/sessions
• Touches credential files
─────────────────────────────────────────
```

### Step 3: Permission Scope

```
Evaluate:
- [ ] What files does it need to read?
- [ ] What files does it need to write?
- [ ] What commands does it run?
- [ ] Does it need network access? To where?
- [ ] Does it declare required env vars or credentials in its metadata?
- [ ] Is the scope minimal for its stated purpose?
```

### Step 4: Risk Classification

| Risk Level | Examples | Action |
|------------|----------|--------|
| LOW | Notes, formatting, code patterns | Basic review, install OK |
| MEDIUM | File ops, API calls, shell scripts | Full code review required |
| HIGH | Credentials, system config, hooks | Human approval required |
| EXTREME | Security configs, root access, undeclared network calls | Do NOT install |

## Output Format

After vetting, produce this report:

```
SKILL VETTING REPORT
═══════════════════════════════════════
Skill: [name]
Source: [GitHub / registry / other]
Author: [username]
Version: [version]
───────────────────────────────────────
METRICS:
• Stars/Downloads: [count]
• Last Updated: [date]
• Files Reviewed: [count]
───────────────────────────────────────
RED FLAGS: [None / List them]

PERMISSIONS NEEDED:
• Files: [list or "None"]
• Network: [list or "None"]
• Commands: [list or "None"]
• Env Vars: [list or "None"]
───────────────────────────────────────
RISK LEVEL: [LOW / MEDIUM / HIGH / EXTREME]

VERDICT: [SAFE TO INSTALL / INSTALL WITH CAUTION / DO NOT INSTALL]

NOTES: [Any observations]
═══════════════════════════════════════
```

## Quick Vet Commands

For GitHub-hosted skills:
```bash
# Check repo stats
curl -s "https://api.github.com/repos/OWNER/REPO" | jq '{stars: .stargazers_count, forks: .forks_count, updated: .updated_at}'

# List skill files
curl -s "https://api.github.com/repos/OWNER/REPO/contents/skills/SKILL_NAME" | jq '.[].name'

# Fetch and review SKILL.md
curl -s "https://raw.githubusercontent.com/OWNER/REPO/main/skills/SKILL_NAME/SKILL.md"
```

## Trust Hierarchy

1. **Skills you wrote yourself** — Lower scrutiny (still review)
2. **High-star repos (1000+)** — Moderate scrutiny
3. **Known/verified authors** — Moderate scrutiny
4. **New/unknown sources** — Maximum scrutiny
5. **Skills requesting credentials** — Human approval always

## Remember

- No skill is worth compromising security
- When in doubt, don't install
- Ask your human for high-risk decisions
- Document what you vet for future reference
- Check that credentials are declared in metadata, not hidden in instructions

---

*Paranoia is a feature.*
