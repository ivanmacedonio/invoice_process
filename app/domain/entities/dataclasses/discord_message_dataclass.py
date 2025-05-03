from dataclasses import dataclass


@dataclass
class DiscordMessagePayload:
    title: str
    description: str
    total_invoices_count: int
    approved_invoices_count: int
    rejected_invoices_count: int
    invoiced_amount: int
