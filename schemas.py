from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Set


# class Skill(BaseModel):
#     skill_name: str
#     skill_level: int
#
#     def __eq__(self, other):
#         if type(other) is type(self):
#             return self.skill_name == other.skill_name and self.skill_level == other.skill_level
#         else:
#             return False
#
#     def __hash__(self):
#         return hash((self.skill_level, self.skill_name))


class Person(BaseModel):
    name: str
    skills: Dict[str, int] = Field(default_factory=dict)
    is_working_on_project: bool = Field(default=False)
    next_available_day: int = Field(default=0)
    project_working_on: Optional["Project"] = Field()


class Project(BaseModel):
    name: str
    num_time_to_finish: int
    score_on_finish: int
    best_before: int
    skills_contributors_needed: Dict[str, int] = Field(default_factory=dict)
    currently_assigned_persons_to_skills_to_contribute: Dict[Person, str] = Field(default_factory=list)
    currently_assigned_persons_to_skills_to_mentor: Dict[Person, Set[str]] = Field(default_factory=list)
    day_project_started: Optional[int] = Field()
    is_project_finished: bool = Field(default=False)


class PlannedProject(Project):
    assignees: List[str]


class ParsedData(BaseModel):
    persons: List[Person] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
