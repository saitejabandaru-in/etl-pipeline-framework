from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True)
class LineageEvent:
    stage: str
    rows: int
    details: dict
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


class LineageTracker:
    def __init__(self, pipeline_name: str) -> None:
        self.pipeline_name = pipeline_name
        self.events: list[LineageEvent] = []

    def record(self, stage: str, rows: int, details: dict) -> None:
        self.events.append(LineageEvent(stage=stage, rows=rows, details=details))

    def to_text(self) -> str:
        lines = [f"lineage={self.pipeline_name}"]
        for event in self.events:
            lines.append(f"- {event.stage}: rows={event.rows} at={event.timestamp}")
        return "\n".join(lines)
