from typing import List
from parser import Loader
from schemas import ParsedData, Person, Project
from typing import List, Dict, Optional


def get_available_projects(data: ParsedData) -> List[Project]:
    available_projects: List[Project] = []
    for proj in data.projects:
        if not proj.is_project_finished or \
                len(proj.currently_assigned_persons_to_skills) != len(proj.skills_contributers_needed):
            available_projects.append(proj)
    return available_projects


def get_available_persons(data: ParsedData) -> List[Person]:
    return list(filter(lambda p: not p.is_working_on_project, data.persons))


def find_best_project_to_mentor(person: Person, projects: List[Project]) -> Optional[Project]:
    for proj in projects:
        skills_left = proj.skills_contributers_needed - \
                      set(proj.currently_assigned_persons_to_skills_to_contribute.values())
        skills_left_to_mentor = skills_left - \
                                set().union(*proj.currently_assigned_persons_to_skills_to_mentor.values())
        possible_assignees: Dict[]
        for skill in person.skills:
            if any(skill.skill_name == skill_left.skill_name and \
                   skill.skill_level >= skill_left.skill_level
                   for skill_left in skills_left):
                # We can assign this person to the skill of the project
                #


def assign_person_to_most_suitable_project(person: Person, projects: List[Project]):
    # Find the project the person can mentor on the most
    # Find the project the person can contribute the most
    best_mentored_project: Optional[Project] = find_best_project_to_mentor(person, projects)


def update_end_of_day(data: ParsedData, day: int):
    # Update projects
    for project in data.projects:
        if project.day_project_started is not None:
            project.is_project_finished = project.day_project_started + project.num_time_to_finish <= day

    # Update contributors
    for contributor in data.persons:
        project = contributor.project_working_on
        if project is not None:
            project_end_day: int = project.day_project_started + project.num_time_to_finish - 1
            if day > project_end_day:
                contributor.next_available_day = 0
                contributor.is_working_on_project = True
                contributor.project_working_on = None


def main():
    data: ParsedData = Loader.load("./input_data/a_an_example.in.txt")
    print(data.json(indent=4))

    current_day = 0
    while True:
        available_projects = get_available_projects(data)
        if len(available_projects) == 0:
            break
        available_persons = get_available_persons(data)
        for person in available_persons:
            assign_person_to_most_suitable_project(person, available_projects)
        current_day += 1
        update_end_of_day(data, current_day)


if __name__ == "__main__":
    main()
