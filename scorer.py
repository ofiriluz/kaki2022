from schemas import PlannedProject


class Scorer:
    @staticmethod
    def single_project(start_day: int, project: PlannedProject) -> int:
        end_day = start_day + project.num_time_to_finish - 1
        overdue_days = max(0, end_day - project.best_before)
        return project.score_on_finish - overdue_days
