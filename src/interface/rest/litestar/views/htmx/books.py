# ruff: noqa: PLR6301
import tempfile
from typing import Annotated
from uuid import UUID

from litestar import Controller, delete, get, post
from litestar.contrib.htmx.response import HXLocation
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body
from litestar.response import Template
from litestar.status_codes import HTTP_302_FOUND

from src.domain.dto.book import BookDTO
from src.domain.services.book import create_book, delete_book, get_by_id, get_list_by_category_id, update_book
from src.domain.services.category import get_category_list
from src.domain.services.m2m import set_categories_for_book


class BooksHandler(Controller):
    path = "/books"

    @get(path="/")
    async def index(self, category_id: int) -> Template:
        books = await get_list_by_category_id(category_id=category_id)
        return Template(
            "books/list.html",
            context={"books": books},
        )

    @post(path="/")
    async def upload_book(
        self,
        data: Annotated[
            dict[str, UploadFile],
            Body(media_type=RequestEncodingType.MULTI_PART),
        ],
    ) -> BookDTO:
        u_file = data["file"]
        u_cover = data["cover"]
        with (
            tempfile.NamedTemporaryFile("wb", suffix=u_file.filename, delete=False) as file,
            tempfile.NamedTemporaryFile("wb", suffix=u_cover.filename, delete=False) as cover,
        ):
            while chunk := await data["file"].read(4096):
                file.write(chunk)
            while chunk := await data["cover"].read(4096):
                cover.write(chunk)
        return await create_book(file.name, cover.name)

    @get(path="/{book_id:uuid}/")
    async def book_detail(self, book_id: UUID) -> Template:
        book = await get_by_id(book_id)
        return Template(
            "books/detail.html",
            context={
                "book": book,
            },
        )

    @delete(path="/{book_id:uuid}/", status_code=HTTP_302_FOUND)
    async def book_delete(self, book_id: UUID) -> HXLocation:
        await delete_book(book_id)
        return HXLocation(redirect_to="/")

    @get(path="/{book_id:uuid}/edit/title/")
    async def get_book_title_form(self, book_id: UUID) -> Template:
        book = await get_by_id(book_id)
        return Template(
            "books/edit_title.html",
            context={
                "book": book,
                "edit": True,
            },
        )

    @post(path="/{book_id:uuid}/edit/title/")
    async def set_book_title_form(
        self,
        book_id: UUID,
        data: Annotated[
            dict[str, str],
            Body(media_type=RequestEncodingType.MULTI_PART),
        ],
    ) -> Template:
        await update_book(book_id, title=data["title"])
        book = await get_by_id(book_id)
        return Template(
            "books/edit_title.html",
            context={
                "book": book,
                "edit": False,
            },
        )

    @get(path="/{book_id:uuid}/edit/categories/")
    async def get_book_categories_form(self, book_id: UUID) -> Template:
        book = await get_by_id(book_id)
        categories = await get_category_list()
        return Template(
            "books/edit_categories.html",
            context={
                "categories": categories,
                "book": book,
                "edit": True,
            },
        )

    @post(path="/{book_id:uuid}/edit/categories/")
    async def set_book_categories_form(
        self,
        book_id: UUID,
        data: Annotated[
            dict[str, list[int] | str],
            Body(media_type=RequestEncodingType.MULTI_PART),
        ],
    ) -> Template:
        categories = data.get("categories")
        if categories is None or isinstance(categories, list):
            await set_categories_for_book(book_id, categories or [])
        else:
            await set_categories_for_book(book_id, [int(categories)])

        book = await get_by_id(book_id)
        return Template(
            "books/edit_categories.html",
            context={
                "book": book,
                "edit": False,
            },
        )
