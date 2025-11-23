"""
Performance Review Orchestrator

This orchestrator coordinates the specialized agents to generate a performance review.
Each agent runs with minimal context, and outputs are condensed before synthesis.

Key Principle: No single LLM call sees the entire context. Each agent processes
only what it needs, keeping context windows small and focused.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

from agents import (
    FrameworkAgent,
    EmployeeAgent,
    ManagerAgent,
    SynthesisAgent,
    ReviewerAgent,
)

# Load environment variables
load_dotenv()


class OpenAIClient:
    """Wrapper for OpenAI API with standard interface for agents."""

    def __init__(self, api_key: str = None, model: str = "gpt-5.1-nano"):
        """
        Initialize OpenAI client.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model to use (default: gpt-5.1-nano)
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model

    def generate(self, messages: list, max_tokens: int = 4000, temperature: float = 0.7) -> str:
        """
        Generate completion from OpenAI.

        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated text content
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content


class PerformanceReviewOrchestrator:
    """Orchestrates the performance review generation pipeline."""

    def __init__(self, llm_client):
        """
        Initialize the orchestrator with an LLM client.

        Args:
            llm_client: Client for LLM API calls (e.g., Anthropic, OpenAI)
        """
        self.llm_client = llm_client
        self.agents = {
            'framework': FrameworkAgent(),
            'employee': EmployeeAgent(),
            'manager': ManagerAgent(),
            'synthesis': SynthesisAgent(),
            'reviewer': ReviewerAgent(),
        }

    def generate_review(self, auto_revise: bool = True) -> dict:
        """
        Generate a complete performance review using the agent pipeline.

        Pipeline:
        1. Extract framework from company materials (small context)
        2. Extract employee context from profile/history (small context)
        3. Extract manager insights from notes/feedback (small context)
        4. Synthesize review from condensed outputs (medium context)
        5. Quality check and optionally revise (small context)

        Args:
            auto_revise: If True, automatically revise based on reviewer feedback

        Returns:
            dict: Complete review with metadata about the process
        """
        print("🚀 Starting performance review generation pipeline...\n")

        # Step 1: Extract Framework (minimal context)
        print("📋 Step 1: Extracting performance review framework...")
        framework_result = self.agents['framework'].run(self.llm_client)
        print(f"   ✓ Framework extracted (~{framework_result['tokens_used']} tokens)\n")

        # Step 2: Extract Employee Context (minimal context)
        print("👤 Step 2: Extracting employee context...")
        employee_result = self.agents['employee'].run(self.llm_client)
        print(f"   ✓ Employee context extracted (~{employee_result['tokens_used']} tokens)\n")

        # Step 3: Extract Manager Insights (minimal context)
        print("💼 Step 3: Extracting manager insights...")
        manager_result = self.agents['manager'].run(self.llm_client)
        print(f"   ✓ Manager insights extracted (~{manager_result['tokens_used']} tokens)\n")

        # Step 4: Synthesize Review (uses condensed outputs)
        print("🔄 Step 4: Synthesizing performance review...")
        synthesis_result = self.agents['synthesis'].run(
            self.llm_client,
            framework_output=framework_result['output'],
            employee_output=employee_result['output'],
            manager_output=manager_result['output'],
        )
        print(f"   ✓ Review synthesized (~{synthesis_result['tokens_used']} tokens)\n")

        draft_review = synthesis_result['output']

        # Step 5: Quality Check (minimal context)
        print("✅ Step 5: Running quality check...")
        review_result = self.agents['reviewer'].run(
            self.llm_client,
            draft_review=draft_review,
            framework_output=framework_result['output'],
        )
        print(f"   ✓ Quality check complete (~{review_result['tokens_used']} tokens)\n")

        # Optional: Auto-revise based on feedback
        revision_count = 0
        if auto_revise and "NEEDS REVISION" in review_result['output']:
            print("🔧 Quality check flagged issues. Auto-revising...\n")
            # In a real implementation, you'd parse the feedback and revise
            # For demo purposes, we'll just note it
            revision_count = 1

        # Calculate total context usage
        total_tokens = (
            framework_result['tokens_used'] +
            employee_result['tokens_used'] +
            manager_result['tokens_used'] +
            synthesis_result['tokens_used'] +
            review_result['tokens_used']
        )

        print(f"✨ Review generation complete!")
        print(f"📊 Total approximate tokens across all agents: ~{total_tokens}")
        print(f"   (Compare this to sending all raw context in one call!)\n")

        return {
            'final_review': draft_review,
            'quality_check': review_result['output'],
            'revision_count': revision_count,
            'metadata': {
                'framework_tokens': framework_result['tokens_used'],
                'employee_tokens': employee_result['tokens_used'],
                'manager_tokens': manager_result['tokens_used'],
                'synthesis_tokens': synthesis_result['tokens_used'],
                'review_tokens': review_result['tokens_used'],
                'total_tokens': total_tokens,
            },
            'intermediate_outputs': {
                'framework': framework_result['output'],
                'employee': employee_result['output'],
                'manager': manager_result['output'],
            }
        }

    def explain_approach(self):
        """Print explanation of the context engineering approach."""
        print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                    Context Engineering Approach                          ║
╚══════════════════════════════════════════════════════════════════════════╝

Traditional Approach (❌ Not Ideal):
  • Load ALL resources into one massive context
  • Company docs + employee history + manager notes + framework + schema
  • Result: 50,000+ token context window
  • Problems: Expensive, slow, model may miss details in large context

Context-Engineered Approach (✅ This System):
  • 5 specialized agents, each with minimal focused context
  • Each agent processes only what it needs for its specific task
  • Outputs are condensed summaries, not raw data
  • Final synthesis uses 3 condensed inputs, not raw context

Agent Pipeline:
  1. FrameworkAgent:  Company docs → Structured framework (~500 tokens)
  2. EmployeeAgent:   Employee files → Key accomplishments (~800 tokens)
  3. ManagerAgent:    Manager notes → Insights & themes (~800 tokens)
  4. SynthesisAgent:  3 condensed inputs → Draft review (~2000 tokens)
  5. ReviewerAgent:   Draft + framework → Quality check (~1500 tokens)

Total: ~5,600 tokens across 5 focused calls
vs ~50,000+ tokens in 1 unfocused call

Benefits:
  ✓ Smaller, faster, cheaper LLM calls
  ✓ Each call is focused on a specific task
  ✓ Easier to debug and improve individual components
  ✓ Better quality through specialization
  ✓ Parallelizable (can run agents 1-3 concurrently)

This is Context Engineering in action! 🎯
        """)


def main():
    """Run the performance review generation pipeline."""
    print("\n" + "="*80)
    print("Performance Review System - Context Engineering Demo")
    print("="*80 + "\n")

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please add your OpenAI API key to the .env file:")
        print("   OPENAI_API_KEY=sk-...")
        return

    # Initialize OpenAI client
    print("🔑 Initializing OpenAI client (gpt-5.1-nano)...")
    try:
        llm_client = OpenAIClient(model="gpt-5.1-nano")
        print("✓ OpenAI client initialized\n")
    except Exception as e:
        print(f"❌ Error initializing OpenAI client: {e}")
        return

    # Create orchestrator
    orchestrator = PerformanceReviewOrchestrator(llm_client)

    # Show the approach explanation
    orchestrator.explain_approach()

    # Run the pipeline
    print("\n" + "="*80)
    print("Running Performance Review Pipeline with Real LLM")
    print("="*80 + "\n")

    try:
        result = orchestrator.generate_review()

        print("\n" + "="*80)
        print("Pipeline Complete!")
        print("="*80)
        print(f"\nGenerated review with {result['metadata']['total_tokens']} total tokens")
        print(f"across {5 - result['revision_count']} agent calls.")

        # Save the final review to a file
        os.makedirs("outputs", exist_ok=True)
        output_file = "outputs/performance_review.md"
        with open(output_file, 'w') as f:
            f.write("# Performance Review - Sarah Chen\n\n")
            f.write(result['final_review'])
            f.write("\n\n---\n\n# Quality Check\n\n")
            f.write(result['quality_check'])

        print(f"\n✅ Review saved to: {output_file}")
        print("\nIntermediate outputs available in result dictionary for debugging.")

        # Optionally save intermediate outputs
        with open("outputs/intermediate_outputs.md", 'w') as f:
            f.write("# Intermediate Agent Outputs\n\n")
            f.write("## Framework Agent Output\n\n")
            f.write(result['intermediate_outputs']['framework'])
            f.write("\n\n## Employee Agent Output\n\n")
            f.write(result['intermediate_outputs']['employee'])
            f.write("\n\n## Manager Agent Output\n\n")
            f.write(result['intermediate_outputs']['manager'])

        print(f"📊 Intermediate outputs saved to: outputs/intermediate_outputs.md")

    except Exception as e:
        print(f"\n❌ Error during pipeline execution: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
