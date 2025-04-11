from unittest import TestCase
from app.services.discord import DiscordService, CounterManager
from app.entities.dataclasses.discord_message_dataclass import DiscordMessagePayload


class TestDiscordService(TestCase):
    @classmethod
    def setup_message_payload(self):
        self.message = DiscordMessagePayload(
            title="Test Notification triggered by an integration test",
            description="This is a test notification, please ignore.",
            total_invoices_count=10,
            approved_invoices_count=8,
            rejected_invoices_count=2,
            invoiced_amount=1000
        )

    @classmethod
    def setup_discord_instance(self):
        self.discord_instance = DiscordService()

    @classmethod
    def setup_counter_manager_instance(self):
        self.counter_manager_instance = CounterManager()

    @classmethod
    def setUp(self):
        self.setup_message_payload()
        self.setup_discord_instance()
        self.setup_counter_manager_instance()

    def test_discord_instance_works_successfully(self):
        response = self.discord_instance.execute_webhook(content=self.message)

        self.assertIsNotNone(response.status_code)
        self.assertTrue(isinstance(response.status_code, int))
        self.assertTrue(response.status_code < 299)

    def test_counter_manager_works_successfully(self):
        self.counter_manager_instance.push_total(10)
        self.counter_manager_instance.push_approved(5)
        self.counter_manager_instance.push_money_amount(1000)
        results = self.counter_manager_instance.get_amounts()

        self.assertIsNotNone(results)
        self.assertTrue(isinstance(results, dict))
        self.assertTrue(results['invoices'] == 10)
        self.assertTrue(results['approved'] == 5)
        self.assertTrue(results['money_amount'] == 1000)
