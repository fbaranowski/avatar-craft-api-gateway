class Query:
    create_delete_share = """
        query ($email: String!, $avatar_id: Int!) {
            avatars(email: $email, avatarId: $avatar_id) {
                id
            }
        } 
    """

    shares = """
        query ($email: String!, $avatar_id: Int) {
            avatars(email: $email, avatarId: $avatar_id) {
                id
            }
        } 
    """
