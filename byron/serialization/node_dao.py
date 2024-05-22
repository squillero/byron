from __future__ import annotations

from typing import Optional, Tuple, Sequence, Dict, Type

from lxml import objectify
from lxml.objectify import ObjectifiedElement

from .base_dao import BaseDAO
from .edge_dao import EdgeDAO
from .list_dao import ListDAO


class NodeDAO(BaseDAO):
    _tag: str = "node"
    _id: str
    _out_edges: ListDAO[EdgeDAO]

    def __init__(self, id: str, out_edges: ListDAO[EdgeDAO], tag: Optional[str] = None) -> None:
        self._id = id
        self._out_edges = out_edges
        if tag is not None:
            self._tag = tag

    def __str__(self):
        return f"{self._tag} id:{self._id} => {str(self._out_edges)}"

    @property
    def id(self):
        return self._id

    @property
    def out_edges(self):
        return self._out_edges

    @staticmethod
    def from_object(
        obj: Tuple[str, Sequence[Tuple[str, str, int, Dict[str, str]]]], tag: Optional[str] = None
    ) -> NodeDAO:
        id = obj[0]
        edges = [EdgeDAO.from_object((v, k, d)) for u, v, k, d in obj[1]]
        return NodeDAO(id, ListDAO.from_object(edges, "edges"))

    @staticmethod
    def deobjectify(
        data: ObjectifiedElement, dao_type: Optional[Type[BaseDAO]] = Type['NodeDAO'], tag: Optional[str] = None
    ) -> NodeDAO:
        return NodeDAO(data.get("id"), ListDAO.deobjectify(data.edges, EdgeDAO, "edges"), tag)

    def objectify(self) -> ObjectifiedElement:
        node = objectify.Element(self._tag)
        node.set("id", str(self._id))
        node.append(self._out_edges.objectify())
        return node
