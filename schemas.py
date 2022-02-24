from pydantic import BaseModel, Field
from typing import List


class Skill(BaseModel):
    skill_name: str
    skill_level: int


class Person(BaseModel):
    name: str
    skills: List[Skill] = Field(default_factory=list)


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
