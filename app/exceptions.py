from werkzeug.exceptions import BadRequest, NotFound
from werkzeug import Response
from typing import Union
import json


class CustomNotFound(NotFound):
    def __init__(self, message: Union[str, None] = None) -> None:
        res = Response(
            json.dumps({"errorMsg": message, "code": 404}),
            status=404,
            content_type="application/json",
        )
        super().__init__(message, res)


class CustomBadRequest(BadRequest):
    def __init__(self, message: Union[str, None] = None) -> None:
        res = Response(
            json.dumps({"errorMsg": message, "code": 400}),
            status=400,
            content_type="application/json",
        )
        super().__init__(message, res)
