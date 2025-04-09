from app.interfaces.discord_interface import IDiscord
from discordwebhook import Discord
from app.configs.environments import DISCORD_WEBHOOK_URL
from app.entities.dataclasses.discord_message_dataclass import DiscordMessagePayload


class DiscordService(IDiscord):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Discord, cls).__new__(cls, *args, **kwargs)
            cls._instance.discord_instance = Discord(url=DISCORD_WEBHOOK_URL)
        return cls._instance

    @classmethod
    @staticmethod
    def parse_message(content: DiscordMessagePayload):
        return {
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
                {"name": "Fecha de Inicio",
                    "value": content.start_date, "inline": True},
                {"name": "Fecha de Fin", "value": content.end_date, "inline": True},
            ]
        }

    def execute_webhook(self, content: dict):
        parsed_message = self.parse_message(content)
        self._instance.discord_instance.post(embeds=parsed_message)
