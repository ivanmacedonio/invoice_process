from dataclasses import dataclass


@dataclass
class MercadopagoAuthQueryPayload:
    url: str
    username: str
    password: str
    body: dict
    headers: dict


@dataclass
class MercadopagoQueryPayload:
    url: str
    headers: dict
