class Movie:
    def __init__(self, id: str, title: str, image: str, rating: float, description: str = '', year: int = 0, genre: str = '', duration: str = '', director: str = ''):
        self.id = id
        self.title = title
        self.image = image
        self.rating = rating
        self.description = description        
        self.genre = genre
        self.duration = duration
        self.director = director
       
