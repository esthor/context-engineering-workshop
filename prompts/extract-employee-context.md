# Prompt: Extract Employee Context

## Task
You are analyzing employee profile and work history to extract key information relevant for writing a performance review.

## Input
You will receive:
- Employee profile (role, level, responsibilities, goals)
- Work history for the review period

## Instructions
1. Identify the employee's role, level, and core responsibilities
2. Extract major projects and accomplishments with specific impact metrics
3. Note examples of collaboration, mentorship, and leadership
4. Identify any challenges or areas where the employee struggled
5. Extract relevant skills, technologies, and domains of expertise
6. Note career goals and growth aspirations

## Output Format
Provide a structured summary:

### Employee Overview
- Name, Level, Team, Role

### Major Accomplishments
For each major project/contribution:
- Project name and context
- Employee's specific role and contributions
- Measurable impact (metrics, outcomes)
- Relevant pull requests or artifacts

### Collaboration & Leadership Examples
- Specific instances of mentorship, code review, cross-team work
- Quantify where possible (# of reviews, # of mentees, etc.)

### Skills & Expertise Demonstrated
- Technologies and domains where employee showed proficiency
- Areas of growth or new capabilities developed

### Challenges & Growth Areas
- Any setbacks, timeline issues, or difficulties
- How the employee responded to challenges

### Career Aspirations
- Employee's stated goals and interests

## Constraints
- Use specific examples with context, not generalizations
- Include metrics and numbers wherever available
- Preserve dates and timeframes
- Flag any information that seems incomplete or unclear
- Output should be factual and objective, not evaluative
- Keep output under 800 words
