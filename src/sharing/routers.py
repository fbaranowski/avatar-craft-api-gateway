import aiohttp
from fastapi import APIRouter, Depends, HTTPException

from auth.dependencies import get_current_user_email
from crud.core import execute_query
from crud.queries import Query as crud_queries
from sharing.queries import Query as sharing_queries
from sharing.schema import CreateDeleteShare
from sharing.settings import SharingSettings

router = APIRouter(prefix="/shares")


@router.post("/create")
async def create_share(
    share: CreateDeleteShare, from_user_email: str = Depends(get_current_user_email)
):
    query = sharing_queries.create_delete_share
    variables = {"email": from_user_email, "avatar_id": share.avatar_id}

    crud_response = await execute_query(query, variables)

    data = {
        "from_user": from_user_email,
        "to_user": share.to_user_email,
        "avatar_id": crud_response["avatars"][0]["id"],
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"{SharingSettings.SHARING_URL}/create", json=data
        ) as response:
            result = await response.json()
            return result


@router.get("/from")
async def shares_from_user(
    avatar_id: int | None = None, from_user_email: str = Depends(get_current_user_email)
):
    data = {"from_user": from_user_email}

    if avatar_id:
        data["avatar_id"] = avatar_id

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=f"{SharingSettings.SHARING_URL}/shares", params=data
        ) as response:
            result = await response.json()
            return result


@router.get("/to")
async def shares_to_user(
    avatar_id: int | None = None, to_user_email: str = Depends(get_current_user_email)
):
    data = {"to_user": to_user_email}

    if avatar_id:
        data["avatar_id"] = avatar_id

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=f"{SharingSettings.SHARING_URL}/shares", params=data
        ) as response:
            result = await response.json()
            return result


@router.get("/to/detail")
async def avatar_shared_to_user_detail(
    avatar_id: int, email: str = Depends(get_current_user_email)
):
    query = crud_queries.avatars
    variables = {"email": email, "avatar_id": avatar_id}

    check_share = await shares_to_user(to_user_email=email, avatar_id=avatar_id)

    try:
        shared_to_email = check_share[0]["to_user"]
    except IndexError:
        raise HTTPException(status_code=404, detail="Share record not found")

    if shared_to_email == email:
        variables["shared_to_email"] = shared_to_email
        variables["shared_from_email"] = check_share[0]["from_user"]

    response = await execute_query(query, variables)

    return response


@router.get("/to/download", responses={200: {"content": {"image/jpeg": {}}}})
async def avatar_shared_to_user_download(
    avatar_id: int, avatar_uuid: str, email: str = Depends(get_current_user_email)
):
    query = crud_queries.download_avatar
    variables = {"avatar_uuid": avatar_uuid, "email": email}

    check_share = await shares_to_user(to_user_email=email, avatar_id=avatar_id)

    try:
        shared_to_email = check_share[0]["to_user"]
    except IndexError:
        raise HTTPException(status_code=404, detail="Share record not found")

    if shared_to_email == email:
        variables["shared_to_email"] = shared_to_email
        variables["shared_from_email"] = check_share[0]["from_user"]

    response = await execute_query(query, variables)

    return response


@router.delete("/delete")
async def delete_share(
    share: CreateDeleteShare, from_user_email: str = Depends(get_current_user_email)
):
    query = sharing_queries.create_delete_share
    variables = {"email": from_user_email, "avatar_id": share.avatar_id}

    crud_response = await execute_query(query, variables)

    data = {
        "from_user": from_user_email,
        "to_user": share.to_user_email,
        "avatar_id": crud_response["avatars"][0]["id"],
    }

    async with aiohttp.ClientSession() as session:
        async with session.delete(
            url=f"{SharingSettings.SHARING_URL}/delete", json=data
        ) as response:
            result = await response.json()
            return result
