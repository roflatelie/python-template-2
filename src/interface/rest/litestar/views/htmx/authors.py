from litestar import Controller, get
from litestar.response import Template


class AuthorsHandler(Controller):
    path = "/authors"

    @get(path="/")
    async def index(self) -> Template:
        return Template("books/index.html")
