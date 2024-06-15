from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from currency_service.api import router as api_router
from currency_service.database import init_db
import zlib

app = FastAPI()
app.include_router(api_router)

templates = Jinja2Templates(directory="templates")


class CRC32Middleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if response.headers.get('content-type') == "application/json":
            original_body = b"".join([chunk async for chunk in response.body_iterator])
            crc32_value = zlib.crc32(original_body) & 0xffffffff
            response.headers["X-Content-CRC32"] = f"{crc32_value:08x}"

            async def new_body_iterator():
                yield original_body

            response.body_iterator = new_body_iterator()

        return response


app.add_middleware(CRC32Middleware)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
