import json
import base64
import qrcode
from app.config.dependencies import ARCA_QR_CODE_GENERATOR_URL
import io
from app.domain.entities.dtos.invoice_payloads_dto import BillToPrintDTO


def create_binary_qr_code(payload: BillToPrintDTO):
    url = ARCA_QR_CODE_GENERATOR_URL
    formatted_cuit = int(payload.cuit.replace("-", ""))

    data = {
        'ver': 1,
        'fecha': payload.fecha_factura,
        'cuit': formatted_cuit,
        'ptoVta': int(payload.punto_de_venta),
        'tipoCmp': 6,
        'nroCmp': int(payload.num_comprobante),
        'importe': float(payload.monto_total),
        'moneda': 'PES',
        'ctz': float(1.000),
        'tipoDocRec': 99,
        'nroDocRec': 0,
        'tipoCodAut': 'E',
        'codAut': int(payload.cae)
    }

    data_json = json.dumps(data)
    url = url % (base64.b64encode(data_json.encode('ascii')).decode('ascii'))

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return img_byte_arr
