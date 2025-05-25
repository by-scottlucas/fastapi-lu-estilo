user_not_found_response = {
    404: {
        "description": "User not found.",
        "content": {
            "application/json": {
                "example": {"detail": "User not found."}
            }
        }
    }
}

user_conflict_response = {
    409: {
        "description": "Conflict: Email or CPF already registered.",
        "content": {
            "application/json": {
                "examples": {
                    "EmailConflict": {
                        "summary": "Email already exists",
                        "value": {"detail": "Email already registered."}
                    },
                    "CPFConflict": {
                        "summary": "CPF already exists",
                        "value": {"detail": "CPF already registered."}
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
