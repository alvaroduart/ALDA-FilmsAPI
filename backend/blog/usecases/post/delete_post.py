from blog.domain.repositories.post_repository import PostRepository


class DeletePostUseCase:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def execute(self, post_id: str) -> bool:
        await self.repository.delete(post_id)
        return True
