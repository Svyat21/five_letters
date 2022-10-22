import uvicorn
from starlette.applications import Starlette
from src.routes import routes


app = Starlette(debug=False, routes=routes)


# if __name__ == "__main__":
#     uvicorn.run(app, host='0.0.0.0', port=8000)
