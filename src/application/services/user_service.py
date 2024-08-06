from typing import List, Optional

from src.domain.models.user_model import UserModel
from src.infrastructure.repositories.user_repository import UserRepository
from src.application.schemas.pydantic.user_schema import UserSchema


class UserService:

    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository = UserRepository()) -> None:
        self.user_repository = user_repository

    def create(self, user_schema: UserSchema) -> UserModel:
        return self.user_repository.create(
            UserModel(
                id_card=user_schema.id_card,
                faculty=user_schema.faculty,
                is_entered=user_schema.is_entered
            )
        )
    
    def bulk_create(self, user_schemas: List[UserSchema]) -> None:
        self.user_repository.bulk_create(
            [
                UserModel(
                    id_card=schema.id_card,
                    faculty=schema.faculty,
                    is_entered=schema.is_entered
                ) for schema in user_schemas
            ]
        )

    def get(self, id_card: int) -> Optional[UserModel]:
        return self.user_repository.get(id_card=id_card)
    
    def list(self) -> List[UserModel]:
        return self.user_repository.list()
    
    def update(self, id_card: int, user_schema: UserSchema) -> UserModel:
        return self.user_repository.update(
            id_card=id_card,
            user=UserModel(
                faculty=user_schema.faculty,
                is_entered=user_schema.is_entered
            )
        )
    
    def delete(self, id_card: int) -> None:
        return self.user_repository.delete(
            self.user_repository.get(id_card=id_card)
        )
