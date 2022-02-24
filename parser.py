import os
from typing import List
from schemas import Person, Project, Skill, ParsedData, PlannedProject


class Loader:
    @staticmethod
    def load(dataset: str) -> ParsedData:
        if not os.path.exists(dataset):
            raise Exception("FILE NO EXIST")
        with open(dataset, "r") as f:
            lines = f.readlines()
            first_line = lines[0].split(' ', 1)
            num_contributers = int(first_line[0])
            num_projects = int(first_line[1])
            line_idx = 1
            parsed_data = ParsedData()
            for _ in range(num_projects + num_contributers):
                person_or_project = lines[line_idx].split(' ')
                if len(person_or_project) == 2:
                    person = Person(
                        name=person_or_project[0]
                    )
                    num_skills = int(person_or_project[1])
                    line_idx += 1
                    for _ in range(num_skills):
                        skill = lines[line_idx].split(' ')
                        person.skills.append(Skill(
                            skill_name=skill[0],
                            skill_level=int(skill[1])
                        ))
                        line_idx += 1
                    parsed_data.persons.append(person)
                else:
                    project = Project(
                        name=person_or_project[0],
                        num_time_to_finish=int(person_or_project[1]),
                        score_on_finish=int(person_or_project[2]),
                        best_before=int(person_or_project[3])
                    )
                    num_skills = int(person_or_project[4])
                    line_idx += 1
                    for _ in range(num_skills):
                        skill = lines[line_idx].split(' ')
                        project.skills_contributers_needed.append(Skill(
                            skill_name=skill[0],
                            skill_level=int(skill[1])
                        ))
                        line_idx += 1
                    parsed_data.projects.append(project)
            return parsed_data

    @staticmethod
    def save(dataset: str, projects: List[PlannedProject]):
        with open(f"out_{dataset}", "w") as f:
            f.write(f"{len(projects)}\n")
            for p in projects:
                f.write(f"{p.name}\n")
                f.write(f"{' '.join(p.assignees)}\n")
