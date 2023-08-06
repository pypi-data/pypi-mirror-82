from __future__ import annotations

from typing import Any, Union

from subtypes import Enum


class Operator(Enum):
    EQUAL, UNEQUAL, GREATER, LESS = "__eq__", "__ne__", "__gt__", "__lt__"


class ChainOperator(Enum):
    AND, OR = "__and__", "__or__"


class Direction(Enum):
    ASCENDING, DESCENDING = "asc", "desc"


class ComparableName:
    def __init__(self, name: str, less: str, greater: str) -> None:
        self.name, self.less, self.greater = name, less, greater

    def __str__(self) -> str:
        return self.name


class BaseAttributeMeta(type):
    """The metaclass shared by all attributes, implementing basic functionality."""

    name: str

    def __hash__(cls) -> int:
        return id(cls)

    def __and__(cls, other: Any) -> Expression:
        return Expression(left=cls, operator=ChainOperator.AND, right=other)

    def __or__(cls, other: Any) -> Expression:
        return Expression(left=cls, operator=ChainOperator.OR, right=other)

    def _resolve(cls) -> Any:
        raise ValueError(f"Cannot resolve an object of type '{cls.__name__}' without using it as part of a boolean expression.")


class BooleanAttributeMeta(BaseAttributeMeta):
    """A metaclass for boolean attributes which allows them to be automatically resolved to a True boolean expression, or inverted ('~' operator) for a False one."""

    def __invert__(cls) -> BooleanAttribute:
        return cls(operator=Operator.UNEQUAL, value=True)

    def _resolve(cls) -> BooleanAttribute:
        return cls(operator=Operator.EQUAL, value=True)


class EnumerableAttributeMeta(BaseAttributeMeta):
    """A metaclass for enumerable attributes."""

    def __new__(mcs, name: str, bases: tuple, attributes: dict) -> Any:
        for val in attributes.values():
            if isinstance(val, BooleanAttributeMeta):
                val.owner = attributes["name"]

        return type.__new__(mcs, name, bases, attributes)


class EquatableAttributeMeta(BaseAttributeMeta):
    """A metaclass for equatable attributes."""

    def __hash__(cls) -> int:
        return id(cls)

    def __eq__(cls, other: Any) -> EquatableAttribute:
        return cls(operator=Operator.EQUAL, value=other)

    def __ne__(cls, other: Any) -> EquatableAttribute:
        return cls(operator=Operator.UNEQUAL, value=other)


class ComparableAttributeMeta(BaseAttributeMeta):
    """A metaclass for comparable attributes."""

    def __gt__(cls, other: Any) -> ComparableAttribute:
        return cls(operator=Operator.GREATER, value=other)

    def __lt__(cls, other: Any) -> ComparableAttribute:
        return cls(operator=Operator.LESS, value=other)


class BaseAttribute:
    """An abstract base class for all attributes to inherit from, providing basic functionality."""
    name: Union[str, ComparableName]

    def __init__(self, operator: Operator = None, value: Any = None, direction: Direction = None) -> None:
        self.operator, self.value, self.direction, self.negated = operator, value, direction, False

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"""{self.prefix()}{self.left()}:{self.right()}"""

    def __and__(self, other: Union[BaseAttribute, Expression]) -> Expression:
        return Expression(left=self, operator=ChainOperator.AND, right=other)

    def __or__(self, other: Union[BaseAttribute, Expression]) -> Expression:
        return Expression(left=self, operator=ChainOperator.OR, right=other)

    def prefix(self) -> str:
        negated = not self.negated if self.operator == Operator.UNEQUAL else self.negated
        return "-" if negated else ""

    def left(self) -> str:
        return self.name

    def right(self) -> str:
        return str(self.value)


class BooleanAttribute(BaseAttribute, metaclass=BooleanAttributeMeta):
    """A class for boolean attributes to inherit from."""
    owner: str

    def prefix(self) -> str:
        truth = Operator(self.operator).map_to({
            Operator.EQUAL: True,
            Operator.UNEQUAL: False,
        })

        truth = not truth if self.negated else truth
        return '' if truth else '-'

    def left(self) -> str:
        return self.owner

    def right(self) -> str:
        return self.name


class EnumerableAttribute(BaseAttribute, metaclass=EnumerableAttributeMeta):
    """A class for attributes to inherit from which own any boolean attributes declared within their namespace."""

    def __str__(self) -> str:
        raise TypeError(f"Cannot compile attribute of type {type(self).__name__}.")


class EquatableAttribute(BaseAttribute, metaclass=EquatableAttributeMeta):
    """A class for attributes to inherit from which can be queried with '==' and '!='."""

    def right(self) -> str:
        if self.operator in (Operator.EQUAL, Operator.UNEQUAL):
            return f'"{self.value}"'
        else:
            raise ValueError(f"Invalid operator: '{self.operator}' for attribute of type '{type(self).__name__}'.")


class ComparableAttribute(BaseAttribute, metaclass=ComparableAttributeMeta):
    """A class for attributes to inherit from which can be queried with '>' and '<'."""

    def left(self) -> str:
        return Operator(self.operator).map_to({
            Operator.GREATER: self.name.greater,
            Operator.LESS: self.name.less,
        })

    def right(self) -> str:
        return self.coerce(self.value)

    def coerce(self, value: Any) -> str:
        return value


class OrderableAttributeMixin:
    """A mixin class for attributes to inherit from which maps to an attribute of Message objects, for use in order_by clauses."""

    attr: str

    def __init__(self, direction: Direction) -> None:
        self.direction = direction

    @classmethod
    def asc(cls) -> OrderableAttributeMixin:
        return cls(direction=Direction.ASCENDING)

    @classmethod
    def desc(cls) -> OrderableAttributeMixin:
        return cls(direction=Direction.DESCENDING)


class Expression:
    """A class representing a binary clause of where each side contains either an instanciated attribute or another expression."""

    parentheses = {
        ChainOperator.AND: ("(", ")"),
        ChainOperator.OR: ("{", "}")
    }

    def __init__(self, left: Union[BaseAttributeMeta, BaseAttribute, Expression], operator: ChainOperator, right: Union[BaseAttributeMeta, BaseAttribute, Expression]) -> None:
        self.left, self.right = left._resolve() if isinstance(left, BaseAttributeMeta) else left, right._resolve() if isinstance(right, BaseAttributeMeta) else right
        self.operator, self.negated = operator, False

        for side in (self.left, self.right):
            if isinstance(side, BaseAttribute):
                if side.value is None:
                    raise ValueError(f"Cannot filter {side.name} by {None}.")
                if side.operator is None:
                    raise ValueError(f"Cannot filter {side.name} without a logical operator.")

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        open_paren, close_paren = self.parentheses[self.operator]
        return f"""{'-' if self.negated else ''}{open_paren}{self.left} {self.right}{close_paren}"""

    def __and__(self, other: Union[BaseAttribute, Expression]) -> Expression:
        return Expression(left=self, operator=ChainOperator.AND, right=other)

    def __or__(self, other: Union[BaseAttribute, Expression]) -> Expression:
        return Expression(left=self, operator=ChainOperator.OR, right=other)

    def __invert__(self) -> Expression:
        return self._negate()

    def _negate(self) -> Expression:
        """Negate this boolean expression by either using the logically oposite operator, or, if none exists, using the 'not' logical operator."""
        self.negated = not self.negated
        return self
