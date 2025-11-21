from flask import Flask, request, jsonify

from logic.users_logic import UserLogic
from sdk.request.register_parameters import RegisterRequestParameters
from sdk.response.user_token import UserTokenResponse


class TodosController:
    def __init__(self, app: Flask):
        self.app = app
        self.user_logic = UserLogic()
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/health", methods=["GET"])
        def get_health():
            return "OK", 200

        @self.app.route("/register", methods=["POST"])
        def register():
            request_parameters = RegisterRequestParameters(
                name=request.json["name"],
                email=request.json["email"],
                password=request.json["password"]
            )

            user_token = self.user_logic.register(request_parameters)

            return UserTokenResponse(user_token).__dict__, 200