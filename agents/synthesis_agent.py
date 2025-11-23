"""
Synthesis Agent

Purpose: Synthesize a complete performance review from the outputs of other agents.
This is the only agent that sees multiple contexts, but they're pre-processed and condensed.
"""

from pathlib import Path


class SynthesisAgent:
    """Agent to synthesize performance review from multiple agent outputs."""

    def __init__(self):
        self.name = "synthesis-agent"
        self.prompt_path = Path("prompts/synthesize-review.md")

    def get_prompt(self) -> str:
        """Load the prompt template."""
        with open(self.prompt_path, 'r') as f:
            return f.read()

    def run(self, llm_client, framework_output: str, employee_output: str,
            manager_output: str) -> dict:
        """
        Execute the agent with pre-processed outputs from other agents.

        Args:
            llm_client: LLM client for generation
            framework_output: Output from framework agent
            employee_output: Output from employee agent
            manager_output: Output from manager agent

        Returns:
            dict: Complete performance review
        """
        prompt = self.get_prompt()

        # Construct message with pre-processed, condensed context
        message = f"""{prompt}

# INPUT CONTEXT:

## Performance Review Framework
{framework_output}

## Employee Context
{employee_output}

## Manager Insights
{manager_output}

Now synthesize a complete performance review following the framework and guidelines.
"""

        # Call LLM with synthesized context
        response = llm_client.generate(
            messages=[{"role": "user", "content": message}],
            max_tokens=4000,  # Full review needs more tokens
        )

        return {
            "agent": self.name,
            "output": response,
            "tokens_used": len(message.split()),  # Approximate
        }


if __name__ == "__main__":
    # Example usage
    agent = SynthesisAgent()
    print(f"Agent: {agent.name}")
    print(f"Prompt: {agent.prompt_path}")
    print("\nThis agent takes outputs from:")
    print("  - framework-agent")
    print("  - employee-agent")
    print("  - manager-agent")
