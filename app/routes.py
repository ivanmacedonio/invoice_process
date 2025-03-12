from controllers.credits_billing_controller import credits_billing_blueprint


def register_blueprints(app):

    app.register_blueprint(credits_billing_blueprint,
                           url_prefix="/credits_billing")
