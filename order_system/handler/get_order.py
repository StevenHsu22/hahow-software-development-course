import json

from dependency_injector.wiring import Provide, inject
from flask import current_app, request, jsonify
from flask.views import MethodView

from order_system.database.order_collection_dao import OrderCollectionDAO
from order_system.exception import InvalidAPIUsageException


class GetOrderHandler:
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
        allowed_fields = {"id", "name"}
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
        order = self.__order_collection_dao.get_order_data(
            order_id=request_body.get("id"),
            # name=request_body.get("name"),
        )
        if order is None:
            error_msg = "Request has unrecognized field: id"
            current_app.logger.error(error_msg)
            raise InvalidAPIUsageException(
                error_type="Invalid Input", message=error_msg, status_code=400
            )

        def construct_order_item(db_menu_item: dict):
            return {
                "id": db_menu_item.get("_id"),
                "customer": db_menu_item.get("customer"),
                "orderTime": db_menu_item.get("orderTime"),
                "items": db_menu_item.get("items"),
                "totalPrice": db_menu_item.get("totalPrice"),
                "status": db_menu_item.get("status"),
            }

        response = {"order": construct_order_item(order)}
        current_app.logger.info("Returning the response: " + response.__str__())

        return response


class GetOrderView(MethodView):
    def __init__(
        self, get_order_handler: GetOrderHandler = Provide["get_order_handler"]
    ):
        self.__get_order_handler = get_order_handler

    def post(self):
        raw_response = self.__get_order_handler.handle_request(request.json)
        return jsonify(raw_response)
