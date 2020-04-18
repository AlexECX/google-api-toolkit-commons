from abc import ABC, abstractmethod
from typing import Any, Generic, Iterable, Mapping, Optional, Tuple, TypeVar

import googleapiclient.discovery

from .http import HttpRequest
from .pages import ResourceIterator, ResourcePage
from .serializers import SerializerProtocol
from .utils import EmptyResponse

T = TypeVar("T")


class RequestBuilder(Generic[T], ABC):
    def __init__(
        self,
        service: googleapiclient.discovery.Resource,
        *,
        serializer: SerializerProtocol[T],
        pagination: int = None,
    ):
        self.service = service
        self.serializer: SerializerProtocol[T] = serializer
        self.pagination: Optional[int] = pagination

    def _deserialize(self, data: Mapping[str, Any]) -> T:
        return self.serializer.load(data)

    @abstractmethod
    def get(self, resource_name: str) -> HttpRequest[T]:
        ...

    @abstractmethod
    def batch_get(
        self, resource_names: Iterable[str]
    ) -> HttpRequest[Tuple[Iterable[T], Mapping[str, Any]]]:
        ...

    @abstractmethod
    def create(self, payload: Mapping[str, Any]) -> T:
        ...

    @abstractmethod
    def update(self, resource_name: str, payload: Mapping[str, Any]) -> HttpRequest[T]:
        ...

    @abstractmethod
    def delete(self, resource_name: str) -> HttpRequest[EmptyResponse]:
        ...

    @abstractmethod
    def list(self, *, page_size: int, page_token: str) -> HttpRequest[ResourcePage[T]]:
        ...

    @abstractmethod
    def iterate(
        self, *, page_size: int, page_token: str
    ) -> HttpRequest[ResourceIterator[T]]:
        ...
