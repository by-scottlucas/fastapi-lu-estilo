# app/docs/product_responses.py

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
