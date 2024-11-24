import logging.config
from contextvars import ContextVar
from pathlib import Path

from jinja2 import FileSystemLoader, select_autoescape
from jinja2.environment import Environment
from litestar import Litestar, Router
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.exceptions import MethodNotAllowedException, NotFoundException
from litestar.logging import LoggingConfig
from litestar.static_files import create_static_files_router
from litestar.template import TemplateConfig

from src import settings
from src.di.container import Container, init_container

from .middlewares.apm import ASGITracingMiddleware
from .middlewares.metrics import PrometheusMiddleware
from .views.htmx.router import router as htmx_router
from .views.rest.common import TestHandler


htmx_router = Router(
    path="/",
    route_handlers=[htmx_router],
)

jinja2_env = Environment(
    loader=FileSystemLoader(
        Path("/www/src/interface/rest/litestar/views/htmx/templates"),
    ),
    autoescape=select_autoescape(),
)


class ExceptionFilter(logging.Filter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.excluded = [MethodNotAllowedException, NotFoundException]

    def filter(self, record) -> bool:
        if record.exc_info:
            etype, _, _ = record.exc_info
            for excluded_exception in self.excluded:
                if issubclass(etype, excluded_exception):
                    return False
        return True


container: ContextVar["Container"] = ContextVar("Container")


async def startup() -> None:
    container.set(
        await init_container(),
    )


async def shutdown():
    c = container.get()
    await c.shutdown_resources()


app = Litestar(
    on_startup=[startup],
    on_shutdown=[shutdown],
    route_handlers=[
        create_static_files_router(path="/static", directories=["/www/media"]),
        TestHandler,
        htmx_router,
    ],
    middleware=[
        # TODO: middlewares can"t handle 404, 405
        ASGITracingMiddleware,
        PrometheusMiddleware,
    ],
    template_config=TemplateConfig(
        instance=JinjaTemplateEngine.from_environment(jinja2_env),
    ),
    # TODO: remove logging_config. useless anymore?
    logging_config=LoggingConfig(
        log_exceptions="always",
        configure_root_logger=False,
        handlers={
            "queue_listener": {
                "class": "litestar.logging.standard.QueueListenerHandler",
                "level": settings.settings.log.LEVEL,
                "formatter": settings.settings.log.FORMATTER,
            },
            **settings.CONFIG_DICT["handlers"],
        },
        formatters=settings.CONFIG_DICT["formatters"],
        loggers={
            **settings.CONFIG_DICT["loggers"],
            "litestar": {
                "level": settings.settings.log.LEVEL,
                "handlers": ["console"],
                "propagate": False,
                "filters": ["exception_filter"],
            },
        },
        filters={
            "exception_filter": {
                "()": ExceptionFilter,
            },
        },
    ),
)
