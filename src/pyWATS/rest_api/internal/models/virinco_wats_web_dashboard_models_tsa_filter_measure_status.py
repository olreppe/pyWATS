from enum import IntEnum

class VirincoWATSWebDashboardModelsTSAFilterMeasureStatus(IntEnum):
    VALUE_0 = 0
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_8 = 8
    VALUE_32 = 32
    VALUE_64 = 64
    VALUE_128 = 128
    VALUE_16384 = 16384

    def __str__(self) -> str:
        return str(self.value)
