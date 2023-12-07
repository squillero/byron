#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#################################|###|#####################################
#  __                            |   |                                    #
# |  |--.--.--.----.-----.-----. |===| This file is part of Byron v0.8    #
# |  _  |  |  |   _|  _  |     | |___| An evolutionary optimizer & fuzzer #
# |_____|___  |__| |_____|__|__|  ).(  https://pypi.org/project/byron/    #
#       |_____|                   \|/                                     #
################################## ' ######################################
# Copyright 2023 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import byron

COMMENT = '#'


def define_frame():
    register = byron.f.choice_parameter(["zero", *[f"t{n}" for n in range(4)]])
    int5 = byron.f.integer_parameter(0, 2**5)
    int8 = byron.f.integer_parameter(0, 2**8)
    int20 = byron.f.integer_parameter(0, 2**20)

    operations_R = byron.f.choice_parameter(['add', 'sub', 'slt', 'sltu', 'sra', 'sll', 'srl', 'and', 'or', 'xor'])
    operations_I = byron.f.choice_parameter(['addi', 'slti', 'sltiu', 'andi', 'ori', 'xori'])
    operations_I_special = byron.f.choice_parameter(['slli', 'srli', 'srai'])
    operations_U = byron.f.choice_parameter(['lui', 'auipc'])
    op_R = byron.f.macro('{op} {r1}, {r2}, {r3}', op=operations_R, r1=register, r2=register, r3=register)
    op_I = byron.f.macro('{op} {r1}, {r2}, {imm:#x}', op=operations_I, r1=register, r2=register, imm=int8)
    op_I_special = byron.f.macro(
        '{op} {r1}, {r2}, {imm:#x}', op=operations_I_special, r1=register, r2=register, imm=int5
    )
    op_U = byron.f.macro('{op} {r1}, {imm:#x}', op=operations_U, r1=register, imm=int20)

    conditions = byron.f.choice_parameter(['eq', 'ne', 'ge', 'lt', 'geu', 'ltu'])
    branch = byron.f.macro(
        'b{cond} {r1}, {r2}, {label}',
        cond=conditions,
        r1=register,
        r2=register,
        label=byron.f.local_reference(backward=True, loop=False, forward=True),
    )
    jump = byron.f.macro('j {label}', label=byron.f.local_reference(backward=True, loop=False, forward=True))

    prologue_main = byron.f.macro(
        r"""# [prologue_main]
.global asm_call

.macro push reg
    addi sp, sp, -8
    sd \reg, 0(sp)
.endm

.macro pop reg
    ld \reg, 0(sp)
    addi sp, sp, 8
.endm

.section .text

asm_call: 
#Save return address
    push ra
#Save stack pointer
    #The sw is not abilitated to modify the sp as for now
#Save s register (callee convenction)
    push s0
    push s1
    push s2
    push s3
    push s4
    push s5
    push s6
    push s7
    push s8
    push s9
    push s10
    push s11
#Save the addresses of the return vectors    
    push a0     #saved vector ptr
    push a1     #temporaries vector ptr

#Init temporary at 0
    mv t0, zero
    mv t1, zero
    mv t2, zero
    mv t3, zero
    mv t4, zero
    mv t5, zero
    mv t6, zero
# [end-prologue_main]"""
    )

    epilogue_main = byron.f.macro(
        r"""# [epilogue_main]
#Store temporaries registers
    pop a0
    sd t0, 0(a0)
    sd t1, 8(a0)
    sd t2, 16(a0)
    sd t3, 24(a0)
    sd t4, 32(a0)
    sd t5, 40(a0)
    sd t6, 48(a0)
#Store saved registers
    pop a0
    sd s0, 0(a0)
    sd s1, 8(a0)
    sd s2, 16(a0)
    sd s3, 24(a0)
    sd s4, 32(a0)
    sd s5, 40(a0)
    sd s6, 48(a0)
    sd s7, 56(a0)
    sd s8, 64(a0)
    sd s9, 72(a0)
    sd s10, 80(a0)
    sd s11, 88(a0)

#Restore s register (callee convenction)
    pop s11
    pop s10
    pop s9
    pop s8
    pop s7
    pop s6
    pop s5
    pop s4
    pop s3
    pop s2
    pop s1
    pop s0
#Restore return address
    pop ra
    jr ra
# [end-epilogue_main]"""
    )

    core_main = byron.framework.bunch(
        [op_R, op_I, op_I_special, op_U],
        size=(10, 15 + 1),
        weights=[
            operations_R.NUM_ALTERNATIVES,
            operations_I.NUM_ALTERNATIVES,
            operations_I_special.NUM_ALTERNATIVES,
            operations_U.NUM_ALTERNATIVES,
        ],
    )

    main = byron.framework.sequence([prologue_main, core_main, epilogue_main])

    return main
