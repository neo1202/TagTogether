from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "FastApi"}

# @app.get("/new-api")
# def new_api():
#     return {"message": "This is a new API!"}


# GET /items/123?q=hello
# {
#   "item_id": 456,
#   "q": null
# }
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}