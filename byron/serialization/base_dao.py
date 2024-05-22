from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Type, Any, Optional

from lxml import objectify, etree
from lxml.objectify import ObjectifiedElement


class BaseDAO(ABC):
    _tag: str

    @property
    def tag(self):
        return self._tag

    @abstractmethod
    def objectify(self) -> ObjectifiedElement:
        pass

    @staticmethod
    @abstractmethod
    def deobjectify(
        data: ObjectifiedElement, dao_type: Type[BaseDAO] = Type['BaseDAO'], tag: Optional[str] = None
    ) -> BaseDAO:
        pass

    @staticmethod
    @abstractmethod
    def from_object(obj: Any, tag: Optional[str] = None) -> BaseDAO:
        pass

    def serialize(self, deannotate=True) -> str:
        objectified = self.objectify()
        if deannotate:
            objectify.deannotate(objectified)
        xml = etree.tostring(objectified, pretty_print=True, encoding="unicode")
        return xml

    @classmethod
    def deserialize(cls, xml: str) -> BaseDAO:
        objectified = objectify.fromstring(xml)
        return cls.deobjectify(objectified)
