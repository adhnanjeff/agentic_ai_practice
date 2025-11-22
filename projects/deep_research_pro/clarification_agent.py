from agents import Agent
from pydantic import BaseModel
from typing import List

class ClarificationQuestions(BaseModel):
    questions: List[str]
    refined_query: str

clarification_instructions = """
You are a research clarification specialist. When given a research query, you must:

1. Generate exactly 3 clarifying questions to better understand the user's needs
2. Create a refined query based on the original query

The questions should help clarify:
- Scope and depth of research needed
- Specific aspects or angles to focus on  
- Target audience or use case for the research

Format your response as:
- 3 specific, actionable questions
- A refined version of the original query

Be concise and focused.
"""

clarification_agent = Agent(
    name="Research Clarification Agent",
    instructions=clarification_instructions,
    model="gpt-4o-mini"
)