from enum import Enum


class SlotState(Enum):
    EMPTY = 0
    PLAYER_1 = 1
    PLAYER_2 = 2

    def to_char(self) -> str:
        if self == SlotState.EMPTY:
            return "-"
        elif self == SlotState.PLAYER_1:
            return "X"
        elif self == SlotState.PLAYER_2:
            return "O"

    @classmethod
    def from_char(cls, char: str):
        if char == "-":
            return cls.EMPTY
        elif char == "X":
            return cls.PLAYER_1
        elif char == "O":
            return cls.PLAYER_2
