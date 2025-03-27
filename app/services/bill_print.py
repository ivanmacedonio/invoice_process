import os
import fitz
from app.configs.logger import logger
from app.utils.create_binary_qr_code import create_binary_qr_code


class BillPrint:

    def __init__(self, invoice):
        self.invoice = invoice

    '''
    Unidades de medida:

    El total del ancho del PDF es de 500px, usar 250 ubica el cursor en el centro del eje X
    El total del alto depende del template seleccionado, se recomienda seguir como referencia
    las etiquetas previamente insertadas
    '''

    def _setup_paths(self):
        self.pdf_path = os.path.join(os.path.dirname(
            __file__), "..", "templates", "input_invoice.pdf")
        self.output_path = "output_invoice.pdf"

    def _setup_doc(self):
        self.doc = fitz.open(self.pdf_path)
        self.page = self.doc[0]

    def _save_pdf(self, doc):
        doc.save(self.output_path)
        logger.info('Invoice PDF has been updated and storaged')
        doc.close()

    def _write_invoicer_fields(self):
        # left side
        self.page.insert_text(
            (20, 100), "DATOS DEL FACTURANTE", fontsize=13, color=(0, 0, 0), fontname="helvetica-bold")
        self.page.insert_text(
            (20, 115), "Dirección: Calle falsa 123", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (20, 130), "Teléfono: 12312312312", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (20, 145), "Email: soporte@hola.com", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (20, 160), "IVA RESPONSABLE INSCRIPTO", fontsize=11, color=(0, 0, 0))

        # right side
        self.page.insert_text(
            (360, 100), "Factura B - N°00044-00513118", fontname="helvetica-bold", fontsize=13, color=(1, 1, 1))
        self.page.insert_text(
            (360, 120), "Fecha: 12/12/12", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (470, 120), "CUIT: 1212121212", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (360, 135), "Razon social: Gestion de emprendimientos", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (360, 150), "deportivos SA", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (360, 165), "Inicio de Actividades: 12/12/12", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (360, 180), "Ingresos brutos: 1212121212", fontsize=11, color=(0, 0, 0))

    def _write_invoice_type(self):
        self.page.insert_text(
            (293, 115), "B", fontsize=20, color=(0.5, 0.5, 0.5), fontname="helvetica-bold")
        self.page.insert_text(
            (270, 140), "COD 06", fontsize=15, color=(0.5, 0.5, 0.5), fontname="helvetica-bold")

    def _write_client_fields(self):
        self.page.insert_text(
            (25, 210), "INFORMACIÓN DEL CLIENTE", fontname="helvetica-bold", fontsize=13, color=(0, 0, 0))
        self.page.insert_text(
            (25, 225), "Cliente: ivan macedonio", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (25, 240), "Dirección: calle falsa 123", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (25, 255), "Provincia: Buenos Aires", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (25, 270), "Email: imacedonio@corp.sportclub.com.ar", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (25, 285), "Documento: 455747162", fontsize=11, color=(0, 0, 0))
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
            (360, 255), "Fecha de inicio de servicios: 2025-03-09", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (360, 270), "Fecha de fin de servicios: 2025-04-09", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (360, 285), "Fecha de pago del servicio: 2025-03-10", fontsize=11, color=(0, 0, 0))

    def _write_transaction_row(self):
        self.page.insert_text(
            (30, 363), "1,00", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (100, 363), "Canje de Créditos SportClub", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (430, 363), "$1.000", fontsize=11, color=(0, 0, 0))
        self.page.insert_text(
            (520, 363), "$1.000", fontsize=11, color=(0, 0, 0))

    def _write_iva_field(self):
        self.page.insert_text(
            (30, 670), "Régimen de Transparencia Fiscal al Consumidor (Ley 27.743)", fontsize=9, color=(0, 0, 0))
        self.page.insert_text(
            (30, 700), "IVA Contenido $ 7.253,82", fontsize=9, color=(0, 0, 0))

    def _write_amounts(self):
        self.page.insert_text(
            (340, 650), "Subtotal", fontsize=13, color=(0, 0, 0))
        self.page.insert_text(
            (470, 650), "$1.000", fontsize=13, color=(0, 0, 0))
        self.page.insert_text(
            (340, 680), "Total Descuento", fontsize=13, color=(0, 0, 0))
        self.page.insert_text(
            (470, 680), "$0", fontsize=13, color=(0, 0, 0))
        self.page.insert_text(
            (340, 715), "Final Total $1.000", fontsize=15, fontname="helvetica-bold", color=(1, 1, 1))

    def _write_cae_fields(self):
        qr_code = create_binary_qr_code(invoice=self.invoice)
        rect = fitz.Rect(400, 700, 500, 800)

        self.page._insert_image(rect, stream=qr_code, filename="qr_code.png")
        self.page.insert_text(
            (120, 760), "N° de CAE: 74377718712214", fontname="helvetica-bold", fontsize=13, color=(0, 0, 0))
        self.page.insert_text(
            (120, 790), "Fecha de Vencimiento: 21/09/2024", fontname="helvetica-bold", fontsize=13, color=(0, 0, 0))

    def write_pdf(self):
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

        # save
        self._save_pdf(self.doc)
