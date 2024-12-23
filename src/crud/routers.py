import aiohttp
from typing import List
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from settings import CrudSettings
from crud.schema import CreateAvatar, EditAvatar, DeleteAvatar


router = APIRouter()

# GRAPHQL_API_URL = 'http://localhost:8100/graphql'
TRANSPORT = AIOHTTPTransport(url=CrudSettings.GRAPHQL_API_URL)


async def execute_query(query: str, variables: dict):
    async with Client(transport=TRANSPORT, fetch_schema_from_transport=False) as client:
        query = gql(query)
        try:
            response = await client.execute(query, variable_values=variables)
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'GraphQL query failed {str(e)}')


async def execute_mutation(mutation: str, variables: dict):
    async with Client(transport=TRANSPORT, fetch_schema_from_transport=False) as client:
        mutation = gql(mutation)
        try:
            response = await client.execute(mutation, variable_values=variables)
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'GraphQL mutation failed: {str(e)}')


@router.get('/users')
async def users(email: str | None = None):
    query = """
        query ($email: String) {
            users(email: $email) {
                id
                mail
                avatars {
                    id
                    name
                    url
                    type
                }
            }
        }
    """
    variables = {"email": email}

    response = await execute_query(query, variables)
    return response


@router.get('/avatars')
async def avatars(email: str, avatar_id: int | None = None, avatar_type: str | None = None):
    query = """
        query ($email: String!, $avatar_id: Int, $avatar_type: String) {
            avatars(email: $email, avatarId: $avatar_id, avatarType: $avatar_type) {
                id
                name
                url
                type
            }  
        } 
    """
    variables = {'email': email, 'avatar_id': avatar_id, 'avatar_type': avatar_type}

    response = await execute_query(query, variables)
    return response


# @router.post('/avatars/create')
# async def create_avatar(email: str, ai_model: str, prompt: str):
#     mutation = """
#         mutation ($email: String!, $aiModel: String!, $prompt: String!) {
#             createAvatar(email: $email, aiModel: $aiModel, prompt: $prompt) {
#                 id
#                 name
#                 url
#                 type
#             }
#         }
#     """
#     variables = {"email": email, "aiModel": ai_model, "prompt": prompt}
#
#     response = await execute_mutation(mutation, variables)
#     return response


@router.post('/avatars/create')
async def create_avatar(avatar: CreateAvatar):
    mutation = """
        mutation ($email: String!, $aiModel: String!, $prompt: String!) {
            createAvatar(email: $email, aiModel: $aiModel, prompt: $prompt) {
                id
                name
                url
                type
            }
        }
    """
    variables = {"email": avatar.email, "aiModel": avatar.ai_model, "prompt": avatar.prompt}

    response = await execute_mutation(mutation, variables)
    return response


@router.post('/avatars/edit')
async def edit_avatar(avatar: EditAvatar):
    mutation = """
        mutation ($email: String!, $avatarsUrls: [String!]!, $aiModel: String!, $prompt: String!) {
            editAvatar(email: $email, avatarsUrls: $avatarsUrls, aiModel: $aiModel, prompt: $prompt) {
                id
                name
                url
                type
            }
        }
    """
    variables = {"email": avatar.email, "avatarsUrls": avatar.avatars_urls, "aiModel": avatar.ai_model, "prompt": avatar.prompt}

    response = await execute_mutation(mutation, variables)
    return response


@router.delete('/avatars/delete')
async def delete_avatar(avatar: DeleteAvatar):
    mutation = """
        mutation ($email: String!, $avatarId: Int!) {
            deleteAvatar(email: $email, avatarId: $avatarId)
        }
    """
    variables = {"email": avatar.email, "avatarId": avatar.avatar_id}

    response = await execute_mutation(mutation, variables)
    return response
