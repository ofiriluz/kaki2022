from pydantic import BaseModel, Field
from typing import List, Set


class Skill(BaseModel):
    skill_name: str
    skill_level: int

    def __eq__(self, other):
        if type(other) is type(self):
            return self.skill_name == other.skill_name and self.skill_level == other.skill_level
        else:
            return False

    def __hash__(self):
        return hash((self.skill_level, self.skill_name))

class Person(BaseModel):
    name: str
    skills: Set[Skill] = Field(default_factory=set)


class Project(BaseModel):
    name: str
    num_time_to_finish: int
    score_on_finish: int
    best_before: int
    skills_contributers_needed: List[Skill] = Field(default_factory=list)


class PlannedProject(Project):
    assignees: List[str]


class ParsedData(BaseModel):
    persons: List[Person] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
