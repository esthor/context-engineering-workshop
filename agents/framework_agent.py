"""
Framework Agent

Purpose: Extract and structure the performance review framework from company materials.
This agent has minimal, focused context - only the company training materials it needs.
"""

from pathlib import Path


class FrameworkAgent:
    """Agent to extract performance review framework from company materials."""

    def __init__(self):
        self.name = "framework-agent"
        self.prompt_path = Path("prompts/extract-framework.md")
        self.resource_paths = [
            Path("resources/company/training-materials/performance-review-guidelines.md"),
            Path("resources/company/training-materials/calibration-guidelines.md"),
            Path("resources/company/level-expectations.md"),
            Path("resources/schema/schema.md"),
        ]

    def get_prompt(self) -> str:
        """Load the prompt template."""
        with open(self.prompt_path, 'r') as f:
            return f.read()

    def get_context(self) -> str:
        """Load only the specific resources this agent needs."""
        context = []
        for path in self.resource_paths:
            if path.exists():
                with open(path, 'r') as f:
                    context.append(f"--- {path.name} ---\n{f.read()}\n")
        return "\n".join(context)

    def run(self, llm_client) -> dict:
        """
        Execute the agent with minimal context.

        Returns:
            dict: Structured framework information
        """
        prompt = self.get_prompt()
        context = self.get_context()

        # Construct the minimal message for the LLM
        message = f"{prompt}\n\n# COMPANY MATERIALS:\n\n{context}"

        # Call LLM with only what it needs
        response = llm_client.generate(
            messages=[{"role": "user", "content": message}],
            max_tokens=2000,  # Framework extraction is concise
        )

        return {
            "agent": self.name,
            "output": response,
            "tokens_used": len(message.split()),  # Approximate
        }


if __name__ == "__main__":
    # Example usage
    agent = FrameworkAgent()
    print(f"Agent: {agent.name}")
    print(f"Prompt: {agent.prompt_path}")
    print(f"Resources: {[str(p) for p in agent.resource_paths]}")
    print(f"\nContext size: ~{len(agent.get_context())} characters")
