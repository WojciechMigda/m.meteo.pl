# -*- coding: utf-8 -*-

import http
import typing
from curl_cffi.requests import AsyncSession
from curl_cffi.requests.errors import RequestsError
from curl_cffi.requests.models import Response

from tenacity import (
    AsyncRetrying,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    retry_if_result
)

# curl_cffi accepts an absolute float/int timeout budget for the request window
TIMEOUT_POLICY = 20.0

class ResilientHttpPolicy:
    """A policy class that holds and executes tenacity retry rules."""
    def __init__(self, max_attempts: int = 4):
        # Define the retry configuration object dynamically
        self.retrier = AsyncRetrying(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=1, min=2, max=10),
            retry=(
                # Swapped httpx errors for curl_cffi's unified RequestsError
                retry_if_exception_type(RequestsError) |
                retry_if_result(self._should_retry_status)
            ),
            reraise=True # Ensures the final exception is thrown when limits are hit
        )

    @staticmethod
    def _should_retry_status(response: Response) -> bool:
        return response.status_code in {
            http.HTTPStatus.FORBIDDEN,
            http.HTTPStatus.REQUEST_TIMEOUT,
            http.HTTPStatus.TOO_MANY_REQUESTS,
            http.HTTPStatus.INTERNAL_SERVER_ERROR,
            http.HTTPStatus.BAD_GATEWAY,
            http.HTTPStatus.SERVICE_UNAVAILABLE,
            http.HTTPStatus.GATEWAY_TIMEOUT,
        }

    async def execute(self, async_func, *args, **kwargs):
        """Wraps any async function execution inside the tenacity loop."""
        async for attempt in self.retrier:
            with attempt:
                return await async_func(*args, **kwargs)

async def plain_fetch(session: AsyncSession, *, method: str, url: str, json_: typing.Any=None) -> Response:
    """To customize 'headers', 'impersonate', and other request parameters
    you can add them to constructed `AsyncSession'. See https://curl-cffi.readthedocs.io/en/latest/api.html#curl_cffi.requests.AsyncSession
    """
    return await session.request(
        method=method.upper(),
        url=url,
        timeout=TIMEOUT_POLICY,
        allow_redirects=True, # mirrors follow_redirects behavior natively
        json=json_,
    )

__all__ = [
    "ResilientHttpPolicy",
    "plain_fetch",
]
