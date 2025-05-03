from dataclasses import dataclass
from typing import List


@dataclass
class ARCABillDTO:
    CantReg: int
    PtoVta: str
    CbteTipo: str
    Concepto: str
    DocTipo: str
    DocNro: str
    CbteDesde: int
    CbteHasta: int
    CbteFch: str
    FchServDesde: str
    FchServHasta: str
    FchVtoPago: str
    ImpTotal: float
    ImpTotConc: float
    ImpNeto: float
    ImpOpEx: float
    ImpIVA: float
    ImpTrib: float
    MonId: str
    MonCotiz: float
    Iva: List
