from dataclasses import dataclass
from datetime import datetime


@dataclass
class DiscordMessagePayload:
    title: str
    description: str
    total_invoices_count: int
    approved_invoices_count: int
    rejected_invoices_count: int
    invoiced_amount: int
    start_date: datetime
    end_date: datetime
