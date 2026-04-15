---
name: claude-api
description: Build apps with the Claude API or Anthropic SDK. Use when writing code that imports anthropic, @anthropic-ai/sdk, or claude_agent_sdk, or when the user asks to use the Claude API.
---

# Claude API Development Guide

Build applications powered by the Claude API using the official Anthropic SDKs.

---

## When This Skill Activates

Trigger when:
- Code imports `anthropic`, `@anthropic-ai/sdk`, or `claude_agent_sdk`
- User asks to build with the Claude API, Anthropic SDK, or Claude agents
- User wants to add Claude to an existing application
- User asks about tool use, function calling, or streaming with Claude

NOT your scope:
- General programming unrelated to Claude
- Other AI SDKs (OpenAI, Gemini, etc.)
- ML/data science, model training, or fine-tuning

---

## Step 0: Load Context

Before writing code, determine:

1. **Language** — Python or TypeScript?
2. **What they're building** — Chatbot, agent, automation, document processor, etc.
3. **Key features needed** — Streaming? Tool use? Vision? Multi-turn?
4. **Environment** — API key set? SDK installed?

Ask if unclear. Then proceed with the correct patterns below.

---

## API Basics

| Field | Value |
|-------|-------|
| **Base URL** | `https://api.anthropic.com` |
| **Auth header** | `x-api-key: YOUR_API_KEY` |
| **API version** | `2023-06-01` |
| **Content type** | `application/json` |

### Model IDs

| Model | ID | Use Case |
|-------|-----|----------|
| Claude Opus 4.6 | `claude-opus-4-6` | Most capable — complex reasoning, coding, analysis |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | Balanced — fast and smart, best default |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | Fast and cheap — classification, extraction, simple tasks |

**Default to `claude-sonnet-4-6`** unless the user specifies otherwise or the task demands Opus-level reasoning.

---

## Python SDK

### Installation

```bash
pip install anthropic
```

### Basic Message

```python
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain quantum computing in one paragraph."}
    ]
)

print(message.content[0].text)
```

### With System Prompt

```python
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="You are a senior Python developer. Give concise, production-ready code.",
    messages=[
        {"role": "user", "content": "Write a retry decorator with exponential backoff."}
    ]
)
```

### Streaming

```python
with client.messages.stream(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write a short story about a robot."}
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Multi-Turn Conversation

```python
conversation = []

def chat(user_message: str) -> str:
    conversation.append({"role": "user", "content": user_message})

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=conversation
    )

    assistant_text = message.content[0].text
    conversation.append({"role": "assistant", "content": assistant_text})
    return assistant_text

# Usage
print(chat("What is Python?"))
print(chat("How does it compare to JavaScript?"))  # Claude remembers context
```

### Vision (Image Input)

```python
import base64
from pathlib import Path

# From file
image_data = base64.standard_b64encode(Path("photo.png").read_bytes()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": "Describe what you see in this image."
                }
            ]
        }
    ]
)

# From URL
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": "https://example.com/image.png"
                    }
                },
                {
                    "type": "text",
                    "text": "What is in this image?"
                }
            ]
        }
    ]
)
```

### Tool Use / Function Calling

```python
import json

tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a given location.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and state, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit"
                }
            },
            "required": ["location"]
        }
    }
]

# Step 1: Send message with tools
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "What's the weather in San Francisco?"}
    ]
)

# Step 2: Check if Claude wants to use a tool
if message.stop_reason == "tool_use":
    # Extract the tool call
    tool_block = next(b for b in message.content if b.type == "tool_use")
    tool_name = tool_block.name
    tool_input = tool_block.input

    # Step 3: Execute the tool (your code)
    def get_weather(location: str, unit: str = "fahrenheit") -> dict:
        # Your actual weather API call here
        return {"temperature": 62, "unit": "fahrenheit", "condition": "foggy"}

    result = get_weather(**tool_input)

    # Step 4: Send tool result back to Claude
    final_message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        tools=tools,
        messages=[
            {"role": "user", "content": "What's the weather in San Francisco?"},
            {"role": "assistant", "content": message.content},
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_block.id,
                        "content": json.dumps(result)
                    }
                ]
            }
        ]
    )

    print(final_message.content[0].text)
```

---

## TypeScript SDK

### Installation

```bash
npm install @anthropic-ai/sdk
```

### Basic Message

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic(); // reads ANTHROPIC_API_KEY from env

const message = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "Explain quantum computing in one paragraph." },
  ],
});

console.log(message.content[0].type === "text" ? message.content[0].text : "");
```

### Streaming

```typescript
const stream = client.messages.stream({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "Write a short story about a robot." },
  ],
});

for await (const event of stream) {
  if (
    event.type === "content_block_delta" &&
    event.delta.type === "text_delta"
  ) {
    process.stdout.write(event.delta.text);
  }
}
```

### Tool Use / Function Calling

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const tools: Anthropic.Tool[] = [
  {
    name: "get_weather",
    description: "Get the current weather for a given location.",
    input_schema: {
      type: "object" as const,
      properties: {
        location: {
          type: "string",
          description: "City and state, e.g. San Francisco, CA",
        },
        unit: {
          type: "string",
          enum: ["celsius", "fahrenheit"],
          description: "Temperature unit",
        },
      },
      required: ["location"],
    },
  },
];

// Step 1: Send message with tools
const message = await client.messages.create({
  model: "claude-sonnet-4-6",
  max_tokens: 1024,
  tools,
  messages: [
    { role: "user", content: "What's the weather in San Francisco?" },
  ],
});

// Step 2: Check for tool use
if (message.stop_reason === "tool_use") {
  const toolBlock = message.content.find(
    (b): b is Anthropic.ToolUseBlock => b.type === "tool_use"
  )!;

  // Step 3: Execute the tool
  const result = { temperature: 62, unit: "fahrenheit", condition: "foggy" };

  // Step 4: Send result back
  const finalMessage = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 1024,
    tools,
    messages: [
      { role: "user", content: "What's the weather in San Francisco?" },
      { role: "assistant", content: message.content },
      {
        role: "user",
        content: [
          {
            type: "tool_result",
            tool_use_id: toolBlock.id,
            content: JSON.stringify(result),
          },
        ],
      },
    ],
  });

  const textBlock = finalMessage.content.find(
    (b): b is Anthropic.TextBlock => b.type === "text"
  );
  console.log(textBlock?.text);
}
```

---

## Agent SDK (Multi-Step Agents)

The Agent SDK enables autonomous multi-step agents that can use tools, reason, and loop until a task is complete.

### Python Agent Loop

```python
import anthropic
import json

client = anthropic.Anthropic()

tools = [
    {
        "name": "search_docs",
        "description": "Search documentation by keyword.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path"},
                "content": {"type": "string", "description": "File content"}
            },
            "required": ["path", "content"]
        }
    }
]

def execute_tool(name: str, input: dict) -> str:
    """Route tool calls to your implementations."""
    if name == "search_docs":
        # Your search logic
        return json.dumps({"results": ["Doc 1: ...", "Doc 2: ..."]})
    elif name == "write_file":
        with open(input["path"], "w") as f:
            f.write(input["content"])
        return json.dumps({"status": "written", "path": input["path"]})
    else:
        return json.dumps({"error": f"Unknown tool: {name}"})

def run_agent(task: str, max_steps: int = 10) -> str:
    """Run an agentic loop: Claude reasons, calls tools, repeats until done."""
    messages = [{"role": "user", "content": task}]

    for step in range(max_steps):
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system="You are a helpful agent. Use the available tools to complete the task. When finished, respond with your final answer.",
            tools=tools,
            messages=messages
        )

        # If Claude is done (no more tool calls), return the text
        if response.stop_reason == "end_turn":
            text_blocks = [b.text for b in response.content if b.type == "text"]
            return "\n".join(text_blocks)

        # Process tool calls
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        messages.append({"role": "user", "content": tool_results})

    return "Agent hit max steps without completing."

# Usage
answer = run_agent("Search the docs for 'authentication' and write a summary to auth-guide.md")
print(answer)
```

### TypeScript Agent Loop

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const tools: Anthropic.Tool[] = [
  {
    name: "search_docs",
    description: "Search documentation by keyword.",
    input_schema: {
      type: "object" as const,
      properties: {
        query: { type: "string", description: "Search query" },
      },
      required: ["query"],
    },
  },
];

async function executeTool(
  name: string,
  input: Record<string, unknown>
): Promise<string> {
  if (name === "search_docs") {
    return JSON.stringify({ results: ["Doc 1: ...", "Doc 2: ..."] });
  }
  return JSON.stringify({ error: `Unknown tool: ${name}` });
}

async function runAgent(task: string, maxSteps = 10): Promise<string> {
  const messages: Anthropic.MessageParam[] = [
    { role: "user", content: task },
  ];

  for (let step = 0; step < maxSteps; step++) {
    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 4096,
      system:
        "You are a helpful agent. Use the available tools to complete the task.",
      tools,
      messages,
    });

    if (response.stop_reason === "end_turn") {
      return response.content
        .filter((b): b is Anthropic.TextBlock => b.type === "text")
        .map((b) => b.text)
        .join("\n");
    }

    messages.push({ role: "assistant", content: response.content });

    const toolResults: Anthropic.ToolResultBlockParam[] = [];
    for (const block of response.content) {
      if (block.type === "tool_use") {
        const result = await executeTool(
          block.name,
          block.input as Record<string, unknown>
        );
        toolResults.push({
          type: "tool_result",
          tool_use_id: block.id,
          content: result,
        });
      }
    }

    messages.push({ role: "user", content: toolResults });
  }

  return "Agent hit max steps without completing.";
}
```

---

## Best Practices

### Token Management

- Set `max_tokens` to the minimum needed for your use case
- Use Haiku for simple extraction/classification, Sonnet for general tasks, Opus for complex reasoning
- For long documents, chunk input rather than sending everything at once
- Monitor usage with `message.usage.input_tokens` and `message.usage.output_tokens`

### Error Handling

```python
import anthropic

try:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
except anthropic.AuthenticationError:
    print("Invalid API key. Check ANTHROPIC_API_KEY.")
except anthropic.RateLimitError:
    print("Rate limited. Implement backoff and retry.")
except anthropic.APIStatusError as e:
    print(f"API error {e.status_code}: {e.message}")
except anthropic.APIConnectionError:
    print("Network error. Check your connection.")
```

### Rate Limits & Retries

```python
import time
import anthropic

client = anthropic.Anthropic()

def call_with_retry(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                messages=messages
            )
        except anthropic.RateLimitError:
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # 1s, 2s, 4s
                time.sleep(wait)
            else:
                raise
```

### Cost Optimization

| Strategy | How |
|----------|-----|
| Use the right model | Haiku for simple tasks, Sonnet for most things, Opus only when needed |
| Minimize input tokens | Send only relevant context, not entire documents |
| Set tight `max_tokens` | Don't set 4096 if you need a one-line answer |
| Cache system prompts | Use prompt caching for repeated system prompts (reduces cost by 90%) |
| Batch requests | Use the Batch API for non-time-sensitive work (50% cost reduction) |

### Prompt Caching

```python
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert assistant with access to the following documentation: ...(long context)...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {"role": "user", "content": "Summarize the key points."}
    ]
)
```

---

## Common Patterns

### Chat Interface

Build a persistent chat that maintains history:

```python
class ChatSession:
    def __init__(self, system_prompt: str = "", model: str = "claude-sonnet-4-6"):
        self.client = anthropic.Anthropic()
        self.model = model
        self.system = system_prompt
        self.messages: list = []

    def send(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=self.system,
            messages=self.messages
        )

        assistant_text = response.content[0].text
        self.messages.append({"role": "assistant", "content": assistant_text})
        return assistant_text

    def reset(self):
        self.messages = []
```

### Document Analysis

```python
def analyze_document(text: str, question: str) -> str:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": f"Document:\n\n{text}\n\nQuestion: {question}"
            }
        ]
    )
    return message.content[0].text
```

### Structured Output (JSON)

```python
import json

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system="Always respond with valid JSON. No markdown, no explanation — just JSON.",
    messages=[
        {
            "role": "user",
            "content": "Extract the name, email, and company from this text: 'Hi, I'm Jane Smith from Acme Corp. Reach me at jane@acme.com'"
        }
    ]
)

data = json.loads(message.content[0].text)
# {"name": "Jane Smith", "email": "jane@acme.com", "company": "Acme Corp"}
```

### RAG (Retrieval-Augmented Generation)

```python
def rag_query(question: str, retrieved_chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(retrieved_chunks)

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system="Answer questions using ONLY the provided context. If the context doesn't contain the answer, say so.",
        messages=[
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )
    return message.content[0].text
```
