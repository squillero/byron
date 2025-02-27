###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

from typing import Any

import byron as byron


class MockParameter(byron.classes.ParameterABC):
    def __init__(self):
        super().__init__()
        self._value = 'test'

    def is_valid(self, obj: Any) -> bool:
        return super().is_valid(obj) and isinstance(obj, str)


def test_macro():
    text = 'Hello, {name}'
    parameters = {'name': MockParameter}

    MacroClass = byron.framework.macro(text, **parameters)

    macro_instance = MacroClass()

    assert isinstance(macro_instance, MacroClass)

    assert macro_instance.text == text

    assert macro_instance.PARAMETERS == parameters
