import uuid

import factory

from src.domain.dto.book import BookDTO


class BookDTOFactory(factory.Factory):
    class Meta:
        model = BookDTO

    id = factory.Sequence(lambda x: uuid.uuid4())
    title = factory.Sequence(lambda x: f"Lorem Ipsum {x}")
    ext = ".txt"
    file = "/files/test.txt"
    cover = "/files/test.png"
