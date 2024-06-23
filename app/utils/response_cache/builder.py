import orjson
from fastapi.responses import ORJSONResponse, Response, RedirectResponse

class BaseBuilder:
    @classmethod
    def encode(cls, value):
        raise NotImplementedError
    
    @classmethod
    def decode(cls, value):
        raise NotImplementedError
    

class ORJsonBuilder(BaseBuilder):
    @classmethod
    def encode(cls, value: ORJSONResponse) -> bytes:
        content = value.body
        headers = value.headers
        status_code = value.status_code

        params = {
            "content": orjson.loads(content),
            "headers": dict(headers),
            "status_code": status_code
        }
        # str
        # return orjson.dumps(params).decode('utf-8')
        return params

    @classmethod
    def decode(cls, value: dict) -> ORJSONResponse:
        return ORJSONResponse(
            content=value["content"],
            headers=value["headers"],
            status_code=value["status_code"]
        )

class BaseRespBuilder(BaseBuilder):
    @classmethod
    def encode(cls, value: Response) -> bytes:
        headers = dict(value.headers)
        status_code = value.status_code
        content = value.body

        return orjson.dumps(
            {
                "headers": headers,
                "status_code": status_code,
                "content": content
            }
        )
    
    @classmethod
    def decode(cls, value: dict) -> Response:
        return Response(
            headers=value["headers"],
            status_code=value["status_code"],
            content=value["content"]
        )
    
# class RedirectRespBuilder(BaseBuilder):
#     @classmethod
#     def encode(cls, value: RedirectResponse) -> bytes:
#         headers = dict(value.headers)
#         status_code = value.status_code

#         return orjson.dumps(
#             {
#                 "headers": headers,
#                 "status_code": status_code,
#             }
#         )
    
#     @classmethod
#     def decode(cls, value: dict) -> RedirectResponse:
#         return RedirectResponse(
#             status_code=value["status_code"],
#             url=value["headers"]["location"]
#         )