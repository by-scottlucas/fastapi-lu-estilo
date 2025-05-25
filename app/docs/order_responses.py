order_not_found_response = {
    404: {
        "description": "Order not found.",
        "content": {
            "application/json": {
                "example": {"detail": "Order not found."}
            }
        }
    }
}

order_conflict_response = {
    409: {
        "description": "Conflict: Order cannot be processed.",
        "content": {
            "application/json": {
                "examples": {
                    "OrderAlreadyProcessed": {
                        "summary": "Order already processed",
                        "value": {"detail": "Order has already been processed and cannot be modified."}
                    },
                    "InvalidOrderStatus": {
                        "summary": "Invalid order status",
                        "value": {"detail": "The status provided for the order is invalid."}
                    }
                }
            }
        }
    }
}

internal_server_error_response = {
    500: {
        "description": "Internal server error.",
        "content": {
            "application/json": {
                "example": {"detail": "Internal server error."}
            }
        }
    }
}

order_list_responses = {
    200: {
        "description": "Successful response with list of orders.",
        "content": {
            "application/json": {
                "examples": {
                    "DefaultList": {
                        "summary": "GET /orders",
                        "description": "Returns all orders without any filters applied.",
                        "value": [
                            {
                                "id": 1,
                                "client_id": 1,
                                "status": "pending",
                                "payment_method": "bank_slip",
                                "payment_status": "pending",
                                "total_amount": 15000,
                                "created_at": "2025-05-25T15:30:00Z",
                                "order_items": [
                                    {
                                        "id": 1,
                                        "product_id": 18,
                                        "quantity": 2,
                                        "price_at_moment": 7500,
                                        "product": {
                                            "id": 1,
                                            "name": "Apple iPhone 14",
                                            "sale_price": 999.99,
                                            "description": "Latest model with A15 chip",
                                            "stock": 10,
                                            "bar_code": "1234567890123",
                                            "category": "Smartphones",
                                            "expiration_date": "2025-12-31",
                                            "images": [
                                                {"id": 1, "image_path": "/images/product1.jpg"},
                                                {"id": 2, "image_path": "/images/product2.jpg"}
                                            ]
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    "FilterByStatus": {
                        "summary": "GET /orders?status=completed",
                        "description": "Returns only completed orders.",
                        "value": [
                            {
                                "id": 1,
                                "client_id": 1,
                                "status": "completed",
                                "payment_method": "bank_slip",
                                "payment_status": "paid",
                                "total_amount": 15000,
                                "created_at": "2025-05-25T15:30:00Z",
                                "order_items": [
                                    {
                                        "id": 1,
                                        "product_id": 18,
                                        "quantity": 2,
                                        "price_at_moment": 7500,
                                        "product": {
                                            "id": 1,
                                            "name": "Apple iPhone 14",
                                            "sale_price": 999.99,
                                            "description": "Latest model with A15 chip",
                                            "stock": 10,
                                            "bar_code": "1234567890123",
                                            "category": "Smartphones",
                                            "expiration_date": "2025-12-31",
                                            "images": [
                                                {"id": 1, "image_path": "/images/product1.jpg"},
                                                {"id": 2, "image_path": "/images/product2.jpg"}
                                            ]
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    "FilterByClientId": {
                        "summary": "GET /orders?client_id=1",
                        "description": "Returns orders placed by client ID 1.",
                        "value": [
                            {
                                "id": 1,
                                "client_id": 1,
                                "status": "pending",
                                "payment_method": "bank_slip",
                                "payment_status": "pending",
                                "total_amount": 15000,
                                "created_at": "2025-05-25T15:30:00Z",
                                "order_items": [
                                    {
                                        "id": 1,
                                        "product_id": 18,
                                        "quantity": 2,
                                        "price_at_moment": 7500,
                                        "product": {
                                            "id": 1,
                                            "name": "Apple iPhone 14",
                                            "sale_price": 999.99,
                                            "description": "Latest model with A15 chip",
                                            "stock": 10,
                                            "bar_code": "1234567890123",
                                            "category": "Smartphones",
                                            "expiration_date": "2025-12-31",
                                            "images": [
                                                {"id": 1, "image_path": "/images/product1.jpg"},
                                                {"id": 2, "image_path": "/images/product2.jpg"}
                                            ]
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    "FilterByDateRange": {
                        "summary": "GET /orders?start_date=2025-05-25&end_date=2025-05-26",
                        "description": "Returns orders created within the given date range.",
                        "value": [
                            {
                                "id": 1,
                                "client_id": 1,
                                "status": "pending",
                                "payment_method": "bank_slip",
                                "payment_status": "pending",
                                "total_amount": 15000,
                                "created_at": "2025-05-25T15:30:00Z",
                                "order_items": [
                                    {
                                        "id": 1,
                                        "product_id": 18,
                                        "quantity": 2,
                                        "price_at_moment": 7500,
                                        "product": {
                                            "id": 1,
                                            "name": "Apple iPhone 14",
                                            "sale_price": 999.99,
                                            "description": "Latest model with A15 chip",
                                            "stock": 10,
                                            "bar_code": "1234567890123",
                                            "category": "Smartphones",
                                            "expiration_date": "2025-12-31",
                                            "images": [
                                                {"id": 1, "image_path": "/images/product1.jpg"},
                                                {"id": 2, "image_path": "/images/product2.jpg"}
                                            ]
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }
    }
}
