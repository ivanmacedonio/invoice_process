from datetime import datetime
from app.entities.dtos.invoice_payloads_dto import ClientDTO, SellDTO, BillDTO


class BillBuilder:
    def build_dtos(self, transaction, bill_data):
        today = datetime.now()

        client_dto = ClientDTO(
            documento=transaction['customerNin'],
            documento_tipo='DNI',
            email=transaction['customerEmail'],
            nombre_completo=transaction['storeName'],
            provincia=transaction['provincia'],
            domicilio=transaction['domicilio'],
            codigo_postal=transaction['codigo_postal']
        )

        sell_dto = SellDTO(
            fecha_de_pago=today,
            inicio_servicios=today,
            fin_servicios=today,
            importe_total=bill_data['ImpTotal'],
            importe_iva=bill_data['ImpIVA'],
            importe_neto=bill_data['ImpNeto']
        )

        bill_dto = BillDTO(
            tipo_comprobante=6,
            num_comprobante=bill_data['CbteDesde'],
            fecha_factura=today,
            payclub_payment_id=transaction['txid'],
            punto_de_venta=bill_data['PtoVta']
        )

        return {
            "client": client_dto,
            "sell": sell_dto,
            "bill": bill_dto
        }
