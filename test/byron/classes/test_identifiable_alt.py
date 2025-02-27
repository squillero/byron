###################################|###|####################################
#   _____                          |   |                                   #
#  |  __ \--.--.----.-----.-----.  |===|  This file is part of Byron, an   #
#  |  __ <  |  |   _|  _  |     |  |___|  evolutionary source-code fuzzer. #
#  |____/ ___  |__| |_____|__|__|   ).(   Version 0.8a1 "Don Juan"         #
#        |_____|                    \|/                                    #
#################################### ' #####################################
# Copyright 2023-24 Giovanni Squillero and Alberto Tonda
# SPDX-License-Identifier: Apache-2.0

import byron as byron


class TestIdentifiable:
    def test_identity(self):
        class MyIdentifiable(byron.classes.IdentifiableABC):
            def __init__(self, id):
                self.id = id

            @property
            def _identity(self):
                return self.id

        obj1 = MyIdentifiable(1)
        obj2 = MyIdentifiable(2)
        obj3 = MyIdentifiable(1)

        assert obj1._identity == 1
        assert obj2._identity == 2
        assert obj3._identity == 1

    def test_hash(self):
        class MyIdentifiable(byron.classes.IdentifiableABC):
            def __init__(self, id):
                self.id = id

            @property
            def _identity(self):
                return self.id

        obj1 = MyIdentifiable(1)
        obj2 = MyIdentifiable(2)
        obj3 = MyIdentifiable(1)

        assert hash(obj1) != hash(obj2)
        assert hash(obj1) == hash(obj3)

    def test_eq(self):
        class MyIdentifiable(byron.classes.IdentifiableABC):
            def __init__(self, id):
                self.id = id

            @property
            def _identity(self):
                return self.id

        obj1 = MyIdentifiable(1)
        obj2 = MyIdentifiable(2)
        obj3 = MyIdentifiable(1)
        obj4 = None
        obj5 = "not an IdentifiableABC object"

        assert obj1 == obj3
        assert obj1 != obj2
        assert obj1 != obj4
        assert obj1 != obj5
