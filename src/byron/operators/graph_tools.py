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

__all__ = ['unroll_individual', 'unroll_selement', 'initialize_subtree', 'fasten_subtree_parameters']

import networkx as nx

from byron.classes import monitor
from byron.classes.frame import FrameABC
from byron.classes.individual import Individual
from byron.classes.macro import Macro
from byron.classes.node import NODE_ZERO, Node
from byron.classes.node_reference import *
from byron.classes.parameter import *
from byron.classes.selement import SElement
from byron.global_symbols import *
from byron.tools.graph import *
from byron.user_messages.checks import *


@monitor.failure_rate
def unroll_individual(individual: Individual, top: type[FrameABC]) -> int | None:
    """
    Recursively unroll a Frame as a subtree inside the Individual's graph.

    Args:
        individual: The individual to unroll the frame into
        top: Frame type to unroll

    Returns:
        The root of the new subtree (an int)
    """

    assert check_valid_types(individual, Individual)
    assert check_valid_types(top, FrameABC, Macro, subclass=True)
    assert not individual.finalized, f"{PARANOIA_VALUE_ERROR}: Individual is finalized"

    G = individual.genome
    new_node_reference = unroll_selement(top, G)
    if not new_node_reference:
        return None
    G.add_edge(NODE_ZERO, new_node_reference.node, _type=FRAMEWORK)
    initialize_subtree(new_node_reference)

    if individual.valid:
        return new_node_reference.node
    else:
        return None


@monitor.failure_rate
def unroll_selement(top: type[SElement], G: nx.classes.MultiDiGraph) -> NodeReference:
    new_node = _recursive_unroll(top, G)
    if not new_node:
        return None

    fasten_subtree_parameters(NodeReference(G, new_node))
    return NodeReference(G, new_node)


def initialize_subtree(node_reference: NodeReference):
    for _, p in get_node_parameters(node_reference.graph, node_reference.node):
        assert p.value is None or (
                isinstance(p, ParameterSharedABC) and not p.is_owner
        ), f"{PARANOIA_VALUE_ERROR}: {p} already initialized"
        p.mutate(1)

    # parameters = get_all_parameters(node_reference.graph, node_reference.node, node_id=True)
    # for p, n in parameters:
    #    if isinstance(p, ParameterStructuralABC):
    #        p.mutate(1, node_reference=NodeReference(node_reference.graph, n))
    #    else:
    #        p.mutate(1)


# =[PRIVATE FUNCTIONS]==================================================================================================


# NOTE[GX]: I'd love being reasonably generic and efficient in a recursive
# function, but I can't use `singledispatch` from `functools` because I'm
# choosing the implementation using the *value* of `top` -- it's a *type*,
def _recursive_unroll(top: type[SElement], G: nx.classes.MultiDiGraph) -> int:
    """Unrolls a frame/macro over the graph."""

    if isinstance(top, str):
        top = next(se for se in SE_DIRECTORY if se == top)
    if issubclass(top, FrameABC):
        new_node = _unroll_frame(top, G)
    elif issubclass(top, Macro):
        new_node = _unroll_macro(top, G)
    else:
        raise NotImplementedError(f"{top!r}")

    return new_node


def _unroll_frame(frame_class: type[FrameABC], G: nx.classes.MultiDiGraph) -> int:
    node_id = Node()
    G.add_node(node_id)

    frame_instance = frame_class()
    G.nodes[node_id]['_type'] = FRAME
    G.nodes[node_id]['_selement'] = frame_instance
    for f in frame_instance.successors:
        new_node_id = _recursive_unroll(f, G)
        G.add_edge(node_id, new_node_id, _type=FRAMEWORK)  # Checkout test/paranoia/networkx

    return node_id


def _unroll_macro(macro_class: type[Macro], G: nx.classes.MultiDiGraph) -> int:
    node_id = Node()
    G.add_node(node_id)

    macro_instance = macro_class()
    G.nodes[node_id]['_type'] = MACRO
    G.nodes[node_id]['_selement'] = macro_instance
    for k, p in macro_instance.parameter_types.items():
        G.nodes[node_id][k] = p()

    return node_id
