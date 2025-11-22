from flask import Flask, request, jsonify

from exceptions.user_exceptions import UserAlreadyExists, AuthenticationFailed
from logic.users_logic import UserLogic
from sdk.request.login_parameters import LoginRequestParameters
from sdk.request.register_parameters import RegisterRequestParameters
from sdk.response.user_token import UserAuthTokenResponse


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
            try:
                request_parameters = RegisterRequestParameters(
                    name=request.json["name"],
                    email=request.json["email"],
                    password=request.json["password"]
                )
                user_token = self.user_logic.register(request_parameters)
                return UserAuthTokenResponse(user_token).__dict__, 200
            except UserAlreadyExists as e:
                return jsonify({"error": e.message}), e.status_code
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route("/login", methods=["POST"])
        def login():
            try:
                request_parameters = LoginRequestParameters(
                    email=request.json["email"],
                    password=request.json["password"]
                )
                auth_token = self.user_logic.login(request_parameters)
                return UserAuthTokenResponse(auth_token).__dict__, 200
            except AuthenticationFailed as e:
                return jsonify({"error": e.message}), e.status_code

        # @self.app.route("/todos", methods=["POST"])
        # def create_todo():