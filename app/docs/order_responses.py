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
                                "payment_method": "credit_card",
                                "payment_status": "pending",
                                "total_amount": 12000,
                                "created_at": "2025-05-25T15:30:00Z",
                                "order_items": [
                                    {
                                        "id": 1,
                                        "product_id": 101,
                                        "quantity": 3,
                                        "price_at_moment": 4000,
                                        "product": {
                                            "id": 101,
                                            "name": "Men's Cotton T-Shirt",
                                            "sale_price": 39.99,
                                            "description": "Soft and breathable cotton t-shirt, available in multiple colors.",
                                            "stock": 50,
                                            "bar_code": "8801234567890",
                                            "category": "Apparel",
                                            "expiration_date": None,
                                            "images": [
                                                {"id": 1, "image_path": "/images/products/tshirt1.jpg"},
                                                {"id": 2, "image_path": "/images/products/tshirt2.jpg"}
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
                                "id": 2,
                                "client_id": 2,
                                "status": "completed",
                                "payment_method": "credit_card",
                                "payment_status": "paid",
                                "total_amount": 8000,
                                "created_at": "2025-05-20T10:00:00Z",
                                "order_items": [
                                    {
                                        "id": 3,
                                        "product_id": 102,
                                        "quantity": 2,
                                        "price_at_moment": 4000,
                                        "product": {
                                            "id": 102,
                                            "name": "Women's Denim Jacket",
                                            "sale_price": 79.99,
                                            "description": "Stylish denim jacket with button closure and side pockets.",
                                            "stock": 25,
                                            "bar_code": "8801234567891",
                                            "category": "Apparel",
                                            "expiration_date": None,
                                            "images": [
                                                {"id": 3, "image_path": "/images/products/jacket1.jpg"},
                                                {"id": 4, "image_path": "/images/products/jacket2.jpg"}
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
                                "payment_method": "credit_card",
                                "payment_status": "pending",
                                "total_amount": 12000,
                                "created_at": "2025-05-25T15:30:00Z",
                                "order_items": [
                                    {
                                        "id": 1,
                                        "product_id": 101,
                                        "quantity": 3,
                                        "price_at_moment": 4000,
                                        "product": {
                                            "id": 101,
                                            "name": "Men's Cotton T-Shirt",
                                            "sale_price": 39.99,
                                            "description": "Soft and breathable cotton t-shirt, available in multiple colors.",
                                            "stock": 50,
                                            "bar_code": "8801234567890",
                                            "category": "Apparel",
                                            "expiration_date": None,
                                            "images": [
                                                {"id": 1, "image_path": "/images/products/tshirt1.jpg"},
                                                {"id": 2, "image_path": "/images/products/tshirt2.jpg"}
                                            ]
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    "FilterByDateRange": {
                        "summary": "GET /orders?start_date=2025-05-20&end_date=2025-05-26",
                        "description": "Returns orders created within the given date range.",
                        "value": [
                            {
                                "id": 3,
                                "client_id": 3,
                                "status": "pending",
                                "payment_method": "paypal",
                                "payment_status": "pending",
                                "total_amount": 6000,
                                "created_at": "2025-05-22T12:00:00Z",
                                "order_items": [
                                    {
                                        "id": 5,
                                        "product_id": 103,
                                        "quantity": 1,
                                        "price_at_moment": 6000,
                                        "product": {
                                            "id": 103,
                                            "name": "Silk Scarf",
                                            "sale_price": 59.99,
                                            "description": "Elegant silk scarf with floral pattern, perfect for all seasons.",
                                            "stock": 15,
                                            "bar_code": "8801234567892",
                                            "category": "Accessories",
                                            "expiration_date": None,
                                            "images": [
                                                {"id": 5, "image_path": "/images/products/scarf1.jpg"},
                                                {"id": 6, "image_path": "/images/products/scarf2.jpg"}
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
