import csv
from io import StringIO
from typing import (
    BinaryIO,
    TextIO,
)

from fastapi import Depends

from .operations import OperationsService
from .. import models


class ReportsService:
    report_fields = [
        'date',
        'kind',
        'amount',
        'description',
    ]

    def __init__(self, operations_service: OperationsService = Depends()):
        self.operations_service = operations_service

    def import_csv(self, user_id: int, file: BinaryIO):
        reader = csv.DictReader(
            (line.decode() for line in file),
            fieldnames=self.report_fields,
        )
        next(reader, None)  # Skip the header
        operations_data = []
        for row in reader:
            operation_data = models.OperationCreate.parse_obj(row)
            if operation_data.description == '':
                operation_data.description = None
            operations_data.append(operation_data)
        self.operations_service.create_many(
            user_id,
            operations_data,
        )

    def export_csv(self, user_id: int) -> TextIO:
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=self.report_fields,
            extrasaction='ignore',
        )

        operations = self.operations_service.get_many(user_id)

        writer.writeheader()
        for operation in operations:
            operation_data = models.Operation.from_orm(operation)
            writer.writerow(operation_data.dict())

        output.seek(0)
        return output
