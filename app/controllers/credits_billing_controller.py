from flask import Blueprint

credits_billing_blueprint = Blueprint(
    'credits_billing_blueprint',
    __name__
)


@credits_billing_blueprint.route('', methods=["GET"])
def execute_credits_billing():
    return {"message": "Running billing procesess for payclub credits."}
