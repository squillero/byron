# -*- coding: utf-8 -*-
###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron       #
#  |  __ <  |  |   _|  _  |     |  |___|  Evolutionary optimizer & fuzzer  #
#  |____/ ___  |__| |_____|__|__|   ).(   v0.8a1 "Don Juan"                #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import pickle
import byron


asm_instruction = byron.f.macro(
    "{inst} {reg}, 0x{imm:04x}",
    inst=byron.f.choice_parameter(["add", "sub", "and", "or", "xor"]),
    reg=byron.f.choice_parameter(["ax", "bx", "cx", "dx"]),
    imm=byron.f.integer_parameter(0, 2**16),
)

section_proc = byron.f.sequence([byron.f.macro("proc {_node} near:"), byron.f.bunch(asm_instruction, 3), byron.f.macro("ret")], name="zap")

asm_call = byron.f.macro("call {target}", target=byron.f.global_reference("zap", creative_zeal=1))

byron.f.as_forest(asm_call)
