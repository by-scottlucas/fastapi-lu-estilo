unauthorized_responses = {
    401: {
        "description": "Unauthorized error responses.",
        "content": {
            "application/json": {
                "examples": {
                    "InvalidCredentials": {
                        "summary": "Invalid email or password",
                        "value": {"detail": "Invalid email or password."}
                    },
                    "InvalidRefreshToken": {
                        "summary": "Invalid refresh token",
                        "value": {"detail": "Invalid refresh token."}
                    },
                    "RefreshTokenExpired": {
                        "summary": "Refresh token expired",
                        "value": {"detail": "Refresh token expired."}
                    }
                }
            }
        }
    }
}

conflict_response = {
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