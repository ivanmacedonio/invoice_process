from interfaces.payclub_interface import IPayclubService, IPayclubRepository


class PayclubService(IPayclubService):

    def __init__(self):
        pass

    def get_last_24_hours_transactions(self, repository: IPayclubRepository):
        pass
