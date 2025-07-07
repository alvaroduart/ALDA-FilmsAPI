from datetime import datetime

class History:
    def __init__(self, userId: str, movieId: str):
        self.userId = userId
        self.movieId = movieId
        self.timestamp = datetime.now()
        

   