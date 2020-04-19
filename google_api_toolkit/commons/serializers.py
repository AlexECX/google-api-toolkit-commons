import json
from typing import (
    Any,
    Callable,
    Dict,
    Mapping,
    MutableMapping,
    Optional,
    Type,
    TypeVar,
    Union,
)

from pydantic import BaseModel
from typing_extensions import Protocol

from .types import AbstractSetIntStr, MappingIntStrAny

T = TypeVar("T", bound=BaseModel)
U = TypeVar("U")


class SerializerProtocol(Protocol[U]):
    def load(self, data: Mapping[str, Any]) -> U:
        ...

    def loads(self, data: Union[str, bytes], **json_kwargs) -> U:
        ...

    def dump(self, obj: U) -> MutableMapping[str, Any]:
        ...

    def dumps(self, obj: U, **json_kwargs) -> str:
        ...


class BaseSerializer(SerializerProtocol[T]):
    """
    Base class for all serializers (except Membership).

    Args:
        model: The class used to instantiate the data.
        dump_null: Will add None fields to the dump result.
            Default False.
        include: Limits which fields will be included for serialization.
        exclude: Limits which fields will be included for serialization.

    """

    # Do include fields with a `None` value.
    dump_null: bool = False
    # The fields to include during serialization.
    include: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None
    # Fields to be excluded from serialization.
    exclude: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None

    def __init__(
        self,
        *,
        model: Type[T],
        dump_null: Optional[bool] = None,
        include: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None,
        exclude: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None,
    ):
        self.model = model
        self.dump_null = dump_null if dump_null is not None else self.dump_null
        self.include = include or self.include
        self.exclude = exclude or self.exclude

    def load(self, data: Mapping[str, Any]) -> T:
        """
        Generate a :attr:`model` instance from a dictionary.

        Args:
            data: A field/value mapping.
        """
        return self.model.parse_obj(data)

    def loads(self, data: Union[str, bytes], **kwargs) -> T:
        """
        Generate a :attr:`model` instance from a json string.

        Args:
            data: A field/value mapping.
            **kwargs: Additional parameter for the parser.
        """
        return self.model.parse_raw(data, **kwargs)

    def dump(
        self,
        obj: T,
        *,
        dump_null: Optional[bool] = None,
        include: Optional[Union[AbstractSetIntStr, MappingIntStrAny]] = None,
        exclude: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        by_alias: bool = True,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Generate a dictionary representation of the :attr:`model`.

        Args:
            obj: A :attr:`model` instance.
            dump_null: Do include fields with a `None` value. Default
                False
            include: Limits which fields will be included.
            exclude: Limits which fields will be included.
            by_alias: Do convert keys to camelCase. Default True.
            **kwargs: Additional parameter for the parser.
        """
        return obj.dict(
            exclude_none=False if dump_null or self.dump_null else True,
            include=include or self.include,
            exclude=exclude or self.exclude,
            by_alias=by_alias,
            **kwargs,
        )

    def dumps(
        self,
        obj: T,
        *,
        dump_null: bool = None,
        include: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        exclude: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        by_alias: bool = True,
        encoder: Optional[Callable[[Any], Any]] = None,
        **kwargs,
    ) -> str:
        """
        Generate a JSON string representation of the :attr:`model`.

        Args:
            obj: A :attr:`model` instance.
            dump_null: Do include fields with a `None` value.
            include: Limits which fields will be included.
            exclude: Limits which fields will be included.
            encoder: Custom encoder to be used.
            by_alias: Do convert keys to camelCase. Default True
            **kwargs: Additional parameter for the parser.
        """
        return self.model.json(
            exclude_none=False if dump_null or self.dump_null else True,
            include=include or self.include,
            exclude=exclude or self.exclude,
            by_alias=by_alias,
            encoder=encoder,
            **kwargs,
        )


class DictSerializer(SerializerProtocol[Dict[str, Any]]):
    """
    This class is useful when you only want to use the Rest api,
    without any (de)serialization to or from a model instance.

    .. code-block:: python

        from google_api_toolkit.people.serializers import DictSerializer
        from google_api_toolkit.people.apis import ContactAPi

        serializer = DictSerializer()
        data = {'hello': True}
        data is serializer.load(data) is serializer.dump(data)
        # True  # It is only a passthrough.

        api = ContactApi(service)
        type(api.list()[0])
        # <class 'google_api_toolkit.people.resources.Person'>
        api = ContactApi(service, serializer=DictSerializer())
        type(api.list()[0])
        # <class 'dict'>
    """

    def load(self, data: Mapping[str, Any]):
        return data

    def loads(self, data: Union[str, bytes], **json_kwargs):
        return json.loads(data, **json_kwargs)

    def dump(
        self,
        obj: Dict[str, Any],
        *,
        dump_null=None,
        include=None,
        exclude=None,
        by_alias=None,
        **kwargs,
    ):
        return obj

    def dumps(
        self,
        obj: Dict[str, Any],
        *,
        dump_null=None,
        include=None,
        exclude=None,
        by_alias=None,
        encoder=None,
        **json_kwargs,
    ) -> str:
        return json.dumps(obj, default=encoder, **json_kwargs)
