from agents import Agent, Runner, trace, gen_trace_id, function_tool
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent
from clarification_agent import clarification_agent
from evaluation_agent import evaluation_agent, EvaluationResult
import asyncio

# Convert existing agents to tools
planner_tool = planner_agent.as_tool(
    tool_name="research_planner",
    tool_description="Plan research searches for a query"
)

search_tool = search_agent.as_tool(
    tool_name="web_searcher", 
    tool_description="Perform web searches and gather information"
)

writer_tool = writer_agent.as_tool(
    tool_name="report_writer",
    tool_description="Write comprehensive research reports"
)

@function_tool
def perform_multiple_searches(search_plan: WebSearchPlan) -> list[str]:
    """Perform multiple web searches based on the search plan"""
    async def _search_all():
        tasks = []
        for item in search_plan.searches:
            input_text = f"Search term: {item.query}\nReason for searching: {item.reason}"
            task = Runner.run(search_agent, input_text)
            tasks.append(task)
        
        results = []
        for task in asyncio.as_completed(tasks):
            try:
                result = await task
                results.append(str(result.final_output))
            except Exception:
                continue
        return results
    
    return asyncio.run(_search_all())

# Create the main research manager agent
research_manager_instructions = """
You are a research manager that coordinates comprehensive research projects.

Your process:
1. Use the research_planner tool to create a search plan
2. Use perform_multiple_searches to gather information  
3. Use the report_writer tool to create the final report
4. Hand off to the evaluator for quality assessment

If you receive feedback from the evaluator that the report needs improvement:
- Analyze the feedback carefully
- Use the appropriate tools to gather additional information or rewrite sections
- Hand off the revised report back to the evaluator

Continue this cycle until the evaluator approves the report for email delivery.
Be systematic, thorough, and responsive to feedback.
"""

research_manager_agent = Agent(
    name="Research Manager",
    instructions=research_manager_instructions,
    tools=[planner_tool, perform_multiple_searches, writer_tool],
    handoffs=[evaluation_agent],
    model="gpt-4o-mini"
)

# Update evaluation agent to hand back to research manager if revision needed
evaluation_agent.handoffs.append(research_manager_agent)

class ResearchManager:

    async def run(self, query: str, clarifications: dict = None):
        """ Run the deep research process with clarifications """
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            
            # Use clarifications to refine query if provided
            if clarifications:
                refined_query = f"{query}\n\nAdditional context: {clarifications}"
            else:
                refined_query = query
            
            print("Starting research...")
            yield "Starting research process..."
            
            # Run the research manager agent
            result = await Runner.run(research_manager_agent, f"Research query: {refined_query}")
            
            yield "Research and evaluation complete!"
            yield result.final_output
        

    
    async def get_clarifications(self, query: str):
        """Get clarifying questions for the user query"""
        result = await Runner.run(
            clarification_agent,
            f"Generate 3 clarifying questions for this research query: {query}"
        )
        return result.final_output