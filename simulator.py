from typing import List
from parser import Loader
from schemas import ParsedData, Person, Project, Skill
from typing import List, Dict, Optional, Tuple


def get_available_projects(data: ParsedData) -> List[Project]:
    available_projects: List[Project] = []
    for proj in data.projects:
        if not proj.is_project_finished or \
                len(proj.currently_assigned_persons_to_skills) != len(proj.skills_contributers_needed):
            available_projects.append(proj)
    return available_projects


def get_available_persons(data: ParsedData) -> List[Person]:
    return list(filter(lambda p: not p.is_working_on_project, data.persons))


def find_best_project_to_be_assigned_to(person: Person, projects: List[Project]) -> Tuple[Optional[Project],
                                                                                          Optional[Skill],
                                                                                          Optional[List[Skill]]]:
    possible_projects_to_assign: Dict[str, List[Skill]] = {}
    for proj in projects:
        skills_left = set(proj.skills_contributers_needed) - \
                      set(proj.currently_assigned_persons_to_skills_to_contribute.values())
        possible_assignees: List[Skill] = []
        for skill in person.skills:
            for skill_left in skills_left:
                if skill.skill_name == skill_left.skill_name and \
                        skill.skill_level >= skill_left.skill_level:
                    # We can assign this person to the skill of the project
                    possible_assignees.append(skill_left)
        if possible_assignees:
            possible_projects_to_assign[proj.name] = possible_assignees
    if len(possible_projects_to_assign) == 0:
        return None, None, None
    most_suitable_skill_per_project: Dict[str, Skill] = {}
    for proj, skills in possible_projects_to_assign.items():
        curr_min = -1
        best_skill = None
        for skill in skills:
            person_skill = next(filter(lambda per_skill: per_skill.skill_name == skill.skill_name,
                                       person.skills))
            distance = person_skill.skill_level - skill.skill_level
            if curr_min == -1 or distance <= curr_min:
                curr_min = distance
                best_skill = person_skill
        most_suitable_skill_per_project[proj] = best_skill
    # Check if the person can also mentor any of the projects
    max_skill_amount_can_mentor = -1
    best_proj = None
    skills_can_mentor = None
    for proj_name, skill in most_suitable_skill_per_project.items():
        proj = next(filter(lambda project: project.name == proj_name,
                           projects))
        skills_left = set(proj.skills_contributers_needed) - \
                      set(proj.currently_assigned_persons_to_skills_to_contribute.values()) - \
                      set(skill) - \
                      set().union(*proj.currently_assigned_persons_to_skills_to_mentor)
        skills_can_mentor = map(lambda skill_left:
                                (any(skill_left.skill_name == other_skill.skill_name and
                                     other_skill.skill_level >= skill_left.skill_level for
                                     other_skill in person.skills), skill_left),
                                skills_left)
        skills_amount_can_mentor = sum(map(lambda s: s[0], skills_can_mentor))
        if max_skill_amount_can_mentor == -1 or skills_amount_can_mentor >= max_skill_amount_can_mentor:
            max_skill_amount_can_mentor = skills_amount_can_mentor
            best_proj = proj
            skills_can_mentor = list(map(lambda s: s[1], skills_can_mentor))
    return best_proj, most_suitable_skill_per_project[best_proj.name], skills_can_mentor


def assign_person_to_most_suitable_project(person: Person, projects: List[Project], current_day: int):
    # Find the project the person can mentor on the most
    # Find the project the person can contribute the most
    best_assigned_project, skill_to_contribute, skills_can_mentor = find_best_project_to_be_assigned_to(person, projects)
    if not best_assigned_project:
        return
    best_assigned_project.currently_assigned_persons_to_skills_to_contribute[person.name] = skill_to_contribute
    best_assigned_project.currently_assigned_persons_to_skills_to_mentor[person.name] = skills_can_mentor
    person.is_working_on_project = True
    person.project_working_on = best_assigned_project
    if len(best_assigned_project.skills_contributers_needed) == \
            len(best_assigned_project.currently_assigned_persons_to_skills_to_contribute):
        best_assigned_project.day_project_started = current_day


def update_projects_and_persons(projects: List[Project], persons: List[Person], current_day: int):
    updated_scores = 0
    for project in projects:
        if not project.day_project_started:
            continue
        days_passed = current_day - project.day_project_started
        if days_passed == project.num_time_to_finish:
            project.is_project_finished = True
            overdue = max(0, current_day - project.best_before)
            updated_scores += project.score_on_finish - overdue
            for person_name in project.currently_assigned_persons_to_skills_to_contribute.keys():
                person = next(filter(lambda p: p.name == person_name, persons))
                person.is_working_on_project = False
                person.project_working_on = None
    return updated_scores


# def add_idle_people_as_mentored(persons: List[Person], projects: List[Project]):
#     for proj in projects:
#



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
    final_score = 0
    while True:
        available_projects = get_available_projects(data)
        if len(available_projects) == 0:
            break
        available_persons = get_available_persons(data)
        for person in available_persons:
            assign_person_to_most_suitable_project(person, available_projects, current_day)
        available_projects = get_available_projects(data)
        if len(available_projects) == 0:
            break
        available_persons = get_available_persons(data)
        add_idle_people_as_mentored(available_persons, available_projects)
        current_day += 1
        final_score += update_projects_and_persons(data.projects, data.persons, current_day)


if __name__ == "__main__":
    main()
