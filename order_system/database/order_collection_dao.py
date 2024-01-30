import json

from bson import ObjectId
from flask import current_app
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.errors import InvalidId


class OrderCollectionDAO:
    def __init__(self, collection: Collection):
        self.__order_collection: Collection = collection
        self.menu_price = {
            "Hamburger": 10,
            "Chicken Sandwich": 8,
            "Fries": 2,
            "Salad": 3,
            "Coke": 2,
            "Sweet Tea": 2,
            "Milkshake": 6,
        }

    def get_order_data(self, order_id: str) -> Cursor:
        """根據輸入的 order_id ，在資料庫中找出相對應的 order 資料。若 id 不存在則返回 None

        :param order_id: 想索取的 order 的 id
        :return: order data
        """
        try:
            data = self.__order_collection.find_one(ObjectId(order_id))
            current_app.logger.info(
                "Successfully retrieve order from mongoDB order collection"
            )
            total_price = 0
            for product_name in data.get("items", []):
                if self.menu_price.get(product_name):
                    total_price += self.menu_price[product_name]
                else:
                    return {"status": "error", "message": "No product found"}

            return {
                "_id": str(data.get("_id", "")),
                "customer": data.get("customer", ""),
                "orderTime": data.get("orderTime", ""),
                "items": data.get("items", []),
                "totalPrice": total_price,
                "status": "success",
            }
        except InvalidId:
            current_app.logger.info("Fail to get order from mongoDB order collection")
            return None

    def create_order_data(self, order: json) -> ObjectId:
        """根據輸入的 order 資料，在資料庫中創建一筆相對應的 order

        :param order: 要 insert 的 order 資料
        :return: 成功 insert 的資料的 id
        """
        result = self.__order_collection.insert_one(order)
        current_app.logger.info(
            "Successfully inserted order: " + str(result.inserted_id)
        )
        return result.inserted_id
