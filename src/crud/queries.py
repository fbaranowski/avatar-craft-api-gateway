class Query:
    users = """
        query ($email: String) {
            users(email: $email) {
                id
                mail
                avatars {
                    id
                    name
                    uuid
                    type
                }
            }
        }
    """

    avatars = """
        query ($email: String!, $avatar_id: Int, $avatar_type: String, $shared_to_email: String, $shared_from_email: String) {
            avatars(email: $email, avatarId: $avatar_id, avatarType: $avatar_type, sharedToEmail: $shared_to_email, sharedFromEmail: $shared_from_email) {
                id
                uuid
                name
                type
            }  
        } 
    """

    download_avatar = """
        query ($email: String!, $avatar_uuid: String!, $shared_to_email: String, $shared_from_email: String) {
            downloadAvatar(email: $email, avatarUuid: $avatar_uuid, sharedToEmail: $shared_to_email, sharedFromEmail: $shared_from_email)
        }
    """


class Mutation:
    create_avatar = """
        mutation ($email: String!, $aiModel: String!, $prompt: String!) {
            createAvatar(email: $email, aiModel: $aiModel, prompt: $prompt) {
                id
                uuid
                name
                type
            }
        }
    """

    delete_avatar = """
        mutation ($email: String!, $avatarId: Int!) {
            deleteAvatar(email: $email, avatarId: $avatarId)
        }
    """
