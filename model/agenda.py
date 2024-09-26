from enum import Enum
from typing import List

class Agenda(Enum):
    AGENDA_ONE = "agenda1"
    AGENDA_TWO = "agenda2"
    AGENDA_THREE = "agenda3"

    @classmethod
    def from_name(cls, agenda_name: str):
        for agenda in cls:
            if agenda.value == agenda_name:
                return agenda
        return None

    @classmethod
    def get_all_except(cls, agenda):
        return [ag for ag in cls if ag != agenda]

    def __str__(self):
        return self.value
    
    @classmethod
    def get_by_name(cls, name):
        if name == "agenda1":
            return Agenda.AGENDA_ONE
        if name == "agenda2":
            return Agenda.AGENDA_TWO
        if name == "agenda3":
            return Agenda.AGENDA_THREE
        return None

