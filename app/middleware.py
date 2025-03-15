import logging
import colorlog
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# Setup Color Logging
log_format = "%(log_color)s%(levelname)s: %(message)s%(reset)s"
formatter = colorlog.ColoredFormatter(
    log_format,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "white",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger("fastapi")
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# Middleware for Logging Requests & Responses
class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        body = await request.body()
        response = await call_next(request)
        response_body = b"".join([chunk async for chunk in response.body_iterator])

        # 🟢 Logging Request
        logger.info(f"REQUEST Body: {body.decode('utf-8')}")

        # 🔴 Logging Response
        logger.info(f"RESPONSE Body: {response_body.decode('utf-8')}")

        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
        )
