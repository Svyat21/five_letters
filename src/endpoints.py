from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.endpoints import HTTPEndpoint
from starlette.templating import Jinja2Templates
from starlette.requests import Request

template = Jinja2Templates('templates')


class HomePage(HTTPEndpoint):
    async def get(self, request: Request):
        return template.TemplateResponse('index.html', {'request': request})
