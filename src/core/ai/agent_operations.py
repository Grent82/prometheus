import asyncio
from enum import Enum

from src.core.id_types import GameId

class AsyncOperationHandler:
    queue = asyncio.Queue()

    async def add_task(self, task):
        await self.queue.put(task)

    async def process_task(self, task):
        await self.handle_task(task)

    async def process_tasks(self):
        while True:
            task = await self.queue.get()
            await self.handle_task(task)

    async def handle_task(self, task):
        self.start()
        if isinstance(task, AsyncMessageTask):
            await self.handle_message_task(task.message)
        elif isinstance(task, AsyncConversationTask):
            await self.handle_conversation_task(task.conversation)
        elif isinstance(task, AsyncActionTask):
            await self.handle_action_task(task.action)
        # Add more conditionals for other types of tasks as needed

    async def handle_message_task(self, message):
        # Implement message sending logic here
        print(f"Sending message: {message}")
        await asyncio.sleep(1)  # Simulate delay
        print(f"Message sent: {message}")

    async def handle_conversation_task(self, conversation):
        # Implement conversation starting logic here
        print(f"Starting conversation: {conversation}")
        await asyncio.sleep(1)  # Simulate delay
        print(f"Conversation started: {conversation}")

    async def handle_action_task(self, action):
        # Implement action performing logic here
        print(f"Performing action: {action}")
        await asyncio.sleep(1)  # Simulate delay
        print(f"Action performed: {action}")

    async def run_event_loop(self):
        await self.process_tasks()

    def start(self):
        asyncio.run(self.run_event_loop())

class AsyncMessageTasktype(Enum):
    START = 0,
    CONTINUE = 1,
    LEAVE = 2

class AsyncMessageTask:
    def __init__(self, agent_id:GameId, other_agent_id:GameId, conversation_id:GameId, msg_uuid:str, type: AsyncMessageTasktype):
        self.agent_id = agent_id.id
        self.other_agent_id = other_agent_id
        self.conversation_id = conversation_id
        self.msg_uuid = msg_uuid

class AsyncConversationTask:
    def __init__(self, conversation):
        self.conversation = conversation

class AsyncActionTask:
    def __init__(self, action):
        self.action = action