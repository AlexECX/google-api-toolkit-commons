from typing import Callable, Generic, TypeVar

from googleapiclient import http

T = TypeVar("T")


class HttpRequest(http.HttpRequest, Generic[T]):
    postproc: Callable[..., T]

    def __init__(
        self,
        http,
        postproc: Callable[..., T],
        uri,
        *,
        method="GET",
        body=None,
        headers=None,
        methodId=None,
        resumable=None,
    ):
        super().__init__(
            http,
            postproc,
            uri,
            method=method,
            body=body,
            headers=headers,
            methodId=methodId,
            resumable=resumable,
        )

    def execute(self, http=None, num_retries: int = 5) -> T:
        return super().execute(http=http, num_retries=num_retries)
