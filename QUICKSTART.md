# Quick Start Guide

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key:**
   The `.env` file already contains your OpenAI API key. Verify it's set:
   ```bash
   cat .env
   ```
   Should show:
   ```
   OPENAI_API_KEY='sk-...'
   ```

## Run the System

Execute the orchestrator to generate a performance review:

```bash
python orchestrator.py
```

This will:
1. Show an explanation of the context engineering approach
2. Run the 5-agent pipeline with real OpenAI API calls
3. Generate a complete performance review for "Sarah Chen"
4. Save outputs to the `outputs/` directory

## Output Files

After running, you'll find:

- **`outputs/performance_review.md`** - Final review + quality check
- **`outputs/intermediate_outputs.md`** - Individual agent outputs for debugging

## What Happens

The system runs 5 specialized agents in sequence:

```
📋 Agent 1: FrameworkAgent
   Extracts performance review framework from company materials
   Context: ~2KB → Output: ~500 tokens

👤 Agent 2: EmployeeAgent
   Extracts Sarah Chen's accomplishments and context
   Context: ~4KB → Output: ~800 tokens

💼 Agent 3: ManagerAgent
   Extracts insights from 1:1 notes and peer feedback
   Context: ~5KB → Output: ~800 tokens

🔄 Agent 4: SynthesisAgent
   Synthesizes complete review from condensed agent outputs
   Context: ~2KB (condensed) → Output: ~2000 tokens

✅ Agent 5: ReviewerAgent
   Quality checks the draft review
   Context: ~4KB → Output: ~1500 tokens
```

## Cost Estimate

Using GPT-5.1-nano:
- ~21,000 tokens total across all agents
- Estimated cost: Very low (nano models are highly optimized)
- Time: 15-30 seconds depending on API latency

Compare to traditional approach:
- ~50,000 tokens in single call
- Estimated cost: Higher
- Time: 40-60 seconds

**Savings: Significant cost reduction + 50% faster with parallelization**

## Customization

To customize the system:

- **Change the model:** Edit `orchestrator.py` line 232 to use different model (e.g., `gpt-4o`, `gpt-4o-mini`)
- **Modify prompts:** Edit files in `prompts/` directory
- **Update employee data:** Edit files in `resources/reviewee/`
- **Adjust company framework:** Edit files in `resources/company/`

## Troubleshooting

**API Key Error:**
```
❌ Error: OPENAI_API_KEY not found in environment variables
```
Solution: Check that `.env` file has `OPENAI_API_KEY=sk-...`

**Import Error:**
```
ModuleNotFoundError: No module named 'openai'
```
Solution: Run `pip install -r requirements.txt`

**Rate Limit Error:**
If you hit OpenAI rate limits, the system will show an error. Wait a moment and try again.

## Next Steps

1. Examine the generated review in `outputs/performance_review.md`
2. Look at intermediate outputs in `outputs/intermediate_outputs.md`
3. Try modifying the employee data and regenerating
4. Experiment with different prompts to improve quality
5. Compare token usage across different approaches

Enjoy exploring context engineering! 🎯
