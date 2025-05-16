"""Initial migration

Revision ID: 2f59cd5dd59a
Revises: 
Create Date: 2025-03-21 09:44:16.711449

"""
from typing import Sequence, Union
import uuid
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f59cd5dd59a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'facturantes',
        sa.Column('id', sa.UUID(), primary_key=True, default=uuid.uuid4),
        sa.Column('cuit', sa.String(), nullable=False),
        sa.Column('razon_social', sa.String(), nullable=False),
        sa.Column('inicio_actividades', sa.DateTime(), nullable=False),
        sa.Column('ii_bb', sa.Integer(), nullable=False),
        sa.Column('telefono', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('numero_cae', sa.String(), nullable=False),
        sa.Column('punto_de_venta', sa.String(), nullable=False),
        sa.Column('fecha_vencimiento_cae', sa.DateTime(), nullable=False),
        sa.Column('arca_secret_key', sa.String(), nullable=False),
        sa.Column('arca_certify', sa.String(), nullable=False),
    )

    op.create_table(
        'clientes',
        sa.Column('id', sa.UUID(), primary_key=True, default=uuid.uuid4),
        sa.Column('nombre_completo', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('documento', sa.String(), nullable=False),
        sa.Column('documento_tipo', sa.String(), nullable=False),
        sa.Column('provincia', sa.String(), nullable=False),
        sa.Column('domicilio', sa.String(), nullable=False),
        sa.Column('codigo_postal', sa.String(), nullable=False)
    )

    op.create_table(
        'facturas',
        sa.Column('id', sa.UUID(), primary_key=True, default=uuid.uuid4),
        sa.Column('facturante_id', sa.UUID(), sa.ForeignKey(
            'facturantes.id'), nullable=False),
        sa.Column('cliente_id', sa.UUID(), sa.ForeignKey(
            'clientes.id'), nullable=False),
        sa.Column('tipo_comprobante', sa.Integer(), nullable=False),
        sa.Column('num_comprobante', sa.Integer(), nullable=False),
        sa.Column('punto_de_venta', sa.Integer(), nullable=False),
        sa.Column('fecha_factura', sa.DateTime(),
                  default=sa.func.now(), nullable=False),
        sa.Column('Mercadopago_payment_id', sa.String(), nullable=False)
    )

    op.create_table(
        'ventas',
        sa.Column('id', sa.UUID(), primary_key=True, default=uuid.uuid4),
        sa.Column('factura_id', sa.UUID(), sa.ForeignKey(
            'facturas.id'), nullable=False),
        sa.Column('inicio_servicios', sa.DateTime(), nullable=False),
        sa.Column('fin_servicios', sa.DateTime(), nullable=False),
        sa.Column('fecha_de_pago', sa.DateTime(), nullable=False),
        sa.Column('importe_total', sa.Integer(), nullable=False),
        sa.Column('importe_neto', sa.Integer(), nullable=False),
        sa.Column('importe_iva', sa.Integer(), nullable=False)
    )

    op.create_foreign_key('fk_facturante_factura', 'facturas',
                          'facturantes', ['facturante_id'], ['id'])
    op.create_foreign_key('fk_cliente_factura', 'facturas',
                          'clientes', ['cliente_id'], ['id'])
    op.create_foreign_key('fk_venta_factura', 'ventas',
                          'facturas', ['factura_id'], ['id'])


def downgrade() -> None:
    op.drop_table('facturas')
    op.drop_table('clientes')
    op.drop_table('caes')
    op.drop_table('facturantes')
    op.drop_table('ventas')
