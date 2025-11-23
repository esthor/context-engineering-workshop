"""
Agents Module

This module contains specialized agents for performance review generation.
Each agent has minimal, focused context and a single clear purpose.

Agent Pipeline:
1. FrameworkAgent - Extract review framework from company materials
2. EmployeeAgent - Extract employee accomplishments and context
3. ManagerAgent - Extract manager insights and peer feedback
4. SynthesisAgent - Synthesize complete review from agent outputs
5. ReviewerAgent - Quality check the draft review

Key Principles:
- Each agent sees only the context it needs
- Agents run independently with minimal context
- Outputs are condensed before passing to synthesis
- No agent sees the full raw context
"""

from .framework_agent import FrameworkAgent
from .employee_agent import EmployeeAgent
from .manager_agent import ManagerAgent
from .synthesis_agent import SynthesisAgent
from .reviewer_agent import ReviewerAgent


__all__ = [
    'FrameworkAgent',
    'EmployeeAgent',
    'ManagerAgent',
    'SynthesisAgent',
    'ReviewerAgent',
]
