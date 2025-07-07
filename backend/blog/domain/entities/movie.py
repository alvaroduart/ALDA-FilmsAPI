class Movie:
    def __init__(self, id: str, title: str, image: str, rating: float, description: str = None, year: int = None, genre: str = None, duration: str = None, director: str = None, cast: list[str] = None):
        self.id = id
        self.title = title
        self.image = image
        self.rating = rating
        self.description = description        
        self.genre = genre
        self.duration = duration
        self.director = director
       
