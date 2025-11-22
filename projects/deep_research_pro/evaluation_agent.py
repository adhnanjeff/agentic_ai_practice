from agents import Agent
from pydantic import BaseModel

class EvaluationResult(BaseModel):
    is_satisfactory: bool
    feedback: str
    score: int  # 1-10 scale

from email_agent import email_agent

evaluation_instructions = """
You are a research report evaluator. Your job is to assess the quality of research reports.

Evaluate reports based on:
1. Completeness - Does it thoroughly address the original query?
2. Accuracy - Is the information reliable and well-sourced?
3. Clarity - Is it well-structured and easy to understand?
4. Depth - Does it provide sufficient detail and analysis?
5. Relevance - Does it stay focused on the query?

Scoring:
- 8-10: Excellent, ready to send via email
- 6-7: Good but needs minor improvements
- 4-5: Adequate but needs significant improvements  
- 1-3: Poor, needs major revision

If score is 8+: Hand off to Email Agent to send the report
If score is below 8: Provide specific feedback for the Research Manager to improve

Always provide detailed, actionable feedback.
"""

evaluation_agent = Agent(
    name="Research Report Evaluator",
    instructions=evaluation_instructions,
    handoffs=[email_agent],
    model="gpt-4o-mini"
)