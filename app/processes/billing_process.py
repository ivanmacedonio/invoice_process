from services.billing import Billing


def billing_process():

    billing_instance = Billing()
    billing_instance.set_tasks([f'task {i}' for i in range(20)])
    billing_instance.run()
