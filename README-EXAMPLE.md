# Context Engineering Workshop - Example System

This is a demonstration of **Context Engineering** principles for building modular LLM applications.

## 🎯 Core Principle

**Minimize context in each LLM invocation.** Instead of dumping all resources into one massive prompt, we use specialized agents that each process only what they need.

## 📁 Project Structure

```
context-engineering-workshop/
├── resources/              # Source data (minimal context per agent)
│   ├── company/           # Company-wide materials
│   │   ├── training-materials/
│   │   │   ├── performance-review-guidelines.md
│   │   │   └── calibration-guidelines.md
│   │   └── level-expectations.md
│   ├── reviewee/          # Employee-specific information
│   │   ├── employee-profile.md
│   │   └── work-history-h2-2024.md
│   ├── manager/           # Manager observations
│   │   ├── 1on1-notes-h2-2024.md
│   │   └── peer-feedback.md
│   └── schema/            # Output schema
│       └── schema.md
│
├── prompts/               # Task-specific prompts
│   ├── extract-framework.md
│   ├── extract-employee-context.md
│   ├── extract-manager-insights.md
│   ├── synthesize-review.md
│   └── review-quality-check.md
│
├── agents/                # Specialized agents (each with minimal context)
│   ├── framework-agent.py
│   ├── employee-agent.py
│   ├── manager-agent.py
│   ├── synthesis-agent.py
│   └── reviewer-agent.py
│
└── orchestrator.py        # Coordinates the agent pipeline
```

## 🔄 Agent Pipeline

### Traditional Approach ❌
```
All Resources (50K+ tokens) → Single LLM Call → Review
```
**Problems:** Expensive, slow, model may miss details in large context

### Context-Engineered Approach ✅
```
Company Docs → FrameworkAgent → Framework Summary (500 tokens)
Employee Files → EmployeeAgent → Accomplishments (800 tokens)
Manager Notes → ManagerAgent → Insights (800 tokens)
                        ↓
         [3 Condensed Summaries (2.1K tokens)]
                        ↓
              SynthesisAgent → Draft Review
                        ↓
              ReviewerAgent → Quality Check
```
**Benefits:** Fast, cheap, focused, debuggable

## 🤖 The Agents

### 1. FrameworkAgent
- **Context:** Company training materials only
- **Task:** Extract evaluation dimensions, rating scale, guidelines
- **Output:** Structured framework (~500 tokens)

### 2. EmployeeAgent
- **Context:** Employee profile and work history only
- **Task:** Extract accomplishments, projects, skills, impact
- **Output:** Factual summary of employee's work (~800 tokens)

### 3. ManagerAgent
- **Context:** 1:1 notes and peer feedback only
- **Task:** Extract themes, insights, stories, growth trajectory
- **Output:** Qualitative insights (~800 tokens)

### 4. SynthesisAgent
- **Context:** Condensed outputs from agents 1-3
- **Task:** Write complete performance review following framework
- **Output:** Draft review (~2000 tokens)

### 5. ReviewerAgent
- **Context:** Draft review + framework
- **Task:** Quality check against guidelines
- **Output:** Assessment and recommendations (~1500 tokens)

## 🚀 Running the Example

```bash
# View the orchestrator demo
python orchestrator.py

# Run individual agents
python agents/framework-agent.py
python agents/employee-agent.py
python agents/manager-agent.py
```

## 📊 Context Comparison

| Approach | Context Size | LLM Calls | Cost | Quality |
|----------|-------------|-----------|------|---------|
| Traditional | ~50K tokens | 1 | High | Variable |
| Context-Engineered | ~5.6K total | 5 | Low | Focused |

## 🎓 Key Lessons

1. **Single-Purpose Agents**: Each agent has one clear task
2. **Minimal Context**: Only load what's needed for the task
3. **Progressive Synthesis**: Condense outputs before combining
4. **Separation of Concerns**: Resources, prompts, and agents are independent
5. **Debuggability**: Easy to inspect and improve individual components

## 🔑 First Principles (from README.md)

- **Raw, No Intermediaries**: Direct file access, no databases
- **Single-Purpose**: One agent, one job
- **Prepare Everything First**: Resources ready before execution
- **Test Early and Often**: Verify each component
- **0% Context is Best**: Use only what you absolutely need
- **SHIP!**: Working code beats perfect benchmarks

## 📝 Example Data

The `resources/` directory contains realistic dummy data:
- Performance review guidelines
- Employee profile for "Sarah Chen"
- Work history with specific projects and metrics
- Manager's 1:1 notes over 6 months
- Peer feedback from 5 colleagues
- Level expectations (L5 vs L6)
- Calibration guidelines

## 🛠️ Next Steps

To turn this into a real application:

1. **Add LLM Integration**: Replace MockLLMClient with Anthropic/OpenAI
2. **Add Error Handling**: Graceful failures, retries
3. **Add Caching**: Cache agent outputs for efficiency
4. **Add Validation**: Ensure outputs match expected format
5. **Add Logging**: Track token usage and performance
6. **Add Tests**: Unit tests for each agent
7. **Scale**: Handle multiple employees in parallel

## 💡 Why This Matters

Context engineering is about **making your luck** by designing systems that:
- Work reliably with LLMs (not against them)
- Are easy to debug and improve
- Scale efficiently
- Produce consistent quality

Instead of hoping a single mega-prompt works, we engineer a pipeline of focused, specialized components.

**3 months of hacking with LLMs can save you 5 minutes of context engineering!** ⏱️
