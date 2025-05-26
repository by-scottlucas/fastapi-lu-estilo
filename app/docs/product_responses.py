product_not_found_response = {
    404: {
        "description": "Product not found.",
        "content": {
            "application/json": {
                "example": {"detail": "Product not found."}
            }
        }
    }
}

product_conflict_response = {
    409: {
        "description": "Conflict: Product with same barcode already exists.",
        "content": {
            "application/json": {
                "examples": {
                    "BarCodeConflict": {
                        "summary": "Barcode already exists",
                        "value": {"detail": "Product with this barcode already registered."}
                    }
                }
            }
        }
    }
}

invalid_product_data_response = {
    422: {
        "description": "Validation error: Invalid product data.",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "loc": ["body", "name"],
                            "msg": "field required",
                            "type": "value_error.missing"
                        }
                    ]
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

product_list_responses = {
    200: {
        "description": "A list of products was successfully retrieved.",
        "content": {
            "application/json": {
                "examples": {
                    "/products": {
                        "summary": "All products (no filters)",
                        "value": [
                            {
                                "id": 1,
                                "name": "Summer Floral Dress",
                                "description": "Light dress with floral print for warm days.",
                                "sale_price": 129.90,
                                "stock": 18,
                                "bar_code": "1002003004001",
                                "category": "Dresses",
                                "images": []
                            },
                            {
                                "id": 2,
                                "name": "Skinny Jeans",
                                "description": "Slim fit dark wash jeans.",
                                "sale_price": 159.90,
                                "stock": 0,
                                "bar_code": "1002003004002",
                                "category": "Pants",
                                "images": []
                            }
                        ]
                    },
                    "/products?stock=true": {
                        "summary": "Products available in stock",
                        "value": [
                            {
                                "id": 1,
                                "name": "Summer Floral Dress",
                                "description": "Light dress with floral print for warm days.",
                                "sale_price": 129.90,
                                "stock": 18,
                                "bar_code": "1002003004001",
                                "category": "Dresses",
                                "images": []
                            }
                        ]
                    },
                    "/products?stock=false": {
                        "summary": "Products out of stock",
                        "value": [
                            {
                                "id": 2,
                                "name": "Skinny Jeans",
                                "description": "Slim fit dark wash jeans.",
                                "sale_price": 159.90,
                                "stock": 0,
                                "bar_code": "1002003004002",
                                "category": "Pants",
                                "images": []
                            }
                        ]
                    },
                    "/products?category=Dresses": {
                        "summary": "Filter by category: Dresses",
                        "value": [
                            {
                                "id": 1,
                                "name": "Summer Floral Dress",
                                "description": "Light dress with floral print for warm days.",
                                "sale_price": 129.90,
                                "stock": 18,
                                "bar_code": "1002003004001",
                                "category": "Dresses",
                                "images": []
                            },
                            {
                                "id": 3,
                                "name": "Midi Social Dress",
                                "description": "Perfect for events and corporate environment.",
                                "sale_price": 189.90,
                                "stock": 12,
                                "bar_code": "1002003004003",
                                "category": "Dresses",
                                "images": []
                            }
                        ]
                    },
                    "/products?min_price=150": {
                        "summary": "Products priced at or above $150",
                        "value": [
                            {
                                "id": 2,
                                "name": "Skinny Jeans",
                                "description": "Slim fit dark wash jeans.",
                                "sale_price": 159.90,
                                "stock": 0,
                                "bar_code": "1002003004002",
                                "category": "Pants",
                                "images": []
                            },
                            {
                                "id": 3,
                                "name": "Midi Social Dress",
                                "description": "Perfect for events and corporate environment.",
                                "sale_price": 189.90,
                                "stock": 12,
                                "bar_code": "1002003004003",
                                "category": "Dresses",
                                "images": []
                            }
                        ]
                    },
                    "/products?max_price=100": {
                        "summary": "Products priced at or below $100",
                        "value": [
                            {
                                "id": 4,
                                "name": "Basic Women's Blouse",
                                "description": "Light blouse for everyday wear.",
                                "sale_price": 89.90,
                                "stock": 30,
                                "bar_code": "1002003004004",
                                "category": "Blouses",
                                "images": []
                            }
                        ]
                    },
                    "/products?stock=true&category=Blouses&max_price=100": {
                        "summary": "Combined filter: in stock, category Blouses, price up to $100",
                        "value": [
                            {
                                "id": 4,
                                "name": "Basic Women's Blouse",
                                "description": "Light blouse for everyday wear.",
                                "sale_price": 89.90,
                                "stock": 30,
                                "bar_code": "1002003004004",
                                "category": "Blouses",
                                "images": []
                            }
                        ]
                    },
                    "/products?skip=0&limit=1": {
                        "summary": "Pagination: first product in the list",
                        "value": [
                            {
                                "id": 1,
                                "name": "Summer Floral Dress",
                                "description": "Light dress with floral print for warm days.",
                                "sale_price": 129.90,
                                "stock": 18,
                                "bar_code": "1002003004001",
                                "category": "Dresses",
                                "images": []
                            }
                        ]
                    }
                }
            }
        }
    },
    404: {
        "description": "No products found matching the given filters.",
        "content": {
            "application/json": {
                "example": {
                    "detail": "No products found for the given criteria."
                }
            }
        }
    }
}