from typing import List

from parser import Loader
from schemas import ParsedData, Person, Skill

from statistics import mean


def num_of_high_skills(p: Person, average_skill_level: float) -> float:
    return len([skill for skill in p.skills if skill.skill_level > average_skill_level])

def find_mentors(persons: List[Person]):
    possible_mentors = [p for p in persons if len(p.skills) > 1]
    average_skill_level = mean([skill.skill_level for p in persons for skill in p.skills])
    mentor_scoring = lambda p: num_of_high_skills(p, average_skill_level)*4 + (len(p.skills))*2
    sorted_by_num_of_high_skills = sorted(possible_mentors, key=mentor_scoring, reverse=True)
    return sorted_by_num_of_high_skills[:len(persons)//10]


def find_people_that_need_mentoring(persons: List[Person], skill: Skill, required_level_for_project):
    return [
        p for p in persons if skill in p.skills and skill.skill_level == (required_level_for_project-1)
    ]

if __name__ == "__main__":
    data: ParsedData = Loader.load("./input_data/c_collaboration.in.txt")
    # print(data.json(indent=4))
    mentors = find_mentors(data.persons)

    for project in data.projects:
        for skill_required in project.skills_contributers_needed:
            people_that_need_mentoring = find_people_that_need_mentoring(data.persons, skill_required, skill_required.skill_level)


