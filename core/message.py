# core/message.py
from dataclasses import dataclass
from typing import Dict, Any
import uuid

@dataclass
class A2AMessage:
    sender: str
    receiver: str
    intent: str
    payload: Dict[str, Any]
    sid: str
    trace_id: str = None

    def __post_init__(self):
        if not self.trace_id:
            self.trace_id = str(uuid.uuid4())