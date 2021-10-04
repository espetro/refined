import os
from functools import wraps

from typing import Dict, Union, TypeVar, Any, Callable, Tuple
from typing_extensions import Annotated, TypeGuard

from refined.predicates import RefinementPredicate, RefinementTypeException

# Type variable to annotate decorators that take a function,
# and return a function with the same signature.
F = TypeVar("F", bound=Callable)
_T = TypeVar("_T", bound=Any)

_ANNOTATION_TYPE = type(Annotated[None, Callable[[None], TypeGuard[None]]])
_TYPEGUARD_TYPE = type(TypeGuard[None])

_ERROR_TEMPLATE = "For parameter {} with refined type {}, {} is not a valid value"


def refined(function: F) -> F:
    """
    A decorator to check if the values for parameters with refined type hints hold the
    conditions.

    A refined type hint is of the form 'Annotated[_T, *_Ts]' where '_T' is a type hint,
    and '_Ts' is a sequence of predicates; predicates are generic classes that inherit
    from the RefinementPredicate base class, and have a 'type_guard' method that returns
    a type guard
    """
    @wraps(function)
    def with_refined_types(*args, **kwargs):
        type_hints = function.__annotations__
        _check_refined_type_hints(type_hints, args, kwargs)

        return function(*args, **kwargs)

    return with_refined_types


def _check_refined_type_hints(type_hints: Dict[str, Any], args: Tuple[Any, ...],
                              kwargs: Dict[str, Any]):
    """Check if the given arguments for the refined type hints fulfill the conditions"""

    num_args, errors, parameters_with_types = len(args), [], list(type_hints.items())
    # assuming that parameters are in order
    args_parameters = parameters_with_types[:num_args]

    for argument, (argument_parameter, type_hint) in zip(args, args_parameters):
        if _is_invalid_type(argument, type_hint):
            refined_type = type_hint.__args__[0]
            errors.append(
                _ERROR_TEMPLATE.format(argument_parameter, refined_type, argument)
            )

    for parameter, type_hint in parameters_with_types[num_args:]:
        if parameter in kwargs and _is_invalid_type(kwargs[parameter], type_hint):
            refined_type = type_hint.__args__[0]
            errors.append(
                _ERROR_TEMPLATE.format(parameter, refined_type, kwargs[parameter])
            )

    if errors:
        error_message = "Conditions do not hold for the following parameters:"
        errors_as_str = os.linesep.join([os.linesep, *errors])
        raise RefinementTypeException(error_message + errors_as_str)


def _is_invalid_type(argument: _T, type_hint: Union[_ANNOTATION_TYPE, Any]) -> TypeGuard[_ANNOTATION_TYPE]:
    """
    The type of an argument is invalid if the argument has a refinement type hint, and
    at least one type guard condition holds false. Predicates are evaluated in order
    """
    if _is_annotated_with_type(argument, type_hint):
        for predicate in (_ for _ in type_hint.__metadata__ if _is_refinement_predicate(_)):
            return _is_invalid_predicate(argument, predicate)

    return False


def _is_annotated_with_type(argument: _T, type_hint: Union[_ANNOTATION_TYPE, Any]) -> TypeGuard[_ANNOTATION_TYPE]:
    """
    An argument is correctly annotated if it has an 'Annotated' type hint whose first
    argument is of type '_T'
    """
    if type(type_hint) is _ANNOTATION_TYPE and len(type_hint.__args__) > 0:
        argument_type, type_hint_input = type(argument), type_hint.__args__[0]

        if hasattr(type_hint_input, "__origin__"):  # i.e. a generic collection type (List, Tuple, etc.)
            return argument_type is type_hint_input.__origin__
        elif isinstance(type_hint_input, (list, dict, tuple, set)):  # i.e. a built-in collection type
            return argument_type is type_hint_input
        else:  # i.e. a raw type (str, int, float, bytes, ...)
            return argument_type is type_hint_input


def _is_refinement_predicate(metadata: Any) -> TypeGuard[RefinementPredicate]:
    return hasattr(metadata, "type_guard")


def _is_invalid_predicate(argument: _T, predicate: RefinementPredicate) -> bool:
    return not (_does_predicate_inherit_from_base(argument, predicate) and
                _condition_holds(argument, predicate))


def _does_predicate_inherit_from_base(argument: _T,
                                      predicate: RefinementPredicate) -> TypeGuard[_TYPEGUARD_TYPE]:
    """
    Check if a refinement predicate is a class that inherits from the
    RefinementPredicate base class, with a bounded type '_B', and for its 'type_guard' method:

     * Its inputs are a bounded by '_B'
     * Its output is a type guard of type '_B'
    """
    argument_type = type(argument)
    parameter_types = predicate.type_guard.__annotations__
    return_type = parameter_types.pop("return", None)
    input_type = parameter_types.pop("value", None)

    if return_type and type(return_type) is _TYPEGUARD_TYPE and hasattr(return_type.__args__[0], "__bound__"):
        type_guard_bound = return_type.__args__[0].__bound__

        if issubclass(argument_type, type_guard_bound) and input_type and hasattr(input_type, "__bound__"):
            type_guard_input_bound = input_type.__bound__
            return issubclass(argument_type, type_guard_input_bound)

    return False


def _condition_holds(argument: _T, predicate: RefinementPredicate) -> TypeGuard[_T]:
    """Checks if the type predicate is true"""
    return predicate.type_guard(argument)
