from flask import Blueprint
from processes.billing_process import billing_process

credits_billing_blueprint = Blueprint(
    'credits_billing_blueprint',
    __name__
)

@credits_billing_blueprint.route('', methods=["GET"])
def execute_credits_billing():
    billing_process()
    return {"message": "Running billing procesess for payclub credits."}
