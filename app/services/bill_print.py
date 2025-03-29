import os
import base64
import fitz
from io import BytesIO
from app.configs.logger import logger
from app.utils.create_binary_qr_code import create_binary_qr_code
from app.entities.dtos.invoice_payloads_dto import BillToPrintDTO
from app.interfaces.bill_print_interface import IBillPrintService


class BillPrint(IBillPrintService):

    def __init__(self, payload: BillToPrintDTO):
        self.payload = payload

    def _setup_paths(self):
        self.pdf_path = os.path.join(os.path.dirname(
            __file__), "..", "templates", "input_invoice.pdf")
        self.output_path = "output_invoice.pdf"

    def _setup_doc(self):
        self.doc = fitz.open(self.pdf_path)
        self.page = self.doc[0]

    def _save_pdf_and_return_binary(self, doc):
        binary_buffer = BytesIO()
        doc.save(binary_buffer)
        binary_buffer.seek(0)

        encoded_pdf = base64.b64encode(
            binary_buffer.getvalue()).decode("utf-8")

        logger.info('Invoice PDF has been updated and storaged')

        return encoded_pdf

    def _write_invoicer_fields(self):
        # left side
        self.page.insert_text(
            (20, 100), "DATOS DEL FACTURANTE", fontsize=13, color=(0, 0, 0), fontname="helvetica-bold")
        self.page.insert_text(
            (20, 115), f"Dirección: {self.payload.direccion_facturante}", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (20, 130), f"Teléfono: {self.payload.telefono_facturante}", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (20, 145), f"Email: {self.payload.email_facturante}", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (20, 160), "IVA RESPONSABLE INSCRIPTO", fontsize=11, color=(0, 0, 0))

        # right side
        self.page.insert_text(
            (360, 100), f"Factura B - N°{self.payload.num_comprobante}", fontname="helvetica-bold", fontsize=13, color=(1, 1, 1))
        self.page.insert_text(
            (360, 120), f"Fecha: {self.payload.fecha_factura}", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (470, 120), f"CUIT: {self.payload.cuit}", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (360, 135), "Razon social: Gestion de emprendimientos", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (360, 150), "deportivos SA", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (360, 165), f"Inicio de Actividades: {self.payload.inicio_actividades}", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (360, 180), f"Ingresos brutos: {self.payload.ingresos_brutos}", fontsize=11, color=(0, 0, 0))

    def _write_invoice_type(self):
        self.page.insert_text(
            (293, 115), "B", fontsize=20, color=(0.5, 0.5, 0.5), fontname="helvetica-bold")
        self.page.insert_text(
            (270, 140), "COD 06", fontsize=15, color=(0.5, 0.5, 0.5), fontname="helvetica-bold")

    def _write_client_fields(self):
        self.page.insert_text(
            (25, 210), "INFORMACIÓN DEL CLIENTE", fontname="helvetica-bold", fontsize=13, color=(0, 0, 0))
        self.page.insert_text(
            (25, 225), f"Cliente: {self.payload.nombre_cliente}", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (25, 240), f"Dirección: {self.payload.direccion_cliente}", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (25, 255), f"Provincia: {self.payload.provincia_cliente}", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (25, 270), f"Email: {self.payload.email_cliente}", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (25, 285), f"Documento: {self.payload.documento_cliente}", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (25, 300), "Condición: Consumidor final", fontsize=11, color=(0, 0, 0))

    def _write_sell_conditions(self):
        self.page.insert_text(
            (360, 210), "CONDICIONES DE VENTA", fontname="helvetica-bold", fontsize=13, color=(0, 0, 0))
        self.page.insert_text(
            (360, 225), "Método de pago: Crédito", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (360, 240), "Tipo: Servicios", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (360, 255), f"Fecha de inicio de servicios: {self.payload.fecha_inicio_servicios}", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (360, 270), f"Fecha de fin de servicios: {self.payload.fecha_fin_servicios}", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (360, 285), f"Fecha de pago del servicio: {self.payload.fecha_pago_servicios}", fontsize=11, color=(0, 0, 0))

    def _write_transaction_row(self):
        self.page.insert_text(
            (30, 363), "1,00", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (100, 363), "Canje de Créditos SportClub", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (430, 363), f"${self.payload.monto_total}", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (520, 363), f"${self.payload.monto_total}", fontsize=11, color=(0, 0, 0))

    def _write_iva_field(self):
        self.page.insert_text(
            (30, 670), "Régimen de Transparencia Fiscal al Consumidor (Ley 27.743)", fontsize=9, color=(0, 0, 0))
        self.page.insert_text(
            (30, 700), f"IVA Contenido $ {self.payload.monto_iva}", fontsize=9, color=(0, 0, 0))

    def _write_amounts(self):
        self.page.insert_text(
            (340, 650), "Subtotal", fontsize=13, color=(0, 0, 0))
        self.page.insert_text(
            (470, 650), f"${self.payload.monto_total}", fontsize=13, color=(0, 0, 0))
        self.page.insert_text(
            (340, 680), "Total Descuento", fontsize=13, color=(0, 0, 0))
        self.page.insert_text(
            (470, 680), "$0", fontsize=13, color=(0, 0, 0))
        self.page.insert_text(
            (340, 713), "Final Total", fontsize=15, fontname="helvetica-bold", color=(1, 1, 1))
        self.page.insert_text(
            (470, 713), f"${self.payload.monto_total}", fontsize=15, fontname="helvetica-bold", color=(1, 1, 1))

    def _write_cae_fields(self):
        qr_code = create_binary_qr_code(payload=self.payload)
        rect = fitz.Rect(30, 730, 100, 810)

        self.page.insert_image(rect, stream=qr_code)
        self.page.insert_text(
            (120, 760), f"N° de CAE: {self.payload.cae}", fontname="helvetica-bold", fontsize=13, color=(0, 0, 0))
        self.page.insert_text(
            (120, 790), f"Fecha de Vencimiento: {self.payload.fecha_vencimiento_cae}", fontname="helvetica-bold", fontsize=13, color=(0, 0, 0))

    def write_and_get_binary_pdf(self):
        # setup
        self._setup_paths()
        self._setup_doc()

        # write fields
        self._write_invoicer_fields()
        self._write_invoice_type()
        self._write_client_fields()
        self._write_sell_conditions()
        self._write_transaction_row()
        self._write_iva_field()
        self._write_amounts()
        self._write_cae_fields()

        # save and return
        binnary_buffer = self._save_pdf_and_return_binary(self.doc)
        return binnary_buffer
