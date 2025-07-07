from blog.domain.entities.history import History
from blog.domain.repositories.history_repository import HistoryRepository
from typing import List


class GetUserHistoryUseCase:
    def __init__(self, repository: HistoryRepository):
        self.repository = repository

    def execute(self, user_id: str) -> List[History]:
        return self.repository.get_by_user_id(user_id)

