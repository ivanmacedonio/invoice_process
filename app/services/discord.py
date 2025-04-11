from app.interfaces.discord_interface import IDiscord, ICounterManager
from discordwebhook import Discord
from app.configs.environments import DISCORD_WEBHOOK_URL
from app.entities.dataclasses.discord_message_dataclass import DiscordMessagePayload


class DiscordService(IDiscord):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DiscordService, cls).__new__(
                cls, *args, **kwargs)
            cls._instance.discord_instance = Discord(url=DISCORD_WEBHOOK_URL)
        return cls._instance

    @staticmethod
    def parse_message(content: DiscordMessagePayload):
        return [
            {
                "title": content.title,
                "description": content.description,
                "fields": [
                    {"name": "Facturas procesadas en total",
                     "value": content.total_invoices_count, "inline": True},
                    {"name": "Facturas procesadas correctamente",
                     "value": content.approved_invoices_count, "inline": True},
                    {"name": "Facturas procesadas erroneamente",
                     "value": content.rejected_invoices_count, "inline": True},
                    {"name": "Monto total facturado",
                     "value": content.invoiced_amount, "inline": True},
                ]
            }
        ]

    def execute_webhook(self, content: DiscordMessagePayload):
        parsed_message = self.parse_message(content)
        response = self._instance.discord_instance.post(embeds=parsed_message)
        return response


class CounterManager(ICounterManager):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CounterManager, cls).__new__(
                cls, *args, **kwargs)
            cls._instance.amounts = {
                "invoices": 0,
                "approved": 0,
                "money_amount": 0
            }
        return cls._instance

    @classmethod
    def push_approved(cls, v: int):
        cls._instance.amounts['approved'] += v
        return cls

    @classmethod
    def push_total(cls, v: int):
        cls._instance.amounts['invoices'] += v

    @classmethod
    def push_money_amount(cls, v: int):
        cls._instance.amounts['money_amount'] += v

    def get_amounts(self):
        return self._instance.amounts
