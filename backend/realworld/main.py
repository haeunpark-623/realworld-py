from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from realworld import __version__
from realworld.config import get_settings
from realworld.db import engine
from realworld.errors import RealWorldError
from realworld.routers import articles as articles_router
from realworld.routers import comments as comments_router
from realworld.routers import tags as tags_router
from realworld.routers import users as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="RealWorld API",
        version=__version__,
        description="RealWorld (Conduit) bulletin board — FastAPI backend",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["meta"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.exception_handler(RealWorldError)
    async def realworld_error_handler(request: Request, exc: RealWorldError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"errors": {"body": [exc.message]}},
        )

    app.include_router(users_router.router)
    app.include_router(articles_router.router)
    app.include_router(comments_router.router)
    app.include_router(tags_router.router)

    return app


app = create_app()
