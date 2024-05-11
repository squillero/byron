# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://github.com/squillero/byron #
#       |_____|                   \|/                                     #
################################## ' ######################################
from typing import Collection

import networkx as nx

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
# v1 / August 2023 / Squillero (GX)

from copy import deepcopy
from collections import defaultdict

from .ea_tools import *
from byron.classes import *
from byron.randy import rrandom
from byron.registry import *
from byron.tools.graph import *
from byron.user_messages import *


def _connected_nodes(G: nx.MultiDiGraph, n: Node | int) -> Collection[Node | int]:
    graph = nx.Graph((u, v) for u, v, t in G.edges(data='_type') if t == FRAMEWORK)
    # graph.add_nodes_from((n, NODE_ZERO))  # NOTE[GX]: Better safe than sorry
    graph.remove_node(NODE_ZERO)
    return nx.node_connected_component(graph, n)


def _generic_node_crossover(parent1: Individual, parent2: Individual, *, choosy: bool = False, link_type: str):
    # assert parent1.run_paranoia_checks()
    # assert parent2.run_paranoia_checks()

    common_selements_raw = group_selements([parent1, parent2], only_direct_targets=(link_type == LINK), choosy=choosy)
    common_selements = defaultdict(lambda: defaultdict(list))
    for path, elements in common_selements_raw.items():
        if len(elements) < 2:
            continue
        for ind, nodes in elements.items():
            if 664 in nodes:
                pass
            plausible_nodes = [
                n for n in nodes if link_type in set(t for u, v, t in ind.genome.in_edges(n, data='_type'))
            ]
            if not plausible_nodes:
                continue
            common_selements[path][ind] = plausible_nodes
        if len(common_selements[path]) != 2:
            del common_selements[path]

    if not common_selements:
        raise ByronOperatorFailure

    target = rrandom.choice(tuple(common_selements.keys()))
    node1 = rrandom.choice(common_selements[target][parent1])
    node2 = rrandom.choice(common_selements[target][parent2])
    P1 = deepcopy(parent1.genome)
    P2 = deepcopy(parent2.genome)
    # P2.remove_node(NODE_ZERO)
    new_genome = nx.compose(P1, P2)
    node1_fanin = new_genome.in_edges(node1, data=True, keys=True)
    node2_fanin = new_genome.in_edges(node2, data=True, keys=True)
    node1_parent_link = rrandom.choice([(u, v, k, d) for u, v, k, d in node1_fanin if d['_type'] == link_type])
    # node2_parent_link = rrandom.choice(
    #    [(u, v, k, d) for u, v, k, d in node2_fanin if d['_type'] == node1_parent_link[3]['_type']]
    # )

    # 1. trovare i successori di node2
    # 2. trovare il nodo p1 = parent strutturale di node1
    # 3. per S = {node2, tutti i suoi successori} definire P = {parents strutturali di ogni nodo di S}
    # 4. dato P' = P - S, se P' != {p2(parent strutturale di node 2)} => fallisce
    # 5. scollegare i nodi che possiedono parent strutturale p2 da esso e collegarli al p1
    new_nodes_of_P2 = nx.descendants(new_genome, node2) | {node2}
    node1_parent = node1_parent_link[0]
    node1_parent_struct = [
        u for u, v, k, d in new_genome.in_edges(node1_parent, keys=True, data='_type') if d == FRAMEWORK
    ]
    if len(node1_parent_struct) != 1:
        logger.debug(f"generic_node_crossover: Failed (node 1 have many structural parent)")
        raise ByronOperatorFailure
    node1_parent_struct = node1_parent_struct[0]
    node2_parent_struct = [u for u, v, k, d in new_genome.in_edges(node2, keys=True, data='_type') if d == FRAMEWORK]
    if len(node2_parent_struct) != 1:
        logger.debug(f"generic_node_crossover: Failed (node 2 have many structural parent)")
        raise ByronOperatorFailure
    node2_parent_struct = node2_parent_struct[0]

    parents_struct = set()
    for new_node in new_nodes_of_P2:
        parent_struct = [
            (u, k) for u, v, k, d in new_genome.in_edges(new_node, keys=True, data='_type') if d == FRAMEWORK
        ]
        if len(parent_struct) != 1:
            logger.debug(f"generic_node_crossover: Failed (new successor have many structural parent)")
            raise ByronOperatorFailure
        parent_struct = parent_struct[0]
        parents_struct.add(parent_struct[0])
        if (parent_struct[0]) == node2_parent_struct:
            new_genome.remove_edge(node2_parent_struct, new_node, parent_struct[1])
            new_genome.add_edge(node1_parent_struct, new_node, parent_struct[1], **{'_type': FRAMEWORK})

    different_parent_struct = parents_struct - new_nodes_of_P2
    if different_parent_struct != {node2_parent_struct}:
        logger.debug(f"generic_node_crossover: Failed (invalid structure)")
        raise ByronOperatorFailure

    logger.debug(
        f"generic_node_crossover: "
        + f"{node1}/{new_genome.nodes[node1]['_selement'].__class__}"
        + " <-> "
        + f"{node2}/{new_genome.nodes[node2]['_selement'].__class__}"
    )

    # NOTE[GX]: replace link in node1_parent -> node1 with node1_parent -> node2 preserving links order
    node1_parent_complete_fanout = tuple(new_genome.edges(node1_parent_link[0], data=True, keys=True))
    for edge in node1_parent_complete_fanout:
        new_genome.remove_edge(edge[0], edge[1], key=edge[2])
    for edge in node1_parent_complete_fanout:
        if edge == node1_parent_link:
            new_genome.add_edge(edge[0], node2, edge[2], **edge[3])
        else:
            new_genome.add_edge(edge[0], edge[1], key=edge[2], **edge[3])
    discard_useless_components(new_genome)

    if not get_structure_tree(new_genome):
        logger.debug(f"generic_node_crossover: Failed (invalid structure)")
        raise ByronOperatorFailure

    Node.reset_labels(new_genome)
    new_individual = Individual(parent1.top_frame, new_genome)
    # assert new_individual.run_paranoia_checks()

    # assert parent1.run_paranoia_checks()
    # assert parent2.run_paranoia_checks()
    if not new_individual.valid:
        logger.debug(f"generic_node_crossover: Failed (invalid individual)")
        return list()

    return [new_individual]


@genetic_operator(num_parents=2)
def node_crossover_choosy(parent1: Individual, parent2: Individual):
    # Swaps two node with exactly the same path-type (ie. parents must be of the same types)
    return _generic_node_crossover(parent1, parent2, choosy=True, link_type=LINK)


@genetic_operator(num_parents=2)
def node_crossover_unfussy(parent1: Individual, parent2: Individual):
    # Swaps two target nodes of the same type
    return _generic_node_crossover(parent1, parent2, choosy=False, link_type=LINK)


@genetic_operator(num_parents=2)
def leaf_crossover_unfussy(parent1: Individual, parent2: Individual):
    # Swaps two generic nodes of the same type
    return _generic_node_crossover(parent1, parent2, choosy=False, link_type=FRAMEWORK)
