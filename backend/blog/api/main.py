from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from blog.api.routes import (
    user_route,
    movie_route,
    comment_route,
    favorite_route,
    history_route,
    contact_route,
)

from blog.api.openapi_tags import openapi_tags

app = FastAPI(
    title="Films API",
    description="API backend de Filmes com Clean Architecture, FastAPI e PostgreSQL",
    version="1.0.0",
    contact={
        "name": "Álvaro Mendes",
        "email": "alvarohenriqueduartemendes98@gmail.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    openapi_tags=openapi_tags,
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def ola():
    return {"olá": "fastapi"}


# Inclusão das rotas
app.include_router(user_route.router, prefix="/users", tags=["Users"])
app.include_router(movie_route.router, prefix="/movies", tags=["Movies"])
app.include_router(comment_route.router, prefix="/comments", tags=["Comments"])
app.include_router(favorite_route.router, prefix="/favorites", tags=["Favorites"])
app.include_router(history_route.router, prefix="/history", tags=["History"])
app.include_router(contact_route.router, prefix="/contacts", tags=["Contacts"])
