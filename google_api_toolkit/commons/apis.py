from abc import ABC, abstractmethod
from typing import Any, Generic, Iterable, Mapping, Tuple, TypeVar

from .builders import RequestBuilder
from .pages import ResourceIterator, ResourcePage
from .utils import EmptyResponse

T = TypeVar("T")
RequestBuilderType = TypeVar("RequestBuilderType", bound=RequestBuilder)


class GoogleRestApi(Generic[T], ABC):
    """
    Base class for Rest api wrappers.
    """

    @abstractmethod
    def get(self, resource_name: str) -> T:
        ...

    @abstractmethod
    def batch_get(
        self, resource_names: Iterable[str]
    ) -> Tuple[Iterable[T], Mapping[str, Any]]:
        ...

    @abstractmethod
    def create(self, payload: Mapping[str, Any]) -> T:
        ...

    @abstractmethod
    def update(self, resource_name: str, payload: Mapping[str, Any]) -> T:
        ...

    @abstractmethod
    def delete(self, resource_name: str) -> EmptyResponse:
        ...

    @abstractmethod
    def list(self, *, page_size: int, page_token: str) -> ResourcePage[T]:
        ...

    @abstractmethod
    def iterate(self, *, page_size: int, page_token: str) -> ResourceIterator[T]:
        ...
