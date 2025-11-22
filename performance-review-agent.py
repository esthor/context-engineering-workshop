# import libs


# prompt for performance framework
prompt_performance_framework = "define a generic performance review for an employee performance review for a software engineer at a big tech company."

# Company Context
prompt_training_material_agent = f"read the files in {training_materials} and "


# Indivudal Context
prompt_reviewee_agent = f"read the files in {reviewee_agent} and ""

# Manager Context
prompt_manager_history_agent = f"read the files in {reviewee_agent} and ""


# for each history file => call history-agent (file(n) => intersting bits, citation)
# 
# synthesizer_of_history => (tool())


prompt_training_materials_review_agent = f"review the {draft_review} and list any misalignments with the performance framework"


""

# llm invocation


# do something with that - hook it back


