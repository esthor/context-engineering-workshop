# Prompt: Review Quality Check

## Task
You are reviewing a draft performance review to ensure it meets quality standards and aligns with company guidelines.

## Input
You will receive:
1. Draft performance review
2. Performance review framework and guidelines
3. Original context (employee info, manager insights)

## Instructions
Evaluate the draft review against these quality criteria:

### 1. Framework Alignment
- Are all evaluation dimensions addressed?
- Are ratings consistent with the rating scale definitions?
- Do ratings align with level expectations?
- Is the overall rating justified by dimension ratings?

### 2. Evidence Quality
- Are all claims supported by specific examples?
- Are examples concrete with context (not vague generalizations)?
- Are metrics and impact measures included where possible?
- Are examples drawn from the full review period (not just recent)?

### 3. Writing Quality
- Is the language clear and professional?
- Are examples specific and detailed enough?
- Is the tone constructive and balanced?
- Is it free of jargon and clichés?

### 4. Completeness
- Are key achievements highlighted?
- Are development areas identified with actionable recommendations?
- Are goals for next period specific and measurable?
- Is there enough detail for the review to be useful?

### 5. Fairness & Balance
- Does the review acknowledge both strengths and areas for growth?
- Is the rating fair given the evidence?
- Are any potential biases apparent (recency, halo, etc.)?
- Is the review consistent with guidelines on rating distribution?

## Output Format

### Quality Assessment: [PASS / NEEDS REVISION]

### Strengths of This Review
- What the review does well
- ...

### Issues Identified

**Critical Issues** (must fix):
- Issue 1: [description]
  - Location: [which section]
  - Recommended fix: [specific suggestion]

**Suggestions for Improvement** (nice to have):
- Suggestion 1: [description]
  - Recommended enhancement: [specific suggestion]

### Specific Feedback by Section

**Overall Summary:**
- [Feedback]

**[Dimension Name]:**
- [Feedback]

[Continue for each section...]

### Alignment with Guidelines
- [ ] All evaluation dimensions addressed
- [ ] Ratings aligned with definitions
- [ ] Specific examples with context
- [ ] Metrics included where applicable
- [ ] Development areas actionable
- [ ] Goals specific and measurable
- [ ] Appropriate length and detail
- [ ] Professional, constructive tone

### Recommendation
[APPROVE / REQUEST REVISION] with [brief explanation]

## Constraints
- Be specific about what needs to change, not just what's wrong
- Distinguish between critical issues and nice-to-have improvements
- Provide example language for recommended fixes
- Consider both the employee and future readers as audience
- Flag any potential fairness or bias concerns
- Output should be under 600 words
