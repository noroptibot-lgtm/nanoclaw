# Template Skill (template-skill)

## Overview
The Template Skill provides a minimal starting point for creating new skills. This is a placeholder template that should be customized with actual skill instructions and metadata when creating a new skill.

## Who Should Use This Skill
- Developers starting to create a new skill
- Anyone using the skill creation process who needs a basic template structure

## Purpose and Use Cases
This template serves as a structural foundation for new skills. It should not be used directly but rather customized to create functional, domain-specific skills.

**Note:** Replace the name and description in the SKILL.md frontmatter with appropriate values for your specific skill.

## What's Included
- Basic SKILL.md structure with YAML frontmatter
- Placeholder sections for skill instructions
- Minimal file structure ready for customization

## How It Works
1. Copy this template when creating a new skill
2. Replace the `name` field with your skill's short identifier
3. Replace the `description` field with a clear explanation of when Claude should use the skill
4. Add detailed instructions below the frontmatter
5. Create additional directories (`scripts/`, `references/`, `assets/`) as needed

## Technical Details
**Required Structure:**
- YAML frontmatter with `name` and `description` fields
- Markdown instructions following the frontmatter
- Optional bundled resources directories

**File Format:**
```yaml
---
name: your-skill-name
description: Clear description of what the skill does and when to use it
---

# Your Skill Instructions

Add detailed instructions here...
```

## Best Practices
- Use the `skill-creator` skill for comprehensive guidance on skill creation
- Follow the six-step skill creation process
- Ensure the description clearly indicates when the skill should be used
- Write instructions in imperative/infinitive form
- Test the skill with real examples before deployment
