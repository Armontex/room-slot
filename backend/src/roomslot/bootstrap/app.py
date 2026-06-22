from fastapi import FastAPI

from roomslot.api.routers import api_router
from roomslot.bootstrap.admin import register_admin
from roomslot.bootstrap.engine import create_db_engine
from roomslot.bootstrap.lifespan import lifespan
from roomslot.bootstrap.register_exception_handlers import register_exception_handlers
from roomslot.bootstrap.register_middlewares import register_middlewares
from roomslot.config.settings import get_settings
from roomslot.logging.setup import setup_logging


def create_app() -> FastAPI:
    settings = get_settings()

    setup_logging(settings.logging)

    engine = create_db_engine(settings.db)

    app = FastAPI(
        title=settings.service.name,
        version=settings.service.version,
        debug=False,
        lifespan=lifespan,
    )

    app.state.settings = settings
    app.state.engine = engine

    register_admin(
        app=app,
        engine=engine,
        settings=settings.admin,
    )

    app.include_router(api_router)

    register_middlewares(app, settings)
    register_exception_handlers(app)

    return app
