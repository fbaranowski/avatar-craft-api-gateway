from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError, TransportServerError

from auth.settings import AuthSettings
from crud.exceptions import GraphQLQueryException

transport = AIOHTTPTransport(url=AuthSettings.GRAPHQL_API_URL)


async def create_user(email):
    async with Client(transport=transport, fetch_schema_from_transport=False) as client:
        query = gql(
            """
            mutation ($email: String!) {
                createUser(email: $email) {
                    id
                    mail
                }
            }
            """
        )
        variables = {"email": email}
        try:
            await client.execute(query, variable_values=variables)
        except (TransportServerError, TransportQueryError) as error:
            raise GraphQLQueryException(err=error)
