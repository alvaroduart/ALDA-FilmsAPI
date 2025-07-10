from datetime import datetime

class Comment:
    def __init__(self, id: str, movieId: str, userId: str, userName: str, content: str, createdAt: datetime):
        self.id = id
        self.movieId = movieId
        self.userId = userId
        self.userName = userName
        self.content = content
        self.createdAt = createdAt if createdAt is not None else datetime.now()
      


