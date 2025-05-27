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

user_list_responses = {
    200: {
        "description": "Successful response with list of users.",
        "content": {
            "application/json": {
                "examples": {
                    "DefaultList": {
                        "summary": "GET /users",
                        "description": "Returns all users without filters.",
                        "value": [
                            {
                                "id": 1,
                                "name": "John Doe",
                                "cpf": "123.456.789-00",
                                "email": "john@example.com",
                                "password": "strongpassword123",
                                "role": "user"
                            },
                            {
                                "id": 2,
                                "name": "Jane Smith",
                                "cpf": "987.654.321-00",
                                "email": "jane@example.com",
                                "password": "securepass456",
                                "role": "admin"
                            }
                        ]
                    },
                    "FilterByName": {
                        "summary": "GET /users?name=John",
                        "description": "Returns users whose names contain 'John'.",
                        "value": [
                            {
                                "id": 1,
                                "name": "John Doe",
                                "cpf": "123.456.789-00",
                                "email": "john@example.com",
                                "password": "strongpassword123",
                                "role": "user"
                            }
                        ]
                    },
                    "FilterByEmail": {
                        "summary": "GET /users?email=jane@example.com",
                        "description": "Returns users whose emails match 'jane@example.com'.",
                        "value": [
                            {
                                "id": 2,
                                "name": "Jane Smith",
                                "cpf": "987.654.321-00",
                                "email": "jane@example.com",
                                "password": "securepass456",
                                "role": "admin"
                            }
                        ]
                    },
                    "PaginationExample": {
                        "summary": "GET /users?skip=1&limit=1",
                        "description": "Skips the first user and limits the result to one user.",
                        "value": [
                            {
                                "id": 2,
                                "name": "Jane Smith",
                                "cpf": "987.654.321-00",
                                "email": "jane@example.com",
                                "password": "securepass456",
                                "role": "admin"
                            }
                        ]
                    }
                }
            }
        }
    }
}
