class BaseCustomException(Exception):
    def __init__(self, transaction, message):
        super().__init__(
            f"Transaction with MercadopagoId {transaction.get('txid')}: {message}")


class AlreadyInvoicedException(BaseCustomException):
    def __init__(self, transaction):
        super().__init__(transaction, "Transaction was already invoiced.")


class InvalidTransactionType(BaseCustomException):
    def __init__(self, transaction):
        super().__init__(transaction, "Invalid transaction type.")


class RejectedTransaction(BaseCustomException):
    def __init__(self, transaction):
        super().__init__(transaction, "Transaction was rejected.")
