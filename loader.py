import os
from schemas import Person, Project, Skill, ParsedData


class Loader:
    @staticmethod
    def load(file_path):
        if not os.path.exists(file_path):
            raise Exception("FILE NO EXIST")
        with open(file_path, "r") as f:
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
                        project.skills.append(Skill(
                            skill_name=skill[0],
                            skill_level=int(skill[1])
                        ))
                        line_idx += 1
                    parsed_data.projects.append(project)
            return parsed_data

