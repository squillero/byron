from __future__ import annotations

from collections import namedtuple
from typing import Optional, Tuple, Sequence, Dict, Type

import networkx as nx
from lxml import objectify
from lxml.objectify import ObjectifiedElement

from .base_dao import BaseDAO
from .edge_dao import EdgeDAO
from .list_dao import ListDAO
from .dict_str_dao import DictStrDAO


class NodeDAO(BaseDAO):
    _tag: str = "node"
    _id: str
    _data: DictStrDAO
    _out_edges: ListDAO[EdgeDAO]

    BaseObject = namedtuple('NodeDAOBaseObject', ['id', 'graph'])

    def __init__(self, id: str, data: DictStrDAO, out_edges: ListDAO[EdgeDAO], tag: Optional[str] = None) -> None:
        self._id = id
        self._data = data
        self._out_edges = out_edges
        if tag is not None:
            self._tag = tag

    def __str__(self):
        return f"{self._tag} id:{self._id} => {str(self._out_edges)}"

    @property
    def id(self) -> str:
        return self._id

    @property
    def out_edges(self) -> ListDAO[EdgeDAO]:
        return self._out_edges

    @staticmethod
    def from_object(obj: BaseObject, tag: Optional[str] = None) -> NodeDAO:
        edges = [EdgeDAO.from_object((v, k, d)) for u, v, k, d in obj.graph.out_edges(obj.id, keys=True, data=True)]
        data = obj.graph.nodes[obj.id]
        return NodeDAO(obj.id, DictStrDAO.from_object(data, "data"), ListDAO.from_object(edges, "edges"))

    @staticmethod
    def deobjectify(
        data: ObjectifiedElement, dao_type: Optional[Type[BaseDAO]] = Type['NodeDAO'], tag: Optional[str] = None
    ) -> NodeDAO:
        return NodeDAO(
            data.get("id"),
            DictStrDAO.deobjectify(data.data, tag="data"),
            ListDAO.deobjectify(data.edges, EdgeDAO, "edges"),
            tag,
        )

    def objectify(self) -> ObjectifiedElement:
        node = objectify.Element(self._tag)
        node.set("id", str(self._id))
        node.append(self._data.objectify())
        node.append(self._out_edges.objectify())
        return node
