# agents/planner.py
import json
from core.message import A2AMessage
from core.llm import call_llm

class PlannerAgent:

    REQUIRED_FIELDS = [
        "subject", "description",
        "requester_email", "priority", "category"
    ]

    VALID_INTENTS = ["CREATE_TICKET", "OUT_OF_SCOPE"]

    def receive(self, message, memory):

        context = memory.get(message.sid)

        system_prompt = f"""
You are an enterprise ITSM planning agent.

You MUST return only one of these intents:
- CREATE_TICKET (if user reports issue or requests service)
- OUT_OF_SCOPE (if unrelated to IT support)

Never invent any other intent.

Required fields for CREATE_TICKET:
{self.REQUIRED_FIELDS}

Return STRICT JSON only:

{{
  "intent": "CREATE_TICKET or OUT_OF_SCOPE",
  "slots": {{
    "subject": null,
    "description": null,
    "requester_email": null,
    "priority": null,
    "category": null
  }},
  "missing_fields": []
}}

Current known slots:
{json.dumps(context["slots"])}
"""

        result = call_llm(system_prompt, message.payload["query"])

        # Defensive normalization
        intent = result.get("intent", "").strip().upper()

        if intent not in self.VALID_INTENTS:
            intent = "CREATE_TICKET"  # Safe default for ITSM systems

        # Merge slots
        for k, v in result.get("slots", {}).items():
            if v:
                context["slots"][k] = v

        context["intent"] = intent
        memory.update(message.sid, context)

        # If out of scope → respond politely
        if intent == "OUT_OF_SCOPE":
            return A2AMessage(
                sender="PlannerAgent",
                receiver="User",
                intent="OUT_OF_SCOPE",
                payload={
                    "message": "I can assist with IT support requests such as creating tickets. Please describe your issue."
                },
                sid=message.sid
            )

        # If missing fields → Clarification
        missing = result.get("missing_fields", [])

        if missing:
            return A2AMessage(
                sender="PlannerAgent",
                receiver="QuestionAgent",
                intent="MISSING_FIELDS",
                payload={
                    "missing_fields": missing,
                    "context": context
                },
                sid=message.sid
            )

        # Otherwise → Create ticket
        return A2AMessage(
            sender="PlannerAgent",
            receiver="TicketAgent",
            intent="CREATE_TICKET",
            payload={"slots": context["slots"]},
            sid=message.sid
        )