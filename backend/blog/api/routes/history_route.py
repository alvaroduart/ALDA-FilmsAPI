from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from typing import List
from blog.api.schemas.history_schema import HistoryInput, HistoryOutput
from blog.domain.repositories.history_repository import HistoryRepository
from blog.api.deps import get_current_user, get_history_repository
from blog.usecases.history.add_to_history import AddToHistoryUseCase
from blog.usecases.history.get_user_history import GetUserHistoryUseCase
from blog.usecases.history.remove_from_history import RemoveFromHistoryUseCase

security = HTTPBearer()
router = APIRouter(prefix="/history", tags=["History"])


@router.post("/", response_model=HistoryOutput)
async def add_to_history(
    data: HistoryInput,
    credentials=Depends(security),
    user=Depends(get_current_user),
    repo: HistoryRepository = Depends(get_history_repository),
):
    usecase = AddToHistoryUseCase(repo)
    result = await usecase.execute(user.id, data.movieId)
    return HistoryOutput.from_entity(result)


@router.get("/", response_model=List[HistoryOutput])
async def get_user_history(
    user=Depends(get_current_user),
    credentials=Depends(security),
    repo: HistoryRepository = Depends(get_history_repository),
):
    usecase = GetUserHistoryUseCase(repo)
    history = await usecase.execute(user.id)
    return [HistoryOutput.from_entity(h) for h in history]


@router.delete("/", status_code=204)
async def remove_from_history(
    data: HistoryInput,
    user=Depends(get_current_user),
    credentials=Depends(security),
    repo: HistoryRepository = Depends(get_history_repository),
):
    usecase = RemoveFromHistoryUseCase(repo)
    await usecase.execute(user.id, data.movieId)
