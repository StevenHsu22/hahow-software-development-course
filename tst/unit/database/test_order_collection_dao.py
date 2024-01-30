from unittest.mock import Mock, create_autospec

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.results import InsertOneResult

from order_system.database.order_collection_dao import OrderCollectionDAO


def test_get_order_when_call_succeed(test_app_context):
    with test_app_context():
        expected = {
                "_id": "111122223333444455556666",
                "customer": "test",
                "orderTime": 1706599106,
                "items": ["Sweet Tea","Chicken Sandwich"],
                "totalPrice": 10,
                "status": "success",
            }
        mock_collection = create_autospec(Collection)
        mock_collection.find_one = Mock(return_value=expected)

        order_dao = OrderCollectionDAO(mock_collection)
        # Valid ObjectId must be a 12-byte input or a 24-character hex string
        test_id = "111122223333444455556666"
        assert order_dao.get_order_data(test_id) == expected
        mock_collection.find_one.assert_called_once_with(ObjectId(test_id))


def test_create_order_when_call_succeed(test_app_context):
    with test_app_context():
        expected_result = Mock(InsertOneResult)
        expected_id = ObjectId("111122223333444455556666")
        expected_result.inserted_id = Mock(return_value=expected_id)
        mock_collection = create_autospec(Collection)
        mock_collection.insert_one = Mock(return_value=expected_result)

        order_dao = OrderCollectionDAO(mock_collection)
        test_order_data = {
                "id": "111122223333444455556666",
                "customer": "test",
                "orderTime": 1706599106,
                "items": ["Sweet Tea","Chicken Sandwich"],
                "totalPrice": 10,
                "status": "success",
            }
        # Valid ObjectId must be a 12-byte input or a 24-character hex string
        assert order_dao.create_order_data(test_order_data) == expected_result.inserted_id
        mock_collection.insert_one.assert_called_once_with(test_order_data)
