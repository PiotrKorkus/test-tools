from datetime import datetime
import re
from typing import Dict, List


class ResultEntry:
    def __init__(self, json_message: Dict):
        self.timestamp = datetime.fromisoformat(json_message.get("timestamp"))
        self.level = json_message.get("level")
        self.thread_id = json_message.get("threadId")
        self.target = json_message.get("target")

    def __repr__(self) -> str:
        return f"ResultEntry({self.timestamp}, {self.level}, {self.thread_id}, {self.target})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, ResultEntry):
            return NotImplemented
        return self.timestamp == other.timestamp

    def __lt__(self, other) -> bool:
        if not isinstance(other, ResultEntry):
            return NotImplemented
        return self.timestamp < other.timestamp

    def __gt__(self, other) -> bool:
        if not isinstance(other, ResultEntry):
            return NotImplemented
        return self.timestamp > other.timestamp


class ResultRuntime(ResultEntry):
    def __init__(self, json_message: Dict):
        super().__init__(json_message)
        self.id = json_message.get("fields").get("id")
        self.location = json_message.get("fields").get("location")

    ...


class ResultOrchestration(ResultEntry):
    def __init__(self, json_message: Dict):
        super().__init__(json_message)
        self.message = json_message.get("fields").get("message")

    def __repr__(self) -> str:
        return f"ResultEntry({self.message})"

    def __str__(self) -> str:
        return f"ResultOrchestration(timestamp={self.timestamp}, level={self.level}, message={self.message}, target={self.target}, thread_id={self.thread_id})"


def find_log(logs: List[ResultOrchestration], field: str, pattern: str):
    # TODO: Create a class for all Results from single rust execution and implement it there
    regex = re.compile(pattern)
    for log in logs:
        if regex.search(getattr(log, field)):
            return log
    return None
