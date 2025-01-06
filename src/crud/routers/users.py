from fastapi import APIRouter, Depends, HTTPException

from auth.dependencies import check_admin_role, get_current_user_email
from crud.core import execute_query
from crud.exceptions import AdminPrivilegesRequiredException
from crud.queries import Query

router = APIRouter(prefix="/users")


@router.get("/")
async def users(
    email: str | None = None,
    current_user_email: str = Depends(get_current_user_email),
    is_admin: bool = Depends(check_admin_role),
):
    if (not email and not is_admin) or (email != current_user_email and not is_admin):
        raise AdminPrivilegesRequiredException()

    query = Query.users
    variables = {"email": email}
    response = await execute_query(query, variables)
    return response
