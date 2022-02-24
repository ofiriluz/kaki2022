from typing import List

from parser import Loader
from schemas import ParsedData, Person

from statistics import mean


def num_of_high_skills(p: Person, average_skill_level: float) -> float:
    return len([skill for skill in p.skills if skill.skill_level > average_skill_level])

def find_mentors(persons: List[Person]):
    possible_mentors = [p for p in persons if len(p.skills) > 1]
    average_skill_level = mean([skill.skill_level for p in persons for skill in p.skills])
    mentor_scoring = lambda p: num_of_high_skills(p, average_skill_level)*4 + (len(p.skills))*2
    sorted_by_num_of_high_skills = sorted(possible_mentors, key=mentor_scoring, reverse=True)
    return sorted_by_num_of_high_skills[:len(persons)//10]


if __name__ == "__main__":
    data: ParsedData = Loader.load("./input_data/c_collaboration.in.txt")
    # print(data.json(indent=4))
    mentors = find_mentors(data.persons)
