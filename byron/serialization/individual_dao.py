from __future__ import annotations

from typing import Optional, Type
from lxml import objectify
from lxml.objectify import ObjectifiedElement

from byron.classes import Individual
from .base_dao import BaseDAO
from .genome_dao import GenomeDAO


class IndividualDAO(BaseDAO):
    _tag: str = "individual"
    _id: int
    _genome: GenomeDAO

    def __init__(self, id: int, genome: GenomeDAO, tag: Optional[str] = None) -> None:
        self._id = id
        self._genome = genome
        if tag is not None:
            self._tag = tag

    def __str__(self):
        return f"{self._tag} id:{self._id} => {str(self._genome)}"

    @property
    def id(self) -> int:
        return self._id

    @property
    def genome(self) -> GenomeDAO:
        return self._genome

    @staticmethod
    def from_object(obj: Individual, tag: Optional[str] = None) -> IndividualDAO:
        return IndividualDAO(obj.id, GenomeDAO.from_object(obj.genome))

    @staticmethod
    def deobjectify(
        data: ObjectifiedElement, dao_type: Optional[Type[BaseDAO]] = Type['IndividualDAO'], tag: Optional[str] = None
    ) -> IndividualDAO:
        return IndividualDAO(data.get("id"), GenomeDAO.deobjectify(data.genome), tag)

    def objectify(self) -> ObjectifiedElement:
        individual = objectify.Element(self._tag)
        individual.set("id", str(self._id))
        individual.append(self._genome.objectify())
        return individual
