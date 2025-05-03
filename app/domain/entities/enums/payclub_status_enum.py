from enum import Enum


class PayclubTransactionStatus(Enum):
    CONFIRMED = "Confirmed"
    REJECTED = "Rejected"

    def __str__(self):
        return str(self.value)
