from typing import Optional

from byron.serialization import BaseDAO


class Serializer:
    _serialization_file: str
    _deserialization_file: str
    _is_to_be_serialized: bool = False
    _is_to_be_deserialized: bool = False

    def __init__(self, serialization_file: Optional[str] = None, deserialization_file: Optional[str] = None):
        if serialization_file is not None:
            self._serialization_file = serialization_file
            self._is_to_be_serialized = True
        if deserialization_file is not None:
            self._deserialization_file = deserialization_file
            self._is_to_be_deserialized = True

    @property
    def is_to_be_serialized(self) -> bool:
        return self._is_to_be_serialized

    @property
    def is_to_be_deserialized(self) -> bool:
        return self._is_to_be_deserialized

    def serialize(self, dao: BaseDAO):
        with open(self._serialization_file, "w") as file:
            file.write(dao.serialize())
