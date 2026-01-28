# Context Engineering Framework

## 5 Pillars of Context
1.  **Skills**: Capabilities of the agent (Tools, Languages).
2.  **Knowledge**: Persistent project information (Architecture, Stack).
3.  **Constraints**: What NOT to do (Anti-patterns, Security).
4.  **Examples**: Few-shot learning samples.
5.  **Feedback**: Iterative improvement loop.

## Best Practices (Gemini 3 + Claude)
- **Token Efficiency**: Use references instead of full copies.
- **Modularity**: Break down complex tasks into sub-agents or specific skill calls.
- **Context Loading**: Only load relevant skills/knowledge for the current task.
- **Structured Output**: Demand JSON or Markdown strict formats.
