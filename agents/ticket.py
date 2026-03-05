# agents/ticket.py
from core.message import A2AMessage
from tools.ticket_tool import create_ticket_tool

class TicketAgent:

    def receive(self, message, memory):

        slots = message.payload["slots"]
        result = create_ticket_tool(slots)

        # Reset memory
        memory.update(message.sid, {
            "intent": None,
            "slots": {},
            "pending_questions": []
        })

        return A2AMessage(
            sender="TicketAgent",
            receiver="User",
            intent="TICKET_CREATED",
            payload={
                "message": f"""
Ticket Created

Ticket ID: {result['ticket_id']}
Status: {result['status']}
"""
            },
            sid=message.sid
        )