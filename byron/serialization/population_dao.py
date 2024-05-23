from __future__ import annotations

from typing import Optional, Type

from lxml import objectify
from lxml.objectify import ObjectifiedElement

from byron.classes import Population
from .base_dao import BaseDAO
from .list_dao import ListDAO
from .individual_dao import IndividualDAO


class PopulationDAO(BaseDAO):
    _tag: str = "population"
    _generation: int
    _individuals: ListDAO[IndividualDAO]

    def __init__(self, generation: int, individuals: ListDAO[IndividualDAO], tag: Optional[str] = None):
        self._generation = generation
        self._individuals = individuals
        if tag is not None:
            self._tag = tag

    def __str__(self):
        return f"{self._tag} generation:{self._generation} => {str(self._individuals)}"

    @property
    def generation(self) -> int:
        return self._generation

    @property
    def individuals(self) -> ListDAO[IndividualDAO]:
        return self._individuals

    @staticmethod
    def from_object(obj: Population, tag: Optional[str] = None) -> PopulationDAO:
        individuals = [IndividualDAO.from_object(I) for i, I in obj]
        return PopulationDAO(obj.generation, ListDAO.from_object(individuals, "individuals"))

    @staticmethod
    def deobjectify(
        data: ObjectifiedElement, dao_type: Optional[Type[BaseDAO]] = Type['PopulationDAO'], tag: Optional[str] = None
    ) -> PopulationDAO:
        return PopulationDAO(data.generation, ListDAO.deobjectify(data.individuals, IndividualDAO, "individuals"), tag)

    def objectify(self) -> ObjectifiedElement:
        population = objectify.Element(self._tag)
        population.generation = str(self._generation)
        population.append(self._individuals.objectify())
        return population
