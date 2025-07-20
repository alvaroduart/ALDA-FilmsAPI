from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from blog.api.deps import get_db_session
from contextlib import asynccontextmanager
import sqlalchemy as sa
from typing import Union, Sequence
from datetime import datetime

from blog.api.routes import (
    user_route,
    movie_route,
    comment_route,
    favorite_route,
    history_route,
    contact_route,
    rating_route,
)

from blog.api.openapi_tags import openapi_tags
from blog.api.filmes_mock import mock_movies
from blog.domain.entities.movie import Movie
import uuid
from blog.infra.models.movie_model import MovieModel
from blog.infra.database import async_session, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event: Criar tabelas e popular dados
    #    async with async_engine.begin() as conn:
    #        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created/checked on startup.")

    # Agora para a população de dados
    async with async_session() as db:  # Use async with para a sessão
        try:
            # Verifica se a tabela já existe e limpa os dados
            # Use await db.scalar(select(func.count()).select_from(MovieModel)) para contar async
            # ou await db.execute(select(MovieModel)) e then .scalars().all() e len()
            # Para uma contagem simples e eficiente:
            total_movies_result = await db.execute(
                sa.select(sa.func.count()).select_from(MovieModel)
            )
            qtd_filmes = total_movies_result.scalar_one()

            if qtd_filmes == 0:
                print("Banco de dados vazio. Populando com dados iniciais...")
                for (
                    movie_data
                ) in (
                    mock_movies
                ):  # Use um nome diferente para evitar conflito com 'movie'
                    # Gerar UUID corretamente no Python antes de inserir
                    movie_id = uuid.uuid4()
                    created_at = datetime.now()

                    await db.execute(  # Use await aqui!
                        sa.text(
                            """
                            INSERT INTO movies (id, title, image, rating, description, genre, duration, director, created_at)
                            VALUES (:id, :title, :image, :rating, :description, :genre, :duration, :director, :created_at)
                        """
                        ),
                        {
                            "id": str(
                                movie_id
                            ),  # UUIDs devem ser strings para o banco de dados
                            "title": movie_data["title"],
                            "image": movie_data["image"],
                            "rating": movie_data["rating"],
                            "description": movie_data["description"],
                            "genre": movie_data["genre"],
                            "duration": movie_data["duration"],
                            "director": movie_data["director"],
                            "created_at": created_at,
                        },
                    )
                await db.commit()  # Use await aqui!
                print("Dados iniciais adicionados com sucesso.")
            else:
                print(
                    f"Banco de dados já contém {qtd_filmes} filmes. Nenhuma população necessária."
                )

        except Exception as e:
            print(f"Erro ao inserir dados iniciais: {e}")
            await db.rollback()  # Em caso de erro, faça rollback assíncrono
        finally:
            # Com 'async with', a sessão é fechada automaticamente ao sair do bloco.
            # Você não precisa mais de db.close() aqui.
            pass

    yield  # Permite que a aplicação FastAPI inicie

    # Shutdown event: Descartar o engine
    await engine.dispose()
    print("Database engine disposed on shutdown.")


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
    lifespan=lifespan,
)

origins = [
    "http://localhost:5173",
    "https://alda-filmsapi.onrender.com"
]

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err["loc"] if isinstance(loc, str))
        errors.append({"field": field, "message": err["msg"]})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Erro de validação nos campos enviados.", "errors": errors},
    )


@app.get("/")
def ola():
    return {"olá": "fastapi"}


# Inclusão das rotas
app.include_router(user_route.router, tags=["Users"])
app.include_router(movie_route.router, tags=["Movies"])
app.include_router(comment_route.router, tags=["Comments"])
app.include_router(favorite_route.router, tags=["Favorites"])
app.include_router(history_route.router, tags=["History"])
app.include_router(contact_route.router, tags=["Contacts"])
app.include_router(rating_route.router, tags=["Ratings"])
