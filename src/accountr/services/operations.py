from typing import (
    List,
    Optional,
)

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from .. import (
    models,
    tables,
)
from ..database import get_session


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_many(self, user_id: int) -> List[tables.Operation]:
        operations = (
            self.session
            .query(tables.Operation)
            .filter(tables.Operation.user_id == user_id)
            .order_by(
                tables.Operation.date.desc(),
                tables.Operation.id.desc(),
            )
            .all()
        )
        return operations

    def get(
        self,
        user_id: int,
        operation_id: int
    ) -> tables.Operation:
        operation = self._get(user_id, operation_id)
        return operation

    def create_many(
        self,
        user_id: int,
        operations_data: List[models.OperationCreate],
    ) -> List[tables.Operation]:
        operations = [
            tables.Operation(
                **operation_data.dict(),
                user_id=user_id,
            )
            for operation_data in operations_data
        ]
        self.session.add_all(operations)
        self.session.commit()
        return operations

    def create(
        self,
        user_id: int,
        operation_data: models.OperationCreate,
    ) -> tables.Operation:
        operation = tables.Operation(
            **operation_data.dict(),
            user_id=user_id,
        )
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(
        self,
        user_id: int,
        operation_id: int,
        operation_data: models.OperationUpdate,
    ) -> tables.Operation:
        operation = self._get(user_id, operation_id)
        for field, value in operation_data:
            setattr(operation, field, value)
        self.session.commit()
        return operation

    def delete(
        self,
        user_id: int,
        operation_id: int,
    ):
        operation = self._get(user_id, operation_id)
        self.session.delete(operation)
        self.session.commit()

    def _get(self, user_id: int, operation_id: int) -> Optional[tables.Operation]:
        operation = (
            self.session
            .query(tables.Operation)
            .filter(
                tables.Operation.user_id == user_id,
                tables.Operation.id == operation_id,
            )
            .first()
        )
        if not operation:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return operation
