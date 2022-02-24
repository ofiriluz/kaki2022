from parser import Loader
from schemas import ParsedData


if __name__ == "__main__":
    data: ParsedData = Loader.load("./input_data/a_an_example.in.txt")
    print(data.json(indent=4))
