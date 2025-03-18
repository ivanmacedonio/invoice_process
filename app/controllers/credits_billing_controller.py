from flask import Blueprint, request
from app.processes.billing_process import billing_facade

credits_billing_blueprint = Blueprint(
    'credits_billing_blueprint',
    __name__
)


@credits_billing_blueprint.route('', methods=["GET"])
def execute_credits_billing():
    args = request.args
    billing_facade(args)
    return {"message": "Running billing procesess for payclub credits."}
