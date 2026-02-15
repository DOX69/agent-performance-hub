# Prompt Patterns

## System Prompt Template
```markdown
You are an expert software engineer specialized in [STACK].
Your goal is to [GOAL].

Context:
- Architecture: [LINK to project-architecture.md]
- Tech Stack: [LINK to tech-stack.md]

Constraints:
- [Constraint 1]
- [Constraint 2]

Output Format:
[Format Definition]
```

## Few-Shot Pattern
User: "Create a button."
Assistant: "<button className='btn-primary'>Click Me</button>"
User: "Create a card."
Assistant: "<div className='card'>...</div>"

## Chain-of-Thought
"Think step-by-step:
1. Analyze the requirements.
2. Identify necessary components.
3. Draft the code.
4. Review against constraints."
