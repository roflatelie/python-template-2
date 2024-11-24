import time
from typing import TYPE_CHECKING

from src.interface.rest.litestar.middlewares.common import path_to_route_name


if TYPE_CHECKING:
    from litestar.types import Receive, Send, Scope, Message

from litestar.enums import ScopeType
from litestar.middleware import AbstractMiddleware

from src.settings import settings


class PrometheusMiddleware(AbstractMiddleware):
    scopes = {ScopeType.HTTP}

    async def __call__(self, scope: "Scope", receive: "Receive", send: "Send") -> None:
        labels = {
            'service': settings.app.NAME,
            'node': settings.log.pod.node,
            'image': settings.log.pod.image,
            "path": path_to_route_name(scope["app"], scope["path"]),
            "method": scope["method"],
        }

        request_start_ns = time.perf_counter_ns()

        async def wrap_send(message: "Message") -> None:
            if message['type'] == "http.response.start":
                request_end_ns = time.perf_counter_ns()
                request_duration_ms = (request_end_ns - request_start_ns) // 1000000
                labels.update({"status_code": message['status']})
                settings.metrics.http_requests_latency.observe(labels, request_duration_ms)
            await send(message)

        await self.app(scope, receive, wrap_send)
