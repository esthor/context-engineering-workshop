"""
Reviewer Agent

Purpose: Quality check a draft performance review against framework and guidelines.
This agent ensures the review meets standards before delivery.
"""

from pathlib import Path


class ReviewerAgent:
    """Agent to review and quality check draft performance reviews."""

    def __init__(self):
        self.name = "reviewer-agent"
        self.prompt_path = Path("prompts/review-quality-check.md")
        # This agent needs the framework for comparison
        self.framework_resource_paths = [
            Path("resources/company/training-materials/performance-review-guidelines.md"),
            Path("resources/company/training-materials/calibration-guidelines.md"),
        ]

    def get_prompt(self) -> str:
        """Load the prompt template."""
        with open(self.prompt_path, 'r') as f:
            return f.read()

    def get_framework_context(self) -> str:
        """Load framework materials for comparison."""
        context = []
        for path in self.framework_resource_paths:
            if path.exists():
                with open(path, 'r') as f:
                    context.append(f"--- {path.name} ---\n{f.read()}\n")
        return "\n".join(context)

    def run(self, llm_client, draft_review: str, framework_output: str = None,
            original_context: dict = None) -> dict:
        """
        Execute the agent to review a draft performance review.

        Args:
            llm_client: LLM client for generation
            draft_review: The draft review to check
            framework_output: Optional pre-processed framework (if available)
            original_context: Optional original context for fact-checking

        Returns:
            dict: Quality assessment and recommendations
        """
        prompt = self.get_prompt()

        # Use pre-processed framework if available, otherwise load directly
        if framework_output:
            framework = framework_output
        else:
            framework = self.get_framework_context()

        # Construct message
        message = f"""{prompt}

# FRAMEWORK AND GUIDELINES:
{framework}

# DRAFT REVIEW TO EVALUATE:
{draft_review}

Provide your quality assessment following the output format in the prompt.
"""

        # Call LLM with focused context
        response = llm_client.generate(
            messages=[{"role": "user", "content": message}],
            max_tokens=2500,  # Quality check is detailed but bounded
        )

        return {
            "agent": self.name,
            "output": response,
            "tokens_used": len(message.split()),  # Approximate
        }


if __name__ == "__main__":
    # Example usage
    agent = ReviewerAgent()
    print(f"Agent: {agent.name}")
    print(f"Prompt: {agent.prompt_path}")
    print(f"Framework resources: {[str(p) for p in agent.framework_resource_paths]}")
