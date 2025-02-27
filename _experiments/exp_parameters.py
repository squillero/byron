###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import byron

byron.builtins.SELF

m1 = byron.macro("macro1")
m2 = byron.macro("macro2")
m3 = byron.macro("macro3")
f1 = byron.framework.sequence([m1, m1], extra_parameters={"_comment": "@"})
f2 = byron.framework.sequence([m2, m2], extra_parameters={"_comment": "#"})
f3 = byron.framework.sequence([m1, m2, m3])
pf1 = byron.framework.sequence([f1, f2, f3])
pf2 = byron.framework.sequence([f2, f1, f3], extra_parameters={"_comment": "$"})
pf3 = byron.framework.sequence([f1, f2, f3])

tot = byron.framework.sequence([pf1, pf2, pf3])

P = byron.Population(top_frame=tot, fitness_function=None)
P.add_random_individual()
text = P.dump_individual(0, extra_parameters={"$dump_node_info": True})
print(text)
