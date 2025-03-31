from typing import TypedDict

class WebhookData(TypedDict):
    user_id: int
    id: int
    type: str
    trace_id: str