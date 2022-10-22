from starlette.applications import Starlette
from src.routes import routes


app = Starlette(debug=False, routes=routes)
