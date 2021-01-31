from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class BaseUser(BaseModel):
    email: str
    username: str


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class OperationKind(str, Enum):
    INCOME = 'income'
    OUTCOME = 'outcome'


class BaseOperation(BaseModel):
    date: date
    kind: OperationKind
    amount: Decimal
    description: Optional[str]


class OperationCreate(BaseOperation):
    pass


class OperationUpdate(BaseOperation):
    pass


class Operation(BaseOperation):
    id: int

    class Config:
        orm_mode = True
