from dataclasses import dataclass, field


@dataclass
class WorkerTask:
    worker_role: str
    task: str


@dataclass
class PlanResult:
    plan_summary: str
    tasks: list[WorkerTask]


@dataclass
class WorkerResult:
    role: str
    findings: str
    data_points: list[str] = field(default_factory=list)


@dataclass
class SupervisorDecision:
    ready_to_aggregate: bool
    follow_up_tasks: list[WorkerTask] = field(default_factory=list)
