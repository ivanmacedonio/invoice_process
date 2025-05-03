from abc import ABC, abstractmethod


class IBillPrintService(ABC):
    @abstractmethod
    def __init__(self, payload):
        if not payload:
            raise ValueError('payload is required')

    @abstractmethod
    def _setup_paths(self):
        pass

    @abstractmethod
    def _setup_doc(self):
        pass

    @abstractmethod
    def _save_pdf_and_return_binary(self, doc):
        if not doc:
            raise ValueError('doc is required')

    @abstractmethod
    def _write_invoicer_fields(self):
        pass

    @abstractmethod
    def _write_invoice_type(self):
        pass

    @abstractmethod
    def _write_client_fields(self):
        pass

    @abstractmethod
    def _write_sell_conditions(self):
        pass

    @abstractmethod
    def _write_transaction_row(self):
        pass

    @abstractmethod
    def _write_iva_field(self):
        pass

    @abstractmethod
    def _write_amounts(self):
        pass

    @abstractmethod
    def _write_cae_fields(self):
        pass

    @abstractmethod
    def write_and_get_binary_pdf(self):
        pass
