import os
from functools import wraps

from typing import Dict, TypeVar, Any, Callable, get_type_hints, Annotated, TypeGuard, Tuple

# Type variable to annotate decorators that take a function,
# and return a function with the same signature.
F = TypeVar("F", bound=Callable[..., Any])
_T = TypeVar("_T", bound=Any)

_ANNOTATION_TYPE = type(Annotated[None, Callable[[None], TypeGuard[None]]])
_TYPEGUARD_TYPE = type(TypeGuard[None])

_ERROR_TEMPLATE = "For parameter {} with refined type {}, {} is not a valid value"


class RefinementTypeException(Exception):
    pass


def refined(function: F) -> F:
    """
    A decorator to check if the values for parameters with refined type hints hold the
    conditions.

    A refined type hint is of the form 'Annotated[_T, *_Ts]' where '_T' is a type hint,
    and '_Ts' is a sequence of type guards (or functions with a unique parameter of
    type '_T')
    """
    @wraps(function)
    def with_refined_types(*args, **kwargs):
        type_hints = get_type_hints(function, include_extras=True)
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
        if _is_invalid_type(type_hint, argument):
            refined_type = type_hint.__args__[0]
            errors.append(_ERROR_TEMPLATE.format(argument_parameter, refined_type, argument))

    for parameter, type_hint in parameters_with_types[num_args:]:
        if parameter in kwargs and _is_invalid_type(type_hint, kwargs[parameter]):
            refined_type = type_hint.__args__[0]
            errors.append(_ERROR_TEMPLATE.format(parameter, refined_type, kwargs[parameter]))

    if errors:
        raise RefinementTypeException(
            f"Conditions do not hold for the following parameters:" +
            os.linesep +
            os.linesep.join(errors)
        )


def _is_invalid_type(type_hint: _ANNOTATION_TYPE | Any,
                     argument: _T) -> TypeGuard[_ANNOTATION_TYPE]:
    """Checks if a refined type hint is invalid (at least one type guard condition holds false)"""
    if _is_annotated_with_type(type_hint, argument):
        for type_guard in type_hint.__metadata__:
            if _is_invalid_type_guard(type_guard, argument):
                return True

    return False


def _is_annotated_with_type(type_hint: _ANNOTATION_TYPE | Any,
                            argument: _T) -> TypeGuard[_ANNOTATION_TYPE]:
    """
    Check if a potential type hint is of type 'Annotated' and its input is of type '_T'
    """
    return (type(type_hint) is _ANNOTATION_TYPE
            and len(type_hint.__args__) > 0
            and type(argument) is type_hint.__args__[0])


def _is_invalid_type_guard(type_guard: _TYPEGUARD_TYPE | Any,
                           argument: _T) -> bool:
    return not (_is_type_guard_callable_with_type(type_guard, argument) and
                _condition_holds(type_guard, argument))


def _is_type_guard_callable_with_type(type_guard: _TYPEGUARD_TYPE | Any,
                                      argument: _T) -> TypeGuard[_TYPEGUARD_TYPE]:
    """
    Check if a potential type guard is a function whose input is of type '_T' and its
    return is of type 'TypeGuard'
    """
    if callable(type_guard):
        parameter_types = get_type_hints(type_guard)
        return_type = parameter_types.pop("return", None)
        input_type = list(parameter_types.values())

        return type(return_type) is _TYPEGUARD_TYPE and len(input_type) == 1 and input_type[0] is type(argument)
    else:
        return False


def _condition_holds(type_guard: _TYPEGUARD_TYPE, argument: _T) -> bool:
    """Checks if the type guard condition holds"""
    return type_guard(argument)
