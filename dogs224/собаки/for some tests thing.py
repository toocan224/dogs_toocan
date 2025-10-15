import enum
class dogpos(enum.Enum):
    sit = 1
    stand = 2
    lay = 3
    none = 4
print(dogpos.sit.value)