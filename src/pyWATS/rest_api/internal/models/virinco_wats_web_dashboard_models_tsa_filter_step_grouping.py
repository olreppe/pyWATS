from enum import IntEnum

class VirincoWATSWebDashboardModelsTSAFilterStepGrouping(IntEnum):
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_4 = 4
    VALUE_8 = 8

    def __str__(self) -> str:
        return str(self.value)
