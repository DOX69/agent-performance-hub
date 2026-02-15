# Agentic Context Engineering (ACE)

## 🎯 Purpose
To implement the **Agentic Context Engineering (ACE)** pattern, which involves using structured, evolving, and detailed contexts to enable more effective agent learning and performance than fixed demonstrations (ICL) or single optimized prompts.

## 🛠️ Mechanism
ACE replaces static prompts with a dynamic context management system that:
1.  **Initializes** with a structured goal and constraints.
2.  **Evolves** the context based on intermediate steps and feedback.
3.  **Retains** key insights while discarding irrelevant history (context pruning).

## 📋 Implementation Pattern

### 1. Structure
Divide the context into:
- **System Role**: Immutable core directives.
- **Dynamic State**: Current variables, progress, and known facts.
- **Task Queue**: Pending actions.
- **History**: Summarized past actions (not raw logs).

### 2. Prompt Template (Example)
```markdown
# System
You are an autonomous coding agent using ACE.

# State
- **Current Goal**: Scrape data from example.com
- **Progress**: 20%
- **Tools Available**: Requests, BeautifulSoup

# History (Summarized)
- Tried getting /login, failed (403).
- Switched to using User-Agent header. Success (200).

# Task Queue
1. Parse HTML for product links.
2. Save to JSON.

# Action
Execute next task from Queue.
```

## 🚀 Benefits
- **Higher Accuracy**: 12.3% improvement over ReAct + ICL.
- **Self-Improvement**: Agent learns from the "History" summary.
- **Token Efficiency**: Pruning keeps context within limits while retaining signal.

## ⚠️ When to Use
- Multi-step complex tasks (e.g., scraping, refactoring).
- Long-running sessions where context window limits are a concern.
