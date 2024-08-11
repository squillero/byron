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

initialized_variable = byron.f.macro('var {_node} = {value}', value=byron.f.integer_parameter(0, 256), _label='')
bunch_of_initialized_variables = byron.f.bunch([initialized_variable], size=(1, 10))
uninitialized_variable = byron.f.macro('var {_node}', _label='')
bunch_of_uninitialized_variables = byron.f.bunch([uninitialized_variable], size=(0, 10, 0))

variables = byron.f.sequence([bunch_of_initialized_variables, bunch_of_uninitialized_variables])

operation = byron.f.macro(
    "{dst} = func({arg})",
    dst=byron.f.global_reference(variables),
    arg=byron.f.global_reference(variables, creative_zeal=100),
)

bunch_of_operations = byron.f.bunch([operation], size=1)
program = byron.f.sequence([variables, bunch_of_operations])
byron.f.as_text(program)
