from sqlalchemy import (
    Column, Integer, BigInteger,
    Boolean, PrimaryKeyConstraint,
    String
)
from src.domain.models.base_model import entity_meta


class UserModel(entity_meta):
    __tablename__ = "users"

    id = Column(Integer)
    id_card = Column(BigInteger, nullable=False) # СНИЛС
    faculty = Column(String(255), nullable=False)
    is_entered = Column(Boolean, nullable=False)

    PrimaryKeyConstraint(id)

    def normalize(self) -> dict:
        return {
            "id": int(self.id.__str__()),
            "id_card": int(self.id_card.__str__()),
            "faculty": self.faculty.__str__(),
            "is_entered": bool(self.is_blocked.__str__())
        }
