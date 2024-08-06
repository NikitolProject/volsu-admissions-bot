from pydantic import BaseModel


class UserSchema(BaseModel):
    id_card: int
    faculty: str
    is_entered: bool
