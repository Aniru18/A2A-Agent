from crewai import LLM, Agent, Crew, Process, Task
from tools import AvailabilityTool
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()

class MarkAgent():
    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]
    def __init__(self):
        self.api_key=os.getenv("GOOGLE_API_KEY_MARK")
        # self.api_key="api_key"

        self.llm=LLM(
                model="gemini-2.5-flash", 
                api_key=self.api_key
            )

        self.agent=Agent(
            role="Sheduling assistant",
            goal="Answer question about Mark's availability using the calender.",
            backstory="you only answers the scheduling quesions and you always use the calender tool.",
            tools=[AvailabilityTool()],
            llm=self.llm
        )


    async def invoke(self, user_question):
        task=Task(
            description=f"user asked: {user_question}",
            expected_output="Polite response about availability",
            agent=self.agent
        )

        crew=Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential
        )

        agent_response=str(crew.kickoff())

        return agent_response

# mark_agent=MarkAgent()
# print(asyncio.run(mark_agent.invoke("Is mark available on 14th November 2025?")))