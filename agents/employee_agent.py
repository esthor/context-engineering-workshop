"""
Employee Agent

Purpose: Extract relevant information about the employee from their profile and work history.
This agent focuses only on factual information about the employee's work.
"""

from pathlib import Path


class EmployeeAgent:
    """Agent to extract employee context from profile and work history."""

    def __init__(self, employee_id: str = "ENG-2847"):
        self.name = "employee-agent"
        self.employee_id = employee_id
        self.prompt_path = Path("prompts/extract-employee-context.md")
        self.resource_paths = [
            Path("resources/reviewee/employee-profile.md"),
            Path("resources/reviewee/work-history-h2-2024.md"),
        ]

    def get_prompt(self) -> str:
        """Load the prompt template."""
        with open(self.prompt_path, 'r') as f:
            return f.read()

    def get_context(self) -> str:
        """Load only the employee-specific resources."""
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
            dict: Structured employee information
        """
        prompt = self.get_prompt()
        context = self.get_context()

        # Construct the minimal message for the LLM
        message = f"{prompt}\n\n# EMPLOYEE INFORMATION:\n\n{context}"

        # Call LLM with only what it needs
        response = llm_client.generate(
            messages=[{"role": "user", "content": message}],
            max_tokens=3000,  # Employee context can be more detailed
        )

        return {
            "agent": self.name,
            "employee_id": self.employee_id,
            "output": response,
            "tokens_used": len(message.split()),  # Approximate
        }


if __name__ == "__main__":
    # Example usage
    agent = EmployeeAgent()
    print(f"Agent: {agent.name}")
    print(f"Employee ID: {agent.employee_id}")
    print(f"Prompt: {agent.prompt_path}")
    print(f"Resources: {[str(p) for p in agent.resource_paths]}")
    print(f"\nContext size: ~{len(agent.get_context())} characters")
