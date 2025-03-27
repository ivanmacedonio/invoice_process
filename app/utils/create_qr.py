import json
import base64
import qrcode


def make_qr(invoice: dict, qr_path: str):
    url = "https://www.afip.gob.ar/fe/qr/?p=%s"

    documento = int(invoice.get('documento', 0))

    if not documento:
        raise ValueError(
            f'{documento} is an invalid document for the QR code creation')

    invoice_date = invoice.get('fecha_factura', None)

    if not invoice_date:
        raise ValueError(
            f'{invoice_date} is an invalid invoice date for the QR code creation')

    fecha_factura = invoice_date.strftime("%Y-%m-%d")

    data = {
        'ver': 1,
        'fecha': fecha_factura,
        'cuit': int(invoice['CUIT']),
        'ptoVta': int(invoice['punto_de_venta']),
        'tipoCmp': int(invoice['tipo_comprobante']),
        'nroCmp': int(invoice['num_comprobante']),
        'importe': float(invoice['importe_total']),
        'moneda': 'PES',
        'ctz': float(1.000),
        'tipoDocRec': 99,
        'nroDocRec': documento,
        'tipoCodAut': 'E',
        'codAut': int(invoice['cae'])
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

    img.save(qr_path, "PNG")
