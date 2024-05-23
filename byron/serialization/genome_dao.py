from __future__ import annotations

from typing import Optional, Type

import networkx as nx
from lxml import objectify
from lxml.objectify import ObjectifiedElement

from .base_dao import BaseDAO
from .list_dao import ListDAO
from .node_dao import NodeDAO


class GenomeDAO(BaseDAO):
    _tag: str = "genome"
    _nodes: ListDAO[NodeDAO]

    def __init__(self, nodes: ListDAO[NodeDAO], tag: Optional[str] = None) -> None:
        self._nodes = nodes
        if tag is not None:
            self._tag = tag

    def __str__(self):
        return f"{self._tag} => {str(self._nodes)}"

    @property
    def nodes(self) -> ListDAO[NodeDAO]:
        return self._nodes

    @staticmethod
    def from_object(obj: nx.MultiDiGraph, tag: Optional[str] = None) -> GenomeDAO:
        nodes = [NodeDAO.from_object((node, obj.out_edges(node, keys=True, data=True))) for node in obj.nodes]
        return GenomeDAO(ListDAO.from_object(nodes, "nodes"))

    @staticmethod
    def deobjectify(
        data: ObjectifiedElement, dao_type: Optional[Type[BaseDAO]] = Type['GenomeDAO'], tag: Optional[str] = None
    ) -> GenomeDAO:
        return GenomeDAO(ListDAO.deobjectify(data.nodes, NodeDAO, "nodes"), tag)

    def objectify(self) -> ObjectifiedElement:
        genome = objectify.Element(self._tag)
        genome.append(self._nodes.objectify())
        return genome
