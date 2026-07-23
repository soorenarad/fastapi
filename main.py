import logging

from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.router import api_router
from core.config import settings


logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.info("Received %s %s", request.method, request.url.path)

        try:
            response = await call_next(request)
        except Exception:
            logger.exception(
                "Unhandled exception while processing %s %s",
                request.method,
                request.url.path,
            )
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"},
            )
        finally:
            logger.info("Finished processing request")

        return response

    app.include_router(api_router)
    return app


app = create_app()

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):

    await websocket.accept()

    while True:

        data = await websocket.receive_text()

        await websocket.send_text(
            f"You sent: {data}"
        )

