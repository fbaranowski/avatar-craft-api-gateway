class Query:
    users = """
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

    avatars = """
        query ($email: String!, $avatar_id: Int, $avatar_type: String) {
            avatars(email: $email, avatarId: $avatar_id, avatarType: $avatar_type) {
                id
                name
                url
                type
            }  
        } 
    """


class Mutation:
    create_avatar = """
        mutation ($email: String!, $aiModel: String!, $prompt: String!) {
            createAvatar(email: $email, aiModel: $aiModel, prompt: $prompt) {
                id
                name
                url
                type
            }
        }
    """

    edit_avatar = """
        mutation ($email: String!, $avatarsUrls: [String!]!, $aiModel: String!, $prompt: String!) {
            editAvatar(email: $email, avatarsUrls: $avatarsUrls, aiModel: $aiModel, prompt: $prompt) {
                id
                name
                url
                type
            }
        }
    """

    delete_avatar = """
        mutation ($email: String!, $avatarId: Int!) {
            deleteAvatar(email: $email, avatarId: $avatarId)
        }
    """
