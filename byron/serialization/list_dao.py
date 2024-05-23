from __future__ import annotations

from typing import TypeVar, Generic, List, Optional, Type

from lxml import objectify
from lxml.objectify import ObjectifiedElement

from .base_dao import BaseDAO

T = TypeVar('T')


class ListDAO(BaseDAO, Generic[T]):
    _tag: str = "list"
    _list: List[T]

    def __init__(self, list: List[T], tag: Optional[str] = None):
        self._list = list
        if tag is not None:
            self._tag = tag

    def __str__(self):
        return f"{self._tag} => {str(self._list)}"

    @property
    def list(self) -> List[T]:
        return self._list

    @staticmethod
    def from_object(obj: List[T], tag: Optional[str] = None) -> ListDAO[T]:
        return ListDAO(obj, tag)

    @staticmethod
    def deobjectify(data: ObjectifiedElement, dao_type: Type[BaseDAO] = T, tag: Optional[str] = None) -> ListDAO[T]:
        # raise error if tag or daotype are none
        return ListDAO([dao_type.deobjectify(d) for d in data.getchildren()], tag)

    def objectify(self) -> ObjectifiedElement:
        l = objectify.Element(self._tag)
        for element in self._list:
            l.append(element.objectify())
        return l
