from litestar import Controller, get
from litestar.response import Template

from src.domain.services.category import get_category_list


class CategoriesHandler(Controller):
    path = "/categories"

    @get(path="/")
    async def index(self) -> Template:  # noqa: PLR6301
        categories = await get_category_list()
        return Template(
            "categories/list.html",
            context={
                "categories": categories,
            },
        )
