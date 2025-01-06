from fastapi import APIRouter

from crud.core import execute_query
from crud.queries import Mutation, Query
from crud.schema import CreateAvatar, DeleteAvatar, EditAvatar

router = APIRouter(prefix="/avatars")


@router.get("/")
async def avatars(
    email: str, avatar_id: int | None = None, avatar_type: str | None = None
):
    query = Query.avatars
    variables = {"email": email, "avatar_id": avatar_id, "avatar_type": avatar_type}

    response = await execute_query(query, variables)

    return response


@router.post("/create")
async def create_avatar(avatar: CreateAvatar):
    mutation = Mutation.create_avatar_by_text
    variables = {
        "email": avatar.email,
        "aiModel": avatar.ai_model,
        "prompt": avatar.prompt,
    }

    response = await execute_query(mutation, variables)

    return response


@router.patch("/edit")
async def edit_avatar(avatar: EditAvatar):
    mutation = Mutation.create_avatar_by_image
    variables = {
        "email": avatar.email,
        "avatarsUrls": avatar.avatars_urls,
        "aiModel": avatar.ai_model,
        "prompt": avatar.prompt,
    }

    response = await execute_query(mutation, variables)

    return response


@router.delete("/delete")
async def delete_avatar(avatar: DeleteAvatar):
    mutation = Mutation.delete_avatar
    variables = {"email": avatar.email, "avatarId": avatar.avatar_id}

    response = await execute_query(mutation, variables)

    return response
