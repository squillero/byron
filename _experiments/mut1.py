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

# byron.rrandom.seed(42)

register = byron.f.choice_parameter(["ah", "bh", "ch", "dh", "al", "bl", "cl", "dl"])
word = byron.f.integer_parameter(0, 2 ** 16)
int_op = byron.f.choice_parameter(["add", "sub", "and", "or", "xor"])
inst = byron.f.macro("{op} {r}, 0x{v:02x}", op=int_op, r=register, v=word)

call = byron.f.macro("call {sub}", sub=byron.f.global_reference("Wazoo", first_macro=True, creative_zeal=1))

vanilla = byron.f.bunch([inst, inst, call], size=(1, 6))
entry_point = byron.f.macro("\nproc {_node} NEAR:", _label="")
proc = byron.f.sequence([entry_point, vanilla, "ret"], name="Wazoo")

# call = byron.f.macro('call {sub}', sub=byron.f.integer_parameter(0, 256))
body = byron.f.bunch([inst, inst, inst, call], size=10)

# prologue = byron.f.bunch(byron.f.macro('{_comment} PROLOGUE (node {_node.path_string})'))
# epilogue = byron.f.bunch([byron.f.macro('{_comment} EPILOGUE (node {_node.path_string})')])

program = byron.f.sequence([body])

population = byron.classes.population.Population(top_frame=program, fitness_function=None)
population.add_random_individual()

print(population.dump_individual(0, {"$dump_node_info": True}))
I = population.individuals[0]
I.as_forest(filename="structure-tree.png", figsize=(25, 15), bbox_inches="tight")
I.as_lgp(filename="code.png", figsize=(25, 15), bbox_inches="tight")

pass
