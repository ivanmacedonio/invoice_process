from flask import Blueprint, request
from app.processes.billing_process import billing_process_facade
from app.configs.environments import API_KEY
from app.configs.logger import logger

credits_billing_blueprint = Blueprint(
    'credits_billing_blueprint',
    __name__
)


def validate_api_key_and_get_status(headers):
    request_api_key = headers.get("Authorization")
    if request_api_key != API_KEY:
        logger.error(f'{request_api_key} is an invalid API_KEY')
        return 401
    return 200


@credits_billing_blueprint.route('', methods=["GET"])
def execute_credits_billing():
    status = validate_api_key_and_get_status(request.headers)
    if status > 200:
        return {"message": "Invalid API_KEY."}

    args = request.args
    billing_process_facade(args)
    return {"message": "Running billing procesess for payclub credits."}
