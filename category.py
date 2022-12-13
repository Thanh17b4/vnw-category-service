from fastapi import APIRouter, Response
from slugify import slugify
from starlette import status

from db import mydb
from model.check_data import is_blank
from schemas import CategoryResult, CategoryListResult, Category

category_router = APIRouter()


@category_router.post('/category', status_code=201)
def create_category(request: Category, response: Response):
    category = request.category_to_dict()
    # Validate data
    is_ok, msg = __validate(category)
    if is_ok is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return msg
    slug = slugify(category["name"])
    with mydb:
        my_cursor = mydb.cursor()
        sql = "INSERT INTO categories (name, slug) VALUES (%s, %s)"
        val = (category["name"], slug)
        my_cursor.execute(sql, val)
        mydb.commit()
        response.status_code = status.HTTP_201_CREATED
        return f"{my_cursor.rowcount} category has been inserted successfully"


def __validate(req: dict):
    if req.get("name") is None or is_blank(req.get("name")) is True:
        return False, "name cannot be null"
    return req, ""


@category_router.get('/category/{id}', status_code=200)
def detail_category(id: int, response: Response):
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("SELECT * FROM categories WHERE id = %d" % id)
        category = my_cursor.fetchone()
        if category is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return False, f"company_id is not correct"
        return True, CategoryResult(category)


@category_router.get('/category', status_code=200)
def all_category(page: int, limit: int, response: Response):
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("SELECT COUNT(*) FROM categories")
        total_categories = my_cursor.fetchone()[0]
        d = total_categories % limit
        if d == 0:
            total_page = total_categories // limit
        else:
            total_page = total_categories // limit + 1
        offset = (page - 1) * limit
        if page > total_page or page <= 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"page is not exist, total page is {total_page}"
        my_cursor.execute("SELECT * FROM categories ORDER BY id ASC LIMIT %s OFFSET %s", (limit, offset))
        categories = my_cursor.fetchall()
        if categories is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return f"query was wrong"
        return CategoryListResult(categories)


@category_router.put('/category/{id}', status_code=200)
async def update_category(id: int, req: Category, response: Response):
    category = req.category_to_dict()
    boolean, result = detail_category(id, response)
    if boolean is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    # check have some changes or not
    ok, msg = __check_changes(result, category)
    if ok is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return msg
    slug = slugify(category["name"])
    with mydb:
        my_cursor = mydb.cursor()
        sql = "UPDATE categories SET name = %s, slug = %s   WHERE id = %s"
        val = (category["name"], slug, id)
        my_cursor.execute(sql, val)
        return f"{my_cursor.rowcount} row affected"


def __check_changes(req: dict, new_req: dict):
    if req["name"] == new_req["name"]:
        return False, "no information have been changed"
    return new_req, ""


@category_router.delete('/category/{id}', status_code=200)
async def delete_category(id: int, response: Response):
    boolean, result = detail_category(id, response)
    if boolean is False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return result
    with mydb:
        my_cursor = mydb.cursor()
        my_cursor.execute("DELETE FROM categories WHERE id = %d" % id)
        return f"{my_cursor.rowcount} row affected"
