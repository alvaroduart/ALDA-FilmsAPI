# env.py
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

load_dotenv()

# Importa o metadata da Base e os modelos reais
from blog.infra.database import Base
from blog.infra.models.user_model import UserModel
from blog.infra.models.movie_model import MovieModel
from blog.infra.models.comment_model import CommentModel
from blog.infra.models.favorite_model import FavoriteModel
from blog.infra.models.history_model import HistoryModel
from blog.infra.models.contact_model import ContactModel

# Carrega as configurações do arquivo .ini
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define o metadata para autogeração das migrations
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Executa as migrations em modo offline (sem conexão direta com o banco)."""
    url = os.environ.get("DATABASE_URL_ALEMBIC")
    if url is None:
        raise Exception("A variável de ambiente 'DATABASE_URL_ALEMBIC' não foi definida.")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Executa as migrations em modo online (com conexão ativa)."""
    url = os.environ.get("DATABASE_URL_ALEMBIC")
    if url is None:
        raise Exception("A variável de ambiente 'DATABASE_URL_ALEMBIC' não foi definida.")

    connectable = engine_from_config(
        {"sqlalchemy.url": url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

# Decide se vai rodar online ou offline
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
