from dataclasses import asdict, dataclass

@dataclass
class PayclubAuthQueryPayload:
    url: str
    username: str
    password: str
    body: dict
    headers: dict
