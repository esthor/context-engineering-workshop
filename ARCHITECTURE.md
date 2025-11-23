# System Architecture - Context Engineering

## Visual Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        RESOURCES                                 │
│  (Raw Data - Never all loaded at once)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Company    │  │   Reviewee   │  │   Manager    │          │
│  │              │  │              │  │              │          │
│  │ • Guidelines │  │ • Profile    │  │ • 1:1 Notes  │          │
│  │ • Framework  │  │ • Work       │  │ • Peer       │          │
│  │ • Levels     │  │   History    │  │   Feedback   │          │
│  │ • Calibrate  │  │              │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
            │                   │                   │
            ▼                   ▼                   ▼
    ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
    │   AGENT 1     │   │   AGENT 2     │   │   AGENT 3     │
    │  Framework    │   │   Employee    │   │   Manager     │
    │               │   │               │   │               │
    │ Context: 2KB  │   │ Context: 4KB  │   │ Context: 5KB  │
    │ Output: 500T  │   │ Output: 800T  │   │ Output: 800T  │
    └───────────────┘   └───────────────┘   └───────────────┘
            │                   │                   │
            └───────────────────┼───────────────────┘
                                ▼
                        ┌───────────────┐
                        │   AGENT 4     │
                        │  Synthesis    │
                        │               │
                        │ Context: 2.1K │   ← Only condensed
                        │               │     outputs, not
                        │ Output: 2000T │     raw resources!
                        └───────────────┘
                                │
                                ▼
                        ┌───────────────┐
                        │   AGENT 5     │
                        │   Reviewer    │
                        │               │
                        │ Context: 3.5K │
                        │ Output: 1500T │
                        └───────────────┘
                                │
                                ▼
                        ┌───────────────┐
                        │ FINAL REVIEW  │
                        └───────────────┘

KEY:
  KB = Kilobytes of context
  T  = Tokens in output
  → = Data flow
```

## Information Flow

### Phase 1: Extraction (Parallel)
```
Resources → Agent 1,2,3 → Condensed Summaries
```
Each agent gets only its slice of resources. Agents 1-3 can run in parallel.

### Phase 2: Synthesis (Sequential)
```
Condensed Summaries → Agent 4 → Draft Review
```
Synthesis sees only the structured outputs from Phase 1, not raw resources.

### Phase 3: Quality Check (Sequential)
```
Draft Review + Framework → Agent 5 → Quality Report
```
Reviewer compares draft against framework for quality assurance.

## Context Window Comparison

### Traditional Approach
```
┌─────────────────────────────────────────────────┐
│         ONE MASSIVE LLM CALL                    │
│                                                 │
│  Company Guidelines:           15,000 tokens    │
│  Employee Work History:        12,000 tokens    │
│  Manager Notes & Feedback:     18,000 tokens    │
│  Schema & Instructions:         5,000 tokens    │
│  ─────────────────────────────────────────      │
│  TOTAL CONTEXT:                50,000 tokens    │
│                                                 │
│  Problems:                                      │
│  • Expensive (~$2.50 per review)                │
│  • Slow (30-60 second response)                 │
│  • May miss details in large context            │
│  • Hard to debug what went wrong                │
│  • Can't parallelize                            │
└─────────────────────────────────────────────────┘
```

### Context-Engineered Approach
```
┌─────────────────────────────────────────────────┐
│         FIVE FOCUSED LLM CALLS                  │
│                                                 │
│  Agent 1 (Framework):           2,000 tokens    │
│  Agent 2 (Employee):            4,000 tokens    │
│  Agent 3 (Manager):             5,000 tokens    │
│  Agent 4 (Synthesis):           6,000 tokens    │
│  Agent 5 (Review):              4,000 tokens    │
│  ─────────────────────────────────────────      │
│  TOTAL CONTEXT:                21,000 tokens    │
│                                                 │
│  Benefits:                                      │
│  • Cheaper (~$1.05 per review = 58% savings)    │
│  • Faster (parallel + smaller contexts)         │
│  • Focused attention on each task               │
│  • Easy to debug individual agents              │
│  • Agents 1-3 can run in parallel               │
└─────────────────────────────────────────────────┘
```

## Agent Responsibilities

### 🏗️ FrameworkAgent
**Purpose:** Extract and structure the performance review framework

**Input Resources:**
- `resources/company/training-materials/performance-review-guidelines.md`
- `resources/company/training-materials/calibration-guidelines.md`
- `resources/company/level-expectations.md`
- `resources/schema/schema.md`

**Prompt:** `prompts/extract-framework.md`

**Output:** Structured framework with:
- Evaluation dimensions
- Rating scale definitions
- Writing guidelines
- Level expectations

**Context Size:** ~2KB → 500 tokens output

---

### 👤 EmployeeAgent
**Purpose:** Extract employee accomplishments and context

**Input Resources:**
- `resources/reviewee/employee-profile.md`
- `resources/reviewee/work-history-h2-2024.md`

**Prompt:** `prompts/extract-employee-context.md`

**Output:** Factual summary with:
- Major accomplishments with metrics
- Collaboration examples
- Skills demonstrated
- Challenges faced
- Career goals

**Context Size:** ~4KB → 800 tokens output

---

### 💼 ManagerAgent
**Purpose:** Extract manager insights and peer feedback

**Input Resources:**
- `resources/manager/1on1-notes-h2-2024.md`
- `resources/manager/peer-feedback.md`

**Prompt:** `prompts/extract-manager-insights.md`

**Output:** Qualitative insights with:
- Performance themes (strengths & development areas)
- Standout stories
- Peer feedback summary
- Growth trajectory
- Contextual factors

**Context Size:** ~5KB → 800 tokens output

---

### 🔄 SynthesisAgent
**Purpose:** Synthesize complete performance review

**Input:** Condensed outputs from Agents 1-3 (NOT raw resources!)

**Prompt:** `prompts/synthesize-review.md`

**Output:** Complete performance review with:
- Overall summary and rating
- Evaluation by dimension
- Key achievements
- Development areas with recommendations
- Goals for next period

**Context Size:** ~2KB condensed → 2000 tokens output

---

### ✅ ReviewerAgent
**Purpose:** Quality check the draft review

**Input:**
- Draft review from SynthesisAgent
- Framework from FrameworkAgent

**Prompt:** `prompts/review-quality-check.md`

**Output:** Quality assessment with:
- Pass/Needs Revision decision
- Issues identified
- Specific recommendations
- Alignment checklist

**Context Size:** ~4KB → 1500 tokens output

---

## Key Design Principles

### 1. Minimal Context Per Agent
Each agent sees only what it needs. No agent processes all raw resources.

### 2. Progressive Condensation
```
Raw Resources (50KB)
    ↓
Agent Summaries (2.1KB)
    ↓
Synthesis (2KB context)
    ↓
Final Review
```

### 3. Single Responsibility
Each agent has one clear job. Easy to test, debug, and improve.

### 4. Parallelization
Agents 1-3 are independent and can run concurrently.

### 5. Separation of Concerns
- **Resources:** Raw data storage
- **Prompts:** Task instructions
- **Agents:** Execution logic
- **Orchestrator:** Coordination

### 6. Debuggability
Each agent's input and output can be inspected independently.

## Cost & Performance Analysis

Based on GPT-5.1-nano (highly optimized nano model):

### Traditional Single-Call Approach
- Input: ~50,000 tokens
- Output: ~2,000 tokens
- **Total context: 50,000 tokens**
- Latency: 30-60 seconds (serial)

### Context-Engineered Multi-Agent Approach
- Agent 1: 2K input + 0.5K output
- Agent 2: 4K input + 0.8K output
- Agent 3: 5K input + 0.8K output
- Agent 4: 2K input + 2K output
- Agent 5: 4K input + 1.5K output
- **Total context: ~21,000 tokens**
- Latency: 15-30 seconds (with parallelization)

**Savings: 58% token reduction + 40-50% faster**

## Extensibility

This architecture makes it easy to:

1. **Add new agents:** Just create a new agent class with its prompt
2. **Modify behavior:** Update individual prompts without touching others
3. **Add resources:** Drop new files in resources/ and update relevant agent
4. **Change LLM:** Swap out LLM client without changing agent logic
5. **Add caching:** Cache agent outputs to avoid re-processing
6. **Scale:** Process multiple employees in parallel

## Testing Strategy

Each component can be tested independently:

```python
# Test individual agent
agent = FrameworkAgent()
context = agent.get_context()
assert "evaluation dimensions" in context.lower()

# Test agent output format
output = agent.run(mock_llm)
assert "Technical Excellence" in output

# Test orchestrator pipeline
orchestrator = PerformanceReviewOrchestrator(mock_llm)
result = orchestrator.generate_review()
assert result['metadata']['total_tokens'] < 25000
```

## Conclusion

This architecture demonstrates that **context engineering** isn't just about writing better prompts—it's about designing systems that:

1. Minimize context through specialization
2. Process information progressively
3. Maintain debuggability and testability
4. Scale efficiently
5. Produce consistent quality

**The whole system is greater than the sum of its prompts.**
