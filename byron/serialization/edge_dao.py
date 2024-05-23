from __future__ import annotations

from typing import Optional, Any, Type

from lxml import objectify
from lxml.objectify import ObjectifiedElement

from .base_dao import BaseDAO
from .dict_str_dao import DictStrDAO


class EdgeDAO(BaseDAO):
    _tag: str = "edge"
    _destination_id: str
    _key: int
    _data: DictStrDAO

    def __init__(self, destination_id: str, key: int, data: DictStrDAO, tag: Optional[str] = None):
        self._destination_id = destination_id
        self._key = key
        self._data = data
        if tag is not None:
            self._tag = tag

    def __str__(self):
        return f"{self._tag} to:{self._destination_id} key:{self._key}=> {str(self._data)}"

    @property
    def destination_id(self) -> str:
        return self._destination_id

    @property
    def key(self) -> int:
        return self._key

    @property
    def data(self) -> DictStrDAO:
        return self._data

    @staticmethod
    def from_object(obj: Any, tag: Optional[str] = None) -> BaseDAO:
        return EdgeDAO(obj[0], obj[1], DictStrDAO.from_object(obj[2], "data"))

    @staticmethod
    def deobjectify(
        data: ObjectifiedElement, dao_type: Optional[Type[BaseDAO]] = Type['EdgeDAO'], tag: Optional[str] = None
    ) -> EdgeDAO:
        return EdgeDAO(data.get("to"), data.key, DictStrDAO.deobjectify(data.data, tag="data"), tag)

    def objectify(self) -> ObjectifiedElement:
        edge = objectify.Element(self._tag)
        edge.set("to", str(self._destination_id))
        edge.key = self._key
        edge.append(self._data.objectify())
        return edge
