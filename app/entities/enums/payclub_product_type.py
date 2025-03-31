from enum import Enum


class PayclubProductTypeEnum(Enum):
    RECEIVED_POINTS = "Received Points"

    def __str__(self):
        return str(self.value)
