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
    register = byron.f.choice_parameter(["zero", *[f"t{n}" for n in range(7)], *[f"s{n}" for n in range(12)]])
    int4 = byron.f.integer_parameter(0, 2**4)
    int5 = byron.f.integer_parameter(0, 2**5)
    int8 = byron.f.integer_parameter(0, 2**8)
    int11 = byron.f.integer_parameter(0, 2**11)  # Incoherence with the manual that say 12bits
    int20 = byron.f.integer_parameter(0, 2**20)

    operations_R = byron.f.choice_parameter(
        [
            'add',
            'sub',
            'slt',
            'sltu',
            'sra',
            'sll',
            'srl',
            'and',
            'or',
            'xor',
            'addw',
            'sllw',
            'srlw',
            'subw',
            'sraw',
            'mul',
            'mulh',
            'mulhu',
            'mulhsu',
            # 'div',
            # 'divu',
            # 'rem',
            # 'remu',
            # 'divw',
            # 'divuw',
            # 'remw',
            # 'remuw',
        ]
    )
    operations_I = byron.f.choice_parameter(['addi', 'slti', 'sltiu', 'andi', 'ori', 'xori', 'addiw'])
    operations_I_special = byron.f.choice_parameter(['slli', 'srli', 'srai'])
    operations_I_special64 = byron.f.choice_parameter(['slliw', 'srliw', 'sraiw'])
    operations_U = byron.f.choice_parameter(['lui', 'auipc'])
    op_R = byron.f.macro('{op} {r1}, {r2}, {r3}', op=operations_R, r1=register, r2=register, r3=register)
    op_I = byron.f.macro('{op} {r1}, {r2}, {imm:#x}', op=operations_I, r1=register, r2=register, imm=int11)
    op_I_special = byron.f.macro(
        '{op} {r1}, {r2}, {imm:#x}', op=operations_I_special, r1=register, r2=register, imm=int5
    )
    op_I_special64 = byron.f.macro(
        '{op} {r1}, {r2}, {imm:#x}', op=operations_I_special64, r1=register, r2=register, imm=int4
    )
    op_U = byron.f.macro('{op} {r1}, {imm:#x}', op=operations_U, r1=register, imm=int20)

    operations_B = byron.f.choice_parameter(['eq', 'ne', 'ge', 'lt', 'geu', 'ltu'])
    op_B = byron.f.macro(
        'b{cond} {r1}, {r2}, {label}',
        cond=operations_B,
        r1=register,
        r2=register,
        label=byron.f.local_reference(backward=True, loop=False, forward=True),
    )

    op_J_imm = byron.f.macro('j {label}', label=byron.f.local_reference(backward=True, loop=False, forward=True))
    op_J_reg = byron.f.macro('jr {r1}', r1=register)

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

    prologue_sub = byron.f.macro(
        r"""
; [prologue_sub]
.globl	{_node}             ; -- Begin function {_node}
{_node}:
push ra
; [end-prologue_sub]""",
        _label='',  # No automatic creation of the label -- it's embedded as "{_node}:"
    )

    epilogue_sub = byron.f.macro(
        r"""; [epilogue_sub]
pull ra
jr ra
; [end-epilogue_sub]"""
    )

    op_pool = [op_R, op_I, op_I_special, op_I_special64, op_U]  # missing op_B, op_J_imm, op_J_reg
    op_pool_weight = [
        operations_R.NUM_ALTERNATIVES,
        operations_I.NUM_ALTERNATIVES,
        operations_I_special.NUM_ALTERNATIVES,
        operations_I_special64.NUM_ALTERNATIVES,
        operations_U.NUM_ALTERNATIVES,
    ]
    assert len(op_pool) == len(op_pool_weight), "The size of the poll must be equal to the size of the weight"

    core_sub = byron.framework.bunch(op_pool, size=(1, 5 + 1), weights=op_pool_weight)
    sub = byron.framework.sequence([prologue_sub, core_sub, epilogue_sub])
    op_JL_imm = byron.f.macro("jal {label}", label=byron.f.global_reference(sub, creative_zeal=1, first_macro=True))
    op_JL_reg = byron.f.macro("jalr {reg}")  # Maybe not feasible

    core_main = byron.framework.bunch(
        op_pool,  # + op_JL_imm, op_JL_reg
        size=(10, 15 + 1),
        weights=op_pool_weight,
    )

    main = byron.framework.sequence([prologue_main, core_main, epilogue_main])

    return main
