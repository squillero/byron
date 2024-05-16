from __future__ import annotations

from typing import Dict, Optional, Type

from lxml import objectify
from lxml.objectify import ObjectifiedElement

from .base_dao import BaseDAO


class DictStrDAO(BaseDAO):
    _tag: str = "dict"
    _dict: Dict[str, str]

    def __init__(self, dict: Dict[str, str], tag: Optional[str] = None):
        self._dict = dict
        if tag is not None:
            self._tag = tag

    # @staticmethod
    # def from_obj(tag: str, dict: Dict[str, str]) -> DictStrDAO:
    #     return DictStrDAO(tag, dict)

    @staticmethod
    def from_object(obj: Dict[str, str], tag: Optional[str] = None) -> DictStrDAO:
        return DictStrDAO(obj, tag)

    def objectify(self) -> ObjectifiedElement:
        d = objectify.Element(self._tag)
        for key, val in self._dict.items():
            sub_element = objectify.SubElement(d, key)
            sub_element._setText(str(val))
        return d

    @staticmethod
    def deobjectify(
        data: ObjectifiedElement, dao_type: Optional[Type[BaseDAO]] = Type['DictStrDAO'], tag: Optional[str] = None
    ) -> DictStrDAO:
        return DictStrDAO({d.tag: d.text for d in data.getchildren()}, tag)
