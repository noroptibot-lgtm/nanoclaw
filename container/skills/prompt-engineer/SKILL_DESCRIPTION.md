# Prompt Engineering (Senior Prompt Engineer)

## Overview

The Prompt Engineering skill provides world-class expertise in LLM optimization, prompt design patterns, structured outputs, and AI product development. This skill enables prompt engineers to design production-grade prompts, build agentic systems, optimize RAG (Retrieval-Augmented Generation) pipelines, and create sophisticated AI applications. It combines prompt patterns, evaluation frameworks, agent orchestration, and system architecture with deep expertise in Claude, GPT-4, and modern LLM frameworks.

## Who Should Use This Skill

- **Prompt Engineers** designing and optimizing LLM interactions
- **AI Product Engineers** building LLM-powered applications
- **ML Engineers** integrating LLMs into production systems
- **AI Researchers** exploring prompt engineering techniques
- **Product Managers** understanding LLM capabilities and limitations
- **Senior Engineers** architecting AI systems and agents
- **AI Consultants** advising on LLM implementation strategies
- **Developer Advocates** creating LLM developer experiences

## Purpose and Use Cases

Use this skill when you need to:
- Design and optimize prompts for specific tasks
- Build RAG (Retrieval-Augmented Generation) systems
- Create multi-agent AI systems
- Implement structured outputs from LLMs
- Evaluate and improve LLM performance
- Design few-shot and chain-of-thought prompting
- Build AI assistants and chatbots
- Optimize token usage and costs
- Implement prompt caching strategies
- Create prompt testing and evaluation frameworks
- Build LLM observability and monitoring
- Design conversation flows and context management

**Keywords that trigger this skill:** prompt engineering, LLM optimization, Claude, GPT-4, RAG, retrieval augmented generation, agents, agentic systems, few-shot learning, chain-of-thought, structured outputs, prompt patterns, AI evaluation

## What's Included

### Prompt Optimizer

**Prompt Design Patterns:**
- **Chain-of-Thought (CoT)** - Step-by-step reasoning
- **Few-Shot Learning** - Learning from examples
- **ReAct** - Reasoning and acting
- **Tree of Thoughts** - Exploring multiple reasoning paths
- **Self-Consistency** - Multiple reasoning paths with voting
- **Meta-Prompting** - LLM generating prompts
- **Prompt Chaining** - Breaking complex tasks into steps
- **Constitutional AI** - Value-aligned responses

**Optimization Capabilities:**
```bash
# Optimize prompt for task
python scripts/prompt_optimizer.py \
  --task summarization \
  --examples training-data.json \
  --model claude-3-5-sonnet \
  --optimize-for accuracy,cost

# A/B test prompts
python scripts/prompt_optimizer.py \
  --variants prompt-v1.txt,prompt-v2.txt \
  --test-cases test-data.json \
  --metrics accuracy,latency,cost

# Auto-generate few-shot examples
python scripts/prompt_optimizer.py \
  --task classification \
  --generate-examples 10 \
  --diversity high
```

**Optimization Features:**
- Automatic few-shot example selection
- Token optimization (reduce tokens while maintaining quality)
- Prompt compression techniques
- Cost-performance trade-off analysis
- Latency optimization
- Multi-model comparison
- Prompt versioning and tracking

### RAG Evaluator

**RAG Pipeline Components:**
```
Query → Embedding → Vector Search → Reranking → Context Assembly → LLM → Response
```

**Evaluation Metrics:**
- **Retrieval Quality:**
  - Recall@K (relevant docs retrieved)
  - Precision@K (relevant docs in top K)
  - MRR (Mean Reciprocal Rank)
  - NDCG (Normalized Discounted Cumulative Gain)

- **Generation Quality:**
  - Faithfulness (grounded in retrieved docs)
  - Answer relevance (addresses the query)
  - Context precision (relevant context used)
  - Context recall (all relevant context retrieved)

- **System Performance:**
  - End-to-end latency
  - Cost per query
  - Token usage
  - Cache hit rate

**RAG Optimization:**
```bash
# Evaluate RAG pipeline
python scripts/rag_evaluator.py \
  --pipeline-config rag-config.yaml \
  --test-queries test-queries.json \
  --output evaluation-report.html

# Optimize chunk size
python scripts/rag_evaluator.py \
  --optimize chunk-size \
  --range 256,512,1024,2048 \
  --metric retrieval-precision

# Tune reranking
python scripts/rag_evaluator.py \
  --optimize reranking \
  --models cohere-rerank,bge-reranker \
  --top-k 5,10,20

# Benchmark embeddings
python scripts/rag_evaluator.py \
  --compare-embeddings \
  --models openai-ada,cohere-embed,bge-large \
  --metric recall@10
```

**RAG Architecture Patterns:**
- **Basic RAG** - Simple retrieval + generation
- **Advanced RAG** - Query rewriting, reranking, filtering
- **Agentic RAG** - Multi-step reasoning with tool use
- **Corrective RAG** - Self-correction and verification
- **Self-RAG** - Self-reflection and adaptive retrieval
- **Hybrid Search** - Combining dense and sparse retrieval

### Agent Orchestrator

**Agent Architectures:**
- **ReAct Agent** - Reasoning and acting in interleaved manner
- **Tool-Using Agent** - Calling external tools and APIs
- **Multi-Agent System** - Specialized agents collaborating
- **Hierarchical Agent** - Manager-worker delegation
- **Reflexion Agent** - Self-reflection and improvement

**Agent Components:**
```python
# Agent structure
{
  "system_prompt": "You are an expert assistant...",
  "tools": [
    {
      "name": "web_search",
      "description": "Search the web for current information",
      "parameters": {...}
    },
    {
      "name": "calculator",
      "description": "Perform mathematical calculations",
      "parameters": {...}
    }
  ],
  "memory": {
    "type": "conversation_buffer",
    "max_messages": 10
  },
  "stopping_criteria": {
    "max_iterations": 5,
    "max_tokens": 4000
  }
}
```

**Orchestration Features:**
```bash
# Create agent
python scripts/agent_orchestrator.py create \
  --name research-agent \
  --tools web_search,calculator,code_executor \
  --memory-type conversation_summary

# Run agent
python scripts/agent_orchestrator.py run \
  --agent research-agent \
  --task "Research the latest developments in quantum computing" \
  --trace-output trace.json

# Multi-agent orchestration
python scripts/agent_orchestrator.py orchestrate \
  --agents researcher,writer,reviewer \
  --task "Write a comprehensive article about AI safety" \
  --coordination sequential

# Agent evaluation
python scripts/agent_orchestrator.py evaluate \
  --agent research-agent \
  --test-cases agent-test-cases.json \
  --metrics success_rate,steps,cost
```

**Agent Capabilities:**
- Tool calling and function execution
- Memory management (short-term, long-term)
- Planning and task decomposition
- Self-correction and error recovery
- Multi-turn conversation
- Context management
- Parallel tool execution
- Agent collaboration

## How It Works

### Prompt Optimization Workflow

**Step 1: Define Task and Success Criteria**
```yaml
# task-config.yaml
task:
  name: "Document Summarization"
  type: "text-to-text"
  input_format: "long-form document"
  output_format: "structured summary"

success_criteria:
  - metric: "faithfulness"
    target: "> 0.9"
  - metric: "conciseness"
    target: "< 30% of input length"
  - metric: "cost"
    target: "< $0.01 per summary"

evaluation_set: "eval-documents.json"
```

**Step 2: Generate and Test Prompt Variants**
```bash
# Generate prompt variants
python scripts/prompt_optimizer.py \
  --task-config task-config.yaml \
  --generate-variants 10 \
  --techniques cot,few-shot,meta-prompting

# Test variants
python scripts/prompt_optimizer.py \
  --variants generated-prompts/ \
  --evaluate \
  --test-set eval-documents.json
```

**Step 3: Review Optimization Results**
```
PROMPT OPTIMIZATION RESULTS
============================

Task: Document Summarization
Variants Tested: 10
Evaluation Set: 50 documents

Best Performing Prompt: variant-7 (Few-Shot + CoT)
---------------------------------------------------

Performance Metrics:
  Faithfulness: 0.94 ✓ (target: > 0.9)
  Conciseness:  28% ✓ (target: < 30%)
  Cost:         $0.008 ✓ (target: < $0.01)
  Latency:      1.2s
  Token Usage:  425 tokens avg

Prompt:
-------
You are an expert at creating concise, accurate summaries of documents.

Follow these steps:
1. Identify the main topic and key points
2. Note supporting details and evidence
3. Organize into a structured summary

Format your summary as:
- Main Topic: [topic]
- Key Points:
  - [point 1]
  - [point 2]
  - [point 3]
- Conclusion: [conclusion]

Focus on factual accuracy. Do not add information not present in the document.

Examples:
[3 high-quality examples]

Document to summarize:
{document}

Comparison with Baseline:
-------------------------
Baseline (simple prompt):
  Faithfulness: 0.78 (-16%)
  Conciseness:  42% (-33%)
  Cost:         $0.015 (-47%)

Improvement Summary:
--------------------
✓ 21% better faithfulness
✓ 33% more concise
✓ 47% cost reduction
✓ Consistent quality across document types

Recommended Actions:
--------------------
1. Deploy variant-7 to production
2. Monitor performance on live traffic
3. Collect edge cases for further fine-tuning
4. A/B test against current production prompt
```

**Step 4: Deploy and Monitor**
```bash
# Deploy optimized prompt
python scripts/prompt_optimizer.py deploy \
  --variant variant-7 \
  --environment production \
  --rollout gradual \
  --monitor-metrics faithfulness,cost

# Monitor performance
python scripts/prompt_optimizer.py monitor \
  --environment production \
  --alert-threshold "faithfulness < 0.9" \
  --dashboard-url https://monitoring.example.com
```

### RAG System Evaluation Workflow

**Step 1: Set Up RAG Pipeline**
```yaml
# rag-config.yaml
indexing:
  chunk_size: 512
  chunk_overlap: 50
  embedding_model: "text-embedding-3-large"

retrieval:
  top_k: 10
  similarity_metric: "cosine"
  hybrid_search:
    enabled: true
    sparse_weight: 0.3
    dense_weight: 0.7

reranking:
  enabled: true
  model: "cohere-rerank-v3"
  top_n: 3

generation:
  model: "claude-3-5-sonnet-20241022"
  temperature: 0.1
  max_tokens: 1000
  system_prompt: |
    You are a helpful assistant. Answer questions based on the provided context.
    If the answer is not in the context, say "I don't have enough information to answer that."
```

**Step 2: Evaluate RAG Performance**
```bash
# Comprehensive RAG evaluation
python scripts/rag_evaluator.py \
  --config rag-config.yaml \
  --test-set qa-test-set.json \
  --output-report rag-evaluation.html

# Test set format:
# [
#   {
#     "query": "What is the capital of France?",
#     "ground_truth_answer": "Paris",
#     "ground_truth_docs": ["doc_id_1", "doc_id_2"]
#   },
#   ...
# ]
```

**Step 3: Review Evaluation Results**
```
RAG PIPELINE EVALUATION
========================

Configuration: rag-config.yaml
Test Set: 100 queries
Evaluation Date: 2025-11-13

RETRIEVAL METRICS
=================

Recall@10: 0.87
  - 87% of relevant documents retrieved in top 10
  - Target: > 0.85 ✓

Precision@3: 0.76
  - 76% of top 3 documents are relevant
  - Target: > 0.70 ✓

MRR (Mean Reciprocal Rank): 0.68
  - Average position of first relevant doc: 1.47
  - Target: > 0.65 ✓

NDCG@10: 0.81
  - Quality of ranking: Good
  - Target: > 0.75 ✓

GENERATION METRICS
==================

Faithfulness: 0.91
  - 91% of answers are grounded in retrieved docs
  - Target: > 0.90 ✓

Answer Relevance: 0.88
  - 88% of answers address the query
  - Target: > 0.85 ✓

Context Precision: 0.79
  - 79% of context is relevant to answer
  - Target: > 0.75 ✓

Context Recall: 0.84
  - 84% of ground truth info is retrieved
  - Target: > 0.80 ✓

SYSTEM PERFORMANCE
==================

Latency (P50): 1.8s
Latency (P95): 3.2s
Latency (P99): 4.5s

Cost per Query: $0.023
Token Usage (Avg): 1,247 tokens

Cache Hit Rate: 34%

FAILURE ANALYSIS
================

Retrieval Failures (13 queries):
  - 8 queries: Relevant docs not in knowledge base
  - 3 queries: Query too ambiguous
  - 2 queries: Embedding mismatch

Generation Failures (9 queries):
  - 5 queries: Hallucination (not grounded in context)
  - 3 queries: Incomplete answer
  - 1 query: Misinterpretation of context

OPTIMIZATION RECOMMENDATIONS
=============================

High Priority:
1. Add missing documents to knowledge base (8 queries)
2. Implement query clarification for ambiguous queries
3. Improve prompt to reduce hallucinations (5 queries)

Medium Priority:
4. Increase chunk overlap to 100 tokens
5. Experiment with query expansion
6. Add citation requirements to prompt

Low Priority:
7. Optimize cache hit rate (current: 34%, target: 50%)
8. Consider hybrid search weight tuning

Estimated Impact:
- Fixing high priority items: +8% performance
- All recommendations: +12% performance
```

**Step 4: Optimize Based on Results**
```bash
# Optimize chunk size
python scripts/rag_evaluator.py optimize \
  --parameter chunk_size \
  --range 256,512,1024 \
  --metric context_precision

# Optimize reranking
python scripts/rag_evaluator.py optimize \
  --parameter reranking_top_n \
  --range 1,3,5,10 \
  --metric answer_relevance

# Test improved configuration
python scripts/rag_evaluator.py \
  --config rag-config-optimized.yaml \
  --test-set qa-test-set.json \
  --compare-with rag-evaluation.html
```

### Agent System Development Workflow

**Step 1: Design Agent Architecture**
```python
# agent-config.yaml
agent:
  name: "research-assistant"
  model: "claude-3-5-sonnet-20241022"

  system_prompt: |
    You are a research assistant that helps users find and analyze information.

    You have access to the following tools:
    - web_search: Search the internet for current information
    - calculator: Perform mathematical calculations
    - code_executor: Execute Python code

    Your process:
    1. Understand the user's request
    2. Plan your approach
    3. Use tools as needed
    4. Synthesize findings
    5. Present clear, well-sourced answers

    Always cite your sources and show your reasoning.

  tools:
    - name: "web_search"
      api: "tavily"
      max_results: 5

    - name: "calculator"
      type: "builtin"

    - name: "code_executor"
      runtime: "python"
      timeout: 30
      allowed_libraries: ["pandas", "numpy", "matplotlib"]

  memory:
    type: "conversation_summary"
    max_messages: 20
    summary_threshold: 10

  constraints:
    max_iterations: 10
    max_tool_calls: 15
    max_tokens: 4000
    timeout: 120

  error_handling:
    max_retries: 3
    fallback_to_direct_answer: true
```

**Step 2: Implement and Test Agent**
```bash
# Create agent
python scripts/agent_orchestrator.py create \
  --config agent-config.yaml

# Test agent with sample queries
python scripts/agent_orchestrator.py test \
  --agent research-assistant \
  --queries test-queries.json \
  --trace-output traces/

# Example query:
# "What is the current price of Bitcoin and how does it compare to its
#  all-time high? Create a simple visualization showing the price trend."
```

**Step 3: Review Agent Execution Trace**
```
AGENT EXECUTION TRACE
======================

Query: "What is the current price of Bitcoin and how does it compare to
        its all-time high? Create a simple visualization."

Agent: research-assistant
Execution Time: 8.3 seconds
Total Cost: $0.042
Iterations: 3
Tool Calls: 5

STEP 1: Planning
----------------
Thought: "I need to find the current Bitcoin price, find its all-time high,
          compare them, and create a visualization. I'll use web search for
          current data and historical ATH, then use code to visualize."

STEP 2: Tool Use - web_search
------------------------------
Input: "Bitcoin current price USD"
Result:
  - Current price: $43,250 (as of 2025-11-13 14:30 UTC)
  - Source: CoinMarketCap

Cost: $0.005
Latency: 1.2s

STEP 3: Tool Use - web_search
------------------------------
Input: "Bitcoin all-time high price when"
Result:
  - All-time high: $68,789 (November 10, 2021)
  - Source: CoinGecko

Cost: $0.005
Latency: 1.1s

STEP 4: Tool Use - calculator
------------------------------
Input: ((43250 - 68789) / 68789) * 100
Result: -37.13%

Cost: $0.001
Latency: 0.1s

STEP 5: Tool Use - code_executor
---------------------------------
Input:
  ```python
  import matplotlib.pyplot as plt
  import numpy as np

  dates = ['ATH (Nov 2021)', 'Today (Nov 2025)']
  prices = [68789, 43250]

  plt.figure(figsize=(10, 6))
  plt.bar(dates, prices, color=['red', 'green'])
  plt.ylabel('Price (USD)')
  plt.title('Bitcoin: All-Time High vs Current Price')
  plt.ylim(0, 75000)

  for i, price in enumerate(prices):
      plt.text(i, price + 2000, f'${price:,}', ha='center')

  plt.tight_layout()
  plt.savefig('bitcoin_comparison.png')
  ```

Result: Successfully created visualization
Output: bitcoin_comparison.png

Cost: $0.008
Latency: 2.3s

STEP 6: Final Response
-----------------------
Agent Response:
  "Based on current data:

  Bitcoin Current Price: $43,250 (as of Nov 13, 2025)
  All-Time High: $68,789 (Nov 10, 2021)

  Comparison: Bitcoin is currently 37.13% below its all-time high.

  I've created a visualization comparing these values (see attached chart).

  Sources:
  - Current price: CoinMarketCap
  - ATH data: CoinGecko"

Cost: $0.023
Latency: 3.6s

EXECUTION SUMMARY
=================

Success: ✓
Total Iterations: 3
Total Tool Calls: 5
  - web_search: 2 calls
  - calculator: 1 call
  - code_executor: 1 call

Performance:
  Total Time: 8.3s
  Total Cost: $0.042
  Average Tool Latency: 1.2s

Quality Metrics:
  Answer Completeness: 100%
  Source Citations: ✓
  Reasoning Clarity: ✓
  Tool Usage Efficiency: Good
```

**Step 4: Deploy Agent to Production**
```bash
# Deploy agent
python scripts/agent_orchestrator.py deploy \
  --agent research-assistant \
  --environment production \
  --scaling auto \
  --monitoring enabled

# Monitor agent performance
python scripts/agent_orchestrator.py monitor \
  --agent research-assistant \
  --metrics success_rate,latency,cost,tool_usage
```

## Technical Details

### Prompt Engineering Techniques

**Chain-of-Thought (CoT):**
```
Prompt: "Let's solve this step by step:
1. First, identify what we know
2. Then, determine what we need to find
3. Finally, work through the solution

Problem: ..."
```

**Few-Shot Learning:**
```
Prompt: "Here are some examples:

Example 1:
Input: ...
Output: ...

Example 2:
Input: ...
Output: ...

Now solve:
Input: ..."
```

**ReAct Pattern:**
```
Prompt: "Solve this using the ReAct framework:

Thought: [Your reasoning]
Action: [Action to take]
Observation: [Result of action]
Thought: [Updated reasoning]
... (repeat until solved)
Final Answer: [Your answer]"
```

### Structured Outputs

```python
# Using Claude's structured outputs
from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Extract information about this person: John Doe, 35 years old, software engineer at Tech Corp."
    }],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "person_info",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                    "occupation": {"type": "string"},
                    "company": {"type": "string"}
                },
                "required": ["name", "age", "occupation"]
            }
        }
    }
)
```

### RAG Best Practices

**Chunk Size Optimization:**
```
Small chunks (256-512 tokens):
  ✓ More precise retrieval
  ✓ Lower token cost
  ✗ May lose context

Large chunks (1024-2048 tokens):
  ✓ More context preserved
  ✗ Less precise retrieval
  ✗ Higher token cost

Recommendation: Start with 512, tune based on use case
```

**Hybrid Search:**
```python
# Combine dense (semantic) and sparse (keyword) search
results = vector_store.hybrid_search(
    query=query,
    dense_weight=0.7,  # Semantic similarity
    sparse_weight=0.3,  # Keyword matching
    top_k=10
)
```

### Agent Design Patterns

**Tool Schema:**
```json
{
  "name": "web_search",
  "description": "Search the web for current information. Use this when you need up-to-date facts, news, or information not in your training data.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The search query"
      },
      "num_results": {
        "type": "integer",
        "description": "Number of results to return (default: 5)",
        "default": 5
      }
    },
    "required": ["query"]
  }
}
```

## Use Cases and Examples

### Building a Customer Support Agent

**Scenario:** AI agent that handles customer support queries with access to knowledge base and ticketing system

**Implementation:**
```python
agent = Agent(
    name="support-agent",
    model="claude-3-5-sonnet",
    system_prompt="""
    You are a helpful customer support agent. Your goal is to resolve
    customer issues efficiently and courteously.

    Process:
    1. Understand the customer's issue
    2. Search the knowledge base for relevant information
    3. If you can resolve it, provide a clear solution
    4. If escalation is needed, create a support ticket

    Always be empathetic and professional.
    """,
    tools=[
        knowledge_base_search_tool,
        create_ticket_tool,
        check_order_status_tool,
        process_refund_tool
    ],
    memory=ConversationBufferMemory(max_messages=20)
)
```

### Optimizing RAG for Technical Documentation

**Scenario:** RAG system for querying technical documentation with high accuracy requirements

**Optimizations Applied:**
- Increased chunk overlap to preserve context
- Implemented query rewriting for technical terms
- Added code block-aware chunking
- Implemented multi-query retrieval
- Added reranking with technical domain model
- Implemented citation tracking

**Results:**
- Faithfulness: 0.78 → 0.95 (+22%)
- Answer relevance: 0.82 → 0.93 (+13%)
- Latency: 2.3s → 1.9s (-17%)

## Best Practices

### Prompt Engineering Best Practices

**Do:**
- Start with clear, specific instructions
- Use examples (few-shot learning)
- Break complex tasks into steps (chain-of-thought)
- Specify output format explicitly
- Test prompts with diverse inputs
- Version and track prompt changes
- Measure performance with metrics

**Don't:**
- Use ambiguous language
- Assume the model has context it doesn't
- Over-engineer prompts prematurely
- Forget to test edge cases
- Ignore cost and latency
- Skip evaluation

### RAG Best Practices

**Do:**
- Optimize chunk size for your use case
- Use hybrid search (dense + sparse)
- Implement reranking
- Cache embeddings
- Monitor retrieval quality
- Add citations to responses
- Handle "I don't know" gracefully

**Don't:**
- Use default settings without testing
- Ignore retrieval quality metrics
- Skip reranking (it significantly helps)
- Forget about token costs
- Allow hallucinations
- Ignore data quality

### Agent Development Best Practices

**Do:**
- Design clear tool interfaces
- Implement error handling and retries
- Set iteration limits
- Log all agent actions
- Test extensively before production
- Monitor agent behavior
- Implement human-in-the-loop for critical actions

**Don't:**
- Give agents unbounded autonomy
- Skip error handling
- Ignore cost implications
- Deploy without monitoring
- Forget about security
- Over-complicate agent logic

## Integration Points

This skill integrates with:
- **LLM APIs:** Claude (Anthropic), GPT-4 (OpenAI), Gemini (Google)
- **LLM Frameworks:** LangChain, LlamaIndex, DSPy, Haystack
- **Vector Databases:** Pinecone, Weaviate, Qdrant, ChromaDB
- **Embeddings:** OpenAI, Cohere, Voyage, BGE models
- **Observability:** LangSmith, Helicone, Weights & Biases
- **Evaluation:** RAGAS, TruLens, DeepEval
- **Deployment:** AWS Bedrock, Azure OpenAI, GCP Vertex AI

## Common Challenges and Solutions

### Challenge: High Token Costs
**Solution:** Implement prompt compression, use caching, optimize context length, use cheaper models for simple tasks, batch requests where possible

### Challenge: Inconsistent Output Quality
**Solution:** Add structured outputs, use few-shot examples, implement validation, add self-consistency checks, fine-tune for specific tasks

### Challenge: RAG Hallucinations
**Solution:** Improve retrieval quality, add explicit grounding instructions, implement citation requirements, add verification steps, use confidence scores

### Challenge: Slow Agent Response Times
**Solution:** Implement parallel tool calling, cache frequent queries, optimize tool execution, use streaming responses, reduce unnecessary iterations

### Challenge: Agent Getting Stuck in Loops
**Solution:** Set iteration limits, implement loop detection, add progress tracking, improve planning prompts, add escape conditions

### Challenge: Poor RAG Retrieval
**Solution:** Optimize chunk size, use hybrid search, improve query rewriting, add metadata filtering, implement query expansion, tune embedding model
