from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError, TransportServerError

from crud.exceptions import GraphQLQueryException
from crud.settings import CrudSettings

transport = AIOHTTPTransport(url=CrudSettings.GRAPHQL_API_URL)


async def execute_query(query: str, variables: dict):
    async with Client(transport=transport, fetch_schema_from_transport=False) as client:
        query = gql(query)
        try:
            response = await client.execute(query, variable_values=variables)
            return response
        except (TransportQueryError, TransportServerError) as error:
            raise GraphQLQueryException(error)
