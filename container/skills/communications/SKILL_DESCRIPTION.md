# Internal Communications (internal-comms)

## Overview
The Internal Communications skill provides a comprehensive set of resources and templates to help write professional internal company communications following established organizational formats and best practices. This skill covers a wide range of communication types including status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, and project updates.

## Who Should Use This Skill
- Team leads preparing progress updates
- Project managers writing status reports
- Communications teams creating company newsletters
- Department heads drafting leadership updates
- Engineers documenting incident reports
- Product managers sharing project updates
- HR or internal communications professionals
- Anyone responsible for formal internal company communications

## Purpose and Use Cases
Use this skill when you need to create internal communications that follow your company's preferred formats and tone. The skill is triggered by requests involving:

**Keywords:** 3P updates, company newsletter, company comms, weekly update, faqs, common questions, updates, internal comms, status reports, leadership updates, project updates, incident reports

**Common use cases:**
- Writing Progress/Plans/Problems (3P) team updates
- Creating company-wide newsletters
- Drafting FAQ responses for common questions
- Preparing status reports for stakeholders
- Composing leadership updates for executives
- Documenting project milestones and updates
- Writing incident reports and post-mortems

## What's Included
This skill includes a structured library of communication templates and guidelines:

**Example Templates (`examples/` directory):**
- `3p-updates.md` - Templates and guidelines for Progress/Plans/Problems team updates
- `company-newsletter.md` - Format and structure for company-wide newsletters
- `faq-answers.md` - Best practices for answering frequently asked questions
- `general-comms.md` - General communication guidelines for other internal communications

**Key Features:**
- Pre-defined formats for common communication types
- Tone and style guidelines consistent with company culture
- Content gathering instructions for each communication type
- Structured templates that ensure completeness and clarity
- Best practices for professional internal communications

## How It Works
The skill follows a simple three-step workflow:

**Step 1: Identify Communication Type**
Claude analyzes your request to determine which type of internal communication you need to create.

**Step 2: Load Appropriate Guidelines**
Based on the identified type, Claude loads the relevant template file from the `examples/` directory:
- For team updates: `3p-updates.md`
- For newsletters: `company-newsletter.md`
- For FAQs: `faq-answers.md`
- For other communications: `general-comms.md`

**Step 3: Follow Template Instructions**
Claude applies the specific formatting, tone, and content structure defined in the loaded template to create your communication.

If the communication type doesn't clearly match an existing template, Claude will ask for clarification about the desired format and approach.

## Technical Details
**Skill Structure:**
- Primary instruction file: `SKILL.md` with YAML frontmatter
- Reference materials stored in `examples/` directory
- All templates use Markdown format for easy editing and version control

**Dependencies:**
- No external dependencies required
- Templates are self-contained reference documents
- Works entirely within Claude's context without external tool calls

**File Organization:**
```
communications/
├── SKILL.md (main instructions)
└── examples/
    ├── 3p-updates.md
    ├── company-newsletter.md
    ├── faq-answers.md
    └── general-comms.md
```

## Best Practices
**For Best Results:**
- Be specific about the type of communication you need (e.g., "3P update" vs. "general update")
- Provide context about your audience (team, leadership, entire company)
- Share key information upfront (progress made, problems encountered, upcoming plans)
- Mention any specific company terminology or acronyms to include
- Specify the desired length or level of detail

**Communication Tips:**
- Use the appropriate template for your audience and purpose
- Maintain a professional yet accessible tone
- Focus on clarity and conciseness
- Include actionable information and next steps
- Proofread for consistency with company style

**Template Customization:**
- Templates can be modified to match your company's specific preferences
- Add new template files to `examples/` for additional communication types
- Update `SKILL.md` to reference any new templates you create
- Consider creating templates for recurring communication needs
