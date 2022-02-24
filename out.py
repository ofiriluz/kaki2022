from typing import List
from schemas import PlannedProject


def submit(dataset: str, projects: List[PlannedProject]):
    with open(f"out_{dataset}", "w") as f:
        f.write(f"{len(projects)}")
        for p in projects:
            f.write(p.name)
            f.write(' '.join(p.assignees))
