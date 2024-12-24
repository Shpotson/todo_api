from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

class CommonErrorBody:
    def __init__(self, msg, type):
        self.loc = ["main.py"]
        self.msg = msg,
        self.type = type

class ValidationErrorResponse(JSONResponse):
    def __init__(
            self,
            error: str
    ) -> None:
        status_code = 422
        headers = None
        media_type = None
        background = None

        error_bodies = []

        error_body = CommonErrorBody(error, status_code)

        error_bodies.append(error_body)

        content = jsonable_encoder(error_bodies)

        super().__init__(content, status_code, headers, media_type, background)


class NotFoundErrorResponse(JSONResponse):
    def __init__(
            self,
            error: str
    ) -> None:
        status_code = 404
        headers = None
        media_type = None
        background = None

        error_bodies = []

        error_body = CommonErrorBody(error, status_code)

        error_bodies.append(error_body)

        content = jsonable_encoder(error_bodies)

        super().__init__(content, status_code, headers, media_type, background)

class OptimisticConcurrencyErrorResponse(JSONResponse):
    def __init__(
            self
    ) -> None:
        status_code = 417
        headers = None
        media_type = None
        background = None

        error = "Optimistic Concurrency Error."

        error_bodies = []

        error_body = CommonErrorBody(error, status_code)

        error_bodies.append(error_body)

        content = jsonable_encoder(error_bodies)

        super().__init__(content, status_code, headers, media_type, background)
