from typing import Any, Iterable, Iterator, List, Optional, TypeVar, cast

from .http import HttpRequest

T = TypeVar("T")


class ResourcePage(List[T]):
    """
    An iterable page of resources from a ``list()`` request.

    Args:
        iterable: An iterable of resources.
        next_page_token: The end-point provided page token. Empty if
            there are no more pages.
        next_request: A prepared request to get the next page. Empty if
            there are no more pages.
        **kwargs: Catch-all for unused or deprecated arguments.
    """

    def __init__(
        self,
        iterable: Iterable[T],
        *,
        next_request: Optional[HttpRequest["ResourcePage[T]"]] = None,
        next_page_token: Optional[str] = None,
        **kwargs
    ):
        super().__init__(iterable)
        self.next_request: Optional[HttpRequest["ResourcePage[T]"]] = next_request
        self.next_page_token = next_page_token


PageType = TypeVar("PageType", bound=ResourcePage)


class PaginationIterator(Iterator[PageType]):
    def __init__(self, page: PageType):
        super().__init__()
        self._next_page: Any = page
        self.page: PageType = self._next_page

    def __next__(self) -> PageType:
        if self._next_page is None:
            raise StopIteration
        self.page = self._next_page
        if self.page.next_request is None:
            self._next_page = None
        else:
            self._next_page = cast(
                HttpRequest[PageType], self.page.next_request
            ).execute()
        return self.page


class ResourceIterator(Iterable[T]):
    """
    Allows iteration over all instances of a resource. The next
    :class:`ResourcePage` is automatically loaded when needed. The
    current page and all of its attributes are accessible via the
    :attr:`page` property.

    Args:
        page: The starting page of the iteration.
    """

    def __init__(self, page: ResourcePage[T]):
        self._page_iterator = PaginationIterator(page)
        self._page = next(self._page_iterator)
        self._iterator = iter(self._page)

    @property
    def page(self):
        """
        Exposes the currently loaded :class:`ResourcePage`.
        """
        return self._page_iterator.page

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        try:
            return next(self._iterator)
        except StopIteration:
            self._page = next(self._page_iterator)
            self._iterator = iter(self._page)
            return self.__next__()
