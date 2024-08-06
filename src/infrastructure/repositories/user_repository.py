from typing import List, Optional

from sqlalchemy.orm import Session, lazyload
from sqlalchemy.orm.session import make_transient

from src.infrastructure.configs.database import get_db_connection
from src.domain.repositories.repository_meta import RepositoryMeta
from src.domain.models.user_model import UserModel


class UserRepository(RepositoryMeta):

    db: Session

    def __init__(self, db: Session = get_db_connection().__next__()) -> None:
        self.db = db

    def list(self) -> List[UserModel]:
        query = self.db.query(UserModel)
        return query.all()

    def get(self, id_card: int) -> Optional[UserModel]:
        return self.db.query(UserModel).filter_by(id_card=id_card).first()

    def create(self, user: UserModel) -> UserModel:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def bulk_create(self, users: List[UserModel]) -> None:
        self.db.bulk_save_objects(users)
        self.db.commit()
    
    def update(self, id_card: int, user: UserModel) -> UserModel:
        old_user = self.get(id_card)
        if old_user:
            old_user.faculty = user.faculty
            old_user.is_entered = user.is_entered
            self.db.merge(old_user)
            self.db.commit()
        return user

    def delete(self, user: UserModel) -> None:
        self.db.delete(user)
        self.db.commit()
        self.db.flush()