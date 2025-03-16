from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class PayclubAuthQueryPayload:
    url: str
    username: str
    password: str
    body: dict
    headers: dict

@dataclass
class PayclubQueryPayload:
    url: str
    headers: dict
