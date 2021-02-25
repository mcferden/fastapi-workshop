from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    UploadFile,
)
from fastapi.responses import StreamingResponse

from .. import models
from ..services.auth import get_current_user
from ..services.reports import ReportsService


router = APIRouter(
    prefix='/reports',
    tags=['reports'],
)


@router.post('/import')
def import_csv(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user: models.User = Depends(get_current_user),
    reports_service: ReportsService = Depends(),
):
    background_tasks.add_task(
        reports_service.import_csv,
        user.id,
        file.file,
    )


@router.get('/export')
def export_csv(
    user: models.User = Depends(get_current_user),
    reports_service: ReportsService = Depends(),
):
    report = reports_service.export_csv(user.id)
    return StreamingResponse(
        report,
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=report.csv'},
    )
