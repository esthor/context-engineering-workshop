"""
Manager Agent

Purpose: Extract insights from manager's observations and peer feedback.
This agent focuses on qualitative insights and patterns.
"""

from pathlib import Path


class ManagerAgent:
    """Agent to extract manager insights from notes and peer feedback."""

    def __init__(self):
        self.name = "manager-agent"
        self.prompt_path = Path("prompts/extract-manager-insights.md")
        self.resource_paths = [
            Path("resources/manager/1on1-notes-h2-2024.md"),
            Path("resources/manager/peer-feedback.md"),
        ]

    def get_prompt(self) -> str:
        """Load the prompt template."""
        with open(self.prompt_path, 'r') as f:
            return f.read()

    def get_context(self) -> str:
        """Load only the manager-related resources."""
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
            dict: Structured manager insights
        """
        prompt = self.get_prompt()
        context = self.get_context()

        # Construct the minimal message for the LLM
        message = f"{prompt}\n\n# MANAGER NOTES AND FEEDBACK:\n\n{context}"

        # Call LLM with only what it needs
        response = llm_client.generate(
            messages=[{"role": "user", "content": message}],
            max_tokens=3000,  # Manager insights can be detailed
        )

        return {
            "agent": self.name,
            "output": response,
            "tokens_used": len(message.split()),  # Approximate
        }


if __name__ == "__main__":
    # Example usage
    agent = ManagerAgent()
    print(f"Agent: {agent.name}")
    print(f"Prompt: {agent.prompt_path}")
    print(f"Resources: {[str(p) for p in agent.resource_paths]}")
    print(f"\nContext size: ~{len(agent.get_context())} characters")
