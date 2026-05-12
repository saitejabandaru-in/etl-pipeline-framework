from dataclasses import dataclass, field
from time import perf_counter


@dataclass
class PipelineMetrics:
    records_in: int = 0
    records_out: int = 0
    errors: list[str] = field(default_factory=list)
    started_at: float = field(default_factory=perf_counter)
    ended_at: float | None = None

    def finish(self) -> None:
        self.ended_at = perf_counter()

    @property
    def latency_seconds(self) -> float:
        end = self.ended_at if self.ended_at is not None else perf_counter()
        return end - self.started_at

    @property
    def throughput(self) -> float:
        if self.latency_seconds == 0:
            return 0
        return self.records_out / self.latency_seconds

    @property
    def error_rate(self) -> float:
        if self.records_in == 0:
            return 0
        return len(self.errors) / self.records_in
