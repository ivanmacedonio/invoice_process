from dataclasses import dataclass


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
