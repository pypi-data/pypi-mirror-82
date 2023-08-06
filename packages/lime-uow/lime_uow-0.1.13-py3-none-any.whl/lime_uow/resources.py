from __future__ import annotations

import abc
import typing

from sqlalchemy import orm

__all__ = (
    "DictRepository",
    "Repository",
    "Resource",
    "SqlAlchemyRepository",
)

T = typing.TypeVar("T", covariant=True)
E = typing.TypeVar("E")


class Resource(abc.ABC, typing.Generic[T]):
    def __init__(self):
        self._is_open = False

    def __enter__(self):
        self._is_open = True
        return self.open()

    def __exit__(self, *args):
        self._is_open = False
        self.rollback()
        return self.close()

    @abc.abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @property
    def is_open(self) -> bool:
        return self._is_open

    @abc.abstractmethod
    def open(self) -> Resource[T]:
        raise NotImplementedError

    @classmethod
    def resource_name(cls) -> str:
        return cls.__name__

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def save(self) -> None:
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        if other.__class__ is self.__class__:
            # noinspection PyTypeChecker
            return self.resource_name == typing.cast(Resource, other).resource_name
        else:
            return NotImplemented

    def __ne__(self, other: object) -> bool:
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        else:
            return not result

    def __hash__(self) -> int:
        return hash(self.resource_name())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.resource_name()}"


class Repository(Resource[E], abc.ABC, typing.Generic[E]):
    """Interface to access elements of a collection"""

    @abc.abstractmethod
    def add(self, item: E, /) -> E:
        raise NotImplementedError

    @abc.abstractmethod
    def all(self) -> typing.Iterable[E]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, item: E, /) -> E:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, item: E, /) -> E:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, item_id: typing.Any, /) -> E:
        raise NotImplementedError


class SqlAlchemyRepository(Repository[E], typing.Generic[E]):
    def __init__(
        self,
        entity: typing.Type[E],
        session: orm.Session,
    ):
        super().__init__()

        self._entity = entity
        self._session = session

    def close(self) -> None:
        pass
        # self._session.close()

    def open(self) -> SqlAlchemyRepository[E]:
        return self

    def rollback(self) -> None:
        self._session.rollback()

    def save(self) -> None:
        self._session.commit()

    def all(self) -> typing.Generator[E, None, None]:
        return self._session.query(self._entity).all()

    def add(self, item: E, /) -> E:
        self._session.add(item)
        return item

    def delete(self, item: E, /) -> E:
        self._session.delete(item)
        return item

    def update(self, item: E, /) -> E:
        self._session.merge(item)
        return item

    def get(self, item_id: typing.Any, /) -> E:
        return self._session.query(self._entity).get(item_id)

    def where(self, predicate: typing.Any, /) -> typing.List[E]:
        return self._session.query(self._entity).filter(predicate).all()


class DictRepository(Repository[E], typing.Generic[E]):
    """Repository implementation based on a dictionary

    This exists primarily to make testing in client code simpler.  It was not designed for efficiency.
    """

    def __init__(
        self,
        *,
        initial_values: typing.Dict[typing.Hashable, E],
        key_fn: typing.Callable[[E], typing.Hashable],
    ):
        super().__init__()

        self._previous_state = initial_values
        self._current_state = initial_values.copy()
        self._key_fn = key_fn

        self.events: typing.List[typing.Tuple[str, typing.Dict[str, typing.Any]]] = []

    def close(self) -> None:
        self.events.append(("close", {}))
        self._current_state = {}

    def open(self) -> DictRepository[E]:
        self.events = [("open", {})]
        return self

    def rollback(self) -> None:
        self.events.append(("rollback", {}))
        self._current_state = self._previous_state.copy()

    def save(self) -> None:
        self.events.append(("save", {}))
        self._previous_state = self._current_state.copy()

    def add(self, item: E, /) -> E:
        self.events.append(("add", {"item": item}))
        key = self._key_fn(item)
        self._current_state[key] = item
        return item

    def all(self) -> typing.Iterable[E]:
        self.events.append(("all", {}))
        return list(self._current_state.values())

    def delete(self, item: E, /) -> E:
        self.events.append(("delete", {"item": item}))
        key = self._key_fn(item)
        del self._current_state[key]
        return item

    def update(self, item: E, /) -> E:
        self.events.append(("update", {"item": item}))
        key = self._key_fn(item)
        self._current_state[key] = item
        return item

    def get(self, item_id: typing.Any, /) -> E:
        self.events.append(("get", {"item_id": item_id}))
        return self._current_state[item_id]
