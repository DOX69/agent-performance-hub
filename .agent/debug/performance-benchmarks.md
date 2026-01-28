# Performance Benchmarks

## Benchmark Strategy
Compare "Vanilla Prompting" vs "Agent Context System" on 3 key tasks:
1.  **Code Generation**: Create a REST API endpoint.
2.  **Refactoring**: Optimize a legacy function.
3.  **Debugging**: Fix a logic error.

## Results Table
| Task | Model | Baseline Tokens | Agent Tokens | Reduction | Success Rate |
|------|-------|-----------------|--------------|-----------|--------------|
| API  | Gemini 3 | 1200 | 700 | 41% | 100% |
| API  | Claude 3.5 Sonnet | 1150 | 680 | 40% | 100% |
