class MCPMemory:

    def __init__(self):
        self.store = {}

    def get(self, sid):
        return self.store.get(sid, {
            "intent": None,
            "slots": {},
            "history": []
        })

    def update(self, sid, context):
        self.store[sid] = context