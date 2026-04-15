# Web Testing (webapp-testing)

## Overview
The Web Testing skill provides a comprehensive toolkit for interacting with and testing local web applications using Playwright. It supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, viewing browser logs, and automating complex user interactions with both static and dynamic web applications.

## Who Should Use This Skill
- Frontend developers testing web applications
- QA engineers automating test scenarios
- Full-stack developers debugging UI behavior
- DevOps engineers verifying deployment functionality
- Product managers validating feature implementations
- Anyone who needs to interact with or test web applications programmatically

## Purpose and Use Cases
Use this skill when you need to test, debug, or interact with local web applications through browser automation.

**Keywords:** web testing, browser automation, Playwright, frontend testing, UI testing, test webapp, verify functionality, debug UI, browser screenshots, console logs

**Common use cases:**
- Testing dynamic web applications (React, Vue, Angular apps)
- Verifying static HTML page functionality
- Debugging UI behavior and interactions
- Capturing screenshots for visual verification
- Inspecting console logs and network requests
- Automating form submissions and user flows
- Testing multi-page workflows
- Verifying element visibility and interactions

## What's Included
This skill provides a complete toolkit for browser automation and testing:

**Helper Scripts:**
- `scripts/with_server.py`: Manages server lifecycle for testing
  - Supports single or multiple concurrent servers
  - Handles startup, health checks, and cleanup
  - Allows testing frontend + backend together

**Reference Examples (`examples/` directory):**
- `element_discovery.py`: Discovering buttons, links, and inputs on a page
- `static_html_automation.py`: Using file:// URLs for local HTML testing
- `console_logging.py`: Capturing console logs during automation

**Key Capabilities:**
- Native Python Playwright script support
- Server lifecycle management (startup/shutdown)
- Multi-server support (frontend + backend simultaneously)
- Screenshot capture (full page or element-specific)
- DOM inspection and element discovery
- Console log capture
- Network request monitoring
- Form filling and interaction automation

## How It Works
The skill uses a decision tree approach to handle different testing scenarios:

**Decision Tree:**
```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Use with_server.py helper + simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

**Workflow for Dynamic Webapps:**

**Step 1: Server Management (if needed)**
```bash
# Single server
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_test.py

# Multiple servers (backend + frontend)
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_test.py
```

**Step 2: Playwright Script**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')  # CRITICAL for dynamic apps
    # ... test logic
    browser.close()
```

**Step 3: Reconnaissance-Then-Action Pattern**
1. Inspect rendered DOM (screenshot, page.content(), locators)
2. Identify selectors from inspection results
3. Execute actions using discovered selectors

## Technical Details
**Technology Stack:**
- Playwright for browser automation
- Python for scripting
- Chromium browser (headless mode)

**Server Lifecycle Management:**
- `with_server.py` handles server startup and health checks
- Supports multiple concurrent servers with different ports
- Automatic cleanup on script completion or failure
- Servers run in background, isolated from main process

**Playwright Capabilities:**
- Synchronous API (`sync_playwright()`)
- Page navigation and waiting strategies
- Element selection (text=, role=, CSS selectors, IDs)
- Screenshot capture (full page or element-specific)
- Console log monitoring
- Network request tracking
- Form filling and interaction

**Critical Requirements:**
- Always launch Chromium in headless mode: `launch(headless=True)`
- Wait for `networkidle` before inspecting dynamic apps
- Close browser when done to release resources
- Use black-box approach with bundled scripts (run with `--help` first)

## Best Practices
**Server Management:**
- Always run `--help` first on helper scripts to see usage
- Use `with_server.py` for managing development servers
- Don't read script source unless absolutely necessary (keeps context clean)
- Support multiple servers when testing full-stack apps

**Playwright Scripting:**
- Use `sync_playwright()` for synchronous, readable scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `wait_for_selector()` or `wait_for_timeout()`
- Wait for `networkidle` before inspection on dynamic apps

**Common Pitfall to Avoid:**
- **Don't**: Inspect DOM before waiting for `networkidle` on dynamic apps
- **Do**: Always `page.wait_for_load_state('networkidle')` before inspection

**Static vs Dynamic Approach:**
- **Static HTML**: Read file directly, identify selectors, write script
- **Dynamic apps**: Use reconnaissance-then-action pattern with networkidle wait

**Element Discovery:**
- Take screenshots first for visual context
- Use `page.content()` to see full rendered HTML
- Use `page.locator('button').all()` to find all elements of a type
- Prefer stable selectors (IDs, roles, data attributes) over CSS classes

**Script Organization:**
- Keep test logic separate from server management
- Use bundled example scripts as reference
- Create reusable functions for common patterns
- Handle errors gracefully with try/finally for browser cleanup

**Debugging:**
- Capture screenshots at each step for visual debugging
- Monitor console logs: `page.on("console", lambda msg: print(msg.text))`
- Check network requests for API failures
- Use `page.pause()` during development for interactive debugging
