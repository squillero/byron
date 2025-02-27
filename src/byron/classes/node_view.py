###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################

# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

# =[ HISTORY ]===============================================================
# v1 / April 2023 / Squillero (GX)

__all__ = ["NodeView"]

from dataclasses import dataclass
from functools import cached_property

import networkx as nx

from byron.classes.node import Node
from byron.classes.node_reference import NodeReference
from byron.classes.parameter import ParameterABC
from byron.classes.selement import SElement
from byron.classes.value_bag import ValueBag
from byron.global_symbols import *
from byron.tools.graph import *
from byron.user_messages import *


# NOTE[GX]: Rewritten almost from scratch taking advantage of 'dataclasses' (py>=3.7) and
# '@cached_property' (py>=3.8)


@dataclass(frozen=True, slots=False)
class NodeView:
    """A lazy, read-only view to almost all node information."""

    ref: NodeReference

    def __str__(self) -> str:
        return str(self.node)

    @property
    def safe_dump(self):
        if self.ref.graph.nodes[self.ref.node]['_type'] == MACRO:
            extra_parameters = DEFAULT_EXTRA_PARAMETERS | self.ref.graph.nodes[self.ref.node]
            extra_parameters |= {'_node': NodeView(self.ref)}
            dumped = None
            while dumped is None:
                try:
                    dumped = self.ref.graph.nodes[self.ref.node]['_selement'].dump(ValueBag(extra_parameters))
                except KeyError as k:
                    if k.args[0] in extra_parameters:
                        return '?'
                    extra_parameters[k.args[0]] = '{' + k.args[0] + '}'
                except Exception as e:
                    return f'{e}'
        else:
            dumped = str(self.ref.graph.nodes[self.ref.node]['_selement'].__class__)
        return dumped

    @property
    def graph(self) -> nx.classes.MultiDiGraph:
        return self.ref.graph

    @property
    def node(self) -> int:
        return self.ref.node

    @property
    def selement(self) -> SElement:
        return self.ref.graph.nodes[self.ref.node]['_selement']

    @property
    def type_(self) -> type:
        return self.ref.graph.nodes[self.ref.node]['_selement'].__class__

    @property
    def node_type(self) -> type:
        return self.ref.graph.nodes[self.ref.node]['_type']

    @property
    def path_string(self) -> str:
        return ".".join(f"{nv}" for nv in self.path[1:])

    @cached_property
    def node_attributes(self) -> ValueBag:
        return dict(self.ref.graph.nodes[self.ref.node])

    @cached_property
    def p(self) -> ValueBag:
        return ValueBag(
            {k: v.value for k, v in self.ref.graph.nodes[self.ref.node].items() if isinstance(v, ParameterABC)}
        )

    @cached_property
    def tree(self) -> nx.DiGraph:
        return get_structure(self.ref.graph)

    @cached_property
    def parent(self) -> 'NodeView':
        """NodeView of the parent in the structure tree"""
        parent = next((u for u, v, k in self.ref.graph.in_edges(self.ref.node, data='_type') if k == FRAMEWORK), 0)
        return NodeView(NodeReference(self.ref.graph, parent))

    @property
    def children(self) -> list['NodeView']:
        """NodeViews of all children in the structure tree"""
        return [
            NodeView(NodeReference(self.ref.graph, v))
            for u, v, d in self.ref.graph.out_edges(self.ref.node, data='_type')
            if d == FRAMEWORK
        ]

    @cached_property
    def path(self) -> tuple['NodeView']:
        """List of NodeView of the nodes in the path from top-frame to node"""
        path = list()
        node = self.ref.node
        while node > 0:
            path.append(NodeView(NodeReference(self.ref.graph, node)))
            node = next(u for u, v, k in self.ref.graph.in_edges(node, data='_type') if k == FRAMEWORK)
        path.append(NodeView(NodeReference(self.ref.graph, node)))
        return tuple(reversed(path))

    @cached_property
    def out_degree(self):
        """Number of successors in the structure tree"""
        return sum(1 for u, v, k in self.ref.graph.out_edges(self.ref.node, data='_type') if k == FRAMEWORK)

    @property
    def fields(self):
        return sorted(k for k in self.__dir__() if k[0] != '_')

    @staticmethod
    def make(G: nx.MultiDiGraph, n: int | Node) -> 'NodeView':
        return NodeView(NodeReference(G, Node(n)))
