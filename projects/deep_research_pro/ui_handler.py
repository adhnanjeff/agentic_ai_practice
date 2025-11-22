from research_manager import ResearchManager
import asyncio

class UIHandler:
    def __init__(self):
        self.research_manager = ResearchManager()
    
    async def handle_research_request(self, query: str):
        """Handle a research request with clarification questions"""
        
        # Step 1: Get clarifying questions
        print("Getting clarifying questions...")
        clarification_response = await self.research_manager.get_clarifications(query)
        
        # In a real UI, you would present these questions to the user
        # For now, we'll simulate user responses
        print("Clarifying questions generated:")
        print(clarification_response)
        
        # Step 2: Simulate user answers (in real implementation, get from UI)
        user_answers = {
            "question_1": "Sample answer 1",
            "question_2": "Sample answer 2", 
            "question_3": "Sample answer 3"
        }
        
        # Step 3: Run research with clarifications
        print("Starting research with clarifications...")
        async for update in self.research_manager.run(query, user_answers):
            print(f"Status: {update}")
        
        return "Research completed successfully"

# Example usage
async def main():
    ui = UIHandler()
    result = await ui.handle_research_request("What are the latest trends in AI?")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())