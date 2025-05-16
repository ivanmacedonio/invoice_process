from enum import Enum


class MercadopagoProductTypeEnum(Enum):
    RECEIVED_POINTS = "Received Points"

    def __str__(self):
        return str(self.value)
