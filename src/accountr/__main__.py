import uvicorn

from .settings import settings


uvicorn.run(
    'accountr.app:app',
    host=settings.server_host,
    port=settings.server_port,
    reload=True,
)
