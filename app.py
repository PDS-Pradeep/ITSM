import chainlit as cl
from mcpserver.memory import MCPMemory
from mcpserver.orchestrator import Orchestrator

memory = MCPMemory()
orchestrator = Orchestrator()

@cl.on_chat_start
async def start():
    sid = id(cl.user_session)
    cl.user_session.set("sid", sid)
    memory.update(sid, memory.get(sid))
    await cl.Message(content="ITSM Intelligent MCP Agent Ready.").send()

@cl.on_message
async def main(message: cl.Message):

    sid = cl.user_session.get("sid")

    response = orchestrator.handle(
        sid=sid,
        query=message.content,
        memory=memory
    )

    await cl.Message(content=response).send()