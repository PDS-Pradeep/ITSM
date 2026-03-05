# orchestrator.py
from core.message import A2AMessage
from agents.planner import PlannerAgent
from agents.question import QuestionAgent
from agents.ticket import TicketAgent

class Orchestrator:

    def __init__(self):
        self.agents = {
            "PlannerAgent": PlannerAgent(),
            "QuestionAgent": QuestionAgent(),
            "TicketAgent": TicketAgent()
        }

    def handle(self, sid, query, memory):

        message = A2AMessage(
            sender="User",
            receiver="PlannerAgent",
            intent="NEW_QUERY",
            payload={"query": query},
            sid=sid
        )

        return self.route(message, memory)

    def route(self, message, memory):

        if message.receiver == "User":
            return message.payload["message"]

        agent = self.agents.get(message.receiver)

        if not agent:
            return "System error: unknown agent."

        response = agent.receive(message, memory)

        return self.route(response, memory)