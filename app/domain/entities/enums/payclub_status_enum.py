from enum import Enum


class MercadopagoTransactionStatus(Enum):
    CONFIRMED = "Confirmed"
    REJECTED = "Rejected"

    def __str__(self):
        return str(self.value)
