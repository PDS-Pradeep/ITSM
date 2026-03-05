# agents/question.py
import json
from core.message import A2AMessage
from core.llm import call_llm

class QuestionAgent:

    def receive(self, message, memory):

        missing = message.payload["missing_fields"]
        context = message.payload["context"]

        system_prompt = f"""
You are a clarification agent.

Generate clear, concise questions for the missing fields.

Missing fields:
{missing}

Context:
{json.dumps(context["slots"])}

Return STRICT JSON:

{{
  "questions": []
}}
"""

        result = call_llm(system_prompt, "Generate clarification questions.", temperature=0.3)

        question = result["questions"][0] if result["questions"] else "Please provide required details."

        return A2AMessage(
            sender="QuestionAgent",
            receiver="User",
            intent="ASK_USER",
            payload={"message": question},
            sid=message.sid
        )