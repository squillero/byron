###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

from networkx.classes import MultiDiGraph

from byron.classes.node_reference import NodeReference


def test_node_reference():
    G = MultiDiGraph()
    p1 = NodeReference(G, 1)
    p2 = NodeReference(G, 2)
    assert p1 is not None
    assert type(p1.graph) == type(G)
    assert p1.node == 1
    assert p1 != p2
    assert p2.node != 3
    assert p1.graph == p2.graph
