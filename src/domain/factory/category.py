import factory

from src.domain.dto.category import CategoryDTO


class CategoryDTOFactory(factory.Factory):
    class Meta:
        model = CategoryDTO

    id = factory.Sequence(int)
    name = factory.Sequence(lambda x: f"Category name {x}")
    parent_id = None
