# MCP Server Builder (mcp-builder)

## Overview
The MCP Server Builder is a comprehensive guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to effectively interact with external services and APIs. This skill provides a complete framework for designing, implementing, and evaluating MCP servers in both Python (FastMCP) and Node/TypeScript, with emphasis on agent-centric design principles and real-world effectiveness.

## Who Should Use This Skill
- Developers building MCP servers to integrate external APIs
- Engineers creating LLM tool integrations
- API designers exposing services to AI agents
- Platform engineers building agent infrastructure
- Developer advocates creating example integrations
- Product teams enabling AI access to their services
- Anyone extending LLM capabilities through the Model Context Protocol

## Purpose and Use Cases
Use this skill when building MCP servers that allow LLMs to access external services, whether implementing in Python (FastMCP) or Node/TypeScript (MCP SDK).

**Keywords:** MCP server, Model Context Protocol, MCP integration, API integration, LLM tools, external service access, FastMCP, MCP SDK, agent tools

**Common use cases:**
- Creating MCP servers for third-party API integrations
- Building internal service access for LLMs
- Exposing database access through MCP tools
- Integrating SaaS platforms (GitHub, Slack, Notion, etc.)
- Creating workflow automation tools for agents
- Building specialized domain tools for AI agents
- Enabling LLM access to company-specific systems

## What's Included
This skill provides a complete four-phase framework for MCP server development:

**Phase 1: Deep Research and Planning**
- Agent-centric design principles
- MCP protocol documentation access
- Framework-specific SDK documentation (Python/TypeScript)
- API documentation study methodology
- Comprehensive implementation planning template

**Phase 2: Implementation**
- Project structure setup for both languages
- Core infrastructure patterns (API requests, error handling, pagination)
- Tool implementation guidelines with validation
- Language-specific best practices (Python and TypeScript)

**Phase 3: Review and Refine**
- Code quality review checklist
- Testing strategies (syntax, imports, builds)
- Quality verification checklists

**Phase 4: Evaluation Creation**
- Evaluation purpose and methodology
- Question generation process (10 complex, realistic questions)
- Answer verification strategies
- XML format specifications

**Reference Documentation (`reference/` directory):**
- `mcp_best_practices.md`: Universal MCP guidelines
- `python_mcp_server.md`: Python/FastMCP implementation guide
- `node_mcp_server.md`: TypeScript/Node implementation guide
- `evaluation.md`: Complete evaluation creation guide

**External Resources (fetched as needed):**
- MCP Protocol specification
- Python SDK documentation
- TypeScript SDK documentation

## How It Works
The skill follows a systematic four-phase workflow:

**Phase 1: Deep Research and Planning**

Step 1.1: Understand agent-centric design principles:
- Build for workflows, not just API endpoints
- Optimize for limited context (return high-signal information)
- Design actionable error messages that guide agents
- Follow natural task subdivisions
- Use evaluation-driven development

Step 1.3: Study MCP protocol documentation from `https://modelcontextprotocol.io/llms-full.txt`

Step 1.4: Study framework documentation:
- Load `reference/mcp_best_practices.md` for all servers
- For Python: Load Python SDK + `reference/python_mcp_server.md`
- For TypeScript: Load TypeScript SDK + `reference/node_mcp_server.md`

Step 1.5: Exhaustively study target API documentation using web search and WebFetch

Step 1.6: Create comprehensive implementation plan covering:
- Tool selection and prioritization
- Shared utilities and helpers
- Input/output design with validation
- Error handling strategy

**Phase 2: Implementation**

Step 2.1: Set up project structure (language-specific)

Step 2.2: Implement core infrastructure first:
- API request helpers
- Error handling utilities
- Response formatting (JSON and Markdown)
- Pagination helpers
- Authentication/token management

Step 2.3: Implement tools systematically:
- Define input schemas (Pydantic for Python, Zod for TypeScript)
- Write comprehensive docstrings/descriptions
- Implement tool logic with proper async/await
- Add tool annotations (readOnlyHint, destructiveHint, etc.)

Step 2.4: Follow language-specific best practices from reference guides

**Phase 3: Review and Refine**

Step 3.1: Code quality review:
- DRY principle (no duplication)
- Composability (shared logic extracted)
- Consistency (similar operations, similar formats)
- Error handling (all external calls protected)
- Type safety (full coverage)
- Documentation (comprehensive docstrings)

Step 3.2: Test and build:
- Python: `python -m py_compile server.py`
- TypeScript: `npm run build`
- Use evaluation harness for testing (servers are long-running processes)

Step 3.3: Use quality checklist from language-specific guide

**Phase 4: Create Evaluations**

Step 4.1: Understand evaluation purpose (test LLM effectiveness with tools)

Step 4.2: Create 10 evaluation questions through:
- Tool inspection
- Content exploration (read-only operations)
- Question generation (complex, realistic scenarios)
- Answer verification

Step 4.3: Ensure questions meet requirements:
- Independent (not dependent on other questions)
- Read-only (non-destructive operations only)
- Complex (multiple tool calls required)
- Realistic (based on real use cases)
- Verifiable (single, clear answer)
- Stable (answer won't change over time)

Step 4.4: Output evaluation XML file with question/answer pairs

## Technical Details
**Supported Frameworks:**
- Python: FastMCP (MCP Python SDK)
- TypeScript: MCP SDK (Official TypeScript implementation)

**MCP Protocol:**
- Tool registration and invocation
- Input validation with schemas
- Response formatting (JSON and Markdown)
- Tool annotations (hints for LLM behavior)
- Error handling and status codes

**Input Validation:**
- Python: Pydantic v2 models with constraints
- TypeScript: Zod schemas with `.strict()`

**Best Practices Implementation:**
- Character limits (e.g., 25,000 tokens)
- Pagination support
- Multiple response formats (concise vs. detailed)
- Human-readable identifiers (names over IDs)
- Actionable error messages

**Quality Assurance:**
- Syntax validation
- Import verification
- Build process checks
- Evaluation harness testing
- Quality checklists

**File Organization:**
```
mcp-server/
├── SKILL.md (main guide)
└── reference/
    ├── mcp_best_practices.md
    ├── python_mcp_server.md
    ├── node_mcp_server.md
    └── evaluation.md
```

## Best Practices
**Agent-Centric Design:**
- Design for complete workflows, not just API wrappers
- Consolidate related operations into single tools
- Optimize for limited context - return only high-signal information
- Provide concise and detailed response format options
- Use human-readable identifiers by default

**Error Handling:**
- Make errors educational and actionable
- Suggest specific next steps in error messages
- Guide agents toward correct usage patterns
- Handle rate limiting and timeout gracefully
- Provide clear authentication/authorization error messages

**Input/Output Design:**
- Use strict validation schemas (Pydantic/Zod)
- Include constraints (min/max, regex, ranges)
- Provide clear field descriptions with examples
- Plan for large-scale usage (thousands of resources)
- Implement character limits and truncation strategies

**Tool Documentation:**
- One-line summary of tool purpose
- Detailed explanation of functionality
- Explicit parameter types with diverse examples
- Complete return type schema
- Usage examples (when to use, when not to use)
- Error handling documentation with remediation steps

**Implementation Quality:**
- Extract shared logic into utilities (DRY principle)
- Use async/await for all I/O operations
- Implement consistent response formats
- Add appropriate tool annotations
- Maintain full type coverage

**Testing Strategy:**
- Create evaluations early in development
- Use realistic, complex questions
- Verify answers are stable and verifiable
- Test with evaluation harness (manages long-running server)
- Iterate based on agent performance

**Progressive Implementation:**
1. Core infrastructure first (API helpers, error handling)
2. Then implement individual tools
3. Code quality review
4. Testing and validation
5. Evaluation creation
6. Iteration based on real usage

**Resource Loading:**
- Load core MCP documentation first
- Load language-specific guides during implementation
- Fetch external SDK documentation as needed
- Load evaluation guide when creating tests
- Keep context lean by loading only what's needed

**Common Pitfalls to Avoid:**
- Don't just wrap API endpoints - design for workflows
- Don't return exhaustive data dumps - optimize for context
- Don't run server directly in main process (it will hang)
- Don't skip evaluations - they validate effectiveness
- Don't use generic error messages - make them actionable
