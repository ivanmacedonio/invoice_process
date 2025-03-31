from datetime import datetime
from app.entities.dtos.invoice_payloads_dto import ClientDTO, SellDTO, BillDTO, BillToPrintDTO
from app.utils.parse_datetime_to_string import parse_datetime_to_string
from app.utils.validate_fields import validate_fields


class BillBuilder:
    def build_dtos(self, transaction, bill_data, invoicer_data, cae_data):

        validate_fields(target_fields={
            "transaction": transaction,
            "bill_data": bill_data,
            "invoicer_data": invoicer_data,
            "cae_data": cae_data
        }, error_message="missing fields while trying to execute the builder")

        today = datetime.now()
        today_formatted = parse_datetime_to_string(today)
        transaction['amount'] = abs(transaction.get('amount'))

        client_dto = ClientDTO(
            documento=transaction.get('customerNin'),
            documento_tipo='DNI',
            email=transaction.get('customerEmail'),
            nombre_completo=transaction.get('storeName'),
            provincia=transaction.get('provincia'),
            domicilio=transaction.get('domicilio'),
            codigo_postal=transaction.get('codigo_postal')
        )

        sell_dto = SellDTO(
            fecha_de_pago=today,
            inicio_servicios=today,
            fin_servicios=today,
            importe_total=bill_data.get('ImpTotal'),
            importe_iva=bill_data.get('ImpIVA'),
            importe_neto=bill_data.get('ImpNeto')
        )

        bill_dto = BillDTO(
            tipo_comprobante=6,
            num_comprobante=bill_data.get('CbteDesde'),
            fecha_factura=today,
            payclub_payment_id=transaction.get('txid'),
            punto_de_venta=bill_data.get('PtoVta')
        )

        bill_to_print_dto = BillToPrintDTO(
            nombre_cliente=transaction.get('storeName'),
            documento_cliente=transaction.get('customerNin'),
            direccion_cliente=transaction.get('domicilio'),
            provincia_cliente=transaction.get('provincia'),
            email_cliente=transaction.get('customerEmail'),
            monto_total=abs(transaction.get('amount')),
            monto_iva=bill_data.get('ImpIVA'),
            cae=cae_data.get('CAE'),
            concepto="Servicios",
            cuit=invoicer_data.get('cuit'),
            direccion_facturante="Paraguay 2060",
            email_facturante=invoicer_data.get('email'),
            punto_de_venta=invoicer_data.get('punto_de_venta'),
            metodo_pago="Crédito",
            tipo_servicio="Servicio",
            ingresos_brutos=invoicer_data.get('ii_bb'),
            num_comprobante=bill_data.get('CbteDesde'),
            telefono_facturante=invoicer_data.get('telefono'),
            inicio_actividades=today_formatted,
            fecha_inicio_servicios=today_formatted,
            fecha_factura=today_formatted,
            fecha_fin_servicios=today_formatted,
            fecha_pago_servicios=today_formatted,
            fecha_vencimiento_cae=cae_data.get('CAEFchVto')
        )

        return {
            "client": client_dto,
            "sell": sell_dto,
            "bill": bill_dto,
            "bill_to_print": bill_to_print_dto
        }
