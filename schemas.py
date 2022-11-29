from pydantic import BaseModel


class Category(BaseModel):
    name: str
    slug: str or None = None

    def category_to_dict(self):
        return vars(self)


def CategoryResult(category) -> dict:
    return {
        "id": category[0],
        "name": category[1],
        "slug": category[2]
    }


def CategoryListResult(categories) -> list:
    return [CategoryResult(category) for category in categories]


