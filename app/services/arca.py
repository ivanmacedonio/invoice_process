from afip import Afip
from app.configs.logger import logger
from app.entities.dtos.arca_bill_dto import ARCABillDTO
from datetime import datetime
from dataclasses import asdict
from app.utils.validate_fields import validate_fields
from app.interfaces.arca_interface import IBillingService, IBuildManager, IInstanceManager
from app.interfaces.bill_repository_interface import IBillRepository
from threading import Lock


class BillingService(IBillingService):
    def __init__(self, instance_manager: IInstanceManager, builder_manager: IBuildManager, repository: IBillRepository) -> None:
        self.instance_manager = instance_manager
        self.builder_manager = builder_manager
        self.repository = repository

    def bill(self, transaction: dict) -> dict:
        invoicer_data = self.repository.get_unique_invoicer()
        arca_instance: Afip = self.instance_manager.get_or_create_instance(
            invoicer_data)
        invoice = self.builder_manager.build_type_b_invoice(
            transaction, invoicer_data, arca_instance)
        arca_response = arca_instance.ElectronicBilling.createVoucher(invoice)
        return {
            "message": arca_response,
            "builded_bill": invoice
        }


class InstanceManager(IInstanceManager):

    def __init__(self, billing_processor):
        self.billing_processor = billing_processor

    _instance_lock = Lock()
    _instance = None

    def get_or_create_instance(self, invoicer_data: dict) -> Afip:
        with self._instance_lock:
            if self._instance is None:
                secret_key = invoicer_data.get('arca_secret_key', None)
                certify = invoicer_data.get('arca_certify', None)
                cuit: str = invoicer_data.get('cuit', None)
                formatted_cuit = int(cuit.replace("-", ""))
                if not all([secret_key, certify, cuit]):
                    raise ValueError(
                        "secret_key, certify and cuit are required to initializate ARCA")

                logger.info("Initializing Afip instance...")
                self._instance = self.billing_processor({
                    "CUIT": 20409378472,
                    # "cert": certify,
                    # "key": secret_key
                })
            return self._instance


class BuildManager(IBuildManager):

    def build_type_b_invoice(self, transaction: dict, invoicer_data: dict, arca_instance: Afip) -> dict:
        ptoVta = int(invoicer_data.get("punto_de_venta", None))
        BILL_TYPE_B_CODE = 6

        last_voucher_number = arca_instance.ElectronicBilling.getLastVoucher(
            ptoVta, BILL_TYPE_B_CODE)
        current_voucher_name = last_voucher_number + 1
        today_formatted = int(datetime.today().strftime("%Y%m%d"))

        importe_gravado = int(transaction.get('amount', None))
        importe_excento_iva = 0
        iva_percentage = 0.21
        importe_iva = importe_gravado * iva_percentage

        validate_fields(target_fields={
            "transaction": transaction,
            "transaction_amount": importe_gravado,
            "current_voucher": current_voucher_name,
            "punto_de_venta": ptoVta,
            "last_voucher_number": last_voucher_number
        }, error_message="missing fields while trying to build the invoice")

        payload = ARCABillDTO(
            CantReg=1,
            PtoVta=ptoVta,
            CbteTipo=BILL_TYPE_B_CODE,
            Concepto=3,
            DocTipo=99,
            DocNro=0,
            CbteDesde=current_voucher_name,
            CbteHasta=current_voucher_name,
            CbteFch=today_formatted,
            FchServDesde=today_formatted,
            FchServHasta=today_formatted,
            FchVtoPago=today_formatted,
            ImpTotal=importe_gravado + importe_excento_iva + importe_iva,
            ImpTotConc=0,
            ImpNeto=importe_gravado,
            ImpOpEx=importe_excento_iva,
            ImpIVA=importe_iva,
            ImpTrib=0,
            MonId="PES",
            MonCotiz=1,
            Iva=[
                {
                    "Id": 5,
                    "BaseImp": importe_gravado,
                    "Importe": importe_iva
                }
            ]
        )
        return asdict(payload)
