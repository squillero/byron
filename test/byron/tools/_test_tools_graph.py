###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import networkx as nx

import byron as byron

FRAMEWORK = 'framework'
NODE_ZERO = 0


class Frame1:
    pass


class Frame2:
    pass


class Frame3:
    pass


def test_get_grammar_tree():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, kind="framework")
    tree = byron.tools.graph.get_grammar_tree(G)
    assert isinstance(tree, nx.DiGraph)
    assert list(tree.edges) == [(1, 2)]


def test_get_successors():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, kind="framework")
    G.add_edge(1, 3, kind="framework")
    ref = byron.classes.NodeReference(G, 1)
    assert byron.tools.graph.get_successors(ref) == [2, 3]


def test_get_predecessor():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, kind="framework")
    G.add_edge(1, 3, kind="framework")
    ref = byron.classes.NodeReference(G, 2)
    assert byron.tools.graph.get_predecessor(ref) == 1


def test_get_siblings():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, kind="framework")
    G.add_edge(1, 3, kind="framework")
    ref = byron.classes.NodeReference(G, 2)
    assert byron.tools.graph.get_siblings(ref) == [2, 3]


def test_set_successors_order():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, kind="framework")
    G.add_edge(1, 3, kind="framework")
    ref = byron.classes.NodeReference(G, 1)
    byron.tools.graph.set_successors_order(ref, [3, 2])
    assert list(G.successors(1)) == [3, 2]


def test_get_successors():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, kind="framework")
    G.add_edge(1, 3, kind="framework")

    node_ref = byron.classes.NodeReference(G, 1)
    successors = byron.tools.graph.get_successors(node_ref)

    assert sorted(successors) == [2, 3]


def test_get_predecessor():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, kind="framework")
    G.add_edge(1, 3, kind="framework")

    node_ref = byron.classes.NodeReference(G, 2)
    predecessor = byron.tools.graph.get_predecessor(node_ref)

    assert predecessor == 1


def test_set_successors_order():
    G = nx.MultiDiGraph()
    G.add_edge(1, 2, kind="framework")
    G.add_edge(1, 3, kind="framework")

    node_ref = byron.classes.NodeReference(G, 1)
    new_order = [3, 2]
    byron.tools.graph.set_successors_order(node_ref, new_order)

    assert byron.tools.graph.get_successors(node_ref) == new_order


def test_is_equal():
    G1 = nx.MultiDiGraph()
    G1.add_edge(1, 2, kind="framework")
    G1.add_edge(1, 3, kind="framework")

    G2 = nx.MultiDiGraph()
    G2.add_edge(1, 2, kind="framework")
    G2.add_edge(1, 3, kind="framework")

    node_ref1 = byron.classes.NodeReference(G1, 1)
    node_ref2 = byron.classes.NodeReference(G2, 1)

    assert byron.tools.graph.is_equal(node_ref1, node_ref2)


def test_get_node_color_dict():
    G = nx.MultiDiGraph()
    G.add_node(1, _frame=Frame1())
    G.add_node(2, _frame=Frame2())
    G.add_node(3, _frame=Frame3())
    color_dict = byron.tools.graph.get_node_color_dict(G)
    assert len(set(color_dict.values())) == len(G.nodes)
    assert color_dict == {1: 0, 2: 1, 3: 2}


def test_get_macros():
    G = nx.MultiDiGraph()
    G.add_node(NODE_ZERO, _frame="frame")
    G.add_node(1, _macro="macro1")
    G.add_node(2, _macro="macro2")
    G.add_node(3, _macro="macro3")
    G.add_edge(NODE_ZERO, 1, kind=FRAMEWORK)
    G.add_edge(NODE_ZERO, 2, kind=FRAMEWORK)
    G.add_edge(NODE_ZERO, 3, kind=FRAMEWORK)

    macros = byron.tools.graph.get_macros(G)
    assert macros == [1, 2, 3]


def test_get_frames():
    G = nx.MultiDiGraph()
    G.add_node(NODE_ZERO, _frame="frame")
    G.add_node(1, _frame="frame1")
    G.add_node(2, _frame="frame2")
    G.add_node(3, _frame="frame3")
    G.add_edge(NODE_ZERO, 1, kind=FRAMEWORK)
    G.add_edge(NODE_ZERO, 2, kind=FRAMEWORK)
    G.add_edge(NODE_ZERO, 3, kind=FRAMEWORK)

    frames = byron.tools.graph.get_frames(G)
    assert frames == [NODE_ZERO, 1, 2, 3]


class Parameter(byron.classes.ParameterABC):
    def mutate(self):
        pass


def test_get_first_macro():
    G = nx.MultiDiGraph()
    T = nx.DiGraph()
    G.add_node(1, _macro="macro1")
    G.add_node(2, _frame="frame1")
    G.add_node(3, _frame="frame1")
    T.add_edge(1, 2)
    T.add_edge(2, 3)
    first_macro = byron.tools.graph._get_first_macro(1, G, T)
    assert first_macro == 1
