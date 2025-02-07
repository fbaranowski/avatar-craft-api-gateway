import base64

from fastapi import APIRouter, Depends, Response

from auth.dependencies import get_current_user_email
from crud.core import execute_query
from crud.queries import Mutation, Query
from crud.schema import CreateAvatar, DeleteAvatar

router = APIRouter(prefix="/avatars")


@router.get("/")
async def avatars(
    email: str = Depends(get_current_user_email),
    avatar_id: int | None = None,
    avatar_type: str | None = None,
):
    query = Query.avatars
    variables = {"email": email, "avatar_id": avatar_id, "avatar_type": avatar_type}

    response = await execute_query(query, variables)

    return response


@router.get("/download", responses={200: {"content": {"image/jpeg": {}}}})
async def download_avatar(
    avatar_uuid: str, email: str = Depends(get_current_user_email)
):
    query = Query.download_avatar
    variables = {"avatar_uuid": avatar_uuid, "email": email}

    response = await execute_query(query, variables)

    base64_image = response.get("downloadAvatar")
    image_bytes = base64.b64decode(base64_image)

    return Response(
        content=image_bytes,
        media_type="image/jpeg",
        headers={"Content-Disposition": f"attachment; filename={avatar_uuid}.jpg"},
    )


@router.post("/create")
async def create_avatar(
    avatar: CreateAvatar, email: str = Depends(get_current_user_email)
):
    mutation = Mutation.create_avatar
    variables = {
        "email": email,
        "aiModel": avatar.ai_model,
        "prompt": avatar.prompt,
    }

    response = await execute_query(mutation, variables)

    return response


@router.delete("/delete")
async def delete_avatar(
    avatar: DeleteAvatar, email: str = Depends(get_current_user_email)
):
    mutation = Mutation.delete_avatar
    variables = {"email": email, "avatarId": avatar.avatar_id}

    response = await execute_query(mutation, variables)

    return response
