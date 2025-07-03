class Post:
    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        content: str,
        user_id: str,
        date: str,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.content = content
        self.user_id = user_id
        self.date = date
