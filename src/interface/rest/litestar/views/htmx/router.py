from litestar import Router, get
from litestar.response import Response, Template

from src.domain.services.book import get_list_by_category_id
from src.domain.services.category import get_default_category
from src.settings import settings

from .authors import AuthorsHandler
from .books import BooksHandler
from .categories import CategoriesHandler


@get(path="/")
async def index() -> Template:
    return Template(
        "index.html",
    )


@get("/healthcheck")
async def healthcheck() -> dict:  # noqa: RUF029
    return {}


@get("/liveness")
async def liveness() -> dict:  # noqa: RUF029
    return {}


@get("/readiness")
async def readiness() -> dict:  # noqa: RUF029
    return {}


@get("/metrics")
async def metrics() -> Response[bytes]:  # noqa: RUF029
    body, headers = settings.metrics.render()
    return Response(
        body,
        headers=headers,
    )


router = Router(
    path="/",
    route_handlers=[
        healthcheck,
        liveness,
        readiness,
        metrics,
        index,
        AuthorsHandler,
        BooksHandler,
        CategoriesHandler,
    ],
)
