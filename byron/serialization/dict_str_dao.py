from __future__ import annotations

from typing import Dict, Optional, Type, TypeVar, Generic

from lxml import objectify
from lxml.objectify import ObjectifiedElement

from .base_dao import BaseDAO

T = TypeVar('T')


class DictStrDAO(BaseDAO, Generic[T]):
    _tag: str = "dict"
    _dict: Dict[str, T]

    def __init__(self, dict: Dict[str, T], tag: Optional[str] = None):
        self._dict = dict
        if tag is not None:
            self._tag = tag

    def __str__(self):
        return f"{self._tag} => {str(self._dict)}"

    @property
    def dict(self) -> Dict[str, T]:
        return self._dict

    @staticmethod
    def from_object(obj: Dict[str, T], tag: Optional[str] = None) -> DictStrDAO:
        new_dict = {k: v if type(v) is str else str(v) for k, v in obj.items()}
        return DictStrDAO(new_dict, tag)

    @staticmethod
    def deobjectify(
        data: ObjectifiedElement, dao_type: Optional[Type[BaseDAO]] = Type['DictStrDAO'], tag: Optional[str] = None
    ) -> DictStrDAO:
        return DictStrDAO({d.tag: d.text for d in data.getchildren()}, tag)

    def objectify(self) -> ObjectifiedElement:
        d = objectify.Element(self._tag)
        for key, val in self._dict.items():
            sub_element = objectify.SubElement(d, key)
            sub_element._setText(str(val))
        return d
