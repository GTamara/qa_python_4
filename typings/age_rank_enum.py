from enum import Enum, unique

@unique
class AgeRank(Enum):
    ALL = 0
    CHILDREN = 1
    ADULTS = 2
