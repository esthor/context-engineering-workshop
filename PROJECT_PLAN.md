# Project Plan

This is an example application to demonstrate highly modularized LLM applications.

The focus is on "Context Engineering", specifically with minimized context window ai agents. Each llm invocation will have the smallest possible scope and context used.

## Project Structure

### Resources

Within `/resources` are all the main sources of context. Most are static (e.g., reference documents and other materials).

### Prompts

Within `/prompts` are all the prompts used by agents throughout the application.

### Agents

Within `/agents` we compose together the context from the resources with the prompts of each context/task-specific component of the larger system. This is where the application really comes together. Each domain (framework, training material, reviewer and reviewee specific information) is synthesized and converted to match the performance review schema. This is further reviewed by another agent to ensure it is a good performance review.
