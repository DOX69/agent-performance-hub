# Anthropic & Agent Behavior Guidelines

This document outlines best practices for how you, the AI agent, should parse instructions, structure your thoughts, and format logic based on Anthropic's prompt engineering guidelines.

## 1. Context Engineering & Memory Usage
- **Maximize Signal, Minimize Noise:** Actively select relevant tools and context. Do not pull the entire project history if only a single module is relevant.
- **Utilize Knowledge Items (KIs):** Always proactively scan available KI summaries at the start of complex tasks to prevent redundant research. A KI acts as persistent memory across sessions.
- **Reference Over Reconstruction:** If an implementation strategy already exists in an artifact (e.g., an implementation plan or previous architectural document), use it rather than generating a new approach from scratch.

## 2. Structured Outputs & Clarity
- **Use Markdown:** Consistently use GitHub-flavored markdown. Use backticks for inline code, files, or symbols. 
- **XML Tagging for Tool Context:** While parsing context, leverage `<blocks>` internally to represent segments of logic. Format your artifacts concisely.
- **Explicitness:** Avoid vague intentions. When leaving comments or explaining code, be concrete. Instead of "optimized this function," state "*Reduced time complexity from O(n^2) to O(n) by using a hash map.*"

## 3. Mitigating Agent Limitations
- **Chunking:** Break down large tasks into smaller, atomic tasks. If a task requires editing 10 files, edit and verify them in reasonable batches (e.g., 2-3 at a time) to avoid cognitive overload and context dropping.
- **Verification (Self-Correction):** After making an edit, verify your own output. If tests fail or code linting complains, correct it autonomously. Ask yourself, "Did my last tool call do exactly what I intended?"
- **Scaffolding:** Provide clear intermediate steps when communicating with the user. If building a multi-part feature, outline the parts before starting.
