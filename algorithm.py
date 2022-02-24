from schemas import ParsedData, PlannedProject
from typing import List
from abc import abstractmethod


class Algorithm:
    data: ParsedData

    def __init__(self, data: ParsedData):
        self.data = data

    @abstractmethod
    def solve(self) -> List[PlannedProject]:
        return []
