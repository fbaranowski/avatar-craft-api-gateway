from fastapi import HTTPException


class GraphQLQueryException(HTTPException):
    def __init__(self, err):
        super().__init__(status_code=500, detail=f"GraphQL query failed {err}")


class AdminPrivilegesRequiredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403, detail="Admin privileges required to get other users' info"
        )
