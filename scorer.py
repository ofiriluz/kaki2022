from typing import Dict, List, Set

from schemas import PlannedProject


class Scorer:
    projects: List[PlannedProject]
    day: int
    contributor_availability: Dict[str, int]

    def __init__(self, projects: List[PlannedProject]):
        self.projects = projects
        self.day = 0

        contributors: Set[str] = set()
        for p in projects:
            for c in p.assignees:
                contributors.add(c)
        self.contributor_availability = {c: 0 for c in contributors}

    def get(self) -> int:
        score: int = 0

        for p in self.projects:
            self._wait_for_availability(p)
            score += self._single_project(p)
            for c in p.assignees:
                self.contributor_availability[c] = self.day + p.num_time_to_finish
        return score

    def _single_project(self, project: PlannedProject) -> int:
        end_day = self.day + project.num_time_to_finish - 1
        overdue_days = max(0, end_day - project.best_before)
        return project.score_on_finish - overdue_days

    def _wait_for_availability(self, project: PlannedProject):
        for c in project.assignees:
            self.day = max(self.day, self.contributor_availability.get(c))
