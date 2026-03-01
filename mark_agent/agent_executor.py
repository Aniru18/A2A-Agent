# Step2: Agent Executor
from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import Part, TextPart

from agent import MarkAgent


class MarkAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent = MarkAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue):

        updater=TaskUpdater(event_queue,context.task_id,context.context_id)
        if not context.current_task: # if there is no current task, create one
            await updater.submit() # create a new task
        await updater.start_work() # start the task

        query = context.get_user_input()

        response = await self.agent.invoke(user_question=query)
        parts = [Part(root=TextPart(text=response))] # converting the message in the format of a2a protocol
        await updater.add_artifact(parts, name="scheduling_result")
        await updater.complete()

        # return response
        

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        return