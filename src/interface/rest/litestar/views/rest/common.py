import asyncio
import random

from litestar import Controller, Response, delete, get, patch, post, put

from src.domain.services.test import blahblah


async def _delay(slow_percent: float, latency_multiply: float):
    if slow_percent and random.random() <= slow_percent:
        await asyncio.sleep(random.random() * latency_multiply)


class TestHandler(Controller):
    path = "/test"

    @get(path="/get/{status_code:int}/{slow_percent:float}/{latency_multiply:float}")
    async def get(self, status_code: int, slow_percent: float, latency_multiply: float) -> Response:
        await _delay(slow_percent, latency_multiply)
        return Response(None, status_code=status_code)

    @post(path="/post/{status_code:int}/{slow_percent:float}/{latency_multiply:float}")
    async def post(self, status_code: int, slow_percent: float, latency_multiply: float) -> Response:
        await _delay(slow_percent, latency_multiply)
        return Response(None, status_code=status_code)

    @put(path="/put/{status_code:int}/{slow_percent:float}/{latency_multiply:float}")
    async def put(self, status_code: int, slow_percent: float, latency_multiply: float) -> Response:
        await _delay(slow_percent, latency_multiply)
        return Response(None, status_code=status_code)

    @patch(path="/patch/{status_code:int}/{slow_percent:float}/{latency_multiply:float}")
    async def patch(self, status_code: int, slow_percent: float, latency_multiply: float) -> Response:
        await _delay(slow_percent, latency_multiply)
        return Response(None, status_code=status_code)

    @delete(path="/delete/{status_code:int}/{slow_percent:float}/{latency_multiply:float}", status_code=204)
    async def delete(self, status_code: int, slow_percent: float, latency_multiply: float) -> None:
        await _delay(slow_percent, latency_multiply)
        return Response(None, status_code=status_code)
