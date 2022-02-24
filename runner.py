from collections import defaultdict
from typing import List
from parser import Loader
from schemas import ParsedData, Person, Skill
from statistics import mean


def num_of_high_skills(p: Person, average_skill_level: float) -> float:
    return len([skill_name for skill_name, skill_level in p.skills.items() if skill_level > average_skill_level])


def find_mentors_by_skill(persons: List[Person]):
    res = defaultdict(list)
    _mentors = find_mentors(persons)
    for p in _mentors:
        for skill_name in p.skills.keys():
            res[skill_name].append(p)

    return res


def find_mentors(persons: List[Person]):
    possible_mentors = [p for p in persons if len(p.skills) > 1]
    average_skill_level = mean([skill_level for p in persons for skill_level in p.skills.values()])
    mentor_scoring = lambda p: num_of_high_skills(p, average_skill_level) * 4 + (len(p.skills)) * 2
    sorted_by_num_of_high_skills = sorted(possible_mentors, key=mentor_scoring, reverse=True)
    return sorted_by_num_of_high_skills[:len(persons) // 10]


def find_people_that_need_mentoring(persons: List[Person], skill_name: str, required_level_for_project: int):
    return [
        p for p in persons if skill_name in p.skills and p.skills[skill_name] == (required_level_for_project - 1)
    ]


if __name__ == "__main__":
    data: ParsedData = Loader.load("./input_data/c_collaboration.in.txt")
    # print(data.json(indent=4))
    mentors_by_skill = find_mentors_by_skill(data.persons)

    for project in data.projects:
        for skill_name_required, skill_level_required in project.skills_contributors_needed.items():
            people_that_need_mentoring = find_people_that_need_mentoring(data.persons, skill_name_required,
                skill_level_required)
            possible_mentors = mentors_by_skill[skill_name_required]
