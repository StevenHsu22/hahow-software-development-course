import json

from dependency_injector.wiring import Provide, inject
from flask import current_app, request, jsonify
from flask.views import MethodView

from order_system.database.order_collection_dao import OrderCollectionDAO
from order_system.exception import InvalidAPIUsageException


class CreateOrderHandler:
    @inject
    def __init__(self, order_collection_dao: OrderCollectionDAO):
        self.__order_collection_dao = order_collection_dao

    @staticmethod
    def validate_input(request_body: json):
        """確認 input 是否符合我們 API 的定義

        :param request_body:
        :return:
        """
        # 這裡應該使用 json schema 來驗證會更好，但不希望讓每個人都要花時間學 json schema，因此用最簡單的方法驗證
        allowed_fields = {"customer", "orderTime", "items"}
        for key in request_body.keys():
            if key not in allowed_fields:
                error_msg = "Request has unrecognized field: " + key
                current_app.logger.error(error_msg)
                raise InvalidAPIUsageException(
                    error_type="Invalid Input", message=error_msg, status_code=400
                )

    def handle_request(self, request_body: json):
        # 這兩行只是為了暫時讓 code 通過 pylint，以方便在課堂上進行章節６的示範
        # 同學在完成這個 function 後請將這兩行刪除
        # assert self.__order_collection_dao is not None
        # assert request_body is not None
        # ------------------------------
        current_app.logger.info("Received request: " + str(request_body))

        self.validate_input(request_body)
        order_data = {
            "customer": request_body.get("customer"),
            "orderTime": request_body.get("orderTime"),
            "items": request_body.get("items"),
        }
        response = self.__order_collection_dao.create_order_data(order_data)
        if response is None:
            error_msg = "Request has unrecognized field: id"
            current_app.logger.error(error_msg)
            raise InvalidAPIUsageException(
                error_type="Invalid Input", message=error_msg, status_code=400
            )

        current_app.logger.info("Returning the response: " + response.__str__())

        return {
            "id": response.id,
            "status": "success",
        }


class CreateOrderView(MethodView):
    def __init__(
        self, create_order_handler: CreateOrderHandler = Provide["create_order_handler"]
    ):
        self.__create_order_handler = create_order_handler

    def post(self):
        raw_response = self.__create_order_handler.handle_request(request.json)
        return jsonify(raw_response)
