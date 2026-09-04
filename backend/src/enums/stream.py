from enum import StrEnum


class StreamEventType(StrEnum):
    WORKFLOW_STARTED = "workflow_started"
    NODE_STARTED = "node_started"
    MESSAGE = "message"
    NODE_FINISHED = "node_finished"
    WORKFLOW_FINISHED = "workflow_finished"
    ERROR = "error"
